"""Afunilamento da revisão sistemática, versão 2.1 do protocolo (26/11/2026).

Parte da versão 2.0 (termo do tema no título, scripts/revisao_afunilamento_titulo.py)
e acrescenta duas restrições, pedidas para concentrar a revisão no problema do TCC:

1. Período de 2018 a 2026, a partir da aplicação do GDPR (maio de 2018) e da
   sanção da LGPD (agosto de 2018), que definem o dever de informar o titular.
2. Sem a QR1 (métodos de detecção de bibliotecas): as buscas S1 deixam de ser
   executadas, e os estudos que tratam só de detecção de bibliotecas, sem medir
   rastreamento nem confrontar declarações, passam a ser excluídos pelo EC8. A
   detecção continua no referencial como fundo (Seção 2.3), com Zhan et al. (2022).

Como as restrições só estreitam a busca original, aplicá-las às exportações de
6/11/2026 dá o mesmo resultado que refazer as buscas com elas.

Como a amostra cega de 125 registros foi sorteada antes das restrições, só parte dela
continua no conjunto triado. O complemento é sorteado entre os demais registros
triados, com semente fixa, até a amostra chegar a 10% dos triados (no mínimo 30),
como pede a Seção 7.2 do protocolo.

Uso:  python scripts/revisao_afunilamento_v21.py
Saída: dados/revisao/afunilamento_v21_20261126.csv (registros mantidos),
       dados/revisao/afunilamento_v21_20261126_removidos.csv (registros da versão
       2.0 que saem na 2.1, com o motivo),
       dados/revisao/reteste_F1_complemento_20261126.csv (complemento da amostra
       cega; se o arquivo já existir, o script só confere se o sorteio é o mesmo,
       para não apagar decisões já registradas) e as contagens do fluxograma PRISMA.
"""
import collections
import csv
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import revisao_triagem as rt  # noqa: E402
from revisao_afunilamento_titulo import mantido as titulo_ok  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent / "dados" / "revisao"
ANO_MIN = 2018
SEMENTE_COMPLEMENTO = 20261126
COMPLEMENTO = "reteste_F1_complemento_20261126.csv"
# Estudos que a síntese da versão 2.0 classificava na QR1 (só detecção de bibliotecas)
# e que foram recuperados também por outra busca: saem na leitura completa pelo EC8.
SO_DETECCAO = {
    "R0399": "Su et al. (2018): distingue bibliotecas de anúncio pelo comportamento de rede",
    "R0414": "Liu et al. (2025): arcabouço para detectar rastreamento de sites em aplicativos",
}
CONTROLES = {
    "C01": "third party tracking in the mobile ecosystem", "C02": "apps, trackers, privacy, and regulators",
    "C03": "before and after gdpr", "C04": "a fait accompli", "C05": "freely given consent",
    "C06": "are we there yet", "C07": "maps: scaling privacy compliance", "C08": "toward a framework for detecting privacy policy",
    "C09": "et tu, brute", "C10": "can enable privacy leaks", "C11": "a study of trackers and data leaks",
}
FORA_DO_ESCOPO_21 = {"C06": "QR1 retirada", "C08": "anterior a 2018"}


def ano(v) -> int:
    try:
        return int(str(v or "0")[:4])
    except ValueError:
        return 0


def buscas(r) -> list:
    return [s.split(":", 1)[1] for s in (r.get("strings") or "").split("|") if ":" in s]


def so_s1(r) -> bool:
    b = buscas(r)
    return bool(b) and all(s == "S1" for s in b)


def ler(nome):
    return list(csv.DictReader(open(RAIZ / nome, encoding="utf-8-sig"), delimiter=";"))


