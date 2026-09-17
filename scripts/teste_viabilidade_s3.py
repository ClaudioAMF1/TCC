#!/usr/bin/env python3
"""
Teste de viabilidade do tema S3 — falsificação de e-mail em domínios públicos.

A PERGUNTA DO TEMA
------------------
E-mail funciona como carta com remetente escrito à mão: qualquer um pode
escrever "Receita Federal" no campo do remetente. O protocolo original não
verifica nada. Existem três proteções que o DONO DO DOMÍNIO precisa ligar:

    SPF    o domínio publica quais servidores podem enviar em nome dele
    DKIM   assinatura criptográfica; detecta adulteração no caminho
    DMARC  a instrução para quem recebe: se falhar, faça o quê?
           none (entrega e avisa) < quarantine (spam) < reject (recusa)

Domínio público sem DMARC em `reject` é tecnicamente falsificável. E golpe com
"Receita Federal" ou "INSS" no remetente é o vetor de fraude mais comum contra
o cidadão brasileiro.

O QUE ESTE TESTE DECIDE
-----------------------
NÃO decide se a adoção é alta ou baixa — isso é resultado, não viabilidade.
Decide três coisas, nesta ordem de importância:

  1. HÁ VARIAÇÃO?  Se 95% dos domínios não tiverem nada, não existe nada a
     explicar, e o trabalho vira estatística descritiva. É o único desfecho
     que mata o tema.

  2. HÁ ESTRATOS COMPARÁVEIS?  Federal, estadual e municipal precisam ter
     domínios suficientes para contraste.

  3. DÁ PARA TESTAR A HERANÇA POR FORNECEDOR?  A hipótese que eleva o tema:
     a postura de um município não é escolha dele, é herdada de quem presta
     o serviço de TI. Municípios atendidos pela mesma empresa estadual de
     tecnologia teriam a mesma configuração. Para testar isso é preciso que
     o fornecedor seja IDENTIFICÁVEL — e ele é, pelos registros NS e MX.

O QUE ESTE SCRIPT NÃO FAZ
-------------------------
Só faz consulta de DNS, que é informação pública publicada pelo próprio dono
do domínio. Não envia e-mail, não tenta falsificar remetente, não testa
entrega, não toca em servidor de terceiro.

DEPENDÊNCIA
-----------
    python3 -m venv .venv && source .venv/bin/activate
    pip install dnspython

USO
---
    python3 scripts/teste_viabilidade_s3.py
    python3 scripts/teste_viabilidade_s3.py --autoteste     # sem rede
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------- o corpus

# Executivo federal: ministérios, agências e as estatais de TI.
FEDERAL = [
    "gov.br", "saude.gov.br", "inss.gov.br", "fazenda.gov.br", "mec.gov.br",
    "defesa.gov.br", "justica.gov.br", "planalto.gov.br", "serpro.gov.br",
    "dataprev.gov.br", "ibge.gov.br", "anvisa.gov.br", "inep.gov.br",
    "bcb.gov.br", "mre.gov.br", "agricultura.gov.br", "turismo.gov.br",
    "cultura.gov.br", "cidades.gov.br", "transportes.gov.br", "mme.gov.br",
    "mcti.gov.br", "ana.gov.br", "aneel.gov.br", "anatel.gov.br",
    "antt.gov.br", "ibama.gov.br", "icmbio.gov.br", "incra.gov.br",
    "funai.gov.br", "pf.gov.br", "prf.gov.br", "cgu.gov.br", "tcu.gov.br",
    "anpd.gov.br", "inpi.gov.br", "inmetro.gov.br", "capes.gov.br",
    "cnpq.br", "fiocruz.br", "embrapa.br",
]

# Judiciário (.jus.br) e Legislativo (.leg.br). Poderes diferentes têm
# governança de TI diferente — é um eixo de contraste que o tema ganha de graça.
JUDICIARIO = ["stf.jus.br", "stj.jus.br", "tse.jus.br", "tst.jus.br",
              "cnj.jus.br", "trf1.jus.br", "tjsp.jus.br", "tjmg.jus.br",
              "tjrj.jus.br", "tjpe.jus.br"]
LEGISLATIVO = ["senado.leg.br", "camara.leg.br", "al.sp.gov.br"]

# Os 26 estados e o DF. Estrato completo, sem amostragem.
ESTADUAL = [f"{uf}.gov.br" for uf in [
    "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms",
    "mt", "pa", "pb", "pe", "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc",
    "se", "sp", "to",
]]

# Capitais. O padrão de nome municipal é IRREGULAR — algumas usam
# <cidade>.<uf>.gov.br, outras uma sigla (pbh, pmf). Estes são CANDIDATOS:
# o script reporta quais resolvem e quais não, em vez de fingir certeza.
MUNICIPAL = [
    "riobranco.ac.gov.br", "maceio.al.gov.br", "macapa.ap.gov.br",
    "manaus.am.gov.br", "salvador.ba.gov.br", "fortaleza.ce.gov.br",
    "vitoria.es.gov.br", "goiania.go.gov.br", "saoluis.ma.gov.br",
    "cuiaba.mt.gov.br", "campogrande.ms.gov.br", "pbh.gov.br",
    "belem.pa.gov.br", "joaopessoa.pb.gov.br", "curitiba.pr.gov.br",
    "recife.pe.gov.br", "teresina.pi.gov.br", "rio.rj.gov.br",
    "natal.rn.gov.br", "portoalegre.rs.gov.br", "portovelho.ro.gov.br",
    "boavista.rr.gov.br", "pmf.sc.gov.br", "prefeitura.sp.gov.br",
    "capital.sp.gov.br", "aracaju.se.gov.br", "palmas.to.gov.br",
    "guarulhos.sp.gov.br", "campinas.sp.gov.br", "santos.sp.gov.br",
    "niteroi.rj.gov.br", "londrina.pr.gov.br", "maringa.pr.gov.br",
    "joinville.sc.gov.br", "uberlandia.mg.gov.br", "contagem.mg.gov.br",
    "caxias.rs.gov.br", "sorocaba.sp.gov.br", "ribeiraopreto.sp.gov.br",
    "feiradesantana.ba.gov.br",
]

# Seletores DKIM mais comuns. DKIM vive em <seletor>._domainkey.<dominio>, e
# não há como descobrir o seletor pelo DNS — só sondando nomes conhecidos.
# Isso SUBCONTA por construção, e a subcontagem vai declarada no resultado.
SELETORES_DKIM = ["default", "google", "selector1", "selector2", "s1", "s2",
                  "k1", "mail", "dkim", "smtp", "mandrill", "zoho", "dkim1"]

# Fornecedores reconhecíveis pelo domínio-base dos registros NS e MX. É o
# instrumento da hipótese de herança: se o NS de uma prefeitura aponta para a
# Celepar, quem configura o DNS dela é a Celepar, não ela.
FORNECEDORES = {
    "google.com": "Google", "googlemail.com": "Google",
    "outlook.com": "Microsoft", "microsoft.com": "Microsoft",
    "protection.outlook.com": "Microsoft", "office365.com": "Microsoft",
    "serpro.gov.br": "SERPRO", "dataprev.gov.br": "Dataprev",
    "celepar.pr.gov.br": "Celepar (PR)", "celepar.br": "Celepar (PR)",
    "prodam.sp.gov.br": "Prodam (SP capital)",
    "procempa.com.br": "Procempa (POA)", "prodesp.sp.gov.br": "Prodesp (SP)",
    "prodemge.gov.br": "Prodemge (MG)", "prodeb.ba.gov.br": "Prodeb (BA)",
    "ciasc.sc.gov.br": "Ciasc (SC)", "prodepa.pa.gov.br": "Prodepa (PA)",
    "emprel.recife.pe.gov.br": "Emprel (Recife)",
    "registro.br": "Registro.br", "cloudflare.com": "Cloudflare",
    "awsdns-01.org": "AWS", "awsdns.com": "AWS", "amazonaws.com": "AWS",
    "locaweb.com.br": "Locaweb", "uolhost.com.br": "UOL",
    "rnp.br": "RNP", "zimbra.com": "Zimbra",
}


# ------------------------------------------------------------------ parsing

def dominio_base(host: str) -> str:
    """Últimos rótulos do hostname, para casar com a tabela de fornecedores.

    Em '.br' o registrável tem três rótulos (algo.gov.br), fora dele dois.
    Casamento por SUFIXO DE RÓTULO, nunca por substring: 'google.com' dentro
    de 'notgoogle.com.br' não pode casar. É o mesmo erro que 'pix' em
    'capixaba' e 'sus' em 'Direct Cursus' já causaram neste repositório.
    """
    partes = [p for p in (host or "").strip(".").lower().split(".") if p]
    if not partes:
        return ""
    n = 3 if partes[-1] == "br" and len(partes) >= 3 else 2
    return ".".join(partes[-n:])


def classificar_fornecedor(hosts) -> str:
    """Nome do fornecedor a partir dos hostnames de NS ou MX."""
    for h in hosts or []:
        partes = [p for p in (h or "").strip(".").lower().split(".") if p]
        # tenta sufixos de 2, 3 e 4 rótulos, do mais específico ao mais geral
        for n in (4, 3, 2):
            if len(partes) >= n:
                suf = ".".join(partes[-n:])
                if suf in FORNECEDORES:
                    return FORNECEDORES[suf]
    for h in hosts or []:
        base = dominio_base(h)
        if base:
            return f"próprio/outro ({base})"
    return "desconhecido"


def parse_spf(txts):
    """Devolve (tem_spf, qualificador). O qualificador é o rigor declarado:
    -all recusa, ~all marca como suspeito, ?all é neutro, +all não protege."""
    for t in txts or []:
        t = t.strip()
        if t.lower().startswith("v=spf1"):
            m = re.search(r"([-~?+])all\b", t, re.I)
            return True, (m.group(1) if m else "sem_all")
    return False, None


ORDEM_DMARC = {"reject": 3, "quarantine": 2, "none": 1}


def parse_dmarc(txts):
    """Devolve (tem_dmarc, politica, pct).

    `pct` importa: p=reject com pct=20 aplica a política a 20% das mensagens.
    Ler só o `p=` superestima a proteção real — é a armadilha clássica deste
    tipo de levantamento.
    """
    for t in txts or []:
        t = t.strip()
        if not t.lower().startswith("v=dmarc1"):
            continue
        m = re.search(r"\bp\s*=\s*(none|quarantine|reject)\b", t, re.I)
        pol = m.group(1).lower() if m else "invalido"
        mp = re.search(r"\bpct\s*=\s*(\d{1,3})\b", t, re.I)
        pct = int(mp.group(1)) if mp else 100
        return True, pol, max(0, min(pct, 100))
    return False, None, None


# Domínios que não seguem o padrão de nome e seriam classificados errado pela
# contagem de rótulos. 'pbh.gov.br' é Belo Horizonte (município, não federal);
# 'al.sp.gov.br' é a Assembleia Legislativa de SP (legislativo estadual, não
# município). A regra por rótulo acerta a maioria — estes são as exceções.
ESFERA_OVERRIDE = {
    "pbh.gov.br": "municipal",
    "al.sp.gov.br": "legislativo",
    "cnpq.br": "federal", "fiocruz.br": "federal", "embrapa.br": "federal",
}


def esfera_de(dominio: str) -> str:
    d = dominio.lower()
    if d in ESFERA_OVERRIDE:
        return ESFERA_OVERRIDE[d]
    if d.endswith(".jus.br"):
        return "judiciario"
    if d.endswith(".leg.br"):
        return "legislativo"
    partes = d.split(".")
    # <cidade>.<uf>.gov.br tem 4 rótulos; <uf>.gov.br tem 3
    if d.endswith(".gov.br"):
        if len(partes) >= 4:
            return "municipal"
        if len(partes) == 3 and len(partes[0]) == 2:
            return "estadual"
        return "federal"
    return "federal"


# ------------------------------------------------------------------- coleta
#
# Dois motores de DNS. O `dnspython` é mais rápido, mas exige instalação, e
# instalar biblioteca no Python do sistema é bloqueado no macOS (PEP 668).
# O `dig` já vem no macOS e em qualquer Linux, e não precisa de nada.
# O script escolhe sozinho: usa o que estiver disponível.


def parse_txt_dig(saida: str):
    """Extrai registros TXT da saída de `dig +short`.

    Um TXT longo é quebrado em pedaços de 255 bytes, que o dig imprime como
    várias strings entre aspas na MESMA linha: "pedaço1" "pedaço2". Elas
    precisam ser concatenadas — um SPF longo cortado no meio não casaria com
    'v=spf1', e o domínio apareceria como desprotegido sem estar.
    """
    registros = []
    for linha in saida.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        pedacos = re.findall(r'"((?:[^"\\]|\\.)*)"', linha)
        registros.append("".join(pedacos) if pedacos else linha)
    return registros


class ConsultorDig:
    """Resolve via o binário `dig`. Sem dependência de biblioteca."""

    nome = "dig"

    def __init__(self, timeout=5.0):
        self.timeout = timeout

    def _dig(self, nome, tipo):
        import subprocess
        try:
            p = subprocess.run(
                ["dig", "+short", f"+time={int(self.timeout)}", "+tries=1",
                 tipo, nome],
                capture_output=True, text=True, timeout=self.timeout + 3)
        except Exception:
            return ""
        return p.stdout

    def consultar(self, nome, tipo):
        saida = self._dig(nome, tipo)
        if tipo == "TXT":
            return parse_txt_dig(saida)
        linhas = [l.strip() for l in saida.splitlines() if l.strip()]
        if tipo == "MX":
            # formato: "10 aspmx.l.google.com."
            return [l.split()[-1] for l in linhas if l.split()]
        return linhas


class ConsultorDnspython:
    nome = "dnspython"

    def __init__(self, timeout=5.0):
        import dns.resolver
        self.r = dns.resolver.Resolver()
        self.r.lifetime = timeout
        self.r.timeout = timeout

    def consultar(self, nome, tipo):
        try:
            resp = self.r.resolve(nome, tipo)
        except Exception:
            return []
        if tipo == "TXT":
            return ["".join(s.decode() for s in rr.strings) for rr in resp]
        if tipo == "MX":
            return [str(rr.exchange) for rr in resp]
        if tipo == "NS":
            return [str(rr.target) for rr in resp]
        return [str(rr) for rr in resp]


def escolher_motor(preferido, timeout):
    """Devolve uma FÁBRICA de consultor — cada thread cria o seu."""
    import shutil

    def tem_dig():
        return shutil.which("dig") is not None

    def tem_dnspython():
        try:
            import dns.resolver  # noqa: F401
            return True
        except ImportError:
            return False

    if preferido == "dnspython" or (preferido == "auto" and tem_dnspython()):
        if not tem_dnspython():
            sys.exit("Motor 'dnspython' pedido, mas a biblioteca não está instalada.")
        return lambda: ConsultorDnspython(timeout)

    if preferido in ("dig", "auto"):
        if not tem_dig():
            sys.exit(
                "Nenhum motor de DNS disponível.\n\n"
                "Opção 1 — instalar o dnspython no ambiente virtual do projeto:\n"
                "    python3 -m venv .venv\n"
                "    source .venv/bin/activate\n"
                "    python3 -m pip install dnspython\n\n"
                "Opção 2 — ter o comando 'dig' no PATH (já vem no macOS e no Linux).\n"
            )
        return lambda: ConsultorDig(timeout)

    sys.exit(f"Motor desconhecido: {preferido}")


def coletar(dominio, consultor, sondar_dkim):
    c = consultor.consultar
    d = {"dominio": dominio, "esfera": esfera_de(dominio)}

    ns = c(dominio, "NS")
    if not ns and not c(dominio, "A"):
        d["resolve"] = False
        return d
    d["resolve"] = True

    d["spf"], d["spf_qualificador"] = parse_spf(c(dominio, "TXT"))
    d["dmarc"], d["dmarc_politica"], d["dmarc_pct"] = parse_dmarc(
        c(f"_dmarc.{dominio}", "TXT"))

    mx = c(dominio, "MX")
    d["tem_mx"] = bool(mx)
    d["fornecedor_ns"] = classificar_fornecedor(ns)
    d["fornecedor_mx"] = classificar_fornecedor(mx) if mx else "sem_mx"

    d["dkim_seletores"] = []
    if sondar_dkim:
        for sel in SELETORES_DKIM:
            if c(f"{sel}._domainkey.{dominio}", "TXT"):
                d["dkim_seletores"].append(sel)
    d["dkim"] = bool(d["dkim_seletores"])
    return d


# ---------------------------------------------------------------- relatório

def pct(k, n):
    return f"{100*k/n:.1f}%" if n else "—"


def pureza_por_fornecedor(regs, campo_forn, minimo=3):
    """Quanto a postura de um domínio é explicada por QUEM presta o serviço.

    Para cada fornecedor com ao menos `minimo` domínios, mede a fração que
    compartilha a política DMARC mais comum daquele fornecedor. Compara com a
    mesma fração calculada sobre o conjunto inteiro.

    Pureza por fornecedor MUITO acima da base é o sinal da hipótese de
    herança. Isto é indício, não teste: com poucos domínios por fornecedor a
    pureza sobe por acaso, e a monografia usaria um modelo com efeito
    aleatório por fornecedor.
    """
    def politica(r):
        return r["dmarc_politica"] if r.get("dmarc") else "ausente"

    base_cont = Counter(politica(r) for r in regs)
    base = base_cont.most_common(1)[0][1] / len(regs) if regs else 0

    grupos = defaultdict(list)
    for r in regs:
        grupos[r[campo_forn]].append(r)

    linhas, soma, total = [], 0, 0
    for forn, membros in grupos.items():
        if len(membros) < minimo or forn.startswith("desconhecido"):
            continue
        c = Counter(politica(m) for m in membros)
        dom, n = c.most_common(1)[0]
        p = n / len(membros)
        linhas.append((forn, len(membros), dom, p))
        soma += p * len(membros)
        total += len(membros)
    media = soma / total if total else 0
    linhas.sort(key=lambda x: (-x[1], x[0]))
    return base, media, linhas, total


def relatar(regs, args):
    vivos = [r for r in regs if r.get("resolve")]
    mortos = [r for r in regs if not r.get("resolve")]

    print("\n  PORTA 1 — O CORPUS EXISTE?")
    print("  " + "=" * 62)
    print(f"    Domínios consultados .............. {len(regs)}")
    print(f"    Resolvem .......................... {len(vivos)}")
    print(f"    Não resolvem (nome candidato errado) {len(mortos)}")
    if mortos:
        print("      " + ", ".join(r["dominio"] for r in mortos[:12]))
        print("      (o padrão de nome municipal é irregular; estes saem do corpus)")
    por_esf = Counter(r["esfera"] for r in vivos)
    print("\n    Por esfera:")
    for e, n in por_esf.most_common():
        print(f"        {n:>4}  {e}")

    print("\n  PORTA 2 — HÁ VARIAÇÃO? (a que decide o tema)")
    print("  " + "=" * 62)
    n = len(vivos)
    k_spf = sum(1 for r in vivos if r["spf"])
    k_dmarc = sum(1 for r in vivos if r["dmarc"])
    k_dkim = sum(1 for r in vivos if r["dkim"])
    print(f"    Com SPF ........................... {k_spf:>4}/{n}  {pct(k_spf,n)}")
    print(f"    Com DMARC ......................... {k_dmarc:>4}/{n}  {pct(k_dmarc,n)}")
    print(f"    Com DKIM (seletor conhecido) ...... {k_dkim:>4}/{n}  {pct(k_dkim,n)}")
    print("      ^ DKIM SUBCONTA: o seletor não é descobrível pelo DNS, só")
    print("        sondável. Um domínio com seletor incomum aparece sem DKIM.")

    print("\n    Rigor declarado no SPF:")
    for q, c in Counter(r["spf_qualificador"] for r in vivos if r["spf"]).most_common():
        rotulo = {"-": "-all  recusa", "~": "~all  marca como suspeito",
                  "?": "?all  neutro (não protege)", "+": "+all  aceita qualquer um",
                  "sem_all": "sem 'all' (incompleto)"}.get(q, str(q))
        print(f"        {c:>4}  {rotulo}")

    print("\n    Política DMARC — a variável dependente do trabalho:")
    pol = Counter(r["dmarc_politica"] for r in vivos if r["dmarc"])
    for p_ in ("reject", "quarantine", "none", "invalido"):
        if pol.get(p_):
            print(f"        {pol[p_]:>4}  p={p_}")
    print(f"        {n - k_dmarc:>4}  sem DMARC")
    parciais = [r for r in vivos if r.get("dmarc") and (r.get("dmarc_pct") or 100) < 100]
    if parciais:
        print(f"\n    ⚠ {len(parciais)} domínios têm pct<100: a política vale só para")
        print("      parte das mensagens. Ler só o 'p=' superestima a proteção.")

    print("\n    Proteção efetiva contra falsificação (DMARC p=reject, pct=100):")
    efetiva = sum(1 for r in vivos
                  if r.get("dmarc") and r.get("dmarc_politica") == "reject"
                  and (r.get("dmarc_pct") or 100) == 100)
    print(f"        {efetiva}/{n}  ({pct(efetiva, n)})  — o resto é falsificável")

    print("\n  PORTA 3 — HÁ CONTRASTE ENTRE ESFERAS?")
    print("  " + "=" * 62)
    print(f"    {'esfera':<14}{'n':>5}{'SPF':>9}{'DMARC':>9}{'reject':>9}")
    for e, tot in por_esf.most_common():
        g = [r for r in vivos if r["esfera"] == e]
        print(f"    {e:<14}{tot:>5}{pct(sum(1 for r in g if r['spf']), tot):>9}"
              f"{pct(sum(1 for r in g if r['dmarc']), tot):>9}"
              f"{pct(sum(1 for r in g if r.get('dmarc_politica')=='reject'), tot):>9}")

    print("\n  PORTA 4 — DÁ PARA TESTAR A HERANÇA POR FORNECEDOR?")
    print("  " + "=" * 62)
    print("    A hipótese que eleva o tema: a postura não é escolha do órgão,")
    print("    é herdada de quem presta o serviço de TI.\n")
    for campo, rotulo in (("fornecedor_ns", "quem opera o DNS"),
                          ("fornecedor_mx", "quem recebe o e-mail")):
        base, media, linhas, cobertos = pureza_por_fornecedor(vivos, campo)
        print(f"    {rotulo.upper()}")
        print(f"      Fornecedores com ≥3 domínios ... {len(linhas)} "
              f"(cobrindo {cobertos} domínios)")
        if linhas:
            print(f"      Concordância dentro do fornecedor  {media:.0%}")
            print(f"      Concordância no conjunto todo ...  {base:.0%}")
            delta = media - base
            print(f"      Diferença ......................  {delta:+.0%}  "
                  f"{'← sinal de herança' if delta >= 0.15 else ''}")
            for forn, cnt, dom, p in linhas[:8]:
                print(f"          {cnt:>3}  {forn[:34]:<34} {dom:<11} {p:.0%}")
        print()

    # ------------------------------------------------------------- veredito
    print("  VEREDITO")
    print("  " + "=" * 62)
    tx = k_dmarc / n if n else 0
    varia = 0.10 <= tx <= 0.90
    corpus_ok = n >= 60
    esferas_ok = sum(1 for e, c in por_esf.items() if c >= 10) >= 3
    base_ns, media_ns, linhas_ns, _ = pureza_por_fornecedor(vivos, "fornecedor_ns")
    heranca_ok = len(linhas_ns) >= 3

    def m(b):
        return "✅" if b else "❌"
    print(f"    {m(corpus_ok)} Corpus ......... {n} domínios resolvem (precisa ≥60)")
    print(f"    {m(varia)} VARIAÇÃO ....... {pct(k_dmarc,n)} com DMARC "
          f"(precisa entre 10% e 90%)")
    print(f"    {m(esferas_ok)} Estratos ....... {sum(1 for e,c in por_esf.items() if c>=10)} "
          f"esferas com ≥10 domínios (precisa ≥3)")
    print(f"    {m(heranca_ok)} Herança ........ {len(linhas_ns)} fornecedores de DNS "
          f"com ≥3 domínios (precisa ≥3)")

    print("""
  COMO LER

    VARIAÇÃO fechada é o ÚNICO desfecho que mata o tema. Se quase ninguém
    tem DMARC, não há o que explicar: o trabalho vira contagem, e contagem
    não é pesquisa. Nesse caso o tema ainda pode virar OUTRA pergunta —
    "por que a adoção é tão baixa?" — mas aí é entrevista e análise de
    política pública, não medição, e o método muda inteiro.

    HERANÇA fechada não mata: você perde a hipótese que eleva o trabalho e
    fica com o contraste entre esferas, que é mais magro mas ainda é pesquisa.

    Corpus pequeno se resolve ampliando: as 5.570 prefeituras existem, e o
    leitor de Certificate Transparency que já está neste repositório
    (scripts/ct_direto.py) enumera domínios .gov.br que emitiram certificado.
    O tema que morreu deixou a ferramenta de herança.
