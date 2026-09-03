#!/usr/bin/env python3
"""
Teste de viabilidade do tema N3 — apps móveis governamentais brasileiros.

Responde à pergunta que decide o tema: EXISTEM APLICATIVOS SUFICIENTES?
O N1 morreu porque a variável independente era inobservável. Aqui a variável
(governamental vs. comercial) é observável por construção — o que falta
verificar é apenas o tamanho do corpus.

DEPENDÊNCIA
-----------
    python3 -m venv .venv && source .venv/bin/activate
    pip install google-play-scraper

  (macOS com Python do Homebrew bloqueia instalação no sistema — PEP 668.)

USO
---
    python3 teste_viabilidade_n3.py

Consulta apenas METADADOS públicos da loja. Não baixa APK, não instala nada,
não acessa área autenticada.

SAÍDA
-----
    dados/apps_gov_AAAAMMDD.csv   candidatos, para você marcar quais são oficiais
    dados/apps_gov_AAAAMMDD.json  bruto
"""

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from google_play_scraper import search, app as get_app
except ImportError:
    sys.exit(
        "Falta a dependência 'google-play-scraper'.\n\n"
        "No macOS com Python do Homebrew, instalar no sistema é bloqueado\n"
        "(PEP 668). Use o ambiente virtual do projeto:\n\n"
        "    cd ~/Documents/TCC\n"
        "    python3 -m venv .venv\n"
        "    source .venv/bin/activate\n"
        "    pip install google-play-scraper cryptography\n\n"
        "Depois rode o script de novo. Em terminal novo, reative com\n"
        "    source .venv/bin/activate"
    )

PAUSA = 1.5

# Termos de busca cobrindo as três esferas e os grandes prestadores de serviço
# público digital. Amplo de propósito: filtramos depois, à mão.
TERMOS = [
    "gov.br", "governo federal", "governo do estado", "prefeitura",
    "ministério da saúde", "receita federal", "INSS", "SUS",
    "detran", "tribunal", "SERPRO", "Dataprev",
    "carteira digital", "cadastro único", "meu INSS",
    "secretaria estadual", "secretaria municipal", "defensoria",
    "polícia militar", "corpo de bombeiros", "procon",
]

# Sinais de que o publicador é órgão público. Casamento por TOKEN, não por
# substring: 'sus' dentro de 'Direct CURSUS' trouxe o Yandex Maps para dentro,
# e 'serpro' dentro de 'SERPROS' trouxe um fundo de pensão. Mesmo erro que o
# coletor de CT cometia com 'pix' em 'capixaba'.
SINAIS_DEV = {
    "gov", "governo", "governos", "ministerio", "ministério", "prefeitura",
    "prefeituras", "estado", "secretaria", "tribunal", "serpro", "dataprev",
    "inss", "sus", "detran", "municipio", "município", "federal", "estadual",
    "distrital", "defensoria", "procuradoria", "camara", "câmara", "senado",
    "conselho", "autarquia", "instituto", "agencia", "agência", "policia",
    "polícia", "bombeiros", "justica", "justiça", "datasus", "datasp",
}

# Publicadores oficiais cujo NOME não contém nenhum sinal acima. Sem esta
# lista, o publicador do gov.br federal — o mais importante do corpus — fica
# de fora, junto das empresas estaduais de tecnologia, que são o braço de TI
# dos governos e portanto órgãos públicos.
OFICIAIS_CONHECIDOS = {
    "serviços e informações do brasil",   # gov.br federal: Meu INSS, Meu SUS, CNH...
    "justiça eleitoral brasileira",       # e-Título, Mesário, Resultados
    "justiça do trabalho",
    "celepar",                            # Paraná
    "prodam sp",                          # São Paulo capital
    "procempa",                           # Porto Alegre
    "ciasc - centro de inform. autom. de santa catarina",
    "prodap - centro de gestão da tec. da informação ap",
    "empro tecnologia e informação",      # Rio Preto
    "companhia de informática de jundiaí - cijun",
    "inova pmsc",                         # PM de Santa Catarina
    "dgti sedec",                         # Defesa Civil RJ
    "cbmsc - diti",
    "divisão de tic - corpo de bombeiros",
    "corpo de bombeiros militar de minas gerais",
    "corpo de bombeiros militar do maranhão",
    "hospital das clínicas da fmusp",
    "instituto de identificação ricardo gumbleton daunt",
}

# Publicadores que os sinais acima capturam por engano.
FALSOS_CONHECIDOS = {
    "direct cursus computer systems trading llc",  # Yandex ('cursus' contém 'sus')
    "serpros fundo multipatrocinado",              # fundo de pensão, não o SERPRO
    "tribunal superior electoral",                 # República Dominicana
}


def parece_oficial(dev: str) -> bool:
    d = (dev or "").strip().lower()
    if not d:
        return False
    if d in FALSOS_CONHECIDOS:
        return False
    if d in OFICIAIS_CONHECIDOS:
        return True
    tokens = set(re.split(r"[^a-zà-ÿ]+", d)) - {""}
    return bool(tokens & SINAIS_DEV)


