#!/usr/bin/env python3
"""
Teste de viabilidade — abuso de marca brasileira em logs de Certificate Transparency.

Responde às três perguntas que decidem o tema:

  A) Existem certificados imitando marcas brasileiras, e quantos?
  B) Qual a TAXA DE CHEGADA de candidatos novos? (é o que sustenta o eixo temporal)
  C) A classificação legítimo vs. suspeito é viável, ou vira ruído?

A pergunta B é a mais importante. Um acervo histórico grande não adianta se
quase nada novo aparece por semana: sem fluxo, não há como medir a lacuna
entre emissão e bloqueio.

USO
---
    python3 teste_viabilidade_ct.py                # todas as marcas
    python3 teste_viabilidade_ct.py --marcas itau,inss
    python3 teste_viabilidade_ct.py --dias 60      # janela de novidade

Só biblioteca padrão. Consulta o crt.sh, que é público e gratuito.
NÃO visita nenhum domínio suspeito — apenas lê o log.

NOTA SOBRE A FONTE DE DADOS
---------------------------
O crt.sh é um serviço COMUNITÁRIO e cai com frequência; erros 502/503 são dele,
não do seu script nem do tema. Ele serve bem para ESTE teste (consulta ao
acervo histórico), mas NÃO é a fonte do estudo final.

No estudo real, a coleta correta é acompanhar os logs de CT AO VIVO, porque a
variável dependente é temporal: você precisa do instante da emissão, não de um
retrato do passado. Isso se faz assinando o fluxo de certificados novos
(certstream e equivalentes) ou lendo os logs pela API de CT diretamente.
Vantagem adicional: coleta ao vivo não depende da saúde do crt.sh.

SAÍDA
-----
    dados/ct_candidatos_AAAAMMDD.csv   suspeitos, para revisão manual
    dados/ct_bruto_AAAAMMDD.json       contagens por marca
"""

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

PAUSA = 3.0        # crt.sh é um serviço comunitário: seja educado
TIMEOUT = 180      # consultas amplas demoram
TETO_POR_MARCA = 20000

# Marcas-alvo e seus domínios legítimos conhecidos.
# A lista de legítimos é DELIBERADAMENTE MÍNIMA: o objetivo é medir o teto de
# candidatos suspeitos. A revisão manual do CSV é que refina.
MARCAS = {
    "itau":        ["itau.com.br", "itau.com", "itau", "itauunibanco.com.br"],
    "bradesco":    ["bradesco.com.br", "bradesco.b.br", "bradesco.com"],
    "santander":   ["santander.com.br", "santander.com"],
    "nubank":      ["nubank.com.br", "nubank.com"],
    "caixa":       ["caixa.gov.br", "caixaeconomica.com.br"],
    "bancodobrasil": ["bb.com.br", "bancodobrasil.com.br"],
    "inss":        ["inss.gov.br", "gov.br"],
    "receitafederal": ["gov.br", "fazenda.gov.br"],
    "serpro":      ["serpro.gov.br"],
    "detran":      ["gov.br"],
    "mercadolivre": ["mercadolivre.com.br", "mercadolibre.com"],
    "mercadopago": ["mercadopago.com.br", "mercadopago.com"],
}

SUFIXOS_COMPOSTOS = {
    "com.br", "gov.br", "org.br", "net.br", "edu.br", "art.br", "ind.br",
    "inf.br", "adv.br", "eco.br", "app.br", "blog.br",
    "co.uk", "com.ar", "com.mx", "com.co", "com.au", "co.za",
}


def dominio_registravel(host: str) -> str:
    """Aproximação de eTLD+1. Para o estudo real, troque por tldextract."""
    h = host.lower().strip().lstrip("*.").rstrip(".")
    p = [x for x in h.split(".") if x]
    if len(p) < 2:
        return h
    if ".".join(p[-2:]) in SUFIXOS_COMPOSTOS and len(p) >= 3:
        return ".".join(p[-3:])
    return ".".join(p[-2:])


