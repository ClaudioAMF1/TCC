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

import csv
import json
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

# Sinais de que o publicador é de fato órgão público. Usados só para ordenar
# a planilha — a decisão final é sua, na coluna OFICIAL.
SINAIS_DEV = [
    "gov", "governo", "ministerio", "ministério", "prefeitura", "estado",
    "secretaria", "tribunal", "serpro", "dataprev", "inss", "sus",
    "detran", "municipio", "município", "federal", "estadual", "distrito",
]


def parece_oficial(dev: str) -> bool:
    d = (dev or "").lower()
    return any(s in d for s in SINAIS_DEV)


def main():
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
