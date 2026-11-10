#!/usr/bin/env python3
"""
Concordância entre avaliadores nas amostras cegas (150 artigos e 100 apps).

QUEM É COMPARADO
----------------
  autor     as planilhas cegas que o autor preenche:
            dados/segundo_avaliador/cega_artigos150_claudio.xlsx
            dados/segundo_avaliador/cega_apps100_claudio.xlsx
            (ou o mesmo nome em .csv, se ele salvar assim)
  sugestao  a pré-triagem assistida (protocolo, Seção 7.3): as colunas
            sugestao_f1 e sugestao_criterio de dados/revisao/triagem_*.csv e
            as colunas "sugerido" de dados/classificacao_396_para_conferir.xlsx
  <nome>    cada arquivo dados/segundo_avaliador/resposta_artigos_<nome>.csv
            e resposta_apps_<nome>.csv (segundo avaliador; o prompt está em
            tcc/revisao/prompt-segundo-avaliador.md)

O QUE MEDE
----------
Artigos: a decisão (I, T, E, R), a decisão que importa para a F2 (I ou T contra
E ou R) e o critério quando os dois excluem. Apps: oficial (S, N, ?) e, quando
os dois dizem S, a esfera e o dado sensível. Para cada par, a concordância
simples e o κ de Cohen; para todos juntos, o κ de Fleiss.

Os 5 apps da amostra que o autor já tinha validado em 04/11 ficam fora da
"sugestao": nesses, a sugestão é a própria validação do autor.

ORDEM
-----
Sem a planilha do autor preenchida, o script não mostra nada: ver antes como
as outras duas classificaram influenciaria a decisão dele. Quem quiser só as
outras (para testar o script) usa --sem-autor, que não grava arquivo.

USO
---
    python3 scripts/segundo_avaliador.py comparar
    python3 scripts/segundo_avaliador.py comparar --sem-autor
    python3 scripts/segundo_avaliador.py autoteste

Grava dados/segundo_avaliador/divergencias_artigos.csv e
divergencias_apps.csv, com os casos em que alguém discorda.
"""

import argparse
import sys
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from revisao_triagem import (binaria, decisao, gravar_planilha,  # noqa: E402
                             kappa_cohen, ler_planilha, mais_recente)

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "dados" / "segundo_avaliador"
CRITERIOS = {"IC1", "EC1", "EC2", "EC3", "EC4", "EC5", "EC6"}


# --------------------------------------------------------------------------
# Leitura de .xlsx só com a biblioteca padrão (o .venv não tem openpyxl)
# --------------------------------------------------------------------------

def _ns(tag: str) -> str:
    return tag[1:].split("}")[0] if tag.startswith("{") else ""


def _coluna(ref: str) -> int:
    n = 0
    for ch in ref:
        if not ch.isalpha():
            break
        n = n * 26 + ord(ch.upper()) - 64
    return n - 1


def ler_xlsx(caminho: Path, aba: str = None):
    """Linhas de uma aba como dicionários; a primeira linha é o cabeçalho."""
    with zipfile.ZipFile(caminho) as z:
        wbk = ET.fromstring(z.read("xl/workbook.xml"))
        m = _ns(wbk.tag)
        comp = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
            comp = ["".join(t.text or "" for t in si.iter(f"{{{m}}}t"))
                    for si in ss.findall(f"{{{m}}}si")]
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        alvo = {r.get("Id"): r.get("Target") for r in rels}
        abas = []
        for s in wbk.iter(f"{{{m}}}sheet"):
            rid = next(v for k, v in s.attrib.items() if k.endswith("}id"))
            abas.append((s.get("name"), alvo[rid]))
        escolhida = next((t for n, t in abas if n == aba), abas[0][1])
        escolhida = escolhida.lstrip("/")
        if not escolhida.startswith("xl/"):
            escolhida = "xl/" + escolhida
        folha = ET.fromstring(z.read(escolhida))
    linhas = []
    for row in folha.iter(f"{{{m}}}row"):
        vals, prox = {}, 0
        for c in row.findall(f"{{{m}}}c"):
            col = _coluna(c.get("r")) if c.get("r") else prox
            prox = col + 1
            if c.get("t") == "inlineStr":
                v = "".join(t.text or "" for t in c.iter(f"{{{m}}}t"))
            else:
                ve = c.find(f"{{{m}}}v")
                v = ve.text if ve is not None and ve.text else ""
                if c.get("t") == "s" and v:
                    v = comp[int(v)]
            if v.strip():
                vals[col] = v.strip()
        if vals:
            linhas.append(vals)
    if not linhas:
        return []
    cab = {k: v for k, v in linhas[0].items()}
    return [{cab[k]: v for k, v in ln.items() if k in cab} for ln in linhas[1:]]


