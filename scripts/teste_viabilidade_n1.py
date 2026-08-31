#!/usr/bin/env python3
"""
Teste de viabilidade do tema N1 — ICS/OT exposta no Brasil.

Responde a duas perguntas em ~10 minutos:

  A) Qual o tamanho do corpus? (contagem por protocolo industrial)
  B) A atribuição organização -> setor é tratável? (amostra para classificar à mão)

USO
---
    export SHODAN_API_KEY="sua_chave_aqui"
    python3 teste_viabilidade_n1.py

    # só as contagens, sem gastar crédito nenhum:
    python3 teste_viabilidade_n1.py --apenas-contagem

CRÉDITOS
--------
As CONTAGENS usam /shodan/host/count, que não consome crédito de consulta.
A AMOSTRA usa /shodan/host/search, que consome 1 crédito por página (100 hosts).
O padrão é 1 página. Confirme sua cota com --info antes de rodar coleta grande.

SAÍDA
-----
    dados/contagens_AAAAMMDD.json    contagens brutas por consulta
    dados/amostra_AAAAMMDD.json      hosts brutos (guarde: crédito gasto não volta)
    dados/atribuicao_AAAAMMDD.csv    planilha para você preencher setor à mão
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.shodan.io"
PAUSA = 1.1  # a API pede no máximo ~1 req/s

# Consultas por protocolo industrial. A porta é o proxy mais confiável de
# protocolo; a tag 'ics' é conveniência da Shodan e pode exigir plano com filtro.
CONSULTAS = {
    "Genérico (tag ICS)":        "country:BR tag:ics",
    "Modbus":                    "country:BR port:502",
    "S7comm (Siemens)":          "country:BR port:102",
    "DNP3":                      "country:BR port:20000",
    "BACnet (automação predial)": "country:BR port:47808",
    "EtherNet/IP":               "country:BR port:44818",
    "IEC 60870-5-104":           "country:BR port:2404",
    "Niagara Fox":               "country:BR port:1911,4911",
    "ATG/tanques":               "country:BR port:10001",
    "PROFINET":                  "country:BR port:34962,34963,34964",
}

# Consulta usada para a amostra de atribuição. Modbus costuma dar o maior N.
CONSULTA_AMOSTRA = "country:BR port:502"


def buscar(caminho, chave, **params):
    params["key"] = chave
    url = f"{API}{caminho}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "pesquisa-academica-tcc"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace")[:200]
        return {"__erro__": f"HTTP {e.code}: {corpo}"}
    except Exception as e:
        return {"__erro__": str(e)}


def mostrar_info(chave):
    info = buscar("/api-info", chave)
    if "__erro__" in info:
        print(f"  ERRO ao consultar a cota: {info['__erro__']}")
        return
    print(f"  Plano ................. {info.get('plan')}")
    print(f"  Créditos de consulta .. {info.get('query_credits')}")
    print(f"  Créditos de varredura . {info.get('scan_credits')}")
    print(f"  Monitoramento ......... {info.get('monitored_ips')}")
    print("\n  Anote esses números. O desenho amostral tem que caber na cota.")


def contar(chave, saida):
    print("\n" + "=" * 62)
    print("PARTE A — Tamanho do corpus (não consome crédito)")
    print("=" * 62)

    resultados, total_modbus = {}, 0
    largura = max(len(k) for k in CONSULTAS)

    for nome, q in CONSULTAS.items():
        r = buscar("/shodan/host/count", chave, query=q)
        if "__erro__" in r:
            print(f"  {nome:<{largura}}  ERRO: {r['__erro__'][:60]}")
            resultados[nome] = {"query": q, "erro": r["__erro__"]}
        else:
            n = r.get("total", 0)
            print(f"  {nome:<{largura}}  {n:>8,}")
            resultados[nome] = {"query": q, "total": n, "facets": r.get("facets")}
            if "port:502" in q:
                total_modbus = n
        time.sleep(PAUSA)

    saida.write_text(json.dumps(resultados, indent=2, ensure_ascii=False))
    print(f"\n  Bruto salvo em: {saida}")

    validos = [v.get("total", 0) for v in resultados.values() if "total" in v]
    soma = sum(validos)
    print(f"\n  Soma bruta (há sobreposição entre consultas): {soma:,}")
    print("\n  LEITURA:")
    if soma >= 3000:
        print("    >= 3.000  → corpus robusto. A quebra setorial se sustenta. N1 confirmado.")
    elif soma >= 800:
        print("    800–3.000 → viável, mas agrupe setores para ter células suficientes.")
    else:
        print("    < 800     → quebra setorial frágil. Reveja o N1 contra o L1.")
    return total_modbus


def amostrar(chave, n_alvo, saida_json, saida_csv):
    print("\n" + "=" * 62)
    print(f"PARTE B — Amostra para atribuição (consome ~1 crédito)")
    print("=" * 62)

    r = buscar("/shodan/host/search", chave, query=CONSULTA_AMOSTRA, page=1)
    if "__erro__" in r:
        print(f"  ERRO: {r['__erro__']}")
        return
    hosts = r.get("matches", [])[:n_alvo]
    if not hosts:
        print("  Nenhum host retornado. Tente outra consulta em CONSULTA_AMOSTRA.")
        return

    saida_json.write_text(json.dumps(r, indent=2, ensure_ascii=False))
    print(f"  {len(hosts)} hosts obtidos. Bruto salvo em: {saida_json}")

    with saida_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ip", "org", "isp", "asn", "cidade", "uf", "porta",
                    "produto", "hostnames", "SETOR", "CONFIANCA_1a3", "NOTAS"])
        for h in hosts:
            loc = h.get("location", {})
            w.writerow([
                h.get("ip_str", ""),
                h.get("org", "") or "",
                h.get("isp", "") or "",
                h.get("asn", "") or "",
                loc.get("city", "") or "",
                loc.get("region_code", "") or "",
                h.get("port", ""),
                (h.get("product", "") or "")[:60],
                ";".join(h.get("hostnames", []))[:80],
                "", "", "",
            ])

    com_org = sum(1 for h in hosts if (h.get("org") or "").strip())
    print(f"  Campo 'org' preenchido pela Shodan em {com_org}/{len(hosts)} hosts.")
    print(f"\n  Planilha para preencher: {saida_csv}")
    print("""
  COMO FAZER O TESTE (cronometre — este é o dado que decide):

    1. Abra o CSV. Marque a hora.
    2. Para cada linha, olhe 'org', 'isp' e 'hostnames' e preencha SETOR com:
         energia | saneamento | predial | industria | telecom |
         academico | governo | hospedagem | desconhecido
       E CONFIANCA de 1 (chute) a 3 (certeza).
    3. Pare ao completar as 20 linhas. Anote quanto tempo levou.

  LEITURA DO RESULTADO:

    >=15 com confiança 2–3 em ~2h  → atribuição tratável. Vá de N1.
    8–14 atribuíveis               → viável, mas planeje uma fatia grande de
                                      'desconhecido' e reporte-a honestamente.
    <=7 atribuíveis                → a atribuição vai consumir o TCC. Vá de L1.

  Observação importante: 'hospedagem' e 'telecom' em excesso significam que os
  dispositivos estão atrás de provedores de nuvem/banda larga, e o operador real
  fica invisível. Isso não é erro seu — é um achado, e vira limitação declarada.
