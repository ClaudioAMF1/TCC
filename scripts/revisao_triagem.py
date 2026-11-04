#!/usr/bin/env python3
"""
Revisão sistemática do N3: das exportações das bases à planilha de triagem.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O protocolo (tcc/revisao/protocolo-revisao-sistematica.md) roda 22 buscas em
cinco bases. Cada base exporta num formato (Scopus e IEEE em CSV, ACM em
BibTeX, BDTD em RIS), e o mesmo artigo aparece em várias. Juntar e tirar
duplicatas à mão é onde a contagem do fluxograma PRISMA se perde. Aqui isso é
automático e pode ser refeito a qualquer momento sem perder as decisões já
marcadas.

ETAPAS
------
    juntar        lê dados/revisao/buscas/, tira duplicatas e grava a planilha
                  de triagem; se já existe uma, mantém as decisões marcadas
    controle      confere o conjunto de controle do protocolo (Seção 5)
    amostra       sorteia registros já decididos para o reteste ou o orientador
    concordancia  κ de Cohen entre a decisão original e a da conferência
    prisma        números de cada fase para o fluxograma
    autoteste     testa as funções, sem rede e sem arquivo do usuário

NOMES DOS ARQUIVOS EXPORTADOS
-----------------------------
    <base>_<string>_<AAAAMMDD>[_<parte>].<csv|bib|ris>

    scopus_S1_20261105.csv    acm_S2_20261105_p2.bib    bdtd_BDTD1_20261105.ris

    base: scopus, ieee, acm, sol, bdtd, bola (bola de neve, digitado à mão)

DECISÕES NA PLANILHA
--------------------
    decisao_f1 / decisao_f2:  I inclui, E exclui, T talvez (só na F1),
                              R revisão da literatura (fonte de bola de neve)
    criterio_f1 / criterio_f2: código do critério de exclusão (EC1 a EC7)

Nada daqui vai para o repositório: as exportações do Scopus trazem o resumo, e
os termos de uso não permitem redistribuí-lo. Fica tudo em dados/revisao/.
"""

import argparse
import csv
import io
import json
import math
import random
import re
import shutil
import sys
import tempfile
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "dados" / "revisao"

# Ordem de preferência ao fundir duplicatas: a primeira base com o registro
# fornece os campos; as outras só preenchem o que faltar.
BASES = ("scopus", "ieee", "acm", "sol", "bdtd", "bola")
NOME_ARQUIVO = re.compile(
    r"^(?P<base>scopus|ieee|acm|sol|bdtd|bola)_(?P<string>[A-Za-z0-9]+)_"
    r"(?P<data>\d{8})(?:_[A-Za-z0-9]+)?$", re.I)

CAMPOS = ["id", "titulo", "autores", "ano", "veiculo", "tipo", "doi", "url",
          "bases", "strings", "outras_versoes", "resumo", "palavras_chave",
          "decisao_f1", "criterio_f1", "decisao_f2", "criterio_f2",
          "observacao"]
DECISOES = ["decisao_f1", "criterio_f1", "decisao_f2", "criterio_f2",
            "observacao"]

# Seção 5 do protocolo. (id, DOI, título, strings que têm de achar)
CONTROLE = [
    ("C01", "10.1145/3201064.3201089",
     "Third party tracking in the mobile ecosystem", "S2"),
    ("C02", "10.14722/ndss.2018.23353",
     "Apps, trackers, privacy, and regulators: a global study of the mobile "
     "tracking ecosystem", "S2"),
    ("C03", "10.14763/2021.4.1611",
     "Before and after GDPR: tracking in mobile apps", "S2"),
    ("C04", "",
     "A fait accompli? An empirical study into the absence of consent to "
     "third-party tracking in Android apps", "S2"),
    ("C05", "10.1145/3548606.3560564",
     "Freely given consent? Studying consent notice of third-party tracking "
     "and its violations of GDPR in Android apps", "S2"),
    ("C06", "10.1145/3324884.3416582",
     "Automated third-party library detection for Android applications: are "
     "we there yet?", "S1"),
    ("C07", "10.2478/popets-2019-0037",
     "MAPS: scaling privacy compliance analysis to a million apps", "S3"),
    ("C08", "10.1145/2884781.2884855",
     "Toward a framework for detecting privacy policy violations in Android "
     "application code", "S3"),
    ("C09", "10.1145/3485447.3512223",
     "Et tu, Brute? Privacy analysis of government websites and mobile apps",
     "S4a S2"),
    ("C10", "10.1145/3615366.3615426",
     "Third-party trackers in COVID-19 mobile applications can enable privacy "
     "leaks", "S4a S4b"),
    ("C11", "10.5753/jisa.2024.3882",
     "COVID-19 mobile applications: a study of trackers and data leaks",
     "S4b"),
]