def main():
    bruto = collections.Counter()
    for f in sorted((RAIZ / "buscas").glob("*.csv")):
        base, string, _ = rt.origem_de(f)
        if string == "S1":
            continue
        bruto[base] += sum(1 for r in rt.ler_exportacao(f) if titulo_ok(r.get("titulo")) and ano(r.get("ano")) >= ANO_MIN)

    linhas = ler("triagem_20261106.csv")
    v20 = [r for r in linhas if titulo_ok(r["titulo"])]
    sel = [r for r in v20 if ano(r["ano"]) >= ANO_MIN and not so_s1(r)]
    ids = {r["id"] for r in sel}
    f2 = {x["id"]: x for x in ler("leitura_F2_registro_20261113.csv")}
    val = {v["id"]: v for v in ler("leitura_F2_registro_20261121_validacao_parcial.csv")}

    # decisão F2 na versão 2.1
    def dec21(i):
        x = f2.get(i)
        if not x:
            return "", ""
        d, c = (x["decisao"] or "").strip(), (x["criterio"] or "").strip()
        if i in SO_DETECCAO and d == "I":
            return "E", "EC8"
        return d, c

    with open(RAIZ / "afunilamento_v21_20261126.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "titulo", "ano", "buscas", "decisao_f1", "decisao_f2", "criterio_f2", "observacao"])
        for r in sel:
            d, c = dec21(r["id"])
            w.writerow([r["id"], r["titulo"], r["ano"], "|".join(buscas(r)), rt.decisao(r.get("decisao_f1")), d, c,
                        SO_DETECCAO.get(r["id"], "")])
    with open(RAIZ / "afunilamento_v21_20261126_removidos.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "titulo", "ano", "buscas", "decisao_f1", "decisao_f2_v20", "motivo"])
        for r in v20:
            if r["id"] in ids:
                continue
            motivo = (f"publicado antes de {ANO_MIN} (protocolo v2.1)" if ano(r["ano"]) < ANO_MIN
                      else "recuperado só pela busca S1, da QR1, retirada no protocolo v2.1")
            w.writerow([r["id"], r["titulo"], r["ano"], "|".join(buscas(r)), rt.decisao(r.get("decisao_f1")),
                        (f2.get(r["id"]) or {}).get("decisao", ""), motivo])

    # complemento da amostra cega: 10% dos triados, arredondado para cima, no mínimo 30
    reteste = {r["id"] for r in ler("reteste_F1_20261116.csv")}
    ja = sorted(ids & reteste)
    alvo = max(30, -(-len(sel) // 10))
    extra = sorted(random.Random(SEMENTE_COMPLEMENTO).sample(sorted(ids - reteste), max(0, alvo - len(ja))))
    destino = RAIZ / COMPLEMENTO
    if destino.exists():
        gravados = [r["id"] for r in ler(COMPLEMENTO)]
        assert gravados == extra, f"o sorteio não confere com {COMPLEMENTO}: {gravados} != {extra}"
    else:
        por_id = {r["id"]: r for r in linhas}
        with open(destino, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, delimiter=";")
            w.writerow(["id", "titulo", "ano", "veiculo", "tipo", "resumo", "palavras_chave", "decisao", "criterio",
                        "observacao"])
            for i in extra:
                r = por_id[i]
                w.writerow([i, r["titulo"], r["ano"], r["veiculo"], r["tipo"], r["resumo"], r["palavras_chave"],
                            "", "", ""])

    total = sum(bruto.values())
    f1 = collections.Counter(rt.decisao(r.get("decisao_f1")) for r in sel)
    exc1 = collections.Counter((r.get("criterio_f1") or "sem código") for r in sel if rt.decisao(r.get("decisao_f1")) == "E")
    enc = [r["id"] for r in sel if rt.decisao(r.get("decisao_f1")) in ("I", "T")]
    st = collections.Counter(f2[i]["status"] for i in enc if i in f2)
    decs = {i: dec21(i) for i in enc}
    inc = [i for i in enc if decs[i][0] == "I"]
    exc = [i for i in enc if decs[i][0] == "E"]
    sem_texto_proprio = [i for i in exc if (f2[i].get("texto_correspondente") or "").strip().lower() == "não"]
    em_aberto = [i for i in enc if not decs[i][0]]
    ab = collections.Counter(f2[i]["status"] for i in em_aberto)
    duvida = [i for i in em_aberto if f2[i]["status"] == "escopo_pendente"]
    lidos = len(inc) + len(exc) - len(sem_texto_proprio) + len(duvida)
    conf = [i for i in inc + exc if (val.get(i, {}).get("validacao_pessoal") or "").startswith("conferido")]
    conf_d = collections.Counter(decs[i][0] for i in conf)
    tit = " || ".join((r["titulo"] or "").lower() for r in sel)
    ctl = sorted(c for c, t in CONTROLES.items() if t in tit)

    print(f"Identificados por base: {dict(bruto)} | total {total}")
    print(f"Duplicatas: {total - len(sel)} | únicos triados: {len(sel)}")
    print(f"F1: {dict(f1)} | exclusões por critério: {dict(exc1.most_common())}")
    print(f"Encaminhados à leitura completa: {len(enc)} (I {f1['I']}, T {f1['T']}) | revisões para a bola de neve: {f1['R']}")
    print(f"Situação F2 dos encaminhados: {dict(st)}")
    print(f"Propostas I: {len(inc)} | E: {len(exc)} {dict(collections.Counter(decs[i][1] for i in exc))} "
          f"(sem texto próprio: {len(sem_texto_proprio)}) | em aberto: {len(em_aberto)} {dict(ab)}")
    print(f"Textos lidos (inclui a dúvida de escopo): {lidos}")
    print(f"Decisões conferidas pelo autor: {len(conf)} {dict(conf_d)}")
    print(f"Amostra cega (125 sorteados antes do título) dentro da v2.1: {len(ja)} de {len(sel)} "
          f"({100 * len(ja) / len(sel):.1f}%) | complemento (semente {SEMENTE_COMPLEMENTO}): {len(extra)} "
          f"| total: {len(ja) + len(extra)} ({100 * (len(ja) + len(extra)) / len(sel):.1f}%)")
    print(f"Controles recuperados: {ctl} ({len(ctl)}) | fora do escopo da v2.1: {FORA_DO_ESCOPO_21}")
    print(f"Retirados da v2.0: {len(v20) - len(sel)}; propostas de inclusão que saem: "
          f"{sum(1 for r in v20 if r['id'] not in ids and (f2.get(r['id']) or {}).get('decisao') == 'I') + len([i for i in SO_DETECCAO if i in ids])}")


if __name__ == "__main__":
    main()