""")


def main():
    p = argparse.ArgumentParser(description="Teste de viabilidade do tema N1.")
    p.add_argument("--apenas-contagem", action="store_true",
                   help="só a Parte A; não gasta crédito algum")
    p.add_argument("--info", action="store_true", help="mostra a cota e sai")
    p.add_argument("--n", type=int, default=20, help="tamanho da amostra (padrão 20)")
    p.add_argument("--dir", default="dados", help="diretório de saída")
    args = p.parse_args()

    chave = os.environ.get("SHODAN_API_KEY", "").strip()
    if not chave:
        sys.exit("ERRO: defina SHODAN_API_KEY no ambiente.\n"
                 '  export SHODAN_API_KEY="sua_chave"\n'
                 "Nunca escreva a chave dentro do script nem a envie ao git.")

    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d")

    print("\n" + "=" * 62)
    print("TESTE DE VIABILIDADE — N1: ICS/OT exposta no Brasil")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print("=" * 62)
    mostrar_info(chave)

    if args.info:
        return

    contar(chave, d / f"contagens_{hoje}.json")

    if not args.apenas_contagem:
        amostrar(chave, args.n,
                 d / f"amostra_{hoje}.json",
                 d / f"atribuicao_{hoje}.csv")

    print("\nGuarde os JSONs brutos. Os dados mudam com o tempo e crédito não volta.\n")


if __name__ == "__main__":
    main()
