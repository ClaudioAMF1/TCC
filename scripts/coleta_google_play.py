#!/usr/bin/env python3
"""
Coleta direta da Google Play, com o hash de cada APK registrado.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O piloto mostrou que o AndroZoo tem só 92 dos 396 apps de governo (23%), e
que, na mesma faixa de instalações, a chance de um app de governo estar lá é
bem menor que a de um comercial. Os outros 304 precisam vir direto da loja.

Este script baixa, confere e registra. Cada APK sai com SHA-256, versionCode,
data e fonte, numa planilha no mesmo formato da amostra do piloto, e o APK
base cai na mesma pasta dados/apks/ que a etapa 'detectar' já lê.

QUEM BAIXA É O apkeep
---------------------
Ferramenta de código aberto da EFF (github.com/EFForg/apkeep). Este script não
reimplementa o protocolo da loja: chama o apkeep, acha o APK base no que ele
baixou, confere o pacote e registra.

Duas observações da documentação do apkeep entram no desenho:

- app restrito por região só baixa se a conta já o tiver baixado com IP do
  país. Rodando do Brasil isso joga a favor; quando falha, a falha vira dado:
  quantos apps de governo não estão disponíveis para coleta automática;
- app publicado como App Bundle vem em APKs divididos. O script tenta o APK
  completo e, se não vier, os divididos, e guarda o 'base', que tem o código.

CREDENCIAIS
-----------
Uma conta Google criada para a pesquisa, não a pessoal. O token AAS é obtido
uma vez (passo a passo em tcc/coleta-passo-a-passo.md) e fica só no
ambiente:

    export GOOGLE_PLAY_EMAIL="conta.da.pesquisa@gmail.com"
    export GOOGLE_PLAY_AAS_TOKEN="..."

O script entrega as credenciais ao apkeep num arquivo temporário com permissão
600, apagado ao fim. Elas não vão para a linha de comando nem para mensagem.

USO
---
    python3 scripts/coleta_google_play.py autoteste
    python3 scripts/coleta_google_play.py teste              # 5 apps fora do AndroZoo
    python3 scripts/coleta_google_play.py teste --n 10
    python3 scripts/coleta_google_play.py lista --arquivo dados/lista.csv   # coluna appId
    python3 scripts/coleta_google_play.py corpus             # governo e controle inteiros
    python3 scripts/coleta_google_play.py corpus --so-fora-do-androzoo

SAÍDA (em dados/, que não é versionado)
-----
    dados/apks/<SHA256>.apk          APK base, ao lado dos que vieram do AndroZoo
    dados/apks_play/<appId>/         tudo o que o apkeep baixou, inclusive divididos
    dados/coleta_play_AAAAMMDD.csv   uma linha por app; serve de amostra para
                                     'piloto_androzoo.py detectar --amostra'
"""

import argparse
import csv
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from piloto_androzoo import (DADOS, HOJE, ler_planilha, mais_recente,  # noqa: E402
                             sha256_arquivo, wilson)

PAUSA = 5.0
OPCOES_BASE = "locale=pt_BR,timezone=America/Sao_Paulo"
CAMPOS = ["appId", "grupo", "esfera", "sensivel", "categoria", "faixa", "fonte",
          "data_utc", "status", "motivo", "modo", "sha256", "vercode", "versao",
          "pacote_apk", "tamanho", "n_divididos", "arquivo"]


def mascarar(texto: str) -> str:
    """Tira o token de qualquer texto antes de imprimir ou gravar."""
    texto = str(texto)
    token = os.environ.get("GOOGLE_PLAY_AAS_TOKEN")
    if token:
        texto = texto.replace(token, "***")
    return re.sub(r"(aas_token\s*=\s*|-t\s+)\S+", r"\1***", texto)


# ================================================================= credenciais

