#!/usr/bin/env python3
"""
Piloto do N3: do corpus ao primeiro número de concordância entre detectores.

POR QUE ESTE SCRIPT EXISTE
--------------------------
A entrega 6 do Capstone I é um piloto de 20 aplicativos passados ponta a ponta
pelos detectores, com números preliminares de concordância (H4). Os dois
scripts anteriores pararam antes do primeiro APK. Este começa nele.

POR QUE ESTES TRÊS DETECTORES
-----------------------------
A proposta citava MobSF, Androguard e Exodus. A leitura do código mudou isso:

    MobSF 4.5.3 (mobsf/MalwareAnalyzer/views/Trackers.py) baixa a base do
    Exodus e aplica as mesmas regex de assinatura de código às classes do DEX.
    É a mesma base com a mesma regra. Concordância alta entre os dois é
    construção, não achado.

    Androguard não detecta rastreador: extrai classes e textos. É o extrator.

Para a H4 separar o efeito da BASE do efeito do MÉTODO, o piloto usa:

    A  Exodus, assinatura de código   nas classes do DEX (o que o MobSF faz)
    B  Exodus, assinatura de rede     nos domínios achados nos textos do APK
    C  Disconnect, lista de domínios  nos mesmos domínios de B

    A × B  mesma base, método diferente  -> efeito do método
    B × C  mesmo método, base diferente  -> efeito da base

O MobSF entra opcionalmente (--mobsf) como verificação de implementação do A.

ETAPAS
------
    cobertura     quais apps do corpus e do controle estão no AndroZoo
    amostra       sorteia os 20 do piloto entre os cobertos (semente fixa)
    baixar        baixa os APKs da amostra pelo sha256 e confere o hash
    detectar      aplica A, B e C (e o MobSF, se houver relatórios)
    concordancia  κ de Fleiss e τ de Kendall entre os detectores
    autoteste     valida a lógica sem rede e sem APK

CHAVE DO ANDROZOO
-----------------
A chave é de uso individual. Nunca entra no repositório nem em arquivo:

    export ANDROZOO_API_KEY="..."

O script a lê do ambiente e não a imprime; mensagens de erro passam por um
filtro que a mascara.

DEPENDÊNCIA
-----------
    pip install androguard          # só para 'detectar'; o resto é stdlib

USO
---
    python3 scripts/piloto_androzoo.py autoteste
    python3 scripts/piloto_androzoo.py cobertura --lista dados/androzoo/latest.csv.gz
    python3 scripts/piloto_androzoo.py amostra
    python3 scripts/piloto_androzoo.py baixar
    python3 scripts/piloto_androzoo.py detectar
    python3 scripts/piloto_androzoo.py concordancia

SAÍDA (tudo em dados/, que não é versionado)
-----
    dados/piloto_cobertura_AAAAMMDD.csv
    dados/piloto_amostra.csv
    dados/apks/<sha256>.apk
    dados/bases/exodus_trackers_AAAAMMDD.json, disconnect_services_AAAAMMDD.json
    dados/piloto_deteccao_AAAAMMDD.json
    dados/piloto_concordancia_AAAAMMDD.json
"""

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import os
import random
import re
import sys
import tempfile
import time
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

DADOS = Path("dados")
HOJE = datetime.now(timezone.utc).strftime("%Y%m%d")

URL_LISTA_ANDROZOO = "https://androzoo.uni.lu/static/lists/latest.csv.gz"
URL_DOWNLOAD_ANDROZOO = "https://androzoo.uni.lu/api/download"
URL_EXODUS = "https://reports.exodus-privacy.eu.org/api/trackers"
URL_DISCONNECT = ("https://raw.githubusercontent.com/disconnectme/"
                  "disconnect-tracking-protection/master/services.json")

# Categorias da Disconnect usadas no detector C. 'Content', 'Social' e
# 'FingerprintingGeneral' ficam de fora: incluem google.com, facebook.com e
# developers.google.com, que aparecem em quase todo APK como link e gerariam
# falso positivo em massa. A escolha é parâmetro, porque ela mesma move a taxa.
CATEGORIAS_DISCONNECT = ("Advertising", "Analytics", "FingerprintingInvasive")

AGENTE = "Mozilla/5.0 (pesquisa academica; TCC IDP; piloto N3)"
PAUSA = 1.0
Z = 1.959964


def mascarar(texto: str) -> str:
    """Tira a chave de qualquer mensagem antes de imprimir."""
    chave = os.environ.get("ANDROZOO_API_KEY")
    texto = str(texto)
    if chave:
        texto = texto.replace(chave, "***")
    return re.sub(r"apikey=[^&\s]+", "apikey=***", texto)


def mais_recente(padrao: str):
    achados = sorted(DADOS.glob(padrao))
    return achados[-1] if achados else None


def wilson(k: int, n: int):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + Z * Z / n
    centro = (p + Z * Z / (2 * n)) / den
    meia = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return (max(0.0, centro - meia), min(1.0, centro + meia))


def linha(titulo):
    print("\n" + titulo)
    print("  " + "=" * 62)


# ===================================================================== cobertura

