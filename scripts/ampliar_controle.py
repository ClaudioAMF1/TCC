#!/usr/bin/env python3
"""
Amplia o grupo de controle comercial dentro de cada categoria da loja.

POR QUE ESTE SCRIPT EXISTE
--------------------------
A H1 compara governo e comercial com categoria e faixa de instalações como
covariáveis. O teste de 17/09 deu 92,4% de suporte comum olhando só a faixa,
mas 27,4% exigindo a mesma categoria: em muitas categorias o controle não chega
às faixas em que os apps de governo estão. Este script procura comerciais
exatamente nas células (categoria × faixa) que faltam.

COMO PROCURA
------------
Para cada categoria com falta, busca na Google Play brasileira:

    - o nome da categoria, sozinho e com termos genéricos ("app", "grátis"...);
    - as palavras mais frequentes nos títulos dos apps de governo daquela
      categoria ("ônibus", "nota", "vacina"...). Elas trazem apps comerciais do
      mesmo assunto, que são o par mais justo para a comparação.

Percorre os resultados alternando o fim e o início da lista (no fim ficam os
pequenos), lê a ficha de cada candidato e aceita só se:

    - o publicador não é órgão público (o mesmo classificador do corpus);
    - a categoria é a mesma do app de governo;
    - a faixa de instalações é uma das que faltam naquela categoria.

Para quando a célula enche, as buscas acabam ou o teto de fichas por
categoria é atingido.

O QUE NÃO FAZ
-------------
Não procura controle abaixo de 10^2 instalações, a não ser com --faixa-minima.
App comercial com menos de cem instalações quase não aparece na busca, e os 30
apps de governo nessas faixas já ficam fora da H1 pelo suporte comum.

USO
---
    python3 scripts/ampliar_controle.py autoteste
    python3 scripts/ampliar_controle.py --diagnostico      # só mede, não busca
    python3 scripts/ampliar_controle.py                    # busca (~1 a 2 h)
    python3 scripts/ampliar_controle.py --por-celula 3 --max-fichas 120

SAÍDA (em dados/, que não é versionado)
-----
    dados/controle_ampliado_AAAAMMDD.json   controle antigo + novos, com a origem
    dados/cache_fichas_controle.json         fichas já lidas: rodar de novo retoma
O piloto (piloto_androzoo.py) passa a usar o controle ampliado quando ele existe.
"""

import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from piloto_androzoo import DADOS, HOJE, ler_planilha, mais_recente  # noqa: E402
from teste_viabilidade_n3_robusto import (ISCAS_CAUDA, faixa_instalacao,  # noqa: E402
                                          instalacoes_de, normalizar)

PAUSA = 1.0
PARADAS = {"de", "da", "do", "das", "dos", "e", "o", "a", "os", "as", "em", "no", "na",
           "para", "com", "por", "app", "aplicativo", "the", "and", "for", "of",
           "oficial", "mobile", "digital", "novo", "nova", "mais", "meu", "minha"}


def expoente(faixa):
    try:
        return int(str(faixa).split("^")[1])
    except (IndexError, ValueError):
        return None


# =================================================================== entradas

def carregar_gov():
    corpus = mais_recente("n3_corpus_*.csv")
    if not corpus:
        sys.exit("Não achei dados/n3_corpus_*.csv.")
    gov = []
    for r in ler_planilha(corpus):
        if (r.get("OFICIAL_S_N") or "").upper() == "N":
            continue
        gov.append({"appId": r["appId"], "titulo": r.get("titulo", ""),
                    "desenvolvedor": r.get("desenvolvedor", ""),
                    "categoria": r.get("categoria", ""), "faixa": r.get("faixa", "")})
    return gov, corpus


def carregar_controle():
    fonte = mais_recente("controle_ampliado_*.json") or mais_recente("n3_relatorio_*.json")
    if not fonte:
        sys.exit("Não achei o controle: dados/n3_relatorio_*.json.")
    return json.loads(fonte.read_text(encoding="utf-8")).get("controle", []), fonte


# ================================================================= diagnóstico

def celulas_em_falta(gov, controle, por_celula, faixa_minima):
    """{categoria: {faixa: quantos comerciais faltam}} nas células onde há app
    de governo. Faixas abaixo da mínima ficam de fora por desenho."""
    ctrl = Counter((c.get("genre"), c.get("faixa")) for c in controle)
    falta = defaultdict(dict)
    for cat, fx in sorted({(g["categoria"], g["faixa"]) for g in gov}):
        e = expoente(fx)
        if not cat or e is None or e < faixa_minima:
            continue
        n = por_celula - ctrl.get((cat, fx), 0)
        if n > 0:
            falta[cat][fx] = n
    return dict(falta)