# ===================================================================== leitura

def decodificar(bruto: bytes) -> str:
    try:
        return bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        return bruto.decode("cp1252")


def ler_planilha(caminho: Path):
    """CSV do script ou salvo à mão. O Excel em português grava com ';' e às
    vezes em Windows-1252; o Numbers grava com ',' em UTF-8."""
    texto = decodificar(Path(caminho).read_bytes())
    cab = texto.split("\n", 1)[0]
    sep = ";" if cab.count(";") > cab.count(",") else ","
    # Colunas a mais numa linha (vírgula sem aspas) vêm numa lista sob a
    # chave None; são descartadas em vez de derrubar a leitura.
    return [{k.strip(): (v or "").strip() for k, v in r.items()
             if k is not None and not isinstance(v, list)}
            for r in csv.DictReader(io.StringIO(texto, newline=""),
                                    delimiter=sep)]


def gravar_planilha(caminho: Path, linhas, campos):
    """';' e BOM: o Excel em português abre direto, com acento."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        for ln in linhas:
            w.writerow({k: re.sub(r"\s+", " ", str(ln.get(k, "") or ""))
                        .strip() for k in campos})


COLUNAS = {
    "titulo": ["title", "document title", "titulo", "título"],
    "autores": ["author full names", "authors", "autores"],
    "ano": ["year", "publication year", "ano"],
    "veiculo": ["source title", "publication title", "veiculo", "veículo"],
    "doi": ["doi"],
    "resumo": ["abstract", "resumo"],
    "tipo": ["document type", "document identifier", "tipo"],
    "url": ["link", "pdf link", "url"],
}
COLUNAS_PALAVRAS = ["author keywords", "index keywords", "ieee terms",
                    "inspec controlled terms", "palavras_chave",
                    "palavras-chave"]
SEM_RESUMO = re.compile(r"^\[?no abstract available\]?$", re.I)


def ano_de(s: str) -> str:
    m = re.search(r"(19|20)\d\d", s or "")
    return m.group(0) if m else ""


def registro_de_csv(linha: dict) -> dict:
    baixo = {k.lower().strip(): v for k, v in linha.items()}
    reg = {}
    for campo, nomes in COLUNAS.items():
        reg[campo] = next((baixo[n] for n in nomes if baixo.get(n)), "")
    reg["palavras_chave"] = "; ".join(baixo[n] for n in COLUNAS_PALAVRAS
                                      if baixo.get(n))
    reg["ano"] = ano_de(reg["ano"])
    if SEM_RESUMO.match(reg["resumo"].strip()):
        reg["resumo"] = ""
    return reg


ACENTOS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308",
           "~": "\u0303", "=": "\u0304", ".": "\u0307", "c": "\u0327",
           "u": "\u0306", "v": "\u030c", "H": "\u030b"}
_ACENTO = re.compile(
    r"\\(?:([`'^\"~=.])|([cuvH])(?=[\s{]))\s*\{?\s*([A-Za-z])\s*\}?")


def limpar_latex(s: str) -> str:
    s = re.sub(r"\\i(?![A-Za-z])", "i", s)
    s = _ACENTO.sub(lambda m: unicodedata.normalize(
        "NFC", m.group(3) + ACENTOS[m.group(1) or m.group(2)]), s)
    s = (s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
         .replace("--", "-"))
    s = re.sub(r"\\[A-Za-z]+\s*", " ", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


_NOME_CAMPO = re.compile(r"\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*")


def _campos_bib(corpo: str) -> dict:
    virg = corpo.find(",")
    if virg < 0:
        return {}
    p, n, out = virg + 1, len(corpo), {}
    while p < n:
        m = _NOME_CAMPO.match(corpo, p)
        if not m:
            break
        nome, p = m.group(1).lower(), m.end()
        if p < n and corpo[p] == "{":
            prof, q = 0, p
            while q < n:
                if corpo[q] == "{":
                    prof += 1
                elif corpo[q] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                q += 1
            valor, p = corpo[p + 1:q], q + 1
        elif p < n and corpo[p] == '"':
            q, prof = p + 1, 0
            while q < n and not (corpo[q] == '"' and prof == 0
                                 and corpo[q - 1] != "\\"):
                prof += {"{": 1, "}": -1}.get(corpo[q], 0)
                q += 1
            valor, p = corpo[p + 1:q], q + 1
        else:
            q = corpo.find(",", p)
            q = n if q < 0 else q
            valor, p = corpo[p:q], q
        out[nome] = limpar_latex(valor)
        while p < n and corpo[p] in " \t\r\n,":
            p += 1
    return out


def ler_bibtex(texto: str):
    regs, i, n = [], 0, len(texto)
    while True:
        j = texto.find("@", i)
        if j < 0:
            break
        m = re.match(r"@\s*([A-Za-z]+)\s*\{", texto[j:])
        if not m:
            i = j + 1
            continue
        tipo, k = m.group(1).lower(), j + m.end()
        prof, p = 1, k
        while p < n and prof > 0:
            prof += {"{": 1, "}": -1}.get(texto[p], 0)
            p += 1
        i = p
        if tipo in ("comment", "preamble", "string"):
            continue
        c = _campos_bib(texto[k:p - 1])
        regs.append({
            "titulo": c.get("title", ""),
            "autores": "; ".join(a.strip() for a in
                                 re.split(r"\s+and\s+", c.get("author", ""))
                                 if a.strip()),
            "ano": ano_de(c.get("year", "")),
            "veiculo": c.get("booktitle") or c.get("journal", ""),
            "doi": c.get("doi", ""),
            "resumo": c.get("abstract", ""),
            "palavras_chave": c.get("keywords", ""),
            "tipo": tipo,
            "url": c.get("url", ""),
        })
    return regs


def ler_ris(texto: str):
    brutos, atual, ultimo = [], {}, None
    for linha in texto.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  -\s?(.*)$", linha)
        if not m:
            if atual and ultimo and linha.strip():
                atual[ultimo][-1] += " " + linha.strip()
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            brutos.append(atual)
            atual, ultimo = {}, None
            continue
        atual.setdefault(tag, []).append(val)
        ultimo = tag
    if atual:
        brutos.append(atual)

    def um(r, *tags):
        return next((r[t][0] for t in tags if r.get(t)), "")

    return [{
        "titulo": um(r, "TI", "T1"),
        "autores": "; ".join(r.get("AU", []) or r.get("A1", [])),
        "ano": ano_de(um(r, "PY", "Y1", "DA")),
        "veiculo": um(r, "T2", "JO", "JF", "BT"),
        "doi": um(r, "DO"),
        "resumo": um(r, "AB", "N2"),
        "palavras_chave": "; ".join(r.get("KW", [])),
        "tipo": um(r, "TY"),
        "url": um(r, "UR"),
    } for r in brutos]


def ler_exportacao(caminho: Path):
    texto = decodificar(caminho.read_bytes())
    ext = caminho.suffix.lower()
    if ext == ".bib":
        return ler_bibtex(texto)
    if ext == ".ris":
        return ler_ris(texto)
    if ext == ".csv":
        return [registro_de_csv(ln) for ln in ler_planilha(caminho)]
    raise ValueError(f"formato não reconhecido: {caminho.name}")


def origem_de(caminho: Path):
    m = NOME_ARQUIVO.match(caminho.stem)
    if not m:
        return None
    return m.group("base").lower(), m.group("string"), m.group("data")


# ================================================================ duplicatas

def norm_doi(s: str) -> str:
    s = (s or "").strip().lower()
    m = re.search(r"10\.\d{4,9}/\S+", s)
    return m.group(0).rstrip(".;,") if m else ""


def chave_titulo(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def titulo_util(chave: str) -> bool:
    """Títulos de uma ou duas palavras ("Privacy") juntariam artigos
    diferentes."""
    return len(chave.split()) >= 4


def fundir(registros):
    """Junta por DOI e por título normalizado (união e busca). Cada registro
    traz 'base' e 'string'. Devolve uma lista de registros únicos."""
    pai = list(range(len(registros)))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    vistos = {}
    for i, r in enumerate(registros):
        for chave in (("doi", norm_doi(r.get("doi"))),
                      ("tit", chave_titulo(r.get("titulo")))):
            if not chave[1] or (chave[0] == "tit" and not titulo_util(chave[1])):
                continue
            if chave in vistos:
                pai[raiz(i)] = raiz(vistos[chave])
            else:
                vistos[chave] = i

    grupos = {}
    for i in range(len(registros)):
        grupos.setdefault(raiz(i), []).append(registros[i])

    unicos = []
    for membros in grupos.values():
        membros.sort(key=lambda r: (not norm_doi(r.get("doi")),
                                    not r.get("resumo"),
                                    BASES.index(r["base"])
                                    if r.get("base") in BASES else 99))
        u = {k: membros[0].get(k, "") for k in
             ("titulo", "autores", "ano", "veiculo", "tipo", "doi", "url",
              "resumo", "palavras_chave")}
        for outro in membros[1:]:
            for k in u:
                if not u[k] and outro.get(k):
                    u[k] = outro[k]
        u["doi"] = norm_doi(u["doi"])
        bases = {r["base"] for r in membros if r.get("base")}
        u["bases"] = "|".join(b for b in BASES if b in bases)
        u["strings"] = "|".join(sorted({f'{r["base"]}:{r["string"]}'
                                        for r in membros if r.get("base")}))
        outros = sorted({norm_doi(r.get("doi")) for r in membros}
                        - {u["doi"], ""})
        u["outras_versoes"] = " | ".join(outros)
        unicos.append(u)
    return unicos


def chaves_de(r):
    out = set()
    for d in [r.get("doi", "")] + (r.get("outras_versoes", "") or "").split("|"):
        d = norm_doi(d)
        if d:
            out.add(("doi", d))
    t = chave_titulo(r.get("titulo"))
    if titulo_util(t):
        out.add(("tit", t))
    return out


def manter_decisoes(unicos, anteriores):
    """Os ids e as decisões da planilha anterior passam para a nova. Registros
    que sumiram das exportações são mantidos, para não perder decisão."""
    indice = {}
    for a in anteriores:
        for ch in chaves_de(a):
            indice.setdefault(ch, a)
    usados, saida = set(), []
    for u in unicos:
        ant = next((indice[ch] for ch in chaves_de(u) if ch in indice), None)
        if ant is not None and ant["id"] not in usados:
            usados.add(ant["id"])
            u["id"] = ant["id"]
            for k in DECISOES:
                u[k] = ant.get(k, "")
        saida.append(u)
    sumidos = [a for a in anteriores if a.get("id") and a["id"] not in usados]
    saida.extend(sumidos)
    numeros = [int(r["id"][1:]) for r in saida
               if re.fullmatch(r"R\d+", r.get("id", ""))]
    prox = max(numeros, default=0) + 1
    novos = [u for u in saida if not u.get("id")]
    novos.sort(key=lambda r: chave_titulo(r.get("titulo")))
    for u in novos:
        u["id"] = f"R{prox:04d}"
        prox += 1
    saida.sort(key=lambda r: r["id"])
    return saida, len(sumidos), len(novos)


# ================================================================== etapas

def mais_recente(pasta: Path, padrao: str):
    achados = sorted(p for p in pasta.glob(padrao) if ".bak" not in p.suffixes)
    return achados[-1] if achados else None


def juntar(pasta: Path, hoje: str = None):
    buscas = pasta / "buscas"
    arquivos = sorted(p for p in buscas.glob("*")
                      if p.suffix.lower() in (".csv", ".bib", ".ris"))
    if not arquivos:
        sys.exit(f"Nenhuma exportação em {buscas}. Veja o passo a passo, "
                 "parte 2.")
    registros, contagem, ignorados = [], [], []
    for arq in arquivos:
        origem = origem_de(arq)
        if origem is None:
            ignorados.append(arq.name)
            continue
        base, string, data = origem
        regs = ler_exportacao(arq)
        for r in regs:
            r["base"], r["string"] = base, string
        registros.extend(regs)
        contagem.append({"arquivo": arq.name, "base": base, "string": string,
                         "data": data, "registros": len(regs)})
    if ignorados:
        print("Arquivos com nome fora do padrão (ignorados): "
              + ", ".join(ignorados))

    unicos = fundir(registros)
    anterior = mais_recente(pasta, "triagem_*.csv")
    anteriores = ler_planilha(anterior) if anterior else []
    linhas, sumidos, novos = manter_decisoes(unicos, anteriores)

    hoje = hoje or date.today().strftime("%Y%m%d")
    saida = pasta / f"triagem_{hoje}.csv"
    if saida.exists():
        shutil.copy2(saida, saida.with_suffix(".bak.csv"))
    gravar_planilha(saida, linhas, CAMPOS)

    bruto_bases = sum(c["registros"] for c in contagem if c["base"] != "bola")
    unicos_bases = sum(1 for u in unicos
                       if set(u["bases"].split("|")) - {"bola", ""})
    resumo = {"data": hoje, "arquivos": contagem, "bruto_bases": bruto_bases,
              "unicos_bases": unicos_bases,
              "duplicatas_bases": bruto_bases - unicos_bases,
              "unicos_total": len(unicos)}
    (pasta / "contagens.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nRESULTADO DA JUNÇÃO")
    print("  " + "=" * 62)
    print(f"  {'arquivo':<36} {'base':<7} {'string':<6} {'registros':>9}")
    for c in contagem:
        print(f"  {c['arquivo']:<36} {c['base']:<7} {c['string']:<6} "
              f"{c['registros']:>9}")
    print(f"\n  Registros das bases, com repetição: {bruto_bases}")
    print(f"  Duplicatas removidas:               {bruto_bases - unicos_bases}")
    print(f"  Registros únicos:                   {len(unicos)}")
    if anteriores:
        print(f"  Decisões mantidas de {anterior.name}; {novos} registros "
              f"novos; {sumidos} da planilha anterior sem exportação "
              "(mantidos).")
    if len(unicos) > 1500:
        print("\n  Mais de 1.500 registros: o protocolo prevê o refinamento da "
              "Seção 5. Me mande as contagens antes de triar.")
    print(f"\n  Planilha de triagem: {saida}")
    return saida


def achar_controle(linhas, doi, titulo):
    ct = chave_titulo(titulo)
    for r in linhas:
        if doi and ("doi", norm_doi(doi)) in chaves_de(r):
            return r
        rt = chave_titulo(r.get("titulo"))
        if rt and (rt == ct or (min(len(rt), len(ct)) >= 30
                                and (rt.startswith(ct) or ct.startswith(rt)))):
            return r
    return None


def controle(planilha: Path):
    linhas = ler_planilha(planilha)
    print("\nCONJUNTO DE CONTROLE (protocolo, Seção 5)")
    print("  " + "=" * 62)
    achados, falhas = 0, []
    for cid, doi, titulo, esperadas in CONTROLE:
        r = achar_controle(linhas, doi, titulo)
        if r is None:
            print(f"  {cid}  NÃO ACHADO   {titulo[:52]}")
            falhas.append(cid)
            continue
        achados += 1
        strings = set(s.split(":", 1)[1] for s in r.get("strings", "").split("|")
                      if ":" in s)
        faltam = [s for s in esperadas.split() if s not in strings]
        nota = "" if not faltam else f"   não veio pela {', '.join(faltam)}"
        print(f"  {cid}  achado ({r['id']})  {r.get('strings', '')}{nota}")
    print(f"\n  Achados: {achados} de {len(CONTROLE)}")
    if falhas:
        print("  Para cada não achado: busque o título exato na base. Se a base "
              "tem o artigo, a string falhou (me mande qual). Se não tem, é "
              "limite de cobertura e o artigo entra pela bola de neve.")


def decisao(v: str) -> str:
    v = (v or "").strip().upper()[:1]
    return v if v in "IETR" and v else ""


def amostra(planilha: Path, fase: str, n: int, semente: int, nome: str,
            pasta: Path):
    linhas = [r for r in ler_planilha(planilha)
              if decisao(r.get(f"decisao_{fase}"))]
    if not linhas:
        sys.exit(f"Nenhum registro decidido na {fase.upper()} ainda.")
    if n <= 0:
        n = max(30, math.ceil(0.10 * len(linhas)))
    n = min(n, len(linhas))
    sorteados = random.Random(semente).sample(linhas, n)
    sorteados.sort(key=lambda r: r["id"])
    saida = pasta / f"conferencia_{nome}_{date.today():%Y%m%d}.csv"
    gravar_planilha(saida, [{"id": r["id"], "titulo": r.get("titulo"),
                             "resumo": r.get("resumo"),
                             "palavras_chave": r.get("palavras_chave"),
                             "decisao": "", "criterio": ""}
                            for r in sorteados],
                    ["id", "titulo", "resumo", "palavras_chave", "decisao",
                     "criterio"])
    print(f"{n} de {len(linhas)} registros sorteados (semente {semente}).")
    print(f"Planilha sem as decisões originais: {saida}")


def kappa_cohen(pares):
    n = len(pares)
    if n == 0:
        return float("nan")
    cats = sorted({c for p in pares for c in p})
    po = sum(a == b for a, b in pares) / n
    pe = sum((sum(a == c for a, _ in pares) / n)
             * (sum(b == c for _, b in pares) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def binaria(d: str) -> str:
    return "passa" if d in ("I", "T") else "fica"


def concordancia(planilha: Path, conferencia: Path, fase: str):
    orig = {r["id"]: r for r in ler_planilha(planilha)}
    pares, diverg = [], []
    for c in ler_planilha(conferencia):
        o = orig.get(c.get("id"))
        a = decisao(o.get(f"decisao_{fase}")) if o else ""
        b = decisao(c.get("decisao"))
        if not (a and b):
            continue
        pares.append((a, b))
        if binaria(a) != binaria(b):
            diverg.append((c["id"], a, b, (o.get("titulo") or "")[:60]))
    if not pares:
        sys.exit("Nenhum par com as duas decisões preenchidas.")
    kb = kappa_cohen([(binaria(a), binaria(b)) for a, b in pares])
    k3 = kappa_cohen(pares)
    acordo = sum(binaria(a) == binaria(b) for a, b in pares) / len(pares)
    print(f"\nCONCORDÂNCIA NA {fase.upper()} ({len(pares)} pares)")
    print("  " + "=" * 62)
    print(f"  Acordo, passa (I ou T) contra fica (E ou R): {acordo:.1%}")
    print(f"  κ de Cohen, mesma divisão:                   {kb:.3f}")
    print(f"  κ de Cohen, I/E/T/R separados:               {k3:.3f}")
    print("  Critério do protocolo: κ ≥ 0,6 na divisão passa/fica.")
    if diverg:
        print("\n  Divergências:")
        for i, a, b, t in diverg:
            print(f"    {i}  original {a}  conferência {b}  {t}")


def prisma(planilha: Path, pasta: Path):
    linhas = ler_planilha(planilha)
    cont_arq = pasta / "contagens.json"
    cont = json.loads(cont_arq.read_text(encoding="utf-8")) if cont_arq.exists() else {}

    def de_bola(r):
        return set(r.get("bases", "").split("|")) - {""} == {"bola"}

    def fase(rs, rotulo):
        f1 = [decisao(r.get("decisao_f1")) for r in rs]
        passam = [r for r in rs if decisao(r.get("decisao_f1")) in ("I", "T")]
        exc1 = {}
        for r in rs:
            if decisao(r.get("decisao_f1")) == "E":
                c = r.get("criterio_f1") or "sem código"
                exc1[c] = exc1.get(c, 0) + 1
        nao_obtidos = [r for r in passam
                       if (r.get("criterio_f2") or "").upper() == "EC7"]
        avaliados = [r for r in passam if decisao(r.get("decisao_f2"))
                     and r not in nao_obtidos]
        exc2 = {}
        for r in avaliados:
            if decisao(r.get("decisao_f2")) == "E":
                c = r.get("criterio_f2") or "sem código"
                exc2[c] = exc2.get(c, 0) + 1
        incl = [r for r in avaliados if decisao(r.get("decisao_f2")) == "I"]
        print(f"\n  {rotulo}")
        print(f"    Triados em F1:                 {len(rs)}"
              f"  (sem decisão: {f1.count('')})")
        print(f"    Excluídos em F1:               {sum(exc1.values())}  "
              + ", ".join(f"{k} {v}" for k, v in sorted(exc1.items())))
        print(f"    Revisões (bola de neve):       {f1.count('R')}")
        print(f"    Buscados em texto completo:    {len(passam)}")
        print(f"    Não obtidos (EC7):             {len(nao_obtidos)}")
        print(f"    Avaliados em F2:               {len(avaliados)}"
              f"  (sem decisão: {len(passam) - len(nao_obtidos) - len(avaliados)})")
        print(f"    Excluídos em F2:               {sum(exc2.values())}  "
              + ", ".join(f"{k} {v}" for k, v in sorted(exc2.items())))
        print(f"    Incluídos:                     {len(incl)}")
        return len(incl)

    print("\nNÚMEROS PARA O FLUXOGRAMA PRISMA 2020")
    print("  " + "=" * 62)
    if cont:
        por_base = {}
        for c in cont.get("arquivos", []):
            if c["base"] != "bola":
                por_base[c["base"]] = por_base.get(c["base"], 0) + c["registros"]
        print("  Identificados nas bases: " + ", ".join(
            f"{b} {por_base[b]}" for b in BASES if b in por_base)
            + f"  (total {cont.get('bruto_bases', 0)})")
        print(f"  Duplicatas removidas:    {cont.get('duplicatas_bases', 0)}")
    a = fase([r for r in linhas if not de_bola(r)], "Bases")
    b = fase([r for r in linhas if de_bola(r)], "Bola de neve")
    print(f"\n  Total de estudos incluídos: {a + b}")


# ================================================================ autoteste

def autoteste():
    ok = True

    def confere(cond, msg):
        nonlocal ok
        print(("  ok    " if cond else "  FALHA ") + msg)
        ok = ok and cond

    print("Autoteste")
    confere(origem_de(Path("acm_S2_20261105_p2.bib"))
            == ("acm", "S2", "20261105"), "nome de arquivo com parte")
    confere(origem_de(Path("Scopus_S4a_20261105.csv"))
            == ("scopus", "S4a", "20261105"), "nome de arquivo com S4a")
    confere(origem_de(Path("minha_busca.csv")) is None,
            "nome fora do padrão é ignorado")

    bib = r"""