def credenciais():
    email = os.environ.get("GOOGLE_PLAY_EMAIL")
    token = os.environ.get("GOOGLE_PLAY_AAS_TOKEN")
    if not email or not token:
        sys.exit("Faltam as credenciais. Só no terminal, nunca em arquivo do repositório:\n\n"
                 '    export GOOGLE_PLAY_EMAIL="conta.da.pesquisa@gmail.com"\n'
                 '    read -s "GOOGLE_PLAY_AAS_TOKEN?Token AAS: " && export GOOGLE_PLAY_AAS_TOKEN\n\n'
                 "Como obter o token: tcc/coleta-passo-a-passo.md")
    return email, token


def escrever_ini(email, token):
    """Arquivo de configuração do apkeep, legível só pelo dono, fora do
    repositório. Devolve (caminho, pasta temporária para apagar depois)."""
    pasta = Path(tempfile.mkdtemp(prefix="apkeep_"))
    ini = pasta / "apkeep.ini"
    ini.write_text(f"[google]\nemail = {email}\naas_token = {token}\n", encoding="utf-8")
    os.chmod(ini, 0o600)
    return ini, pasta


# ================================================================= o que baixou

def _e_apk(caminho: Path):
    """(é APK?, tem código?) olhando o conteúdo do zip, não a extensão."""
    try:
        with zipfile.ZipFile(caminho) as z:
            nomes = z.namelist()
    except (zipfile.BadZipFile, OSError):
        return False, False
    return ("AndroidManifest.xml" in nomes,
            any(re.fullmatch(r"classes\d*\.dex", n) for n in nomes))


def achar_base(pasta: Path, app_id: str):
    """Acha o APK base no que o apkeep deixou na pasta. Aceita APK único, APKs
    divididos soltos e contêiner (.apks, .xapk ou zip com APKs dentro).
    Devolve (caminho do base ou None, lista dos divididos)."""
    for cont in list(pasta.rglob("*")):
        if not cont.is_file() or cont.parent.name == "_extraido":
            continue
        e_apk, _ = _e_apk(cont)
        if e_apk or not zipfile.is_zipfile(cont):
            continue
        destino = cont.parent / "_extraido"
        with zipfile.ZipFile(cont) as z:
            for n in z.namelist():
                if n.endswith(".apk") and "/" not in n.strip("/"):
                    destino.mkdir(exist_ok=True)
                    (destino / Path(n).name).write_bytes(z.read(n))
    apks = []
    for f in sorted(pasta.rglob("*")):
        if f.is_file():
            e_apk, tem_dex = _e_apk(f)
            if e_apk:
                apks.append((f, tem_dex))
    com_dex = [f for f, d in apks if d]
    if not com_dex:
        return None, [f for f, _ in apks]
    preferidos = [f for f in com_dex if f.name in (f"{app_id}.apk", "base.apk")]
    base = preferidos[0] if preferidos else max(com_dex, key=lambda f: f.stat().st_size)
    return base, [f for f, _ in apks if f != base]


def info_apk(caminho: Path):
    """(pacote, versionCode, versionName) pelo Androguard; None se não houver."""
    try:
        try:
            from loguru import logger
            logger.remove()
        except ImportError:
            pass
        from androguard.core.apk import APK
    except ImportError:
        return None, None, None
    try:
        a = APK(str(caminho))
        return a.get_package(), a.get_androidversion_code(), a.get_androidversion_name()
    except Exception:  # noqa: BLE001 — APK ilegível vira falha registrada, não erro
        return None, None, None


MOTIVOS = [
    (r"invalid app response", "indisponível para a conta ou a região, ou removido da loja"),
    (r"\b(401|403)\b|unauthori[sz]ed|authenticat|token", "falha de autenticação"),
    (r"\b404\b|not found|notfound", "não encontrado na loja"),
    (r"timed? ?out|timeout", "tempo esgotado"),
]


def motivo_falha(texto: str) -> str:
    t = (texto or "").lower()
    for padrao, motivo in MOTIVOS:
        if re.search(padrao, t):
            return motivo
    linhas = [l.strip() for l in mascarar(texto).splitlines() if l.strip()]
    return (linhas[-1][:120] if linhas else "nada foi baixado, sem mensagem")