def ler_tabela(caminho: Path, aba: str = None):
    if caminho.suffix.lower() == ".xlsx":
        return ler_xlsx(caminho, aba)
    return ler_planilha(caminho)


# --------------------------------------------------------------------------
# Normalização
# --------------------------------------------------------------------------

def sem_acento(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def coluna(linha: dict, *pedacos):
    """Valor da primeira coluna cujo nome (sem acento) contém um dos pedaços."""
    for k, v in linha.items():
        if any(p in sem_acento(k) for p in pedacos):
            return (v or "").strip()
    return ""


def criterio(v: str) -> str:
    v = (v or "").strip().upper().replace(" ", "")
    return v if v in CRITERIOS else ""


def oficial(v: str) -> str:
    v = (v or "").strip().upper()[:1]
    return v if v in ("S", "N", "?") else ""


def esfera(v: str) -> str:
    v = sem_acento(v)
    for nome in ("federal", "estadual", "municipal"):
        if v.startswith(nome[:3]):
            return nome
    if v.startswith("dist"):
        return "estadual"
    return "-" if v == "-" else ""


def sensivel(v: str) -> str:
    v = sem_acento(v)
    if v in ("sim", "s"):
        return "sim"
    if v in ("nao", "n"):
        return "não"
    return "-" if v == "-" else ""


# --------------------------------------------------------------------------
# Avaliadores
# --------------------------------------------------------------------------

def arquivo_do_autor(base: str):
    achados = [p for p in (PASTA / f"{base}.xlsx", PASTA / f"{base}.csv")
               if p.exists()]
    return max(achados, key=lambda p: p.stat().st_mtime) if achados else None


def artigos_avaliadores(ids):
    av = {}
    p = arquivo_do_autor("cega_artigos150_claudio")
    if p:
        av["autor"] = {}
        for r in ler_tabela(p):
            i = coluna(r, "id")
            if i in ids:
                av["autor"][i] = {
                    "decisao": decisao(coluna(r, "decisao")),
                    "criterio": criterio(coluna(r, "criterio")),
                    "motivo": coluna(r, "motivo")}
    triagem = mais_recente(RAIZ / "dados" / "revisao", "triagem_*.csv")
    if triagem:
        av["sugestao"] = {r["id"]: {"decisao": decisao(r.get("sugestao_f1")),
                                    "criterio": criterio(r.get("sugestao_criterio")),
                                    "motivo": r.get("sugestao_motivo", "")}
                          for r in ler_planilha(triagem) if r["id"] in ids}
    for p in sorted(PASTA.glob("resposta_artigos_*.csv")):
        nome = p.stem[len("resposta_artigos_"):]
        av[nome] = {r["id"]: {"decisao": decisao(r.get("decisao")),
                              "criterio": criterio(r.get("criterio")),
                              "motivo": r.get("motivo", "")}
                    for r in ler_planilha(p) if r.get("id") in ids}
    return av


def apps_avaliadores(ids):
    av = {}
    p = arquivo_do_autor("cega_apps100_claudio")
    if p:
        av["autor"] = {}
        for r in ler_tabela(p):
            i = coluna(r, "appid")
            if i in ids:
                av["autor"][i] = {"oficial": oficial(coluna(r, "oficial")),
                                  "esfera": esfera(coluna(r, "esfera")),
                                  "sensivel": sensivel(coluna(r, "sensivel")),
                                  "motivo": coluna(r, "motivo")}
    planilha = RAIZ / "dados" / "classificacao_396_para_conferir.xlsx"
    if planilha.exists():
        av["sugestao"] = {}
        for r in ler_xlsx(planilha, "Apps"):
            i = r.get("appId", "")
            if i in ids and not r.get("Grupo", "").startswith("4"):
                av["sugestao"][i] = {
                    "oficial": oficial(r.get("Oficial sugerido")),
                    "esfera": esfera(r.get("Esfera sugerida")),
                    "sensivel": sensivel(r.get("Sensível sugerido")),
                    "motivo": r.get("Motivo / o que conferir", "")}
    for p in sorted(PASTA.glob("resposta_apps_*.csv")):
        nome = p.stem[len("resposta_apps_"):]
        av[nome] = {r["appId"]: {"oficial": oficial(r.get("oficial")),
                                 "esfera": esfera(r.get("esfera")),
                                 "sensivel": sensivel(r.get("sensivel")),
                                 "motivo": r.get("motivo", "")}
                    for r in ler_planilha(p) if r.get("appId") in ids}
    return av


# --------------------------------------------------------------------------
# Concordância
# --------------------------------------------------------------------------

def kappa_fleiss(itens):
    """itens: lista de listas de rótulos, todas com o mesmo número de
    avaliadores."""
    if not itens:
        return float("nan")
    n = len(itens[0])
    tot = Counter()
    p_i = []
    for rot in itens:
        c = Counter(rot)
        tot.update(c)
        p_i.append((sum(v * v for v in c.values()) - n) / (n * (n - 1)))
    pbar = sum(p_i) / len(itens)
    pe = sum((v / (len(itens) * n)) ** 2 for v in tot.values())
    return (pbar - pe) / (1 - pe) if pe < 1 else float("nan")


ARTIGOS = [
    ("decisão (I, T, E ou R)", lambda r: r["decisao"], None),
    ("segue para a F2 (I ou T contra E ou R)",
     lambda r: binaria(r["decisao"]) if r["decisao"] else "", None),
    ("critério, quando os dois excluem", lambda r: r["criterio"],
     lambda r: r["decisao"] == "E"),
]
APPS = [
    ("oficial (S, N ou ?)", lambda r: r["oficial"], None),
    ("esfera, quando os dois dizem S", lambda r: r["esfera"],
     lambda r: r["oficial"] == "S"),
    ("sensível, quando os dois dizem S", lambda r: r["sensivel"],
     lambda r: r["oficial"] == "S"),
]


def valor(av, nome, i, pega, filtro):
    r = av[nome].get(i)
    if not r or (filtro and not filtro(r)):
        return ""
    return pega(r)


def fmt(x, pct=False):
    if x != x:  # nan
        return "  —  "
    return (f"{100 * x:5.1f}%" if pct else f"{x:5.2f}").replace(".", ",")


def medir(av, ids, variaveis):
    nomes = list(av)
    res = []
    for rotulo, pega, filtro in variaveis:
        linhas = []
        for a, b in combinations(nomes, 2):
            pares = [(valor(av, a, i, pega, filtro), valor(av, b, i, pega, filtro))
                     for i in ids]
            pares = [p for p in pares if p[0] and p[1]]
            po = (sum(x == y for x, y in pares) / len(pares)) if pares else float("nan")
            linhas.append((f"{a} × {b}", len(pares), po, kappa_cohen(pares)))
        if len(nomes) > 2:
            itens = [[valor(av, n, i, pega, filtro) for n in nomes] for i in ids]
            itens = [x for x in itens if all(x)]
            po = (sum(len(set(x)) == 1 for x in itens) / len(itens)) if itens else float("nan")
            linhas.append((f"os {len(nomes)} (Fleiss)", len(itens), po,
                           kappa_fleiss(itens)))
        res.append((rotulo, linhas))
    return res


def imprimir(titulo, av, total, res):
    print(f"\n{titulo}")
    for nome, d in av.items():
        cheios = sum(1 for r in d.values() if any(v for k, v in r.items()
                                                  if k != "motivo"))
        print(f"  {nome:<12} {cheios} de {total} decididos")
    for rotulo, linhas in res:
        print(f"\n  {rotulo}")
        print(f"    {'':<28}{'n':>5}  {'concorda':>8}  {'κ':>5}")
        for par, n, po, k in linhas:
            print(f"    {par:<28}{n:>5}  {fmt(po, True):>8}  {fmt(k):>5}")
    print("\n  Referência do protocolo: κ ≥ 0,6.")


def divergencias(av, ids, titulos, variaveis, campos_saida, chave):
    nomes = list(av)
    saida = []
    for i in ids:
        diverge = []
        for rotulo, pega, filtro in variaveis:
            vals = {valor(av, n, i, pega, filtro) for n in nomes} - {""}
            if len(vals) > 1:
                diverge.append(rotulo.split(",")[0].split(" (")[0])
        if not diverge:
            continue
        ln = {chave: i, "titulo": titulos.get(i, ""), "diverge_em": "; ".join(diverge)}
        for n in nomes:
            r = av[n].get(i, {})
            for c in campos_saida:
                ln[f"{c}_{n}"] = r.get(c, "")
        saida.append(ln)
    cab = [chave, "titulo", "diverge_em"] + [f"{c}_{n}" for c in campos_saida
                                            for n in nomes]
    return saida, cab


def comparar(sem_autor: bool):
    amostra_art = ler_planilha(PASTA / "artigos_cego_amostra150.csv")
    amostra_app = ler_planilha(PASTA / "apps_cego_amostra100.csv")
    ids_art = [r["id"] for r in amostra_art]
    ids_app = [r["appId"] for r in amostra_app]
    av_art = artigos_avaliadores(set(ids_art))
    av_app = apps_avaliadores(set(ids_app))

    def preenchidos(av, campo):
        return sum(1 for r in av.get("autor", {}).values() if r[campo])

    feitos_art = preenchidos(av_art, "decisao")
    feitos_app = preenchidos(av_app, "oficial")
    if sem_autor:
        av_art.pop("autor", None)
        av_app.pop("autor", None)
        print("Sem o autor (--sem-autor): só imprime, não grava divergências.")
    elif feitos_art == 0 and feitos_app == 0:
        sys.exit("As planilhas cegas do autor ainda estão em branco "
                 "(dados/segundo_avaliador/cega_*_claudio.xlsx).\n"
                 "Preencha antes de ver como os outros classificaram. "
                 "Para só testar o script: --sem-autor.")
    else:
        for nome, feitos, total in (("artigos", feitos_art, len(ids_art)),
                                    ("apps", feitos_app, len(ids_app))):
            if feitos < total:
                print(f"Atenção: o autor decidiu {feitos} de {total} {nome}; "
                      "a conta usa só esses.")

    for av, nome, ids, var in ((av_art, "ARTIGOS", ids_art, ARTIGOS),
                               (av_app, "APPS", ids_app, APPS)):
        if len(av) < 2:
            print(f"\n{nome}: menos de dois avaliadores, nada a comparar.")
            continue
        imprimir(f"{nome} ({len(ids)} da amostra)", av, len(ids),
                 medir(av, ids, var))
    if "sugestao" in av_app:
        fora = len(ids_app) - len(av_app["sugestao"])
        print(f"\n  ({fora} apps já validados pelo autor ficam fora da sugestão.)")

    if sem_autor:
        return
    tit_art = {r["id"]: r.get("titulo", "") for r in amostra_art}
    tit_app = {r["appId"]: r.get("titulo", "") for r in amostra_app}
    for av, ids, tit, var, campos, chave, arq in (
            (av_art, ids_art, tit_art, ARTIGOS, ["decisao", "criterio", "motivo"],
             "id", "divergencias_artigos.csv"),
            (av_app, ids_app, tit_app, APPS,
             ["oficial", "esfera", "sensivel", "motivo"], "appId",
             "divergencias_apps.csv")):
        linhas, cab = divergencias(av, ids, tit, var, campos, chave)
        gravar_planilha(PASTA / arq, linhas, cab)
        print(f"Gravado: dados/segundo_avaliador/{arq} ({len(linhas)} casos)")


# --------------------------------------------------------------------------
# Autoteste
# --------------------------------------------------------------------------

def _xlsx_teste(caminho: Path):
    m = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    with zipfile.ZipFile(caminho, "w") as z:
        z.writestr("xl/workbook.xml",
                   f'<workbook xmlns="{m}" xmlns:r="{r}"><sheets>'
                   '<sheet name="Outra" sheetId="1" r:id="rId1"/>'
                   '<sheet name="Apps" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<Relationships xmlns="http://schemas.openxmlformats.org/'
                   'package/2006/relationships">'
                   '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>'
                   '<Relationship Id="rId2" Target="/xl/worksheets/sheet2.xml"/>'
                   '</Relationships>')
        z.writestr("xl/sharedStrings.xml",
                   f'<sst xmlns="{m}"><si><t>appId</t></si><si><t>SEU '
                   'SENSÍVEL</t></si><si><r><t>br.gov</t></r><r><t>.x</t></r>'
                   '</si></sst>')
        z.writestr("xl/worksheets/sheet1.xml", f'<worksheet xmlns="{m}"/>')
        z.writestr("xl/worksheets/sheet2.xml",
                   f'<worksheet xmlns="{m}"><sheetData>'
                   '<row r="1"><c r="A1" t="s"><v>0</v></c>'
                   '<c r="C1" t="s"><v>1</v></c></row>'
                   '<row r="2"><c r="A2" t="s"><v>2</v></c>'
                   '<c r="C2" t="inlineStr"><is><t>Não</t></is></c></row>'
                   '<row r="3"/></sheetData></worksheet>')


def autoteste():
    erros = []

    def confere(cond, msg):
        if not cond:
            erros.append(msg)

    # Cohen: 20 sim-sim, 5 sim-não, 10 não-sim, 15 não-não → κ = 0,40
    pares = [("s", "s")] * 20 + [("s", "n")] * 5 + [("n", "s")] * 10 + [("n", "n")] * 15
    confere(abs(kappa_cohen(pares) - 0.40) < 1e-9, "kappa de Cohen")
    # Fleiss, 10 itens, 14 avaliadores, 5 categorias → κ = 0,210
    tabela = [[0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0],
              [2, 2, 8, 1, 1], [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2],
              [6, 5, 2, 1, 0], [0, 2, 2, 3, 7]]
    itens = [[str(j) for j, q in enumerate(ln) for _ in range(q)] for ln in tabela]
    confere(abs(kappa_fleiss(itens) - 0.2099) < 1e-3, "kappa de Fleiss")
    confere(kappa_fleiss([["a", "a", "a"]] * 3) != kappa_fleiss([["a", "a", "a"]] * 3),
            "Fleiss com uma só categoria deve dar nan")
    confere([oficial(x) for x in ("Sim", "s", "Não", "?", "", "x")]
            == ["S", "S", "N", "?", "", ""], "oficial")
    confere([esfera(x) for x in ("Federal", "ESTADUAL ", "municipal", "-", "Distrito Federal", "")]
            == ["federal", "estadual", "municipal", "-", "estadual", ""], "esfera")
    confere([sensivel(x) for x in ("Sim", "NAO", "não", "-", "talvez")]
            == ["sim", "não", "não", "-", ""], "sensivel")
    confere([criterio(x) for x in ("ec3", " IC1", "EC7", "")]
            == ["EC3", "IC1", "", ""], "criterio")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "t.xlsx"
        _xlsx_teste(p)
        ln = ler_xlsx(p, "Apps")
        confere(ln == [{"appId": "br.gov.x", "SEU SENSÍVEL": "Não"}],
                f"leitura de xlsx: {ln}")
        confere(sensivel(coluna(ln[0], "sensivel")) == "não", "coluna sem acento")
    av = {"a": {"1": {"oficial": "S", "esfera": "federal", "sensivel": "sim"},
                "2": {"oficial": "N", "esfera": "-", "sensivel": "-"}},
          "b": {"1": {"oficial": "S", "esfera": "estadual", "sensivel": "sim"},
                "2": {"oficial": "N", "esfera": "-", "sensivel": "-"}}}
    linhas, _ = divergencias(av, ["1", "2"], {}, APPS, ["oficial"], "appId")
    confere(len(linhas) == 1 and linhas[0]["diverge_em"] == "esfera",
            f"divergências: {linhas}")
    print("AUTOTESTE OK" if not erros else "AUTOTESTE COM FALHA: " + "; ".join(erros))
    return 0 if not erros else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="etapa", required=True)
    sub.add_parser("autoteste")
    s = sub.add_parser("comparar")
    s.add_argument("--sem-autor", action="store_true",
                   help="compara só os outros avaliadores, sem gravar arquivo")
    a = ap.parse_args()
    if a.etapa == "autoteste":
        sys.exit(autoteste())
    comparar(a.sem_autor)


if __name__ == "__main__":
    main()