@inproceedings{10.1145/1,
author = {Silva, Jo{\~a}o and Doe, J.},
title = {The {GDPR} and Tracking: An {\'E}tica \c{c}ase},
year = {2021},
booktitle = {Proc. of X},
doi = {10.1145/1},
abstract = {We study {nested {braces}} and 50\% of apps.},
keywords = {privacy, trackers}
}
@comment{ignorar}
@article{k2, title = "Other {Paper} Title Here", author = "A, B", year = 2020}
"""
    regs = ler_bibtex(bib)
    confere(len(regs) == 2, "BibTeX: duas entradas, comentário ignorado")
    confere(regs[0]["titulo"] == "The GDPR and Tracking: An Ética çase",
            f"BibTeX: acentos e chaves ({regs[0]['titulo']!r})")
    confere(regs[0]["autores"] == "Silva, João; Doe, J.", "BibTeX: autores")
    confere(regs[0]["resumo"] == "We study nested braces and 50% of apps.",
            "BibTeX: resumo com chaves aninhadas")
    confere(regs[1]["titulo"] == "Other Paper Title Here"
            and regs[1]["ano"] == "2020", "BibTeX: aspas e valor sem chave")

    ris = ("TY  - JOUR\nTI  - Um estudo de rastreadores em aplicativos\n"
           "AU  - Souza, A.\nAU  - Lima, B.\nPY  - 2023///\n"
           "AB  - Primeira linha\ncontinuação do resumo\nDO  - 10.5753/X.1\n"
           "ER  - \nTY  - THES\nTI  - Tese sobre LGPD\nER  - \n")
    regs = ler_ris(ris)
    confere(len(regs) == 2 and regs[0]["autores"] == "Souza, A.; Lima, B.",
            "RIS: dois registros e autores")
    confere(regs[0]["resumo"] == "Primeira linha continuação do resumo"
            and regs[0]["ano"] == "2023", "RIS: linha de continuação e ano")

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "buscas").mkdir()
        scopus = ("\ufeffAuthors,Author full names,Title,Year,Source title,DOI,"
                  "Link,Abstract,Author Keywords,Index Keywords,Document Type\n"
                  'X,"Binns, Reuben",Third party tracking in the mobile '
                  "ecosystem,2018,WebSci,10.1145/3201064.3201089,u,"
                  '"Apps, trackers",k1,k2,Conference paper\n'
                  "Y,Y,Privacy,2020,Z,,u,[No abstract available],,,Article\n")
        (p / "buscas" / "scopus_S2_20261105.csv").write_text(
            scopus, encoding="utf-8")
        ieee = ('"Document Title",Authors,"Publication Title",'
                '"Publication Year",Abstract,DOI,"PDF Link"\n'
                '"Third Party Tracking in the Mobile Ecosystem",R. Binns,'
                'WebSci,2018,,https://doi.org/10.1145/3201064.3201089,l\n'
                '"Third-party library detection: are we there yet",X. Zhan,'
                'ASE,2020,"TPL tools",,l\n')
        (p / "buscas" / "ieee_S1_20261105.csv").write_text(ieee,
                                                           encoding="utf-8")
        bib2 = ("@inproceedings{a, title={Third-Party Library Detection: "
                "Are We There Yet?}, doi={10.1145/3324884.3416582}, "
                "year={2020}}")
        (p / "buscas" / "acm_S1_20261105.bib").write_text(bib2,
                                                          encoding="utf-8")
        (p / "buscas" / "anotacoes.csv").write_text("x\n", encoding="utf-8")

        saida = juntar(p, hoje="20261105")
        linhas = ler_planilha(saida)
        confere(len(linhas) == 3, f"junção: 5 registros viram 3 ({len(linhas)})")
        binns = next(r for r in linhas if r["doi"] == "10.1145/3201064.3201089")
        confere(binns["bases"] == "scopus|ieee"
                and binns["strings"] == "ieee:S1|scopus:S2"
                and binns["resumo"] == "Apps, trackers",
                "junção por DOI com prefixo https e resumo preservado")
        zhan = next(r for r in linhas if "library" in r["titulo"].lower())
        confere(zhan["doi"] == "10.1145/3324884.3416582"
                and zhan["bases"] == "ieee|acm",
                "junção por título; DOI vem do registro que tem")
        priv = next(r for r in linhas if r["titulo"] == "Privacy")
        confere(priv["resumo"] == "", "'[No abstract available]' vira vazio")
        cont = json.loads((p / "contagens.json").read_text(encoding="utf-8"))
        confere(cont["bruto_bases"] == 5 and cont["duplicatas_bases"] == 2,
                "contagens para o PRISMA")

        # Marca decisões, acrescenta uma exportação e junta de novo.
        for r in linhas:
            if r["id"] == binns["id"]:
                r["decisao_f1"], r["observacao"] = "I", "controle"
        gravar_planilha(saida, linhas, CAMPOS)
        (p / "buscas" / "scopus_S4a_20261106.csv").write_text(
            'Title,Year,DOI\n"Et tu, Brute? Privacy analysis of government '
            'websites and mobile apps",2022,10.1145/3485447.3512223\n',
            encoding="utf-8")
        saida2 = juntar(p, hoje="20261106")
        linhas2 = ler_planilha(saida2)
        b2 = next(r for r in linhas2 if r["doi"] == "10.1145/3201064.3201089")
        confere(b2["id"] == binns["id"] and b2["decisao_f1"] == "I"
                and b2["observacao"] == "controle",
                "nova junção mantém id e decisão")
        novo = next(r for r in linhas2 if r["doi"] == "10.1145/3485447.3512223")
        confere(novo["id"] == "R0004", f"registro novo recebe o próximo id "
                f"({novo['id']})")
        c9 = achar_controle(linhas2, "", "Et tu, Brute? Privacy analysis of "
                            "government websites and mobile apps")
        confere(c9 is not None, "controle achado só pelo título")

    pares = [("P", "P")] * 4 + [("N", "N")] * 4 + [("P", "N"), ("N", "P")]
    confere(abs(kappa_cohen(pares) - 0.6) < 1e-9, "κ de Cohen = 0,6 no "
            "exemplo de conta feita à mão")
    confere(decisao(" t ") == "T" and decisao("x") == "" and decisao("") == "",
            "leitura das decisões")

    print("\nAUTOTESTE OK" if ok else "\nAUTOTESTE COM FALHA")
    return 0 if ok else 1


# ===================================================================== main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="etapa", required=True)
    sub.add_parser("juntar")
    sub.add_parser("autoteste")
    for nome in ("controle", "prisma"):
        s = sub.add_parser(nome)
        s.add_argument("--planilha", type=Path)
    s = sub.add_parser("amostra")
    s.add_argument("--planilha", type=Path)
    s.add_argument("--fase", choices=["f1", "f2"], default="f1")
    s.add_argument("--n", type=int, default=0,
                   help="0 = 10%% dos decididos, no mínimo 30")
    s.add_argument("--semente", type=int, default=20261116)
    s.add_argument("--nome", default="reteste")
    s = sub.add_parser("concordancia")
    s.add_argument("conferencia", type=Path)
    s.add_argument("--planilha", type=Path)
    s.add_argument("--fase", choices=["f1", "f2"], default="f1")
    a = ap.parse_args()

    if a.etapa == "autoteste":
        sys.exit(autoteste())
    if a.etapa == "juntar":
        juntar(PASTA)
        return
    planilha = a.planilha or mais_recente(PASTA, "triagem_*.csv")
    if planilha is None:
        sys.exit("Não achei dados/revisao/triagem_*.csv. Rode antes: "
                 "python3 scripts/revisao_triagem.py juntar")
    if a.etapa == "controle":
        controle(planilha)
    elif a.etapa == "prisma":
        prisma(planilha, PASTA)
    elif a.etapa == "amostra":
        amostra(planilha, a.fase, a.n, a.semente, a.nome, PASTA)
    elif a.etapa == "concordancia":
        concordancia(planilha, a.conferencia, a.fase)


if __name__ == "__main__":
    main()
