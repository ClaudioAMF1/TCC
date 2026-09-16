#!/usr/bin/env python3
"""
Teste de viabilidade ROBUSTO do tema N3 — apps móveis governamentais brasileiros.

POR QUE ESTE SCRIPT EXISTE
--------------------------
O primeiro teste (`teste_viabilidade_n3.py`) respondeu "existem aplicativos
suficientes?" — 396 candidatos, 71 publicadores. É a pergunta mais fácil, e é
a única que ele responde.

Um corpus grande não garante estudo executável. Cada hipótese do desenho tem
uma PORTA própria, e uma porta fechada mata a hipótese mesmo com 400 apps:

    H1 (gov × comercial)   precisa de PAREAMENTO. Se os apps de governo vivem
                           em faixas de instalação e categorias onde não existe
                           comercial equivalente, a comparação não é pareável.
    H2 (SDK não declarado) precisa de DECLARAÇÃO. Sem política de privacidade
                           publicada e acessível, não há com o que confrontar
                           o detectado. H2 morre sem APK nenhum ser baixado.
    H3 (dado sensível)     precisa de CÉLULAS POVOADAS. Se só 8 apps tratam
                           dado do Art. 11, não há contraste a medir.
    H1/H3 (ambas)          precisam de POTÊNCIA. Com o n disponível, qual é a
                           menor diferença detectável? Se for maior que o
                           efeito que a literatura reporta, o estudo nasce
                           incapaz de encontrar o que procura.

Este script mede as quatro portas ANTES de baixar o primeiro APK, e mede um
quinto item: um sinal preliminar da variável dependente.

O SINAL PRELIMINAR
------------------
A Play Store declara `containsAds` por aplicativo. Anúncio embarcado implica,
quase sempre, SDK de anúncio — que é rastreador. Isso NÃO substitui a análise
estática: é um limite inferior grosseiro, e a relação "tem anúncio -> tem
rastreador" não vale ao contrário (analytics não mostra anúncio). Mas é uma
medida da variável dependente obtida de graça, que responde a pergunta que
antecede tudo: ESSA VARIÁVEL VARIA ENTRE OS GRUPOS? Se governo e comercial
tiverem a mesma taxa aqui, é indício a favor da H1 antes do esforço maior.

O QUE ESTE SCRIPT NÃO FAZ
-------------------------
Não baixa APK, não instala, não descompila, não acessa área autenticada.
Lê metadados públicos da loja e faz uma requisição GET à URL de política de
privacidade que o próprio publicador divulgou.

DEPENDÊNCIA
-----------
    python3 -m venv .venv && source .venv/bin/activate
    pip install google-play-scraper

USO
---
    python3 scripts/teste_viabilidade_n3_robusto.py              # completo
    python3 scripts/teste_viabilidade_n3_robusto.py --limite 40  # rodada curta
    python3 scripts/teste_viabilidade_n3_robusto.py --autoteste  # sem rede

SAÍDA
-----
    dados/n3_fichas_AAAAMMDD.json      ficha completa de cada app (cache)
    dados/n3_corpus_AAAAMMDD.csv       planilha JÁ PRÉ-CLASSIFICADA p/ revisão
    dados/n3_relatorio_AAAAMMDD.json   os números das cinco portas
"""

import argparse
import csv
import json
import math
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

PAUSA = 1.0
TIMEOUT_HTTP = 10
AGENTE = "Mozilla/5.0 (pesquisa academica; TCC IDP; metadados publicos)"


# ---------------------------------------------------------------- normalização