""")
    return {
        "coleta": datetime.now(timezone.utc).isoformat(),
        "n": n, "spf": k_spf, "dmarc": k_dmarc, "dkim": k_dkim,
        "reject_efetivo": efetiva, "por_esfera": dict(por_esf),
        "politicas": dict(pol),
        "veredito": {"corpus": corpus_ok, "variacao": varia,
                     "estratos": esferas_ok, "heranca": heranca_ok},
    }


# ------------------------------------------------------------------ autoteste

def autoteste():
    f = []

    casos_spf = [
        (["v=spf1 include:_spf.google.com -all"], (True, "-")),
        (["v=spf1 mx ~all"], (True, "~")),
        (["v=spf1 +all"], (True, "+")),
        (["v=spf1 include:x.com"], (True, "sem_all")),
        (["google-site-verification=abc"], (False, None)),
        ([], (False, None)),
    ]
    for txts, esp in casos_spf:
        got = parse_spf(txts)
        if got != esp:
            f.append(f"parse_spf({txts}) = {got}, esperado {esp}")

    casos_dmarc = [
        (["v=DMARC1; p=reject; rua=mailto:a@b"], (True, "reject", 100)),
        (["v=DMARC1; p=quarantine; pct=20"], (True, "quarantine", 20)),
        (["v=DMARC1; p=none"], (True, "none", 100)),
        (["v=spf1 -all"], (False, None, None)),
    ]
    for txts, esp in casos_dmarc:
        got = parse_dmarc(txts)
        if got != esp:
            f.append(f"parse_dmarc({txts}) = {got}, esperado {esp}")

    casos_esfera = [
        ("gov.br", "federal"), ("saude.gov.br", "federal"),
        ("sp.gov.br", "estadual"), ("pr.gov.br", "estadual"),
        ("curitiba.pr.gov.br", "municipal"),
        ("pbh.gov.br", "municipal"),      # override: não segue o padrão
        ("al.sp.gov.br", "legislativo"),  # override: não é município
        ("stf.jus.br", "judiciario"), ("senado.leg.br", "legislativo"),
    ]
    for d, esp in casos_esfera:
        got = esfera_de(d)
        if got != esp:
            f.append(f"esfera_de({d!r}) = {got!r}, esperado {esp!r}")

    casos_forn = [
        (["aspmx.l.google.com."], "Google"),
        (["x-com.mail.protection.outlook.com."], "Microsoft"),
        (["ns1.celepar.pr.gov.br."], "Celepar (PR)"),
        (["ns1.notgoogle.com.br."], "próprio/outro (notgoogle.com.br)"),
        ([], "desconhecido"),
    ]
    for hosts, esp in casos_forn:
        got = classificar_fornecedor(hosts)
        if got != esp:
            f.append(f"fornecedor({hosts}) = {got!r}, esperado {esp!r}")

    # parser da saída do dig — inclui o caso do TXT longo partido em pedaços,
    # que é onde um SPF de verdade seria perdido se a concatenação falhasse
    casos_dig = [
        ('"v=spf1 -all"\n', ["v=spf1 -all"]),
        ('"v=spf1 include:a.com " "include:b.com -all"\n',
         ["v=spf1 include:a.com include:b.com -all"]),
        ('"a" \n"b"\n', ["a", "b"]),
        ('', []),
        ('\n\n', []),
    ]
    for saida, esp in casos_dig:
        got = parse_txt_dig(saida)
        if got != esp:
            f.append(f"parse_txt_dig({saida!r}) = {got}, esperado {esp}")
    # o SPF longo tem que sobreviver à concatenação
    if parse_spf(parse_txt_dig('"v=spf1 include:a.com " "include:b.com ~all"')) != (True, "~"):
        f.append("SPF partido em dois pedaços não foi remontado")

    # pureza: dois fornecedores perfeitamente homogêneos, cada um com política
    # própria -> pureza por fornecedor 100%, base 50%
    regs = ([{"dmarc": True, "dmarc_politica": "reject", "fornecedor_ns": "A"}] * 4
            + [{"dmarc": True, "dmarc_politica": "none", "fornecedor_ns": "B"}] * 4)
    base, media, linhas, cob = pureza_por_fornecedor(regs, "fornecedor_ns")
    if not (abs(base - 0.5) < 1e-9 and abs(media - 1.0) < 1e-9 and len(linhas) == 2):
        f.append(f"pureza = base {base}, media {media}, {len(linhas)} linhas")

    if f:
        print("AUTOTESTE FALHOU:")
        for x in f:
            print("  -", x)
        sys.exit(1)
    total = (len(casos_spf) + len(casos_dmarc) + len(casos_esfera)
             + len(casos_forn) + len(casos_dig) + 2)
    print(f"AUTOTESTE OK — {total} verificações passaram, sem tocar na rede.")


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Viabilidade do S3: há variação em SPF/DKIM/DMARC no setor público?")
    ap.add_argument("--autoteste", action="store_true", help="valida a lógica, sem rede")
    ap.add_argument("--sem-dkim", action="store_true",
                    help="pula a sondagem de seletores DKIM (13 consultas por domínio)")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--threads", type=int, default=12)
    ap.add_argument("--motor", choices=["auto", "dig", "dnspython"], default="auto",
                    help="motor de DNS. 'auto' usa dnspython se houver, senão dig")
    args = ap.parse_args()

    if args.autoteste:
        autoteste()
        return

    fabrica = escolher_motor(args.motor, args.timeout)

    dominios = FEDERAL + JUDICIARIO + LEGISLATIVO + ESTADUAL + MUNICIPAL
    dominios = list(dict.fromkeys(dominios))

    print("\n" + "=" * 64)
    print("TESTE DE VIABILIDADE — S3: falsificação de e-mail no setor público")
    print(f"Coleta em {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print("=" * 64)
    print(f"\n  Motor de DNS: {fabrica().nome}")
    print(f"  {len(dominios)} domínios. Só consulta de DNS — nenhum e-mail é")
    print("  enviado, nenhuma falsificação é tentada, nenhum servidor é tocado.\n")

    def tarefa(d):
        return coletar(d, fabrica(), not args.sem_dkim)

    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        regs = list(ex.map(tarefa, dominios))

    rel = relatar(regs, args)

    saida = Path("dados")
    saida.mkdir(parents=True, exist_ok=True)
    hoje = datetime.now(timezone.utc).strftime("%Y%m%d")
    (saida / f"s3_dns_{hoje}.json").write_text(
        json.dumps({"relatorio": rel, "registros": regs}, indent=2, ensure_ascii=False))

    csv_path = saida / f"s3_dns_{hoje}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dominio", "esfera", "resolve", "spf", "spf_qualificador",
                    "dmarc", "dmarc_politica", "dmarc_pct", "dkim",
                    "dkim_seletores", "tem_mx", "fornecedor_ns", "fornecedor_mx"])
        for r in regs:
            w.writerow([r["dominio"], r["esfera"], r.get("resolve"), r.get("spf"),
                        r.get("spf_qualificador"), r.get("dmarc"),
                        r.get("dmarc_politica"), r.get("dmarc_pct"), r.get("dkim"),
                        "|".join(r.get("dkim_seletores") or []), r.get("tem_mx"),
                        r.get("fornecedor_ns"), r.get("fornecedor_mx")])
    print(f"  Planilha: {csv_path}")
    print(f"  Bruto: {saida / f's3_dns_{hoje}.json'}\n")


if __name__ == "__main__":
    main()
