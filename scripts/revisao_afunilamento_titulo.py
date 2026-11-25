"""Afunilamento da revisão sistemática pelo título (versão 2.0 do protocolo, 25/11/2026).

Depois da simulação de defesa, as 17 buscas de 6/11/2026 foram restringidas: além da
string original, o TÍTULO do registro precisa conter um termo do fenômeno ou do
contexto de governo. Como a restrição só estreita a busca original, aplicá-la sobre
as exportações de 6/11 dá o mesmo resultado que refazer as buscas com a restrição de
título (TITLE no Scopus, Document Title no IEEE Xplore, título na BDTD e na SOL).

Uso:  python scripts/revisao_afunilamento_titulo.py
Saída: dados/revisao/afunilamento_titulo_20261125.csv (ids mantidos) e as contagens
       do fluxograma PRISMA na tela.
"""
import collections
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import revisao_triagem as rt  # noqa: E402

FENOMENO = re.compile(r"(tracker|tracking|third[- ]party|sdk|librar|privacy polic|data safety|privacy label|"
                      r"privacy analysis|privacy compliance|rastrea|política de privacidade|data flow|leak)")
CONTEXTO = re.compile(r"\b(government|governmental|e-government|e-gov|public sector|public administration|"
                      r"public service|governo|governamental|setor público|covid|covid-19|contact[- ]tracing|"
                      r"pandemic|brazil|brasil|lgpd)\b")
RAIZ = Path(__file__).resolve().parent.parent / "dados" / "revisao"


def mantido(titulo: str) -> bool:
    t = (titulo or "").lower()
    return bool(FENOMENO.search(t) or CONTEXTO.search(t))


def main():
    bruto = collections.Counter()
    for f in sorted((RAIZ / "buscas").glob("*.csv")):
        base, _, _ = rt.origem_de(f)
        bruto[base] += sum(1 for r in rt.ler_exportacao(f) if mantido(r.get("titulo")))
    linhas = list(csv.DictReader(open(RAIZ / "triagem_20261106.csv", encoding="utf-8-sig"), delimiter=";"))
    sel = [r for r in linhas if mantido(r["titulo"])]
    ids = {r["id"] for r in sel}
    f1 = collections.Counter(rt.decisao(r.get("decisao_f1")) for r in sel)
    exc1 = collections.Counter((r.get("criterio_f1") or "sem código") for r in sel
                               if rt.decisao(r.get("decisao_f1")) == "E")
    f2 = [x for x in csv.DictReader(open(RAIZ / "leitura_F2_registro_20261113.csv", encoding="utf-8-sig"),
                                    delimiter=";") if x["id"] in ids]
    dec2 = collections.Counter((x["decisao"] or "").strip() for x in f2)
    val = [v for v in csv.DictReader(open(RAIZ / "leitura_F2_registro_20261121_validacao_parcial.csv",
                                          encoding="utf-8-sig"), delimiter=";")
           if v["id"] in ids and (v.get("validacao_pessoal") or "").startswith("conferido")]
    with open(RAIZ / "afunilamento_titulo_20261125.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "titulo", "decisao_f1", "decisao_f2"])
        d2 = {x["id"]: (x["decisao"] or "").strip() for x in f2}
        for r in sel:
            w.writerow([r["id"], r["titulo"], rt.decisao(r.get("decisao_f1")), d2.get(r["id"], "")])
    total = sum(bruto.values())
    print("Identificados por base:", dict(bruto), "| total", total)
    print("Duplicatas removidas:", total - len(sel), "| registros únicos triados:", len(sel))
    print("Triagem por título e resumo:", dict(f1), "| exclusões por critério:", dict(exc1))
    print("Encaminhados à leitura completa:", f1["I"] + f1["T"], "| revisões para a bola de neve:", f1["R"])
    print("Textos com decisão registrada:", dec2["I"] + dec2["E"], "| propostas I:", dec2["I"], "| E:", dec2["E"],
          "| sem decisão:", dec2[""])
    print("Decisões conferidas pelo autor:", len(val),
          dict(collections.Counter((v["decisao"] or "").strip() for v in val)))


if __name__ == "__main__":
    main()