# ===================================================================== coleta

def rodar_apkeep(apkeep, app_id, destino, ini, opcoes):
    cmd = [apkeep, "-a", app_id, "-d", "google-play", "-i", str(ini), "-o", opcoes,
           str(destino)]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        return mascarar(r.stdout + "\n" + r.stderr)
    except subprocess.TimeoutExpired:
        return "timeout"


def coletar_um(app, args, ini, executar=rodar_apkeep, info=info_apk):
    app_id = app["appId"]
    pasta = DADOS / "apks_play" / app_id
    linha = {k: app.get(k, "") for k in ("appId", "grupo", "esfera", "sensivel",
                                         "categoria", "faixa")}
    linha.update({"fonte": "google-play",
                  "data_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    if pasta.exists() and args.refazer:
        shutil.rmtree(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    base, divididos = achar_base(pasta, app_id)
    modo, saida = ("já baixado" if base else ""), ""
    for nome_modo, opcoes in (("completo", OPCOES_BASE),
                              ("dividido", OPCOES_BASE + ",split_apk=true")):
        if base:
            break
        saida = executar(args.apkeep, app_id, pasta, ini, opcoes)
        base, divididos = achar_base(pasta, app_id)
        modo = nome_modo
    if not base:
        linha.update({"status": "falha", "motivo": motivo_falha(saida), "modo": ""})
        return linha

    sha = sha256_arquivo(base)
    pacote, vercode, versao = info(base)
    destino = DADOS / "apks" / f"{sha}.apk"
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        shutil.copy2(base, destino)
    linha.update({"status": "ok", "motivo": "", "modo": modo, "sha256": sha,
                  "vercode": vercode or "", "versao": versao or "",
                  "pacote_apk": pacote or "", "tamanho": base.stat().st_size,
                  "n_divididos": len(divididos), "arquivo": str(destino)})
    if pacote and pacote != app_id:
        linha.update({"status": "falha", "motivo": f"pacote do APK é {pacote}"})
    return linha


def gravar(linhas_novas):
    """Atualiza a planilha do dia app por app: rodar de novo retoma, não apaga."""
    saida = DADOS / f"coleta_play_{HOJE}.csv"
    existentes = {}
    if saida.exists():
        existentes = {r["appId"]: r for r in ler_planilha(saida)}
    for r in linhas_novas:
        existentes[r["appId"]] = r
    DADOS.mkdir(exist_ok=True)
    with saida.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(existentes.values())
    return saida, list(existentes.values())


def relatar(linhas, saida):
    print("\n  RESULTADO")
    print("  " + "=" * 62)
    ok = [r for r in linhas if r.get("status") == "ok"]
    lo, hi = wilson(len(ok), len(linhas))
    print(f"  Baixados e conferidos: {len(ok)} de {len(linhas)}"
          + (f"  (IC95% {lo:.0%} a {hi:.0%})" if linhas else ""))
    modos = Counter(r.get("modo") for r in ok)
    if modos:
        print("  Modo: " + ", ".join(f"{m} {n}" for m, n in modos.items()))
    falhas = Counter(r.get("motivo") for r in linhas if r.get("status") != "ok")
    for m, n in falhas.most_common():
        print(f"    falha: {n}  {m}")
    por_faixa = defaultdict(lambda: [0, 0])
    for r in linhas:
        por_faixa[r.get("faixa") or "?"][1] += 1
        por_faixa[r.get("faixa") or "?"][0] += r.get("status") == "ok"
    if len(por_faixa) > 1:
        print("  Por faixa de instalações:")
        for fx, (k, n) in sorted(por_faixa.items()):
            print(f"      {fx:<6} {k}/{n}")
    print(f"\n  Planilha: {saida}")
    if ok:
        print("  Para detectar rastreadores nesses APKs:")
        print(f"    python3 scripts/piloto_androzoo.py detectar --amostra {saida}\n")


# ================================================================== seleção

def faixa_grupo(faixa: str) -> str:
    try:
        e = int(str(faixa).split("^")[1])
    except (IndexError, ValueError):
        return "?"
    return "baixa" if e <= 2 else ("media" if e <= 4 else "alta")


def selecionar_teste(linhas, n, semente):
    """n apps de governo fora do AndroZoo, alternando faixa baixa, média e
    alta. O teste precisa incluir os pequenos: é neles que a coleta é difícil."""
    rng = random.Random(semente)
    grupos = defaultdict(list)
    for r in linhas:
        if r.get("grupo") == "governo" and r.get("no_androzoo") == "não":
            grupos[faixa_grupo(r.get("faixa"))].append(r)
    for g in grupos.values():
        g.sort(key=lambda r: r["appId"])
        rng.shuffle(g)
    ordem = [g for g in ("baixa", "media", "alta", "?") if grupos.get(g)]
    escolhidos = []
    while len(escolhidos) < n and any(grupos[g] for g in ordem):
        for g in ordem:
            if grupos[g] and len(escolhidos) < n:
                escolhidos.append(grupos[g].pop())
    return escolhidos


def carregar_lista(args):
    if args.modo == "lista":
        return [r for r in ler_planilha(Path(args.arquivo)) if r.get("appId")]
    cobertura = mais_recente("piloto_cobertura_*.csv")
    if not cobertura:
        sys.exit("Rode antes: python3 scripts/piloto_androzoo.py cobertura --lista ...")
    linhas = ler_planilha(cobertura)
    if args.modo == "teste":
        return selecionar_teste(linhas, args.n, args.semente)
    if args.so_fora_do_androzoo:
        linhas = [r for r in linhas if r.get("no_androzoo") == "não"]
    return linhas[:args.limite] if args.limite else linhas


# ================================================================= autoteste

def _zip(caminho, nomes):
    with zipfile.ZipFile(caminho, "w") as z:
        for n in nomes:
            z.writestr(n, b"x" * (50 if n.endswith(".dex") else 10))


def autoteste():
    falhas = []
    tmp = Path(tempfile.mkdtemp(prefix="coleta_autoteste_"))
    global DADOS
    dados_original = DADOS
    DADOS = tmp / "dados"
    try:
        # 1. APK único
        p = tmp / "a"
        p.mkdir()
        _zip(p / "br.gov.x.apk", ["AndroidManifest.xml", "classes.dex"])
        base, div = achar_base(p, "br.gov.x")
        if not base or base.name != "br.gov.x.apk" or div:
            falhas.append(f"APK único: base={base}, divididos={div}")
        # 2. divididos soltos: o base é o que tem código
        p = tmp / "b"
        p.mkdir()
        _zip(p / "base.apk", ["AndroidManifest.xml", "classes.dex", "classes2.dex"])
        _zip(p / "split_config.arm64_v8a.apk", ["AndroidManifest.xml", "lib/x.so"])
        base, div = achar_base(p, "br.gov.y")
        if not base or base.name != "base.apk" or len(div) != 1:
            falhas.append(f"divididos: base={base}, divididos={div}")
        # 3. contêiner .apks com APKs dentro
        p = tmp / "c"
        p.mkdir()
        interno = tmp / "interno.apk"
        _zip(interno, ["AndroidManifest.xml", "classes.dex"])
        with zipfile.ZipFile(p / "br.gov.z.apks", "w") as z:
            z.write(interno, "base.apk")
            z.writestr("split_config.pt.apk", b"nao e zip")
            z.writestr("toc.pb", b"x")
        base, _ = achar_base(p, "br.gov.z")
        if not base or base.name != "base.apk" or base.parent.name != "_extraido":
            falhas.append(f"contêiner: base={base}")
        # 4. nada com código
        p = tmp / "d"
        p.mkdir()
        _zip(p / "so_recursos.apk", ["AndroidManifest.xml", "res/x.xml"])
        base, _ = achar_base(p, "br.gov.w")
        if base is not None:
            falhas.append("APK sem classes.dex não pode ser o base")

        # 5. motivos de falha
        for texto, esp in (("Error: Invalid app response", "indisponível"),
                           ("HTTP 401 Unauthorized", "autenticação"),
                           ("app not found", "não encontrado"), ("", "sem mensagem")):
            if esp not in motivo_falha(texto):
                falhas.append(f"motivo_falha({texto!r}) = {motivo_falha(texto)!r}")

        # 6. credenciais: arquivo 600, token mascarado
        os.environ["GOOGLE_PLAY_AAS_TOKEN"] = "tok-secreto-123"
        ini, pasta_ini = escrever_ini("x@gmail.com", "tok-secreto-123")
        if oct(ini.stat().st_mode & 0o777) != "0o600":
            falhas.append(f"ini com permissão {oct(ini.stat().st_mode & 0o777)}")
        if "tok-secreto-123" in mascarar("aas_token = tok-secreto-123 e -t tok-secreto-123"):
            falhas.append("token apareceu em mensagem")
        shutil.rmtree(pasta_ini)
        del os.environ["GOOGLE_PLAY_AAS_TOKEN"]

        # 7. seleção: repetível e alternando faixas
        linhas = [{"grupo": "governo", "appId": f"g{i}", "no_androzoo": "não",
                   "faixa": f"10^{i % 7}"} for i in range(30)]
        linhas += [{"grupo": "governo", "appId": "no_acervo", "no_androzoo": "sim",
                    "faixa": "10^2"}, {"grupo": "controle", "appId": "c1",
                                       "no_androzoo": "não", "faixa": "10^2"}]
        s1, s2 = selecionar_teste(linhas, 5, 7), selecionar_teste(linhas, 5, 7)
        if [r["appId"] for r in s1] != [r["appId"] for r in s2]:
            falhas.append("seleção muda com a mesma semente")
        if {faixa_grupo(r["faixa"]) for r in s1} != {"baixa", "media", "alta"}:
            falhas.append("seleção não passou pelas três faixas")
        if any(r["appId"] in ("no_acervo", "c1") for r in s1):
            falhas.append("seleção pegou app do acervo ou do controle")

        # 8. coleta com apkeep simulado: o completo falha, o dividido funciona
        chamadas = []

        def apkeep_falso(_bin, app_id, destino, _ini, opcoes):
            chamadas.append((app_id, opcoes))
            if app_id == "br.gov.bloqueado":
                return "Error: Invalid app response"
            if "split_apk=true" in opcoes:
                _zip(destino / "base.apk", ["AndroidManifest.xml", "classes.dex"])
                _zip(destino / "split_config.xxhdpi.apk", ["AndroidManifest.xml"])
            return ""

        args = argparse.Namespace(apkeep="apkeep", refazer=False)
        ok = coletar_um({"appId": "br.gov.ok", "grupo": "governo"}, args, Path("x"),
                        executar=apkeep_falso,
                        info=lambda c: ("br.gov.ok", 42, "1.0"))
        if (ok["status"], ok["modo"], ok["vercode"], ok["n_divididos"]) != \
                ("ok", "dividido", 42, 1):
            falhas.append(f"coleta com divididos = {ok}")
        if not (DADOS / "apks" / f"{ok['sha256']}.apk").exists():
            falhas.append("APK base não foi para dados/apks/")
        if [o for a, o in chamadas if a == "br.gov.ok"] != \
                [OPCOES_BASE, OPCOES_BASE + ",split_apk=true"]:
            falhas.append(f"ordem das tentativas = {chamadas}")
        ruim = coletar_um({"appId": "br.gov.bloqueado", "grupo": "governo"}, args,
                          Path("x"), executar=apkeep_falso, info=lambda c: (None,) * 3)
        if ruim["status"] != "falha" or "indisponível" not in ruim["motivo"]:
            falhas.append(f"falha de região = {ruim}")
        trocado = coletar_um({"appId": "br.gov.ok2", "grupo": "governo"}, args, Path("x"),
                             executar=apkeep_falso,
                             info=lambda c: ("com.outro", 1, "1"))
        if trocado["status"] != "falha" or "com.outro" not in trocado["motivo"]:
            falhas.append(f"pacote trocado não foi barrado: {trocado}")
        n_antes = len(chamadas)
        coletar_um({"appId": "br.gov.ok", "grupo": "governo"}, args, Path("x"),
                   executar=apkeep_falso, info=lambda c: ("br.gov.ok", 42, "1.0"))
        if len(chamadas) != n_antes:
            falhas.append("baixou de novo o que já estava na pasta")

        # 9. planilha do dia: rodar de novo atualiza, não apaga
        saida, todas = gravar([ok, ruim])
        _, todas = gravar([dict(ruim, status="ok", motivo="")])
        if len(todas) != 2 or {r["appId"]: r["status"] for r in todas} != \
                {"br.gov.ok": "ok", "br.gov.bloqueado": "ok"}:
            falhas.append(f"planilha do dia = {todas}")
    finally:
        DADOS = dados_original
        shutil.rmtree(tmp, ignore_errors=True)

    if falhas:
        print("AUTOTESTE FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print("AUTOTESTE OK — 9 grupos de verificação passaram, sem rede e sem apkeep.")


# ======================================================================= main

def main():
    ap = argparse.ArgumentParser(description="Coleta direta da Google Play pelo apkeep.")
    sub = ap.add_subparsers(dest="modo", required=True)
    for nome, ajuda in (("teste", "n apps de governo fora do AndroZoo"),
                        ("lista", "apps de uma planilha com coluna appId"),
                        ("corpus", "governo e controle da planilha de cobertura")):
        p = sub.add_parser(nome, help=ajuda)
        p.add_argument("--apkeep", default=shutil.which("apkeep") or "apkeep")
        p.add_argument("--pausa", type=float, default=PAUSA)
        p.add_argument("--refazer", action="store_true", help="apaga e baixa de novo")
        if nome == "teste":
            p.add_argument("--n", type=int, default=5)
            p.add_argument("--semente", type=int, default=20261028)
        if nome == "lista":
            p.add_argument("--arquivo", required=True)
        if nome == "corpus":
            p.add_argument("--so-fora-do-androzoo", action="store_true")
            p.add_argument("--limite", type=int)
    sub.add_parser("autoteste", help="valida a lógica sem rede")
    args = ap.parse_args()

    if args.modo == "autoteste":
        autoteste()
        return
    if not shutil.which(args.apkeep) and not Path(args.apkeep).exists():
        sys.exit("Não achei o apkeep. Instale pelo passo a passo:\n"
                 "    tcc/coleta-passo-a-passo.md")
    email, token = credenciais()
    apps = carregar_lista(args)
    print(f"\n  COLETA DIRETA DA GOOGLE PLAY ({len(apps)} apps)")
    print("  " + "=" * 62)
    ini, pasta_ini = escrever_ini(email, token)
    linhas = []
    try:
        for i, app in enumerate(apps, 1):
            r = coletar_um(app, args, ini)
            linhas.append(r)
            gravar([r])
            estado = (f"ok  {int(r['tamanho']) / 1e6:6.1f} MB  {r['modo']:<10}"
                      if r["status"] == "ok" else f"FALHA  {r['motivo'][:40]}")
            print(f"  [{i:>3}/{len(apps)}] {estado}  {app['appId']}")
            if r.get("modo") != "já baixado" and i < len(apps):
                time.sleep(args.pausa)
    finally:
        shutil.rmtree(pasta_ini, ignore_errors=True)
    saida, _ = gravar([])
    relatar(linhas, saida)


if __name__ == "__main__":
    main()
