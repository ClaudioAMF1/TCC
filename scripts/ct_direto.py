#!/usr/bin/env python3
"""
Leitura DIRETA dos logs de Certificate Transparency — sem crt.sh.

Por que existe: o crt.sh é um índice comunitário sobre os logs, e cai. Os logs
em si são públicos, têm API padronizada (RFC 6962) e estão sempre no ar. Ler
direto dá o instante exato da emissão, que é a variável dependente do estudo.

O QUE FAZ
---------
Pega a lista oficial de logs, descobre o tamanho atual de cada árvore, baixa as
entradas mais recentes, extrai os nomes de domínio de cada certificado e conta
quantos batem com marcas brasileiras. Com o intervalo de tempo coberto pela
amostra, extrapola a TAXA SEMANAL — o número que decide o tema.

DEPENDÊNCIA
-----------
    pip3 install cryptography

USO
---
    python3 ct_direto.py                 # amostra padrão
    python3 ct_direto.py --entradas 4000 # amostra maior, mais precisão
    python3 ct_direto.py --listar-logs   # só mostra os logs disponíveis

Só leitura de log público. Não visita nenhum domínio.
"""

import argparse
import base64
import json
import re
import struct
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography import x509
except ImportError:
    sys.exit("Falta a dependência. Rode:\n    pip3 install cryptography")

LISTA_LOGS = "https://www.gstatic.com/ct/log_list/v3/log_list.json"
LOTE = 256          # a maioria dos logs limita o tamanho do lote; o servidor corta
TIMEOUT = 60

# Marcas-alvo. Termos curtos ou ambíguos geram ruído — mantenha específico.
MARCAS = [
    "itau", "bradesco", "santander", "nubank", "bancodobrasil",
    "caixa", "inss", "receitafederal", "serpro", "detran",
    "mercadolivre", "mercadopago", "gov-br", "govbr", "sefaz",
    "correios", "pix",
]

# Domínios legítimos, para não contar o próprio dono como suspeito.
LEGITIMOS = re.compile(
    r"(^|\.)("
    r"itau\.com(\.br)?|itau\.b\.br|bradesco\.com(\.br)?|bradesco\.b\.br|"
    r"santander\.com(\.br)?|nubank\.com(\.br)?|bb\.com\.br|bancodobrasil\.com\.br|"
    r"caixa\.gov\.br|mercadolivre\.com(\.br)?|mercadolibre\.com|"
    r"mercadopago\.com(\.br)?|correios\.com\.br|gov\.br"
    r")$"
)