def cobertura(gov, controle):
    """Duas medidas, as mesmas do teste robusto:
    - amplitude: o app de governo está entre a menor e a maior faixa do controle
      da MESMA categoria (é o 27,4% do teste de 17/09);
    - celula: existe comercial na mesma categoria e na mesma faixa."""
    por_cat = defaultdict(list)
    celulas = set()
    for c in controle:
        e = expoente(c.get("faixa"))
        if e is not None:
            por_cat[c.get("genre")].append(e)
            celulas.add((c.get("genre"), c.get("faixa")))
    base = amplitude = celula = 0
    for g in gov:
        e = expoente(g["faixa"])
        if e is None or not g["categoria"]:
            continue
        base += 1
        faixas = por_cat.get(g["categoria"])
        amplitude += bool(faixas) and min(faixas) <= e <= max(faixas)
        celula += (g["categoria"], g["faixa"]) in celulas
    return {"base": base, "amplitude": amplitude, "celula": celula}


def palavras_chave(gov, categoria, k=5):
    """Palavras mais frequentes nos títulos dos apps de governo da categoria,
    sem palavra vazia nem sinal de órgão público (que só traria mais governo)."""
    from teste_viabilidade_n3 import SINAIS_DEV
    sinais = {normalizar(s) for s in SINAIS_DEV}
    cont = Counter()
    for g in gov:
        if g["categoria"] != categoria:
            continue
        for t in set(re.split(r"[^a-z0-9]+", normalizar(g["titulo"]))):
            if len(t) >= 4 and t not in PARADAS and t not in sinais and not t.isdigit():
                cont[t] += 1
    return [t for t, _ in sorted(cont.items(), key=lambda x: (-x[1], x[0]))[:k]]


# ===================================================================== busca

def ampliar(gov, controle, falta, search, get_app, parece_oficial, args, cache,
            dormir=time.sleep, salvar_cache=lambda: None):
    ids_gov = {g["appId"] for g in gov}
    devs_gov = {normalizar(g["desenvolvedor"]) for g in gov if g["desenvolvedor"]}
    ja_tem = {c["appId"] for c in controle}
    vistos, novos = set(), []
    restante = {cat: dict(fx) for cat, fx in falta.items()}

    for cat in sorted(restante, key=lambda c: -sum(restante[c].values())):
        precisa = restante[cat]
        palavras = palavras_chave(gov, cat)
        consultas = ([cat] + [f"{cat} {isca}" for isca in ISCAS_CAUDA[:6]]
                     + palavras + [f"{p} app" for p in palavras[:3]])
        lidas = 0
        print(f"  {cat[:30]:<30} falta {sum(precisa.values()):>2} em "
              f"{', '.join(sorted(precisa))}")
        for q in consultas:
            if not precisa or lidas >= args.max_fichas:
                break
            try:
                res = search(q, lang="pt", country="br", n_hits=30)
            except Exception:  # noqa: BLE001 — busca que falha não para a categoria
                dormir(args.pausa)
                continue
            dormir(args.pausa)
            ordem = []
            for a, b in zip(res, reversed(res)):   # cauda primeiro: os pequenos
                ordem.extend([b, a])
            for r in ordem[:len(res)]:
                aid, dev = r.get("appId"), r.get("developer") or ""
                if (not aid or aid in vistos or aid in ids_gov or aid in ja_tem
                        or parece_oficial(dev) or normalizar(dev) in devs_gov):
                    continue
                vistos.add(aid)
                if aid not in cache:
                    try:
                        f = get_app(aid, lang="pt", country="br")
                    except Exception:  # noqa: BLE001
                        dormir(args.pausa)
                        continue
                    dormir(args.pausa)
                    cache[aid] = {k: f.get(k) for k in (
                        "title", "developer", "genre", "minInstalls", "realInstalls",
                        "installs", "containsAds", "privacyPolicy")}
                    if len(cache) % 20 == 0:
                        salvar_cache()
                lidas += 1
                f = cache[aid]
                fx = faixa_instalacao(instalacoes_de(f))
                if (f.get("genre") != cat or fx not in precisa
                        or parece_oficial(f.get("developer") or "")):
                    if lidas >= args.max_fichas:
                        break
                    continue
                novos.append({"appId": aid, **f, "n_instalacoes": instalacoes_de(f),
                              "faixa": fx, "origem": "ampliacao_categoria", "consulta": q})
                ja_tem.add(aid)
                precisa[fx] -= 1
                if precisa[fx] <= 0:
                    del precisa[fx]
                if not precisa or lidas >= args.max_fichas:
                    break
        achados = sum(1 for n in novos if n["genre"] == cat)
        print(f"      +{achados} comerciais; {lidas} fichas lidas"
              + (f"; ainda faltam {sum(precisa.values())}" if precisa else ""))
    restante = {c: fx for c, fx in restante.items() if fx}
    return novos, restante


def porcento(k, n):
    return f"{k / n:.1%}" if n else "-"