def expandir(achados):
    """Enumera todos os apps de cada publicador já identificado como oficial.

    A busca por termo genérico encontra uma amostra; buscar pelo NOME DO
    PUBLICADOR encontra o catálogo dele. É o que transforma 87 num corpus real.
    """
    devs = sorted({a["dev"] for a in achados.values() if parece_oficial(a["dev"])})
    print(f"\n  Enumerando o catálogo de {len(devs)} publicadores oficiais...\n")

    novos_total = 0
    for i, dev in enumerate(devs, 1):
        try:
            res = search(f'"{dev}"', lang="pt", country="br", n_hits=30)
        except Exception as e:
            print(f"  [{i:>2}/{len(devs)}] {dev[:44]:<44} ERRO: {str(e)[:22]}")
            time.sleep(PAUSA)
            continue

        novos = 0
        for r in res:
            # só o que é REALMENTE do mesmo publicador
            if (r.get("developer") or "").strip() != dev:
                continue
            aid = r.get("appId")
            if aid and aid not in achados:
                achados[aid] = {
                    "appId": aid, "titulo": r.get("title", ""),
                    "dev": r.get("developer", ""),
                    "instalacoes": r.get("installs", "") or r.get("realInstalls", ""),
                    "score": r.get("score"), "termo": f"catalogo:{dev}"[:60],
                }
                novos += 1
        novos_total += novos
        print(f"  [{i:>2}/{len(devs)}] {dev[:44]:<44} +{novos}")
        time.sleep(PAUSA)

    print(f"\n  Expansão adicionou {novos_total} aplicativos.")


def main():
    ap = argparse.ArgumentParser(description="Viabilidade do corpus de apps governamentais.")
    ap.add_argument("--expandir", action="store_true",
                    help="após a busca por termos, enumera o catálogo de cada publicador oficial")
    args = ap.parse_args()

    d = Path("dados")
    d.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d")

    print("\n" + "=" * 62)
    print("TESTE DE VIABILIDADE — N3: apps governamentais brasileiros")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print("=" * 62)
    print(f"\nBuscando {len(TERMOS)} termos na Play Store (só metadados)...\n")

    achados = {}
    for termo in TERMOS:
        try:
            res = search(termo, lang="pt", country="br", n_hits=30)
        except Exception as e:
            print(f"  {termo:<28} ERRO: {str(e)[:45]}")
            time.sleep(PAUSA)
            continue

        novos = 0
        for r in res:
            aid = r.get("appId")
            if aid and aid not in achados:
                achados[aid] = {
                    "appId": aid,
                    "titulo": r.get("title", ""),
                    "dev": r.get("developer", ""),
                    "instalacoes": r.get("installs", "") or r.get("realInstalls", ""),
                    "score": r.get("score"),
                    "termo": termo,
                }
                novos += 1
        print(f"  {termo:<28} {len(res):>3} resultados, {novos:>3} novos")
        time.sleep(PAUSA)

    if args.expandir:
        expandir(achados)

    provaveis = [a for a in achados.values() if parece_oficial(a["dev"])]
    provaveis.sort(key=lambda a: (a["dev"].lower(), a["titulo"].lower()))
    outros = [a for a in achados.values() if not parece_oficial(a["dev"])]

    (d / f"apps_gov_{hoje}.json").write_text(
        json.dumps(list(achados.values()), indent=2, ensure_ascii=False))

    csv_path = d / f"apps_gov_{hoje}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["appId", "titulo", "desenvolvedor", "instalacoes", "score",
                    "termo_busca", "provavel_oficial", "OFICIAL_S_N",
                    "ESFERA", "TRATA_DADO_SENSIVEL_S_N"])
        for a in provaveis + outros:
            w.writerow([a["appId"], a["titulo"], a["dev"], a["instalacoes"],
                        a["score"], a["termo"],
                        "sim" if parece_oficial(a["dev"]) else "", "", "", ""])

    devs = {a["dev"] for a in provaveis}

    print("\n" + "=" * 62)
    print("RESULTADO")
    print("=" * 62)
    print(f"  Aplicativos distintos encontrados ....... {len(achados)}")
    print(f"  Com publicador de aparência oficial ..... {len(provaveis)}")
    print(f"  Publicadores oficiais distintos ......... {len(devs)}")
    print(f"\n  Planilha: {csv_path}")

    print("\n  Maiores publicadores oficiais encontrados:")
    from collections import Counter
    for dev, n in Counter(a["dev"] for a in provaveis).most_common(12):
        print(f"      {n:>3}  {dev[:55]}")

    print("""
  PRÓXIMO PASSO (o que decide o tema):

    Abra o CSV e preencha, para cada linha, OFICIAL_S_N — se é mesmo um app
    publicado por órgão público (confira o desenvolvedor; há muito app de
    terceiro que imita nome de governo). Preencha também ESFERA (federal,
    estadual, municipal) e TRATA_DADO_SENSIVEL_S_N (saúde, biometria,
    previdência).

  LEITURA:

    >= 60 oficiais confirmados   → corpus robusto. N3 confirmado, com espaço
                                    para estratificar por esfera e por
                                    sensibilidade do dado.
    30–59                        → viável; abandone a estratificação por esfera
                                    e mantenha só o contraste com o grupo de
                                    controle comercial.
    < 30                         → corpus fraco. Amplie a busca (apps de
                                    estados e capitais, um a um) antes de
                                    descartar; se não crescer, reveja o tema.

  E ATENÇÃO AO QUE MATOU O N1: verifique se os apps oficiais têm de fato
  publicador identificável. Se a maioria vier publicada por empresa terceirizada
  sem vínculo declarado, a variável independente fica turva — e o tema perde a
  premissa, como o N1 perdeu.
""")

    print("  EM PARALELO, hoje: solicite acesso acadêmico ao AndroZoo")
    print("  (androzoo.uni.lu) — é a fonte correta de APKs para pesquisa e o")
    print("  pedido leva dias, como levou o do Shodan.\n")


if __name__ == "__main__":
    main()