def _pedir(url: str):
    req = urllib.request.Request(url, headers={
        "User-Agent": "pesquisa-academica-tcc-idp",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        corpo = r.read().decode("utf-8", "replace").strip()
    return json.loads(corpo) if corpo else []


def consultar_crtsh(marca: str, tentativas=4):
    """crt.sh é serviço comunitário e cai com frequência.

    Estratégia: curinga duplo (caro, mas é o que acha imitação) com recuo
    exponencial. Erros 5xx são do servidor, não da consulta — insistir resolve
    na maioria das vezes.
    """
    url = f"https://crt.sh/?q={urllib.parse.quote(f'%{marca}%')}&output=json&exclude=expired"
    espera = 8
    ultimo = None

    for n in range(1, tentativas + 1):
        try:
            return _pedir(url)
        except urllib.error.HTTPError as e:
            ultimo = f"HTTP {e.code}"
            if e.code not in (502, 503, 504, 429):
                raise
        except Exception as e:
            ultimo = type(e).__name__

        if n < tentativas:
            print(f"      ({ultimo}; nova tentativa em {espera}s — {n}/{tentativas - 1})",
                  flush=True)
            time.sleep(espera)
            espera *= 2

    raise RuntimeError(f"{ultimo} após {tentativas} tentativas")


def analisar(marca, legitimos, registros, corte):
    """Separa candidatos suspeitos e conta os recentes."""
    legit = {dominio_registravel(d) for d in legitimos}
    suspeitos, vistos = {}, set()

    for reg in registros[:TETO_POR_MARCA]:
        nomes = (reg.get("name_value") or "").split("\n")
        ts = reg.get("entry_timestamp") or reg.get("not_before") or ""
        for nome in nomes:
            nome = nome.strip().lower()
            if not nome or marca not in nome:
                continue
            dom = dominio_registravel(nome)
            if dom in legit or any(dom.endswith("." + l) for l in legit):
                continue
            if dom in vistos:
                continue
            vistos.add(dom)
            suspeitos[dom] = {
                "dominio": dom, "exemplo_nome": nome[:90],
                "emissor": (reg.get("issuer_name") or "")[:70],
                "timestamp": ts[:19],
            }

    recentes = 0
    for s in suspeitos.values():
        try:
            if datetime.fromisoformat(s["timestamp"]).replace(tzinfo=timezone.utc) >= corte:
                recentes += 1
                s["recente"] = "sim"
        except Exception:
            s["recente"] = "?"
    return suspeitos, recentes


def main():
    ap = argparse.ArgumentParser(description="Viabilidade do tema CT / abuso de marca.")
    ap.add_argument("--marcas", help="lista separada por vírgula (padrão: todas)")
    ap.add_argument("--dias", type=int, default=90, help="janela de novidade (padrão 90)")
    ap.add_argument("--dir", default="dados")
    args = ap.parse_args()

    alvos = MARCAS
    if args.marcas:
        pedidas = [m.strip().lower() for m in args.marcas.split(",")]
        alvos = {k: v for k, v in MARCAS.items() if k in pedidas}
        if not alvos:
            raise SystemExit(f"Marcas válidas: {', '.join(MARCAS)}")

    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d")
    corte = datetime.now(timezone.utc) - timedelta(days=args.dias)

    print("\n" + "=" * 68)
    print("TESTE DE VIABILIDADE — abuso de marca brasileira em logs de CT")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"Janela de novidade: últimos {args.dias} dias")
    print("=" * 68)
    print("\nConsultando crt.sh. Consultas amplas levam ~1 min cada; tenha paciência.\n")
    print(f"  {'marca':<16}{'certs':>9}{'domínios susp.':>16}{'recentes':>11}")
    print("  " + "-" * 52)

    todos, resumo = {}, {}
    for marca, legitimos in alvos.items():
        try:
            registros = consultar_crtsh(marca)
        except Exception as e:
            print(f"  {marca:<16}  ERRO: {str(e)[:38]}")
            resumo[marca] = {"erro": str(e)}
            time.sleep(PAUSA)
            continue

        suspeitos, recentes = analisar(marca, legitimos, registros, corte)
        print(f"  {marca:<16}{len(registros):>9,}{len(suspeitos):>16,}{recentes:>11,}")
        resumo[marca] = {
            "certificados": len(registros),
            "dominios_suspeitos": len(suspeitos),
            "recentes": recentes,
        }
        for dom, info in suspeitos.items():
            info["marca"] = marca
            todos[dom] = info
        time.sleep(PAUSA)

    (d / f"ct_bruto_{hoje}.json").write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False))

    csv_path = d / f"ct_candidatos_{hoje}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dominio", "marca", "exemplo_nome", "emissor", "timestamp",
                    "recente", "IMITACAO_S_N", "NOTAS"])
        for info in sorted(todos.values(), key=lambda x: (x["marca"], x["dominio"])):
            w.writerow([info["dominio"], info["marca"], info["exemplo_nome"],
                        info["emissor"], info["timestamp"],
                        info.get("recente", ""), "", ""])

    total_susp = len(todos)
    total_rec = sum(v.get("recentes", 0) for v in resumo.values() if "recentes" in v)
    falhas = sum(1 for v in resumo.values() if "erro" in v)

    if falhas == len(resumo):
        print(f"""
{'=' * 68}
SERVIÇO INDISPONÍVEL — este NÃO é um resultado sobre o tema
{'=' * 68}
  As {falhas} consultas falharam. O crt.sh é mantido pela comunidade e cai com
  frequência; consultas com curinga duplo são o pior caso dele.

  NÃO conclua nada sobre a viabilidade do tema a partir disto.

  O que fazer:
    1. Abra https://crt.sh no navegador. Se também não responder, é o serviço.
    2. Tente de novo daqui a algumas horas, ou com uma marca só:
         python3 scripts/teste_viabilidade_ct.py --marcas itau
    3. Se persistir por mais de um dia, trocamos de fonte — veja a nota sobre
       leitura direta dos logs de CT no cabeçalho deste arquivo.
""")
        return

    print("\n" + "=" * 68)
    print("RESULTADO")
    print("=" * 68)
    print(f"  Domínios suspeitos distintos ............ {total_susp:,}")
    print(f"  Deles, nos últimos {args.dias} dias ................. {total_rec:,}")
    if args.dias:
        print(f"  Taxa aproximada ......................... {total_rec / (args.dias/7):.1f} por semana")
    print(f"\n  Planilha para revisão: {csv_path}")

    if total_susp:
        print("\n  Emissores mais frequentes:")
        for em, n in Counter(i["emissor"][:45] for i in todos.values()).most_common(6):
            print(f"      {n:>5}  {em}")

    print(f"""
  LEITURA — a taxa semanal é o número que decide:

    >= 20/semana  → fluxo rico. Eixo temporal sustentado com folga. Siga.
    5–20/semana   → viável, mas amplie a lista de marcas antes de fechar.
    < 5/semana    → sem fluxo não há lacuna a medir. Tema descartado.

  DEPOIS, o teste de classificação (30 minutos, e é o que evita repetir o N1):

    Abra o CSV, pegue 30 linhas ao acaso e preencha IMITACAO_S_N — o domínio
    parece mesmo tentativa de se passar pela marca, ou é uso legítimo da
    palavra (agência, revenda, homônimo, subdomínio de parceiro)?

      >= 20 de 30 são imitação  → sinal limpo, classificação viável.
      10–19                     → precisa de heurística melhor, mas dá.
      <= 9                      → o sinal está afogado em ruído; reveja.

  IMPORTANTE: não visite nenhum desses domínios no navegador. A classificação
  é feita pelo NOME. Visitar página de phishing não acrescenta nada à pesquisa
  e cria exposição desnecessária.
""")


if __name__ == "__main__":
    main()