def main():
    ap = argparse.ArgumentParser(description="Amplia o controle comercial por categoria.")
    ap.add_argument("--por-celula", type=int, default=2,
                    help="comerciais por célula categoria × faixa (padrão 2)")
    ap.add_argument("--faixa-minima", type=int, default=2,
                    help="menor expoente de faixa procurado (padrão 2, isto é, 10^2)")
    ap.add_argument("--max-fichas", type=int, default=80,
                    help="teto de fichas lidas por categoria")
    ap.add_argument("--pausa", type=float, default=PAUSA)
    ap.add_argument("--diagnostico", action="store_true", help="só mede a falta, não busca")
    ap.add_argument("--autoteste", action="store_true", help="valida a lógica sem rede")
    args = ap.parse_args()
    if args.autoteste:
        autoteste()
        return

    gov, corpus = carregar_gov()
    controle, fonte = carregar_controle()
    antes = cobertura(gov, controle)
    falta = celulas_em_falta(gov, controle, args.por_celula, args.faixa_minima)
    print("\n  AMPLIAÇÃO DO CONTROLE POR CATEGORIA")
    print("  " + "=" * 62)
    print(f"  Governo: {len(gov)} ({corpus})   Controle: {len(controle)} ({fonte})")
    print(f"  Cobertura na mesma categoria, pela amplitude de faixas: "
          f"{antes['amplitude']}/{antes['base']} ({porcento(antes['amplitude'], antes['base'])})")
    print(f"  Cobertura na mesma categoria e na mesma faixa: "
          f"{antes['celula']}/{antes['base']} ({porcento(antes['celula'], antes['base'])})")
    print(f"  Faltam {sum(sum(v.values()) for v in falta.values())} comerciais em "
          f"{sum(len(v) for v in falta.values())} células de {len(falta)} categorias\n")
    if args.diagnostico:
        for cat, fx in sorted(falta.items(), key=lambda x: -sum(x[1].values())):
            print(f"    {sum(fx.values()):>3}  {cat}: " +
                  ", ".join(f"{f} ({n})" for f, n in sorted(fx.items())))
        return

    try:
        from google_play_scraper import app as get_app, search
    except ImportError:
        sys.exit("Falta o google-play-scraper: python3 -m pip install -r requirements.txt")
    from teste_viabilidade_n3 import parece_oficial

    arq_cache = DADOS / "cache_fichas_controle.json"
    cache = json.loads(arq_cache.read_text(encoding="utf-8")) if arq_cache.exists() else {}

    def salvar_cache():
        arq_cache.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    try:
        novos, restante = ampliar(gov, controle, falta, search, get_app, parece_oficial,
                                  args, cache, salvar_cache=salvar_cache)
    finally:
        salvar_cache()

    final = controle + novos
    depois = cobertura(gov, final)
    saida = DADOS / f"controle_ampliado_{HOJE}.json"
    saida.write_text(json.dumps({
        "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "parametros": {"por_celula": args.por_celula, "faixa_minima": args.faixa_minima,
                       "max_fichas": args.max_fichas, "fonte_controle": str(fonte)},
        "cobertura_antes": antes, "cobertura_depois": depois,
        "falta_depois": restante, "novos": novos, "controle": final,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n  RESULTADO")
    print("  " + "=" * 62)
    print(f"  Comerciais novos: {len(novos)}   controle total: {len(final)}")
    print(f"  Cobertura pela amplitude: {porcento(antes['amplitude'], antes['base'])} → "
          f"{porcento(depois['amplitude'], depois['base'])}")
    print(f"  Cobertura na mesma célula: {porcento(antes['celula'], antes['base'])} → "
          f"{porcento(depois['celula'], depois['base'])}")
    if restante:
        print(f"  Ainda faltam {sum(sum(v.values()) for v in restante.values())} "
              "comerciais; as maiores faltas:")
        for cat, fx in sorted(restante.items(), key=lambda x: -sum(x[1].values()))[:8]:
            print(f"    {sum(fx.values()):>3}  {cat}: {', '.join(sorted(fx))}")
    print(f"\n  Controle ampliado: {saida}")
    print("  O piloto passa a usá-lo; rode de novo a cobertura do AndroZoo para ver\n"
          "  quantos dos novos estão no acervo.\n")


# ================================================================= autoteste

def autoteste():
    falhas = []
    from teste_viabilidade_n3 import parece_oficial
    from teste_viabilidade_n3_robusto import suporte_comum

    gov = [
        {"appId": "g1", "titulo": "Ônibus Curitiba Horários", "desenvolvedor": "Prefeitura de Curitiba",
         "categoria": "Mapas e navegação", "faixa": "10^3"},
        {"appId": "g2", "titulo": "Horários de Ônibus SP", "desenvolvedor": "SPTrans",
         "categoria": "Mapas e navegação", "faixa": "10^5"},
        {"appId": "g3", "titulo": "Nota Fiscal Cidadã", "desenvolvedor": "Secretaria da Fazenda",
         "categoria": "Finanças", "faixa": "10^4"},
        {"appId": "g4", "titulo": "Ônibus Interior", "desenvolvedor": "Prefeitura de X",
         "categoria": "Mapas e navegação", "faixa": "10^1"},
    ]
    controle = [{"appId": "c1", "genre": "Mapas e navegação", "faixa": "10^5"}]

    # 1. falta por célula, sem a faixa abaixo da mínima
    falta = celulas_em_falta(gov, controle, 2, 2)
    if falta != {"Mapas e navegação": {"10^3": 2, "10^5": 1}, "Finanças": {"10^4": 2}}:
        falhas.append(f"células em falta = {falta}")

    # 2. cobertura pela amplitude bate com o suporte_comum do teste robusto
    cob = cobertura(gov, controle)
    vivos = [{"genre": g["categoria"], "faixa": g["faixa"]} for g in gov]
    sc = suporte_comum(vivos, {c["appId"]: c for c in controle})
    if cob["amplitude"] != sc["dentro"] or (cob["base"], cob["celula"]) != (4, 1):
        falhas.append(f"cobertura = {cob}, suporte_comum dentro = {sc['dentro']}")

    # 3. palavras: tiram vazias e sinais de órgão público, ficam os assuntos
    pal = palavras_chave(gov, "Mapas e navegação")
    if pal[:2] != ["onibus", "horarios"] or "prefeitura" in pal:
        falhas.append(f"palavras-chave = {pal}")

    # 4. busca simulada: barra órgão público, categoria e faixa erradas; aceita
    # o resto até encher a célula; não relê ficha já lida
    fichas = {
        "pub.gov": {"title": "X", "developer": "Governo do Estado", "genre": "Mapas e navegação",
                    "minInstalls": 1000},
        "outra.cat": {"title": "Y", "developer": "Loja Y", "genre": "Viagens",
                      "minInstalls": 1000},
        "faixa.ok1": {"title": "Ônibus Já", "developer": "Mobi SA", "genre": "Mapas e navegação",
                      "minInstalls": 5000, "containsAds": True},
        "faixa.ok2": {"title": "Busão", "developer": "Busao Ltda", "genre": "Mapas e navegação",
                      "minInstalls": 1000},
        "faixa.ok3": {"title": "Linha", "developer": "Linha Ltda", "genre": "Mapas e navegação",
                      "minInstalls": 2000},
        "grande": {"title": "Maps", "developer": "Big Co", "genre": "Mapas e navegação",
                   "minInstalls": 500_000_000},
        "nota.ok": {"title": "Notas", "developer": "Fin Ltda", "genre": "Finanças",
                    "minInstalls": 10_000},
    }
    lidas = Counter()

    def search_falso(q, **kw):
        if q.startswith("Finanças") or "nota" in q:
            return [{"appId": "nota.ok", "developer": "Fin Ltda"}]
        return [{"appId": a, "developer": fichas[a]["developer"]} for a in
                ("pub.gov", "outra.cat", "faixa.ok1", "faixa.ok2", "faixa.ok3", "grande")]

    def get_app_falso(aid, **kw):
        lidas[aid] += 1
        return fichas[aid]

    args = argparse.Namespace(max_fichas=50, pausa=0)
    novos, restante = ampliar(gov, controle, falta, search_falso, get_app_falso,
                              parece_oficial, args, {}, dormir=lambda s: None)
    ids = sorted(n["appId"] for n in novos)
    if "pub.gov" in ids or "outra.cat" in ids or "grande" in ids:
        falhas.append(f"aceitou o que devia barrar: {ids}")
    if len([n for n in novos if n["genre"] == "Mapas e navegação"]) != 2:
        falhas.append(f"célula 10^3 de Mapas devia receber 2: {ids}")
    if "nota.ok" not in ids:
        falhas.append("Finanças 10^4 devia receber nota.ok")
    if lidas["pub.gov"]:
        falhas.append("leu a ficha de publicador oficial (devia barrar pela busca)")
    if any(n > 1 for n in lidas.values()):
        falhas.append(f"releu fichas: {dict(lidas)}")
    if restante != {"Mapas e navegação": {"10^5": 1}, "Finanças": {"10^4": 1}}:
        falhas.append(f"falta depois = {restante}")
    depois = cobertura(gov, controle + novos)
    if not (depois["celula"] > cob["celula"] and depois["amplitude"] >= cob["amplitude"]):
        falhas.append(f"cobertura não subiu: {cob} → {depois}")

    if falhas:
        print("AUTOTESTE FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print("AUTOTESTE OK — 4 grupos de verificação passaram, sem rede.")


if __name__ == "__main__":
    main()