def pegar(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "pesquisa-academica-tcc-idp"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def logs_utilizaveis():
    """Logs em operação, do ano corrente e do próximo (onde estão as emissões novas)."""
    dados = pegar(LISTA_LOGS)
    ano = datetime.now(timezone.utc).year
    saida = []
    for operador in dados.get("operators", []):
        for log in operador.get("logs", []):
            estado = log.get("state", {})
            if not ({"usable", "qualified"} & set(estado)):
                continue
            nome = log.get("description", "")
            if str(ano) in nome or str(ano + 1) in nome:
                saida.append({"nome": nome, "url": log["url"],
                              "operador": operador.get("name", "")})
    return saida


def nomes_do_certificado(leaf_b64, extra_b64):
    """Extrai (timestamp, [dns_names]) de uma entrada de log (RFC 6962).

    leaf_input = versão(1) tipo(1) timestamp(8) tipo_entrada(2) ...
      tipo_entrada 0 (x509)   -> DER do certificado, com prefixo de 3 bytes
      tipo_entrada 1 (precert)-> hash da chave(32) + TBS; o DER completo vem
                                 no extra_data, também com prefixo de 3 bytes
    """
    bruto = base64.b64decode(leaf_b64)
    if len(bruto) < 12:
        return None, []
    ts_ms = struct.unpack(">Q", bruto[2:10])[0]
    tipo = struct.unpack(">H", bruto[10:12])[0]

    if tipo == 0:
        tam = int.from_bytes(bruto[12:15], "big")
        der = bruto[15:15 + tam]
    elif tipo == 1:
        extra = base64.b64decode(extra_b64 or "")
        if len(extra) < 3:
            return ts_ms, []
        tam = int.from_bytes(extra[0:3], "big")
        der = extra[3:3 + tam]
    else:
        return ts_ms, []

    try:
        cert = x509.load_der_x509_certificate(der)
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ts_ms, [n.lower() for n in san.value.get_values_for_type(x509.DNSName)]
    except Exception:
        return ts_ms, []


def amostrar_log(log, alvo):
    """Baixa as entradas mais recentes de um log. Devolve (nomes, ts_min, ts_max, erros)."""
    base = log["url"].rstrip("/")
    sth = pegar(f"{base}/ct/v1/get-sth", timeout=30)
    tamanho = sth["tree_size"]

    nomes, ts_min, ts_max, erros, obtidas = [], None, None, 0, 0
    fim = tamanho - 1

    while obtidas < alvo and fim > 0:
        inicio = max(0, fim - LOTE + 1)
        try:
            r = pegar(f"{base}/ct/v1/get-entries?start={inicio}&end={fim}")
        except Exception:
            erros += 1
            if erros > 3:
                break
            time.sleep(2)
            fim = inicio - 1
            continue

        entradas = r.get("entries", [])
        if not entradas:
            break

        for e in entradas:
            ts, dns = nomes_do_certificado(e.get("leaf_input", ""), e.get("extra_data", ""))
            obtidas += 1
            if ts:
                ts_min = ts if ts_min is None else min(ts_min, ts)
                ts_max = ts if ts_max is None else max(ts_max, ts)
            nomes.extend(dns)

        fim = inicio - 1
        time.sleep(0.4)

    return nomes, ts_min, ts_max, obtidas


def main():
    ap = argparse.ArgumentParser(description="Amostra direta dos logs de CT.")
    ap.add_argument("--entradas", type=int, default=2000,
                    help="entradas por log (padrão 2000)")
    ap.add_argument("--logs", type=int, default=2, help="quantos logs amostrar")
    ap.add_argument("--listar-logs", action="store_true")
    ap.add_argument("--dir", default="dados")
    args = ap.parse_args()

    print("\n" + "=" * 68)
    print("AMOSTRA DIRETA DE LOGS DE CERTIFICATE TRANSPARENCY")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print("=" * 68)

    try:
        disponiveis = logs_utilizaveis()
    except Exception as e:
        sys.exit(f"\nNão consegui a lista de logs: {e}")

    if args.listar_logs:
        for l in disponiveis:
            print(f"  [{l['operador']}] {l['nome']}\n      {l['url']}")
        return

    if not disponiveis:
        sys.exit("Nenhum log utilizável encontrado na lista oficial.")

    escolhidos = disponiveis[:args.logs]
    print(f"\n{len(disponiveis)} logs utilizáveis; amostrando {len(escolhidos)}:")
    for l in escolhidos:
        print(f"  - {l['nome']} ({l['operador']})")

    todos_nomes, ts_min, ts_max, total = [], None, None, 0
    for l in escolhidos:
        print(f"\n  Baixando de {l['nome']}...", flush=True)
        try:
            nomes, tmin, tmax, n = amostrar_log(l, args.entradas)
        except Exception as e:
            print(f"    ERRO: {str(e)[:60]}")
            continue
        print(f"    {n} entradas, {len(nomes)} nomes DNS")
        todos_nomes.extend(nomes)
        total += n
        if tmin:
            ts_min = tmin if ts_min is None else min(ts_min, tmin)
        if tmax:
            ts_max = tmax if ts_max is None else max(ts_max, tmax)

    if not total:
        sys.exit("\nNenhuma entrada obtida. Tente de novo ou reduza --entradas.")

    # Filtra por marca, descartando os domínios legítimos.
    achados = {}
    for nome in todos_nomes:
        limpo = nome.lstrip("*.")
        if LEGITIMOS.search(limpo):
            continue
        for marca in MARCAS:
            if marca in limpo:
                achados.setdefault(limpo, marca)
                break

    horas = ((ts_max - ts_min) / 3_600_000) if (ts_min and ts_max) else 0

    print("\n" + "=" * 68)
    print("RESULTADO")
    print("=" * 68)
    print(f"  Entradas amostradas ..................... {total:,}")
    print(f"  Nomes DNS extraídos ..................... {len(todos_nomes):,}")
    print(f"  Janela temporal coberta ................. {horas:.2f} horas")
    print(f"  Candidatos (marca BR, não legítimo) ..... {len(achados):,}")

    if horas > 0:
        por_hora = len(achados) / horas
        print(f"\n  Taxa observada .......................... {por_hora:.2f}/hora")
        print(f"  Extrapolação semanal (nesta fatia) ...... {por_hora * 168:.0f}/semana")
        print("\n  ATENÇÃO: isto é a taxa VISTA NA FATIA amostrada de "
              f"{len(escolhidos)} log(s).")
        print("  O ecossistema tem dezenas de logs e cada certificado aparece em")
        print("  vários. O número real difere — sirva-se dele como ORDEM DE GRANDEZA.")

    if achados:
        print("\n  Amostra do que foi encontrado:")
        for dom, marca in list(achados.items())[:25]:
            print(f"      [{marca:<14}] {dom[:60]}")
        print("\n  Marcas mais atingidas:")
        for marca, n in Counter(achados.values()).most_common(10):
            print(f"      {n:>5}  {marca}")

    d = Path(args.dir); d.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    saida = d / f"ct_direto_{hoje}.json"
    saida.write_text(json.dumps({
        "coleta": datetime.now(timezone.utc).isoformat(),
        "logs": [l["nome"] for l in escolhidos],
        "entradas": total, "nomes_dns": len(todos_nomes),
        "horas_cobertas": horas,
        "candidatos": achados,
    }, indent=2, ensure_ascii=False))
    print(f"\n  Salvo em: {saida}")

    print(f"""
  LEITURA:

    Achou candidatos e a taxa é mensurável  → o fenômeno existe e é observável
                                               ao vivo. Tema confirmado; o
                                               coletor definitivo é este script
                                               rodando de forma contínua.
    Zero candidatos em {total:,} entradas       → amplie a amostra (--entradas
                                               10000) antes de concluir. Nesta
                                               janela de poucos minutos, marca
                                               brasileira é agulha no palheiro.

  PRÓXIMO PASSO SE CONFIRMAR: transformar isto em coleta contínua, guardando
  cada candidato com o timestamp de emissão. É a base do estudo — e passa a
  rodar sozinho enquanto você faz outra coisa.
""")


if __name__ == "__main__":
    main()