def normalizar(texto: str) -> str:
    """Minúsculas sem acento. Permite escrever os termos sem acento na fonte."""
    t = unicodedata.normalize("NFKD", (texto or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def tem_termo(texto_norm: str, termo_norm: str) -> bool:
    """Casamento com FRONTEIRA DE PALAVRA, nunca por substring.

    Casamento por substring já produziu três erros neste repositório:
    'pix' casou em 'capixaba', 'sus' em 'Direct Cursus' e 'serpro' em
    'SERPROS'. Aceita expressão de várias palavras ('reconhecimento facial').
    """
    return re.search(rf"\b{re.escape(termo_norm)}\b", texto_norm) is not None


def _norm_conj(termos):
    return {normalizar(t) for t in termos}


# ------------------------------------------------------- classificação: esfera

MUNICIPAL = _norm_conj({
    "prefeitura", "prefeituras", "municipal", "municipais", "municipio",
    "camara municipal", "guarda municipal", "procempa", "prodam sp", "cijun",
    "empro", "saude ja curitiba",
})
ESTADUAL = _norm_conj({
    "estado", "estadual", "estaduais", "governo do estado", "detran",
    "policia militar", "corpo de bombeiros", "tribunal de justica",
    "defensoria publica do estado", "celepar", "ciasc", "prodap",
    "assembleia legislativa", "policia civil",
})
FEDERAL = _norm_conj({
    "federal", "uniao", "ministerio", "inss", "receita federal", "serpro",
    "dataprev", "senado", "camara dos deputados", "governo federal",
    "justica eleitoral", "justica do trabalho", "tse", "stf", "stj", "tst",
    "policia federal", "anvisa", "ibama", "incra", "funai", "banco central",
    "caixa economica", "exercito", "marinha", "aeronautica",
})

# Publicadores cujo nome não carrega sinal de esfera nenhum.
ESFERA_CONHECIDA = {
    normalizar("serviços e informações do brasil"): "federal",
    normalizar("justiça eleitoral brasileira"): "federal",
    normalizar("justiça do trabalho"): "federal",
    normalizar("hospital das clínicas da fmusp"): "estadual",
    normalizar("instituto de identificação ricardo gumbleton daunt"): "estadual",
    normalizar("inova pmsc"): "estadual",
    normalizar("dgti sedec"): "estadual",
    normalizar("cbmsc - diti"): "estadual",
}


def classificar_esfera(dev: str) -> str:
    """Municipal -> estadual -> federal. A ordem importa.

    'Secretaria Municipal de Saúde' contém 'saúde' e 'secretaria', que são
    ambíguos; 'municipal' não é. Por isso o sinal menos ambíguo decide primeiro.
    """
    d = normalizar(dev)
    if not d:
        return "indeterminado"
    if d in ESFERA_CONHECIDA:
        return ESFERA_CONHECIDA[d]
    for conj, rotulo in ((MUNICIPAL, "municipal"), (ESTADUAL, "estadual"),
                         (FEDERAL, "federal")):
        if any(tem_termo(d, t) for t in conj):
            return rotulo
    return "indeterminado"


# ------------------------------------------- classificação: dado sensível (Art. 11)

SENSIVEL = {
    "saude": _norm_conj({
        "saude", "sus", "hospital", "paciente", "pacientes", "medico", "medica",
        "consulta", "consultas", "vacina", "vacinacao", "vacinal", "exame",
        "exames", "prontuario", "enfermagem", "farmacia", "samu", "upa",
        "telemedicina", "psicologico", "psicossocial", "agente de saude",
        "cartao nacional de saude", "e-saude", "esaude",
    }),
    "biometria": _norm_conj({
        "biometria", "biometrico", "biometrica", "reconhecimento facial",
        "prova de vida", "biovalid", "impressao digital", "iris", "datilos",
    }),
    "previdencia": _norm_conj({
        "inss", "previdencia", "previdenciario", "aposentadoria", "beneficio",
        "beneficios", "pensao", "bpc", "auxilio", "loas",
    }),
    "assistencia": _norm_conj({
        "cadastro unico", "cadunico", "bolsa familia", "assistencia social",
        "vulnerabilidade social",
    }),
}

# 'digital' sozinho NÃO entra: 'Carteira Digital de Trânsito' não é biometria.
# 'facial' sozinho também não: só a expressão 'reconhecimento facial'.


def classificar_sensibilidade(titulo: str, descricao: str):
    """Devolve (é_sensível, [categorias]). Heurística — exige revisão manual."""
    texto = normalizar(f"{titulo} {descricao}")
    achadas = [cat for cat, termos in SENSIVEL.items()
               if any(tem_termo(texto, t) for t in termos)]
    return bool(achadas), achadas


# ------------------------------------------------------------ faixa de instalação

def faixa_instalacao(n) -> str:
    """Faixa logarítmica. É o eixo de pareamento: comparar um app municipal de
    500 instalações com um portal comercial de 100 milhões não mede nada."""
    try:
        n = int(n or 0)
    except (TypeError, ValueError):
        return "?"
    if n <= 0:
        return "?"
    e = int(math.floor(math.log10(n)))
    e = max(0, min(e, 9))
    return f"10^{e}"


def instalacoes_de(ficha) -> int:
    for campo in ("minInstalls", "realInstalls"):
        v = ficha.get(campo)
        if isinstance(v, int) and v > 0:
            return v
    bruto = re.sub(r"[^\d]", "", str(ficha.get("installs") or ""))
    return int(bruto) if bruto else 0


# ---------------------------------------------------- porta da H2: política

def checar_politica(url: str):
    """A URL de política de privacidade existe e responde?

    Sem política publicada não há declaração com que confrontar o SDK
    detectado, e a H2 fica sem instrumento. Também registra o tipo do
    conteúdo: política em PDF custa muito mais para processar que em HTML.
    """
    if not url or not url.startswith(("http://", "https://")):
        return {"estado": "ausente", "http": None, "tipo": None}
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_HTTP) as r:
            tipo = (r.headers.get("Content-Type") or "").split(";")[0].strip()
            corpo = r.read(4096)
            if not corpo:
                return {"estado": "vazia", "http": r.status, "tipo": tipo}
            return {"estado": "ok", "http": r.status, "tipo": tipo}
    except urllib.error.HTTPError as e:
        return {"estado": f"http_{e.code}", "http": e.code, "tipo": None}
    except Exception as e:
        return {"estado": "falha", "http": None, "tipo": type(e).__name__}


# ------------------------------------------------------------------- potência

Z_ALFA = 1.959964   # bilateral, alfa = 0,05
Z_BETA = 0.8416212  # poder = 0,80


def menor_diferenca_detectavel(n1: int, n2: int, p_base: float) -> float:
    """Menor diferença de proporção detectável com poder de 80%.

    Busca numérica sobre delta usando a aproximação normal para duas
    proporções. Se este número for MAIOR que o efeito que a literatura
    reporta, o estudo nasce incapaz de detectar o que procura — e isso
    precisa estar escrito antes da coleta, não depois.
    """
    if n1 < 2 or n2 < 2:
        return float("nan")
    p_base = min(max(p_base, 0.01), 0.99)
    for passo in range(1, 991):
        d = passo / 1000
        p2 = p_base + d
        if p2 >= 1.0:
            p2 = p_base - d
            if p2 <= 0.0:
                return float("nan")
        var = p_base * (1 - p_base) / n1 + p2 * (1 - p2) / n2
        if var <= 0:
            continue
        if abs(d) / math.sqrt(var) >= (Z_ALFA + Z_BETA):
            return d
    return float("nan")


def ic_proporcao(k: int, n: int):
    """Intervalo de Wilson 95% — comporta-se bem com n pequeno e p extremo,
    ao contrário do intervalo de Wald, que produz limite negativo."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    z = Z_ALFA
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centro - meia), min(1.0, centro + meia))


# ------------------------------------------------------------------ coleta

def carregar_candidatos(caminho_json):
    """Reaproveita a saída do primeiro teste. Evita refazer a busca."""
    d = Path("dados")
    if caminho_json:
        alvo = Path(caminho_json)
    else:
        achados = sorted(d.glob("apps_gov_*.json"))
        if not achados:
            sys.exit(
                "Não encontrei dados/apps_gov_*.json.\n"
                "Rode antes:  python3 scripts/teste_viabilidade_n3.py --expandir"
            )
        alvo = achados[-1]
    print(f"  Corpus de entrada: {alvo}")
    return json.loads(alvo.read_text(encoding="utf-8")), alvo


def buscar_fichas(app_ids, get_app, cache_path, pausa):
    """get_app() por aplicativo, com cache em disco. É a etapa cara."""
    cache = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        print(f"  Cache: {len(cache)} fichas já coletadas.")

    faltam = [a for a in app_ids if a not in cache]
    print(f"  Buscando ficha completa de {len(faltam)} aplicativos...\n")
    for i, aid in enumerate(faltam, 1):
        try:
            f = get_app(aid, lang="pt", country="br")
            cache[aid] = {
                "appId": aid, "title": f.get("title"), "developer": f.get("developer"),
                "genre": f.get("genre"), "genreId": f.get("genreId"),
                "installs": f.get("installs"), "minInstalls": f.get("minInstalls"),
                "realInstalls": f.get("realInstalls"), "score": f.get("score"),
                "ratings": f.get("ratings"), "containsAds": f.get("containsAds"),
                "offersIAP": f.get("offersIAP"), "privacyPolicy": f.get("privacyPolicy"),
                "developerEmail": f.get("developerEmail"),
                "developerWebsite": f.get("developerWebsite"),
                "released": f.get("released"), "updated": f.get("updated"),
                "version": f.get("version"), "contentRating": f.get("contentRating"),
                "descricao": (f.get("description") or "")[:1200],
            }
        except Exception as e:
            cache[aid] = {"appId": aid, "erro": type(e).__name__}
        if i % 10 == 0 or i == len(faltam):
            print(f"    {i:>4}/{len(faltam)}")
            cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
        time.sleep(pausa)

    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
    return cache


def buscar_controle(search, get_app, celulas, por_celula, pausa, oficiais):
    """Para cada célula (categoria, faixa) ocupada pelo governo, procura
    aplicativos COMERCIAIS na mesma célula.

    É a porta da H1: sem comercial equivalente em categoria e porte, a
    comparação pareada não existe, e o desenho precisa mudar de eixo.
    """
    print(f"\n  Procurando controle comercial em {len(celulas)} células "
          f"(até {por_celula} por célula)...\n")
    controle, cobertas = {}, 0
    for i, (genero, faixa) in enumerate(sorted(celulas), 1):
        try:
            res = search(genero, lang="pt", country="br", n_hits=30)
        except Exception as e:
            print(f"  [{i:>2}/{len(celulas)}] {genero[:24]:<24} {faixa:<6} "
                  f"ERRO {type(e).__name__}")
            time.sleep(pausa)
            continue

        achou = 0
        for r in res:
            aid = r.get("appId")
            dev = (r.get("developer") or "")
            if not aid or aid in controle or normalizar(dev) in oficiais:
                continue
            try:
                f = get_app(aid, lang="pt", country="br")
            except Exception:
                time.sleep(pausa)
                continue
            time.sleep(pausa)
            if f.get("genre") != genero:
                continue
            if faixa_instalacao(instalacoes_de(f)) != faixa:
                continue
            controle[aid] = {
                "appId": aid, "title": f.get("title"), "developer": f.get("developer"),
                "genre": f.get("genre"), "minInstalls": f.get("minInstalls"),
                "realInstalls": f.get("realInstalls"), "installs": f.get("installs"),
                "containsAds": f.get("containsAds"),
                "privacyPolicy": f.get("privacyPolicy"),
                "celula": f"{genero}|{faixa}",
            }
            achou += 1
            if achou >= por_celula:
                break
        cobertas += 1 if achou else 0
        print(f"  [{i:>2}/{len(celulas)}] {genero[:24]:<24} {faixa:<6} +{achou}")
        time.sleep(pausa)
    return controle, cobertas


# -------------------------------------------------------------------- relatório

def linha(titulo):
    print("\n" + titulo)
    print("  " + "=" * 62)


def porcento(k, n):
    return f"{100*k/n:.1f}%" if n else "—"


def relatar(gov, controle, celulas, cobertas, politicas, args):
    rel = {"coleta": datetime.now(timezone.utc).isoformat()}

    # ---- PORTA 1: o corpus sobrevive à ficha completa?
    linha("  PORTA 1 — CORPUS EFETIVO")
    vivos = [f for f in gov if not f.get("erro")]
    mortos = len(gov) - len(vivos)
    print(f"    Candidatos processados ............ {len(gov)}")
    print(f"    Fichas obtidas .................... {len(vivos)}")
    print(f"    Removidos da loja / erro .......... {mortos}")
    rel["corpus"] = {"processados": len(gov), "vivos": len(vivos), "erros": mortos}

    # ---- PORTA 2: as células da estratificação estão povoadas?
    linha("  PORTA 2 — CÉLULAS DA ESTRATIFICAÇÃO (H3)")
    tab = defaultdict(int)
    for f in vivos:
        tab[(f["esfera"], "sensível" if f["sensivel"] else "não sensível")] += 1
    esferas = ["federal", "estadual", "municipal", "indeterminado"]
    print(f"    {'':<16}{'sensível':>12}{'não sensível':>16}")
    for e in esferas:
        print(f"    {e:<16}{tab[(e,'sensível')]:>12}{tab[(e,'não sensível')]:>16}")
    n_sens = sum(v for (e, s), v in tab.items() if s == "sensível")
    print(f"\n    Total sensível (Art. 11) .......... {n_sens} "
          f"({porcento(n_sens, len(vivos))})")
    cats = Counter(c for f in vivos for c in f["categorias"])
    for c, n in cats.most_common():
        print(f"        {c:<14} {n}")
    menor_celula = min([v for v in tab.values() if v] or [0])
    print(f"\n    Menor célula não vazia ............ {menor_celula}")
    rel["celulas"] = {f"{e}|{s}": v for (e, s), v in tab.items()}
    rel["sensiveis"] = n_sens
    rel["categorias_sensiveis"] = dict(cats)

    # ---- PORTA 3: existe controle comercial pareável?
    linha("  PORTA 3 — PAREAMENTO COM CONTROLE COMERCIAL (H1)")
    print(f"    Células (categoria × faixa) no governo ... {len(celulas)}")
    print(f"    Células com ao menos um comercial ....... {cobertas} "
          f"({porcento(cobertas, len(celulas))})")
    print(f"    Aplicativos de controle coletados ....... {len(controle)}")
    top = Counter(f["genre"] for f in vivos if f.get("genre")).most_common(8)
    print("\n    Categorias mais frequentes no governo:")
    for g, n in top:
        print(f"        {n:>4}  {g}")
    rel["pareamento"] = {"celulas": len(celulas), "cobertas": cobertas,
                         "controle": len(controle)}

    # ---- PORTA 4: existe declaração para confrontar?
    linha("  PORTA 4 — POLÍTICA DE PRIVACIDADE (H2)")
    est = Counter(p["estado"] for p in politicas.values())
    ok = est.get("ok", 0)
    print(f"    Com URL que responde 200 .......... {ok} "
          f"({porcento(ok, len(politicas))})")
    for e, n in est.most_common():
        if e != "ok":
            print(f"    {e:<33} {n}")
    tipos = Counter(p["tipo"] for p in politicas.values()
                    if p["estado"] == "ok" and p["tipo"])
    if tipos:
        print("\n    Formato do documento:")
        for t, n in tipos.most_common(5):
            print(f"        {n:>4}  {t}")
    rel["politica"] = {"estados": dict(est), "tipos": dict(tipos)}

    # ---- PORTA 5: a variável dependente varia entre os grupos?
    linha("  PORTA 5 — SINAL PRELIMINAR DA VARIÁVEL DEPENDENTE")
    g_ads = [f for f in vivos if f.get("containsAds") is not None]
    c_ads = [f for f in controle.values() if f.get("containsAds") is not None]
    kg = sum(1 for f in g_ads if f["containsAds"])
    kc = sum(1 for f in c_ads if f["containsAds"])
    lo_g, hi_g = ic_proporcao(kg, len(g_ads))
    lo_c, hi_c = ic_proporcao(kc, len(c_ads))
    print(f"    Governo com anúncio ..... {kg:>4}/{len(g_ads):<5} "
          f"{porcento(kg, len(g_ads)):>7}   IC95% [{lo_g:.3f}; {hi_g:.3f}]")
    print(f"    Controle com anúncio .... {kc:>4}/{len(c_ads):<5} "
          f"{porcento(kc, len(c_ads)):>7}   IC95% [{lo_c:.3f}; {hi_c:.3f}]")
    print("\n    Anúncio implica SDK de anúncio, que é rastreador. O contrário")
    print("    NÃO vale: analytics não mostra anúncio. Isto é limite inferior.")
    rel["anuncio"] = {"gov_k": kg, "gov_n": len(g_ads),
                      "ctrl_k": kc, "ctrl_n": len(c_ads)}

    # ---- PORTA 6: o n disponível enxerga o efeito procurado?
    linha("  PORTA 6 — POTÊNCIA ESTATÍSTICA")
    p_base = kg / len(g_ads) if g_ads else 0.5
    for n_ctrl in (len(c_ads), len(vivos)):
        if n_ctrl < 2:
            continue
        mde = menor_diferenca_detectavel(len(vivos), n_ctrl, p_base)
        print(f"    n_gov={len(vivos):<5} n_ctrl={n_ctrl:<5} -> menor diferença "
              f"detectável: {mde*100:.1f} pontos percentuais")
    print("\n    Poder 80%, alfa 0,05 bilateral, aproximação normal para duas")
    print("    proporções. Para a contagem de rastreadores (binomial negativa)")
    print("    a potência real é diferente; isto é a ordem de grandeza.")
    print("    A literatura de rastreamento em apps de saúde reporta diferenças")
    print("    entre grupos na casa de 15 a 30 pontos. Se o número acima for")
    print("    menor que isso, o desenho enxerga o efeito.")
    rel["potencia"] = {"p_base": p_base, "n_gov": len(vivos),
                       "mde_vs_controle": menor_diferenca_detectavel(
                           len(vivos), max(len(c_ads), 2), p_base)}

    # ---- veredito
    linha("  VEREDITO POR HIPÓTESE")
    def marca(ok_):
        return "✅" if ok_ else "❌"
    h1 = len(celulas) > 0 and cobertas / max(len(celulas), 1) >= 0.6
    h2 = len(politicas) > 0 and ok / max(len(politicas), 1) >= 0.6
    h3 = n_sens >= 30 and menor_celula >= 5
    h4 = len(vivos) >= 60
    print(f"    {marca(h1)} H1 comparativa      — {porcento(cobertas, len(celulas))} "
          f"das células têm controle comercial (precisa de ≥60%)")
    print(f"    {marca(h2)} H2 transparência    — {porcento(ok, len(politicas))} "
          f"das políticas acessíveis (precisa de ≥60%)")
    print(f"    {marca(h3)} H3 dado sensível    — {n_sens} apps sensíveis, menor "
          f"célula {menor_celula} (precisa de ≥30 e ≥5)")
    print(f"    {marca(h4)} H4 concordância     — {len(vivos)} apps para o "
          f"piloto de detectores (precisa de ≥60)")
    rel["veredito"] = {"H1": h1, "H2": h2, "H3": h3, "H4": h4}

    print("""
  COMO LER ISTO

    Todas as portas abertas  -> o desenho está executável como escrito. Leve
                                estes números ao orientador junto da proposta.
    H2 fechada               -> troque a fonte de declaração: use a seção
                                "Segurança dos dados" da própria Play Store,
                                que é estruturada, em vez da política em prosa.
    H3 fechada               -> abandone a estratificação por sensibilidade e
                                mantenha só o contraste gov × comercial.
    H1 fechada               -> o pareamento por categoria e porte não existe.
                                Troque para comparação INTERNA: entre esferas,
                                ou entre apps sensíveis e não sensíveis.
    Potência insuficiente    -> reduza o número de hipóteses e concentre o n.

  Nenhum destes desfechos mata o tema. Todos mudam o desenho — e é por isso
  que o teste vem antes de congelar o protocolo, não depois.
""")
    return rel


# -------------------------------------------------------------------- autoteste

def autoteste():
    """Verifica a classificação sem tocar na rede. Os casos abaixo são os
    erros reais que já apareceram neste repositório."""
    casos_esfera = [
        ("Prefeitura Municipal de Curitiba", "municipal"),
        ("Secretaria Municipal de Saúde de São Paulo", "municipal"),
        ("Governo do Estado de Minas Gerais", "estadual"),
        ("DETRAN-SP", "estadual"),
        ("Ministério da Saúde", "federal"),
        ("Serviços e Informações do Brasil", "federal"),
        ("Justiça Eleitoral Brasileira", "federal"),
        ("Direct Cursus Computer Systems Trading LLC", "indeterminado"),
        ("SERPROS Fundo Multipatrocinado", "indeterminado"),
        ("", "indeterminado"),
    ]
    casos_sens = [
        ("Meu SUS Digital", "acesso ao sus", True),
        ("Biovalid", "prova de vida por reconhecimento facial", True),
        ("Meu INSS", "benefícios e aposentadoria", True),
        ("Carteira Digital de Trânsito", "sua cnh no celular", False),
        ("Nota Fiscal Paulista", "consulte suas notas", False),
    ]
    casos_faixa = [(0, "?"), (900, "10^2"), (1000, "10^3"),
                   (50_000_000, "10^7"), (None, "?")]

    falhas = []
    for dev, esperado in casos_esfera:
        got = classificar_esfera(dev)
        if got != esperado:
            falhas.append(f"esfera({dev!r}) = {got!r}, esperado {esperado!r}")
    for tit, desc, esperado in casos_sens:
        got, _ = classificar_sensibilidade(tit, desc)
        if got != esperado:
            falhas.append(f"sensível({tit!r}) = {got}, esperado {esperado}")
    for n, esperado in casos_faixa:
        got = faixa_instalacao(n)
        if got != esperado:
            falhas.append(f"faixa({n!r}) = {got!r}, esperado {esperado!r}")

    lo, hi = ic_proporcao(0, 50)
    if not (lo == 0.0 and 0 < hi < 0.15):
        falhas.append(f"Wilson(0/50) = [{lo}, {hi}] fora do esperado")
    mde = menor_diferenca_detectavel(100, 100, 0.5)
    if not (0.10 < mde < 0.25):
        falhas.append(f"MDE(100,100,0.5) = {mde:.3f} fora da faixa plausível")

    if falhas:
        print("AUTOTESTE FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print(f"AUTOTESTE OK — {len(casos_esfera)+len(casos_sens)+len(casos_faixa)+2} "
          f"verificações passaram, sem tocar na rede.")


# ------------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(
        description="Teste robusto de viabilidade do N3: mede as portas de cada hipótese.")
    ap.add_argument("--entrada", help="JSON do primeiro teste (padrão: o mais recente)")
    ap.add_argument("--limite", type=int, help="processa só os N primeiros (rodada curta)")
    ap.add_argument("--pares-por-celula", type=int, default=3)
    ap.add_argument("--pausa", type=float, default=PAUSA)
    ap.add_argument("--sem-controle", action="store_true",
                    help="pula a coleta do grupo de controle (etapa mais cara)")
    ap.add_argument("--autoteste", action="store_true", help="valida a lógica, sem rede")
    args = ap.parse_args()

    if args.autoteste:
        autoteste()
        return

    try:
        from google_play_scraper import app as get_app, search
    except ImportError:
        sys.exit(
            "Falta a dependência 'google-play-scraper'.\n\n"
            "    python3 -m venv .venv\n"
            "    source .venv/bin/activate\n"
            "    pip install google-play-scraper\n"
        )

    d = Path("dados")
    d.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d")

    print("\n" + "=" * 64)
    print("TESTE ROBUSTO — N3: apps governamentais brasileiros")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print("=" * 64 + "\n")

    candidatos, _ = carregar_candidatos(args.entrada)

    # reaproveita o classificador de publicador do primeiro teste
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from teste_viabilidade_n3 import parece_oficial

    oficiais_ids = [a["appId"] for a in candidatos if parece_oficial(a.get("dev", ""))]
    nomes_oficiais = {normalizar(a["dev"]) for a in candidatos
                      if parece_oficial(a.get("dev", ""))}
    if args.limite:
        oficiais_ids = oficiais_ids[:args.limite]
    print(f"  Candidatos com publicador oficial: {len(oficiais_ids)}\n")

    fichas = buscar_fichas(oficiais_ids, get_app, d / f"n3_fichas_{hoje}.json", args.pausa)

    gov = []
    for aid in oficiais_ids:
        f = dict(fichas.get(aid, {"appId": aid, "erro": "ausente"}))
        if not f.get("erro"):
            f["esfera"] = classificar_esfera(f.get("developer", ""))
            f["sensivel"], f["categorias"] = classificar_sensibilidade(
                f.get("title", ""), f.get("descricao", ""))
            f["n_instalacoes"] = instalacoes_de(f)
            f["faixa"] = faixa_instalacao(f["n_instalacoes"])
        gov.append(f)

    vivos = [f for f in gov if not f.get("erro")]

    # política de privacidade, em paralelo
    print(f"\n  Verificando {len(vivos)} políticas de privacidade...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        resultados = list(ex.map(lambda f: checar_politica(f.get("privacyPolicy")), vivos))
    politicas = {f["appId"]: r for f, r in zip(vivos, resultados)}

    celulas = {(f["genre"], f["faixa"]) for f in vivos
               if f.get("genre") and f["faixa"] != "?"}
    if args.sem_controle:
        controle, cobertas = {}, 0
        print("\n  Grupo de controle pulado (--sem-controle).")
    else:
        controle, cobertas = buscar_controle(
            search, get_app, celulas, args.pares_por_celula, args.pausa, nomes_oficiais)

    rel = relatar(gov, controle, celulas, cobertas, politicas, args)

    # planilha JÁ pré-classificada — o revisor corrige, não preenche do zero
    csv_path = d / f"n3_corpus_{hoje}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["appId", "titulo", "desenvolvedor", "categoria", "instalacoes",
                    "faixa", "esfera_auto", "sensivel_auto", "categorias_auto",
                    "tem_anuncio", "politica_estado", "atualizado",
                    "OFICIAL_S_N", "ESFERA_REVISADA", "SENSIVEL_REVISADO"])
        for f in sorted(vivos, key=lambda x: (x["esfera"], x.get("developer") or "")):
            w.writerow([f["appId"], f.get("title"), f.get("developer"), f.get("genre"),
                        f["n_instalacoes"], f["faixa"], f["esfera"],
                        "sim" if f["sensivel"] else "não", "|".join(f["categorias"]),
                        f.get("containsAds"), politicas[f["appId"]]["estado"],
                        f.get("updated"), "", "", ""])

    (d / f"n3_relatorio_{hoje}.json").write_text(
        json.dumps({"relatorio": rel, "controle": list(controle.values()),
                    "politicas": politicas}, indent=2, ensure_ascii=False))

    print(f"  Planilha pré-classificada: {csv_path}")
    print(f"  Relatório: {d / f'n3_relatorio_{hoje}.json'}\n")
    print("  A planilha vem PREENCHIDA pela heurística. Sua revisão manual é")
    print("  corrigir o que estiver errado, não classificar do zero — e as")
    print("  correções que você fizer medem a taxa de erro do classificador,")
    print("  que é número para a seção de ameaças à validade.\n")


if __name__ == "__main__":
    main()