def _int(v, padrao=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return padrao


def ler_lista_androzoo(fluxo_texto, pacotes):
    """Varre a lista do AndroZoo e devolve, para cada pacote pedido, a versão
    da Google Play com maior vercode.

    Três cuidados que a lista exige:
    - as colunas mudam entre versões da lista, então o índice vem do cabeçalho;
    - há linha com vírgula no nome do pacote sem aspas; ela fica com campos a
      mais e é contada e descartada, não lida torta;
    - o mesmo APK pode vir de vários mercados ('play.google.com|anzhi'); só
      entra quem tem a Google Play entre eles, porque é dela que vem o corpus.
    """
    leitor = csv.reader(fluxo_texto)
    cab = [c.strip() for c in next(leitor)]
    idx = {c: i for i, c in enumerate(cab)}
    for obrig in ("sha256", "pkg_name", "vercode", "markets"):
        if obrig not in idx:
            raise ValueError(f"coluna '{obrig}' ausente no cabeçalho: {cab}")

    melhor, n_versoes = {}, Counter()
    lidas = malformadas = 0
    for row in leitor:
        lidas += 1
        if len(row) != len(cab):
            malformadas += 1
            continue
        pkg = row[idx["pkg_name"]].strip().strip('"')
        if pkg not in pacotes:
            continue
        mercados = row[idx["markets"]].split("|")
        if "play.google.com" not in mercados:
            continue
        n_versoes[pkg] += 1
        cand = {
            "sha256": row[idx["sha256"]].strip().upper(),
            "vercode": _int(row[idx["vercode"]]),
            "vt_scan_date": row[idx["vt_scan_date"]] if "vt_scan_date" in idx else "",
            "dex_date": row[idx["dex_date"]] if "dex_date" in idx else "",
            "apk_size": _int(row[idx["apk_size"]]) if "apk_size" in idx else 0,
        }
        atual = melhor.get(pkg)
        chave = (cand["vercode"], cand["vt_scan_date"], cand["dex_date"])
        if atual is None or chave > (atual["vercode"], atual["vt_scan_date"],
                                     atual["dex_date"]):
            melhor[pkg] = cand
    return melhor, n_versoes, {"linhas": lidas, "malformadas": malformadas}


def abrir_lista(origem: str):
    """Arquivo local (.csv ou .csv.gz) ou URL. URL é lida em fluxo, sem gravar
    os gigabytes em disco; arquivo local permite repetir sem baixar de novo."""
    if origem.startswith(("http://", "https://")):
        req = urllib.request.Request(origem, headers={"User-Agent": AGENTE})
        bruto = urllib.request.urlopen(req, timeout=60)
        return io.TextIOWrapper(gzip.GzipFile(fileobj=bruto), encoding="utf-8",
                                errors="replace", newline="")
    p = Path(origem)
    if p.suffix == ".gz":
        return io.TextIOWrapper(gzip.open(p, "rb"), encoding="utf-8",
                                errors="replace", newline="")
    return p.open(encoding="utf-8", errors="replace", newline="")


def carregar_populacao():
    """Governo vem da planilha do teste robusto; controle, do relatório dele."""
    corpus = mais_recente("n3_corpus_*.csv")
    relatorio = mais_recente("n3_relatorio_*.json")
    if not corpus:
        sys.exit("Não achei dados/n3_corpus_*.csv. Rode antes:\n"
                 "    python3 scripts/teste_viabilidade_n3_robusto.py")
    apps = []
    with corpus.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            # a revisão manual, quando existir, manda sobre a heurística
            if (r.get("OFICIAL_S_N") or "").strip().upper() == "N":
                continue
            apps.append({
                "grupo": "governo", "appId": r["appId"],
                "categoria": r.get("categoria", ""),
                "faixa": r.get("faixa", ""),
                "esfera": (r.get("ESFERA_REVISADA") or r.get("esfera_auto") or "").strip(),
                "sensivel": (r.get("SENSIVEL_REVISADO") or r.get("sensivel_auto") or "").strip(),
                "anuncio": r.get("tem_anuncio", ""),
                "atualizado": r.get("atualizado", ""),
            })
    if relatorio:
        rel = json.loads(relatorio.read_text(encoding="utf-8"))
        for c in rel.get("controle", []):
            apps.append({
                "grupo": "controle", "appId": c["appId"],
                "categoria": c.get("genre", ""), "faixa": c.get("faixa", ""),
                "esfera": "", "sensivel": "",
                "anuncio": str(c.get("containsAds", "")), "atualizado": "",
            })
    print(f"  Governo:  {sum(a['grupo'] == 'governo' for a in apps):>4}  ({corpus})")
    print(f"  Controle: {sum(a['grupo'] == 'controle' for a in apps):>4}  "
          f"({relatorio or 'relatório não encontrado'})")
    return apps


def defasagem_dias(atualizado, vt_scan_date):
    """Dias entre a cópia do AndroZoo e a última atualização na loja.
    Positivo: a loja tem versão mais nova que a analisada. É aproximação:
    vt_scan_date marca a varredura no VirusTotal, próxima da coleta."""
    try:
        loja = datetime.fromtimestamp(int(float(atualizado)), tz=timezone.utc)
        az = datetime.strptime(vt_scan_date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return ""
    return (loja - az).days


def cmd_cobertura(args):
    linha("  COBERTURA DO ANDROZOO")
    apps = carregar_populacao()
    pacotes = {a["appId"] for a in apps}
    print(f"\n  Lendo a lista do AndroZoo de {args.lista}")
    print("  (a lista tem gigabytes; leva minutos)\n")
    t0 = time.time()
    with abrir_lista(args.lista) as fluxo:
        melhor, n_versoes, est = ler_lista_androzoo(fluxo, pacotes)
    print(f"  {est['linhas']:,} linhas em {time.time() - t0:.0f}s; "
          f"{est['malformadas']} malformadas descartadas")

    DADOS.mkdir(exist_ok=True)
    saida = DADOS / f"piloto_cobertura_{HOJE}.csv"
    campos = ["grupo", "appId", "esfera", "sensivel", "categoria", "faixa",
              "anuncio", "no_androzoo", "versoes_gp", "sha256", "vercode",
              "vt_scan_date", "apk_size", "defasagem_dias"]
    with saida.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for a in apps:
            m = melhor.get(a["appId"])
            w.writerow({**a, "no_androzoo": "sim" if m else "não",
                        "versoes_gp": n_versoes.get(a["appId"], 0),
                        **(m or {}),
                        "defasagem_dias": defasagem_dias(a["atualizado"], m["vt_scan_date"])
                        if m else ""})

    for grupo in ("governo", "controle"):
        g = [a for a in apps if a["grupo"] == grupo]
        k = sum(1 for a in g if a["appId"] in melhor)
        lo, hi = wilson(k, len(g))
        print(f"\n  {grupo:<9} {k:>4}/{len(g):<4} no acervo  "
              f"({k / max(len(g), 1):.1%}, IC95% {lo:.1%} a {hi:.1%})")
        por = defaultdict(lambda: [0, 0])
        chave = "esfera" if grupo == "governo" else "faixa"
        for a in g:
            por[a[chave] or "?"][1] += 1
            por[a[chave] or "?"][0] += a["appId"] in melhor
        for c, (kk, nn) in sorted(por.items()):
            print(f"      {c:<14} {kk:>4}/{nn:<4} {kk / nn:.0%}")
    gov_def = [defasagem_dias(a["atualizado"], melhor[a["appId"]]["vt_scan_date"])
               for a in apps if a["grupo"] == "governo" and a["appId"] in melhor]
    gov_def = sorted(d for d in gov_def if d != "")
    if gov_def:
        print(f"\n  Defasagem (loja − AndroZoo), governo: mediana "
              f"{gov_def[len(gov_def) // 2]} dias; acima de 365 dias: "
              f"{sum(d > 365 for d in gov_def)} de {len(gov_def)}")
    print(f"\n  Planilha: {saida}\n")


# ======================================================================= amostra

def sortear_amostra(linhas, n_gov, n_ctrl, semente):
    """Governo estratificado por esfera × sensibilidade, em rodízio entre os
    estratos para que nenhum fique vazio; controle metade com anúncio, metade
    sem, para que o piloto veja SDK de publicidade e não só analytics.

    A semente fixa torna o sorteio repetível por quem conferir o trabalho."""
    rng = random.Random(semente)
    cobertos = [r for r in linhas if r.get("no_androzoo") == "sim"]

    estratos = defaultdict(list)
    for r in cobertos:
        if r["grupo"] == "governo" and r.get("esfera") in ("federal", "estadual", "municipal"):
            estratos[(r["esfera"], r.get("sensivel", ""))].append(r)
    for chave in estratos:
        estratos[chave].sort(key=lambda r: r["appId"])
        rng.shuffle(estratos[chave])
    escolhidos = []
    ordem = sorted(estratos)
    while len(escolhidos) < n_gov and any(estratos[c] for c in ordem):
        for c in ordem:
            if estratos[c] and len(escolhidos) < n_gov:
                escolhidos.append(estratos[c].pop())

    ctrl = sorted((r for r in cobertos if r["grupo"] == "controle"),
                  key=lambda r: r["appId"])
    rng.shuffle(ctrl)
    com = [r for r in ctrl if str(r.get("anuncio")).lower() == "true"]
    sem = [r for r in ctrl if str(r.get("anuncio")).lower() != "true"]
    metade = n_ctrl // 2
    pegos = com[:metade] + sem[:n_ctrl - metade]
    if len(pegos) < n_ctrl:   # completa se um dos lados faltar
        resto = [r for r in ctrl if r not in pegos]
        pegos += resto[:n_ctrl - len(pegos)]
    return escolhidos + pegos


def cmd_amostra(args):
    linha("  AMOSTRA DO PILOTO")
    origem = Path(args.cobertura) if args.cobertura else mais_recente("piloto_cobertura_*.csv")
    if not origem:
        sys.exit("Rode antes a etapa 'cobertura'.")
    with origem.open(encoding="utf-8") as fh:
        linhas = list(csv.DictReader(fh))
    amostra = sortear_amostra(linhas, args.n_gov, args.n_ctrl, args.semente)
    saida = DADOS / "piloto_amostra.csv"
    with saida.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(amostra)
    total_mb = sum(_int(r.get("apk_size")) for r in amostra) / 1e6
    print(f"  Fonte: {origem}   semente: {args.semente}")
    for r in amostra:
        print(f"    {r['grupo']:<9} {r.get('esfera') or '-':<10} "
              f"sens={r.get('sensivel') or '-':<4} {r['appId']}")
    print(f"\n  {len(amostra)} aplicativos, ~{total_mb:.0f} MB a baixar")
    print(f"  Amostra: {saida}\n")


# ======================================================================== baixar

def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest().upper()


def cmd_baixar(args):
    linha("  DOWNLOAD PELO HASH")
    chave = os.environ.get("ANDROZOO_API_KEY")
    if not chave:
        sys.exit("Defina a chave antes, só no terminal:\n"
                 '    export ANDROZOO_API_KEY="..."')
    origem = DADOS / "piloto_amostra.csv"
    if not origem.exists():
        sys.exit("Rode antes a etapa 'amostra'.")
    with origem.open(encoding="utf-8") as fh:
        amostra = list(csv.DictReader(fh))
    pasta = DADOS / "apks"
    pasta.mkdir(parents=True, exist_ok=True)

    ok = falhas = 0
    for i, r in enumerate(amostra, 1):
        sha = r["sha256"].upper()
        destino = pasta / f"{sha}.apk"
        if destino.exists() and sha256_arquivo(destino) == sha:
            print(f"  [{i:>2}/{len(amostra)}] já baixado    {r['appId']}")
            ok += 1
            continue
        parcial = destino.with_suffix(".part")
        url = f"{URL_DOWNLOAD_ANDROZOO}?apikey={chave}&sha256={sha}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
            with urllib.request.urlopen(req, timeout=300) as resp, parcial.open("wb") as fh:
                for bloco in iter(lambda: resp.read(1 << 20), b""):
                    fh.write(bloco)
            recebido = sha256_arquivo(parcial)
            if recebido != sha:
                parcial.unlink(missing_ok=True)
                raise ValueError(f"hash não confere (recebido {recebido[:12]}…)")
            parcial.rename(destino)
            ok += 1
            print(f"  [{i:>2}/{len(amostra)}] ok  {destino.stat().st_size / 1e6:6.1f} MB  "
                  f"{r['appId']}")
        except Exception as e:  # noqa: BLE001 — registra e segue para o próximo
            falhas += 1
            parcial.unlink(missing_ok=True)
            print(f"  [{i:>2}/{len(amostra)}] FALHA {r['appId']}: {mascarar(e)}")
        time.sleep(args.pausa)
    print(f"\n  {ok} baixados, {falhas} falhas. Pasta: {pasta}\n")


# ===================================================================== detectar

RE_URL = re.compile(r"(?i)\b(?:https?|wss?)://([a-z0-9](?:[a-z0-9.-]*[a-z0-9])?)")
RE_HOST = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}$")
# raízes de nome de pacote Java: 'com.google.android.gms' não é domínio
RAIZES_PACOTE = {"com", "org", "net", "io", "android", "androidx", "java", "javax",
                 "kotlin", "kotlinx", "dalvik", "de", "br", "me", "co", "ch", "fr"}
# texto solto terminado em extensão de arquivo ('Foo.java', 'icon.png') é nome
# de arquivo, não domínio. No APK de teste do Androguard eram 126 de 128.
EXTENSOES = {"java", "kt", "xml", "json", "png", "jpg", "jpeg", "gif", "webp", "svg",
             "txt", "html", "htm", "js", "css", "so", "dex", "class", "properties",
             "ttf", "otf", "mp3", "mp4", "wav", "ogg", "zip", "jar", "apk", "db",
             "sqlite", "pem", "crt", "bin", "dat", "proto", "gz", "smali", "md"}


def extrair_hosts(textos):
    """Domínios citados nos textos do APK: os de URL e os que aparecem sozinhos
    como texto. Nome de pacote Java tem forma de domínio invertido e é
    descartado pela raiz, e nome de arquivo pela extensão. O que ainda sobra
    de falso positivo não casa com lista de rastreador."""
    hosts = set()
    for t in textos:
        if not t or len(t) > 4096:
            continue
        for m in RE_URL.finditer(t):
            hosts.add(m.group(1).lower().rstrip("."))
        s = t.strip().lower()
        if (RE_HOST.match(s) and s.split(".", 1)[0] not in RAIZES_PACOTE
                and s.rsplit(".", 1)[1] not in EXTENSOES):
            hosts.add(s)
    return hosts


def carregar_exodus(caminho=None):
    if caminho:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    else:
        req = urllib.request.Request(URL_EXODUS, headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=60) as r:
            bruto = r.read()
        (DADOS / "bases").mkdir(parents=True, exist_ok=True)
        (DADOS / "bases" / f"exodus_trackers_{HOJE}.json").write_bytes(bruto)
        dados = json.loads(bruto)
    rastreadores = []
    for t in dados["trackers"].values():
        rastreadores.append({
            "id": t["id"], "nome": t["name"],
            "categorias": t.get("categories", []),
            # MobSF ignora assinatura com até 3 caracteres; aqui também
            "codigo": re.compile(t["code_signature"], re.M)
            if len(t.get("code_signature") or "") > 3 else None,
            "rede": re.compile(t["network_signature"], re.M)
            if len(t.get("network_signature") or "") > 3 else None,
        })
    return rastreadores


def carregar_disconnect(caminho=None, categorias=CATEGORIAS_DISCONNECT):
    if caminho:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    else:
        req = urllib.request.Request(URL_DISCONNECT, headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=60) as r:
            bruto = r.read()
        (DADOS / "bases").mkdir(parents=True, exist_ok=True)
        (DADOS / "bases" / f"disconnect_services_{HOJE}.json").write_bytes(bruto)
        dados = json.loads(bruto)
    dominio_entidade = {}
    for cat in categorias:
        for entrada in dados["categories"].get(cat, []):
            for entidade, sites in entrada.items():
                for site, doms in sites.items():
                    if not isinstance(doms, list):
                        continue      # chaves como "dnt": "w3c" não são domínio
                    for d in doms:
                        if "/" in d:
                            continue  # regra de caminho, não de domínio
                        dominio_entidade[d.lower()] = entidade
    return dominio_entidade


def _linha_de(texto, pos):
    ini = texto.rfind("\n", 0, pos) + 1
    fim = texto.find("\n", pos)
    return texto[ini:fim if fim != -1 else len(texto)]


def _por_assinatura(texto, rastreadores, campo):
    """{rastreador: linha que casou}. A linha é a evidência: sem ela, um falso
    positivo como 'maps.google.com' virando 'Google Ads' não tem como ser
    conferido à mão."""
    achados = {}
    for t in rastreadores:
        if t[campo]:
            m = t[campo].search(texto)
            if m:
                achados.setdefault(t["nome"], _linha_de(texto, m.start()))
    return dict(sorted(achados.items()))


def detector_a(classes_txt, rastreadores):
    """Assinatura de código sobre a lista de classes, uma por linha. Buscar no
    texto inteiro com re.M equivale a testar classe por classe: '.' não casa
    quebra de linha, então nenhum casamento atravessa duas classes."""
    return _por_assinatura(classes_txt, rastreadores, "codigo")


def detector_b(hosts_txt, rastreadores):
    """Assinatura de rede sobre os domínios, um por linha. O MobSF reduz o
    domínio ao registrável antes de casar; aqui ele vai inteiro, porque há
    assinatura que depende do subdomínio. O custo aparece no piloto: a
    assinatura do Google Ads no Exodus é '\\.google\\.com', e casa com
    qualquer link de maps.google.com."""
    return _por_assinatura(hosts_txt, rastreadores, "rede")


def detector_c(hosts, dominio_entidade):
    """Casa o domínio e cada sufixo dele: 'ssl.google-analytics.com' casa
    'google-analytics.com'; 'notgoogle-analytics.com' não."""
    achadas = {}
    for h in sorted(hosts):
        partes = h.split(".")
        for i in range(len(partes) - 1):
            ent = dominio_entidade.get(".".join(partes[i:]))
            if ent:
                achadas.setdefault(ent, h)
                break
    return dict(sorted(achadas.items()))


def extrair_apk(caminho: Path):
    """Classes de todos os DEX, textos dos DEX, textos dos recursos e o
    manifesto. É o que o Androguard faz neste piloto: extrair, não detectar."""
    try:
        from loguru import logger
        logger.remove()
    except ImportError:
        pass
    from androguard.core.apk import APK
    from androguard.core.dex import DEX

    apk = APK(str(caminho))
    classes, textos = [], []
    for bruto in apk.get_all_dex():
        dex = DEX(bruto)
        classes.extend(dex.get_classes_names())
        textos.extend(dex.get_strings())
    try:
        for por_local in apk.get_android_resources().get_resolved_strings().values():
            for valores in por_local.values():
                textos.extend(str(v) for v in valores.values())
    except Exception:  # noqa: BLE001 — recurso ilegível não derruba o APK
        pass
    try:
        from lxml import etree
        textos.extend(re.findall(r'"([^"]+)"', etree.tostring(
            apk.get_android_manifest_xml()).decode("utf-8", "replace")))
    except Exception:  # noqa: BLE001
        pass
    return apk.get_package(), apk.get_androidversion_code(), classes, textos


def trackers_mobsf(pasta, sha):
    """Lê o relatório JSON do MobSF (report_json) salvo como <sha256>.json."""
    p = Path(pasta) / f"{sha}.json"
    if not p.exists():
        p = Path(pasta) / f"{sha.lower()}.json"
    if not p.exists():
        return None
    rel = json.loads(p.read_text(encoding="utf-8"))
    return sorted({t["name"] for t in rel.get("trackers", {}).get("trackers", [])})


def cmd_detectar(args):
    linha("  DETECÇÃO")
    try:
        import androguard  # noqa: F401
    except ImportError:
        sys.exit("Falta o Androguard:\n    pip install androguard")
    origem = DADOS / "piloto_amostra.csv"
    if not origem.exists():
        sys.exit("Rode antes a etapa 'amostra'.")
    with origem.open(encoding="utf-8") as fh:
        amostra = list(csv.DictReader(fh))
    rastreadores = carregar_exodus(args.exodus)
    dominios = carregar_disconnect(args.disconnect, args.categorias_disconnect)
    print(f"  Exodus: {len(rastreadores)} rastreadores   "
          f"Disconnect: {len(dominios)} domínios em {', '.join(args.categorias_disconnect)}\n")

    resultados = []
    for i, r in enumerate(amostra, 1):
        sha = r["sha256"].upper()
        caminho = DADOS / "apks" / f"{sha}.apk"
        reg = {"appId": r["appId"], "grupo": r["grupo"], "esfera": r.get("esfera"),
               "sensivel": r.get("sensivel"), "sha256": sha, "vercode": r.get("vercode")}
        if not caminho.exists():
            reg["erro"] = "APK ausente"
            resultados.append(reg)
            print(f"  [{i:>2}/{len(amostra)}] sem APK      {r['appId']}")
            continue
        t0 = time.time()
        try:
            pacote, versao, classes, textos = extrair_apk(caminho)
            hosts = extrair_hosts(textos)
            classes_txt = "\n".join(classes)
            hosts_txt = "\n".join(sorted(hosts))
            evid = {"A": detector_a(classes_txt, rastreadores),
                    "B": detector_b(hosts_txt, rastreadores),
                    "C": detector_c(hosts, dominios)}
            det = {d: list(v) for d, v in evid.items()}
            if args.mobsf:
                m = trackers_mobsf(args.mobsf, sha)
                if m is not None:
                    det["M"] = m
            reg.update({"pacote_apk": pacote, "versao_apk": versao,
                        "n_classes": len(classes), "n_dominios": len(hosts),
                        "detectores": det, "evidencias": evid,
                        "segundos": round(time.time() - t0, 1)})
            if pacote != r["appId"]:
                reg["aviso"] = f"pacote do APK ({pacote}) difere do appId"
            print(f"  [{i:>2}/{len(amostra)}] A={len(det['A']):>2} B={len(det['B']):>2} "
                  f"C={len(det['C']):>2}" + (f" M={len(det['M']):>2}" if "M" in det else "")
                  + f"  {r['appId']}")
        except Exception as e:  # noqa: BLE001
            reg["erro"] = f"{type(e).__name__}: {e}"
            print(f"  [{i:>2}/{len(amostra)}] ERRO {r['appId']}: {reg['erro'][:60]}")
        resultados.append(reg)

    saida = DADOS / f"piloto_deteccao_{HOJE}.json"
    saida.write_text(json.dumps({
        "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bases": {"exodus_rastreadores": len(rastreadores),
                  "disconnect_dominios": len(dominios),
                  "disconnect_categorias": list(args.categorias_disconnect)},
        "apps": resultados}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Resultado: {saida}\n")


# ================================================================= concordancia

def fleiss_kappa(contagens):
    """κ de Fleiss (1971). 'contagens' é uma linha por item, uma coluna por
    categoria, com o número de avaliadores que pôs o item em cada categoria.
    Todos os itens precisam ter o mesmo número de avaliadores."""
    N = len(contagens)
    if N == 0:
        return float("nan")
    n = sum(contagens[0])
    if n < 2 or any(sum(l) != n for l in contagens):
        raise ValueError("todo item precisa do mesmo número (≥2) de avaliadores")
    k = len(contagens[0])
    p_j = [sum(l[j] for l in contagens) / (N * n) for j in range(k)]
    P_i = [(sum(x * x for x in l) - n) / (n * (n - 1)) for l in contagens]
    P_bar = sum(P_i) / N
    P_e = sum(p * p for p in p_j)
    if P_e == 1:
        return float("nan")   # todos na mesma categoria: κ indefinido
    return (P_bar - P_e) / (1 - P_e)


def kendall_tau_b(x, y):
    """τ-b de Kendall (1938), com correção para empates."""
    n = len(x)
    if n != len(y) or n < 2:
        return float("nan")
    conc = disc = emp_x = emp_y = 0
    for i, j in combinations(range(n), 2):
        dx = (x[i] > x[j]) - (x[i] < x[j])
        dy = (y[i] > y[j]) - (y[i] < y[j])
        if dx == 0:
            emp_x += 1
        if dy == 0:
            emp_y += 1
        if dx and dy:
            if dx == dy:
                conc += 1
            else:
                disc += 1
    n0 = n * (n - 1) / 2
    den = math.sqrt((n0 - emp_x) * (n0 - emp_y))
    return (conc - disc) / den if den else float("nan")


def concordancia_par(a, b):
    """Concordância positiva e negativa de um par de detectores binários.
    Mostram o que o κ esconde quando quase tudo é 'sim' ou quase tudo 'não'."""
    sim_sim = sum(1 for p, q in zip(a, b) if p and q)
    nao_nao = sum(1 for p, q in zip(a, b) if not p and not q)
    disc = len(a) - sim_sim - nao_nao
    pos = 2 * sim_sim / (2 * sim_sim + disc) if (2 * sim_sim + disc) else float("nan")
    neg = 2 * nao_nao / (2 * nao_nao + disc) if (2 * nao_nao + disc) else float("nan")
    return {"sim_sim": sim_sim, "nao_nao": nao_nao, "discordantes": disc,
            "conc_positiva": pos, "conc_negativa": neg}


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else 1.0


def calcular_concordancia(apps, detectores):
    validos = [a for a in apps if "detectores" in a
               and all(d in a["detectores"] for d in detectores)]
    cont = {d: [len(a["detectores"][d]) for a in validos] for d in detectores}
    binario = {d: [c > 0 for c in cont[d]] for d in detectores}
    rel = {"n": len(validos), "detectores": list(detectores), "por_detector": {},
           "pares": {}}
    for d in detectores:
        k = sum(binario[d])
        lo, hi = wilson(k, len(validos))
        rel["por_detector"][d] = {
            "com_rastreador": k, "proporcao": k / len(validos) if validos else float("nan"),
            "ic95": [lo, hi],
            "media_rastreadores": sum(cont[d]) / len(validos) if validos else float("nan")}
    linhas = [[sum(1 for d in detectores if not binario[d][i]),
               sum(1 for d in detectores if binario[d][i])] for i in range(len(validos))]
    rel["kappa_fleiss"] = fleiss_kappa(linhas) if validos else float("nan")
    for d1, d2 in combinations(detectores, 2):
        par = concordancia_par(binario[d1], binario[d2])
        par["tau_b"] = kendall_tau_b(cont[d1], cont[d2])
        rel["pares"][f"{d1}x{d2}"] = par
    # A, B e M usam a mesma base: aí dá para comparar o conjunto, não só a contagem
    for d1, d2 in (("A", "B"), ("A", "M")):
        if d1 in detectores and d2 in detectores:
            rel["pares"][f"{d1}x{d2}"]["jaccard_medio"] = (
                sum(jaccard(a["detectores"][d1], a["detectores"][d2]) for a in validos)
                / len(validos) if validos else float("nan"))
    return rel


def cmd_concordancia(args):
    linha("  CONCORDÂNCIA ENTRE DETECTORES (H4, preliminar)")
    origem = Path(args.deteccao) if args.deteccao else mais_recente("piloto_deteccao_*.json")
    if not origem:
        sys.exit("Rode antes a etapa 'detectar'.")
    apps = json.loads(origem.read_text(encoding="utf-8"))["apps"]
    detectores = ["A", "B", "C"]
    if any("M" in a.get("detectores", {}) for a in apps):
        detectores.append("M")
    rel = calcular_concordancia(apps, detectores)
    n = rel["n"]
    print(f"  Aplicativos com todos os detectores: {n} (fonte: {origem})\n")
    for d, v in rel["por_detector"].items():
        print(f"    {d}  com ≥1 rastreador: {v['com_rastreador']:>2}/{n}  "
              f"({v['proporcao']:.0%}, IC95% {v['ic95'][0]:.0%} a {v['ic95'][1]:.0%})"
              f"   média {v['media_rastreadores']:.1f}")
    print(f"\n    κ de Fleiss (presença de ≥1 rastreador): {rel['kappa_fleiss']:.3f}")
    print("\n    Par    τ-b    conc.+  conc.−  discord.  Jaccard")
    for par, v in rel["pares"].items():
        jac = f"{v['jaccard_medio']:.2f}" if "jaccard_medio" in v else "  -"
        print(f"    {par:<5} {v['tau_b']:>5.2f}   {v['conc_positiva']:>5.2f}   "
              f"{v['conc_negativa']:>5.2f}   {v['discordantes']:>5}     {jac}")
    if n < 20:
        print(f"\n  ⚠ n = {n}. É piloto: os números testam o pipeline, não a H4.")
    prev = [v["proporcao"] for v in rel["por_detector"].values()]
    if prev and (min(prev) > 0.9 or max(prev) < 0.1):
        print("  ⚠ Prevalência extrema: o κ fica instável mesmo com acordo alto.")
        print("    Leia junto as concordâncias positiva e negativa.")
    saida = DADOS / f"piloto_concordancia_{HOJE}.json"
    saida.write_text(json.dumps(rel, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Resultado: {saida}\n")


# ===================================================================== autoteste

def autoteste():
    """Verifica a lógica sem rede e sem APK. Os casos vêm dos problemas
    conhecidos da lista do AndroZoo e das bases de rastreadores."""
    falhas = []

    # 1. lista do AndroZoo: cabeçalho fora da ordem, mercado errado, versão
    # mais nova, linha malformada por vírgula no nome do pacote
    lista = io.StringIO(
        "pkg_name,sha256,vercode,markets,vt_scan_date,dex_date,apk_size,sha1\n"
        "br.gov.meuinss,AAA,10,play.google.com,2024-01-01 00:00:00,,100,x\n"
        "br.gov.meuinss,BBB,12,play.google.com|anzhi,2025-01-01 00:00:00,,120,x\n"
        "br.gov.meuinss,CCC,99,anzhi,2026-01-01 00:00:00,,130,x\n"
        "com.exemplo,DDD,5,play.google.com,2023-05-05 00:00:00,,50,x\n"
        "com.virgula,errado,EEE,1,play.google.com,2023-01-01 00:00:00,,1,x\n"
        '"com.aspas,ok",FFF,3,play.google.com,2023-01-01 00:00:00,,1,x\n'
        "fora.do.corpus,GGG,1,play.google.com,2023-01-01 00:00:00,,1,x\n")
    melhor, nv, est = ler_lista_androzoo(
        lista, {"br.gov.meuinss", "com.exemplo", "com.aspas,ok", "com.virgula"})
    if melhor.get("br.gov.meuinss", {}).get("sha256") != "BBB":
        falhas.append(f"versão escolhida = {melhor.get('br.gov.meuinss')}, esperado BBB "
                      "(maior vercode da Google Play, ignorando o anzhi)")
    if nv.get("br.gov.meuinss") != 2:
        falhas.append(f"versões na Google Play = {nv.get('br.gov.meuinss')}, esperado 2")
    if est["malformadas"] != 1 or "com.virgula" in melhor:
        falhas.append(f"linha malformada não foi descartada: {est}")
    if melhor.get("com.aspas,ok", {}).get("sha256") != "FFF":
        falhas.append("pacote entre aspas com vírgula não foi lido")
    if "fora.do.corpus" in melhor:
        falhas.append("pacote fora do corpus entrou")

    # 2. defasagem: loja atualizada um ano depois da cópia do AndroZoo
    ts = datetime(2025, 1, 1, tzinfo=timezone.utc).timestamp()
    if defasagem_dias(ts, "2024-01-01 10:00:00") != 366:
        falhas.append(f"defasagem = {defasagem_dias(ts, '2024-01-01 10:00:00')}, esperado 366")
    if defasagem_dias("", "2024-01-01") != "":
        falhas.append("defasagem sem data da loja deveria ficar vazia")

    # 3. domínios nos textos
    hosts = extrair_hosts([
        "https://app-measurement.com/a", "firebase-settings.crashlytics.com",
        "com.google.android.gms", "Lcom/facebook/ads/AdView;",
        "veja em http://www.Gov.BR/servicos", "texto qualquer", "",
        "AccessibilityDelegateCompat.java", "ic_launcher.png",
    ])
    esperado = {"app-measurement.com", "firebase-settings.crashlytics.com", "www.gov.br"}
    if hosts != esperado:
        falhas.append(f"hosts = {sorted(hosts)}, esperado {sorted(esperado)}")

    # 4. detector A: assinatura casa a classe, não atravessa linha, e
    # assinatura curta (≤3) é ignorada como no MobSF
    base_exodus = {"trackers": {
        "1": {"id": 1, "name": "Google Firebase Analytics",
              "code_signature": "com.google.firebase.analytics.|com.google.android.gms.measurement.",
              "network_signature": "app-measurement\\.com", "categories": ["Analytics"]},
        "2": {"id": 2, "name": "Facebook Ads", "code_signature": "com.facebook.ads",
              "network_signature": "", "categories": ["Advertisement"]},
        "3": {"id": 3, "name": "Atravessa", "code_signature": "Bar;.Lorg",
              "network_signature": "", "categories": []},
        "4": {"id": 4, "name": "Curta", "code_signature": "com", "network_signature": "",
              "categories": []},
    }}
    tmp = Path(tempfile.mkdtemp(prefix="piloto_autoteste_"))
    (tmp / "exodus.json").write_text(json.dumps(base_exodus), encoding="utf-8")
    rast = carregar_exodus(tmp / "exodus.json")
    classes = "\n".join(["Lcom/google/firebase/analytics/FirebaseAnalytics;",
                         "Lcom/foo/Bar;", "Lorg/exemplo/Qualquer;"])
    got = detector_a(classes, rast)
    if got != {"Google Firebase Analytics":
               "Lcom/google/firebase/analytics/FirebaseAnalytics;"}:
        falhas.append(f"detector A = {got}, esperado só o Firebase, com a classe")
    got = detector_b("\n".join(sorted(hosts)), rast)
    if got != {"Google Firebase Analytics": "app-measurement.com"}:
        falhas.append(f"detector B = {got}, esperado só o Firebase, com o domínio")

    # 5. detector C: sufixo casa, prefixo parecido não; categoria e regra de
    # caminho filtradas
    base_disc = {"license": "x", "categories": {
        "Analytics": [{"Google": {"http://www.google.com/": [
            "google-analytics.com", "crashlytics.com", "google.com/analytics"]}}],
        "Content": [{"Google": {"http://www.google.com/": ["gov.br"]}}],
        "Advertising": [{"Meta": {"http://meta.com/": ["facebook.net"], "dnt": "w3c"}}],
    }}
    (tmp / "disconnect.json").write_text(json.dumps(base_disc), encoding="utf-8")
    dom = carregar_disconnect(tmp / "disconnect.json")
    if "google.com/analytics" in dom or "gov.br" in dom:
        falhas.append("Disconnect: regra de caminho ou categoria excluída entrou")
    got = detector_c({"ssl.google-analytics.com", "notgoogle-analytics.com",
                      "firebase-settings.crashlytics.com", "www.gov.br"}, dom)
    if list(got) != ["Google"] or got["Google"] not in (
            "ssl.google-analytics.com", "firebase-settings.crashlytics.com"):
        falhas.append(f"detector C = {got}, esperado Google, com o domínio")
    if list(detector_c({"connect.facebook.net"}, dom)) != ["Meta"]:
        falhas.append("detector C não casou subdomínio de facebook.net")

    # 6. κ de Fleiss: exemplo clássico de 10 itens, 14 avaliadores, 5
    # categorias, κ = 0,210; e caso degenerado
    exemplo = [[0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0],
               [2, 2, 8, 1, 1], [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2],
               [6, 5, 2, 1, 0], [0, 2, 2, 3, 7]]
    k = fleiss_kappa(exemplo)
    if abs(k - 0.210) > 0.001:
        falhas.append(f"κ de Fleiss do exemplo = {k:.4f}, esperado 0,210")
    if not math.isnan(fleiss_kappa([[0, 3], [0, 3]])):
        falhas.append("κ com todos na mesma categoria deveria ser indefinido")
    if abs(fleiss_kappa([[0, 3], [3, 0], [0, 3], [3, 0]]) - 1.0) > 1e-9:
        falhas.append("κ com acordo perfeito deveria ser 1")

    # 7. τ-b de Kendall, conferido com scipy.stats.kendalltau
    for x, y, esp in (([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 1.0),
                      ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], -1.0),
                      ([1, 2, 2, 3], [1, 3, 2, 4], 0.9128709291752769),
                      ([0, 1, 1, 2, 5, 3], [0, 0, 2, 2, 4, 6], 0.7412493166611012)):
        t = kendall_tau_b(x, y)
        if abs(t - esp) > 1e-9:
            falhas.append(f"τ-b({x}, {y}) = {t}, esperado {esp}")

    # 8. Wilson e concordância por par
    lo, hi = wilson(0, 396)
    if not (lo == 0.0 and abs(hi - 0.0096) < 0.0001):
        falhas.append(f"Wilson(0/396) = [{lo}, {hi}], esperado [0; 0,0096]")
    par = concordancia_par([1, 1, 0, 0, 1], [1, 0, 0, 0, 1])
    if (par["sim_sim"], par["nao_nao"], par["discordantes"]) != (2, 2, 1):
        falhas.append(f"concordância por par = {par}")

    # 9. amostra: repetível com a mesma semente, cobre os estratos
    linhas = []
    for i, (esf, sens) in enumerate([(e, s) for e in ("federal", "estadual", "municipal")
                                     for s in ("sim", "não")] * 5):
        linhas.append({"grupo": "governo", "appId": f"g{i:02d}", "esfera": esf,
                       "sensivel": sens, "no_androzoo": "sim", "anuncio": "False"})
    linhas.append({"grupo": "governo", "appId": "fora", "esfera": "federal",
                   "sensivel": "sim", "no_androzoo": "não", "anuncio": "False"})
    for i in range(10):
        linhas.append({"grupo": "controle", "appId": f"c{i}", "esfera": "", "sensivel": "",
                       "no_androzoo": "sim", "anuncio": "True" if i < 4 else "False"})
    a1 = sortear_amostra(linhas, 14, 6, 7)
    a2 = sortear_amostra(linhas, 14, 6, 7)
    if [r["appId"] for r in a1] != [r["appId"] for r in a2]:
        falhas.append("amostra muda com a mesma semente")
    gov = [r for r in a1 if r["grupo"] == "governo"]
    ctrl = [r for r in a1 if r["grupo"] == "controle"]
    if len(gov) != 14 or len({(r["esfera"], r["sensivel"]) for r in gov}) != 6:
        falhas.append(f"amostra do governo = {len(gov)} apps em "
                      f"{len({(r['esfera'], r['sensivel']) for r in gov})} estratos")
    if any(r["appId"] == "fora" for r in a1):
        falhas.append("app fora do AndroZoo entrou na amostra")
    if len(ctrl) != 6 or sum(r["anuncio"] == "True" for r in ctrl) != 3:
        falhas.append("controle deveria ter 6 apps, 3 com anúncio")

    # 10. a chave nunca aparece em mensagem
    os.environ["ANDROZOO_API_KEY"] = "chave-de-teste-123"
    msg = mascarar(f"HTTP 403 em {URL_DOWNLOAD_ANDROZOO}?apikey=chave-de-teste-123&sha256=X")
    del os.environ["ANDROZOO_API_KEY"]
    if "chave-de-teste-123" in msg:
        falhas.append(f"chave vazou na mensagem: {msg}")

    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()

    if falhas:
        print("AUTOTESTE FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print("AUTOTESTE OK — 10 grupos de verificação passaram, sem rede e sem APK.")


# ========================================================================== main

def main():
    ap = argparse.ArgumentParser(description="Piloto do N3: AndroZoo, detecção e concordância.")
    sub = ap.add_subparsers(dest="etapa", required=True)

    p = sub.add_parser("cobertura", help="quais apps estão no AndroZoo")
    p.add_argument("--lista", default=URL_LISTA_ANDROZOO,
                   help="latest.csv.gz local ou URL (padrão: a URL oficial, em fluxo)")
    p.set_defaults(func=cmd_cobertura)

    p = sub.add_parser("amostra", help="sorteia os apps do piloto")
    p.add_argument("--cobertura", help="CSV da etapa cobertura (padrão: o mais recente)")
    p.add_argument("--n-gov", type=int, default=14)
    p.add_argument("--n-ctrl", type=int, default=6)
    p.add_argument("--semente", type=int, default=20261020)
    p.set_defaults(func=cmd_amostra)

    p = sub.add_parser("baixar", help="baixa os APKs da amostra (precisa da chave)")
    p.add_argument("--pausa", type=float, default=PAUSA)
    p.set_defaults(func=cmd_baixar)

    p = sub.add_parser("detectar", help="aplica os detectores A, B e C")
    p.add_argument("--exodus", help="JSON local da base do Exodus (padrão: baixa da API)")
    p.add_argument("--disconnect", help="services.json local (padrão: baixa do GitHub)")
    p.add_argument("--categorias-disconnect", nargs="+", default=list(CATEGORIAS_DISCONNECT))
    p.add_argument("--mobsf", help="pasta com relatórios JSON do MobSF, um <sha256>.json por APK")
    p.set_defaults(func=cmd_detectar)

    p = sub.add_parser("concordancia", help="κ de Fleiss e τ de Kendall")
    p.add_argument("--deteccao", help="JSON da etapa detectar (padrão: o mais recente)")
    p.set_defaults(func=cmd_concordancia)

    p = sub.add_parser("autoteste", help="valida a lógica sem rede")
    p.set_defaults(func=lambda a: autoteste())

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
