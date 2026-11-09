#!/usr/bin/env python3
"""
Ficha atual de cada app do corpus e nome jurídico de quem publica.

POR QUE ESTE SCRIPT EXISTE
--------------------------
A validação de 04/11 mostrou que o nome do desenvolvedor na loja não basta
para saber se o publicador é órgão público: empresas privadas publicam com nome
de serviço público ("Prefeitura Municipal", "Prefeitura Virtual"). A evidência
usada na conferência foi o nome jurídico que a Google Play mostra em "Sobre o
desenvolvedor". Este script coleta, para todos os apps do corpus, a ficha
atual (descrição, e-mail, site, política) e esse nome jurídico, para a
classificação manual dos 396 (oficialidade, esfera e dado sensível).

USO
---
    python3 scripts/fichas_publicadores.py dados/n3_corpus_20260917.csv
    python3 scripts/fichas_publicadores.py autoteste

Grava dados/n3_fichas_AAAAMMDD.json. Só lê páginas públicas da loja, com quatro
requisições em paralelo.
"""

import csv
import html
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMPOS = ("title", "developer", "developerId", "developerEmail",
          "developerWebsite", "privacyPolicy", "genre", "installs", "summary",
          "description", "contentRating", "containsAds", "updated", "version")


def extrai_publicador(pagina: str):
    """Nome jurídico e endereço do bloco "Sobre o desenvolvedor"."""
    k = pagina.find("Sobre o desenvolvedor")
    if k < 0:
        return "", ""
    pedaco = pagina[k + len("Sobre o desenvolvedor"): k + 3000]
    partes = [html.unescape(p).strip() for p in re.split(r"<[^>]+>", pedaco)]
    partes = [p for p in partes if p and p != "expand_more"]
    nome = partes[0] if partes else ""
    endereco = ""
    for p in partes[1:6]:
        if "@" in p or p.startswith("+") or p.startswith("Mais de"):
            continue
        if re.search(r"\d", p) or "\n" in p:
            endereco = " ".join(p.split())
            break
    return nome, endereco


def ficha(app_id: str):
    from google_play_scraper import app
    from google_play_scraper.exceptions import NotFoundError
    for tentativa in range(3):
        try:
            r = app(app_id, lang="pt", country="br")
            return {k: r.get(k) for k in CAMPOS}
        except NotFoundError:
            return {"erro": "indisponivel"}
        except Exception as e:  # rede instável: tenta de novo
            ultimo = f"{type(e).__name__}: {e}"[:200]
            time.sleep(2 + 3 * tentativa)
    return {"erro": ultimo}


def publicador(app_id: str):
    url = (f"https://play.google.com/store/apps/details?id={app_id}"
           "&hl=pt_BR&gl=BR")
    for tentativa in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            pagina = urllib.request.urlopen(req, timeout=40).read().decode(
                "utf-8", "replace")
            return extrai_publicador(pagina)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "", "indisponivel"
            time.sleep(3 + 3 * tentativa)
        except Exception:
            time.sleep(3 + 3 * tentativa)
    return "", "erro"


def coleta(corpus: Path, saida: Path):
    texto = corpus.read_bytes().decode("utf-8-sig")
    ids = [r["appId"] for r in csv.DictReader(io.StringIO(texto, newline=""))]

    def um(i):
        f = ficha(i)
        f["razao_social"], f["endereco_dev"] = publicador(i)
        return i, f

    with ThreadPoolExecutor(4) as ex:
        fichas = dict(ex.map(um, ids))
    saida.write_text(json.dumps({"data": date.today().isoformat(),
                                 "fichas": fichas}, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    fora = [i for i, f in fichas.items() if f.get("erro")]
    sem = [i for i, f in fichas.items() if not f.get("razao_social")]
    print(f"{len(fichas)} apps; {len(fora)} fora da loja ou com erro; "
          f"{len(sem)} sem nome jurídico")
    print(f"Gravado: {saida}")


def autoteste():
    pagina = ('<div>Sobre o desenvolvedor</div><div class="a">BYTES TECNOLOGIA '
              'E DESENVOLVIMENTO LTDA</div><div>code@govdigital.app</div>'
              '<div>Rua X 585\nCENTRO\nRIO DO SUL - SC</div><div>+55 47 1</div>')
    nome, end = extrai_publicador(pagina)
    ok = (nome == "BYTES TECNOLOGIA E DESENVOLVIMENTO LTDA"
          and end == "Rua X 585 CENTRO RIO DO SUL - SC")
    ok = ok and extrai_publicador("<html>sem bloco</html>") == ("", "")
    print("AUTOTESTE OK" if ok else f"AUTOTESTE COM FALHA: {nome!r} {end!r}")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "autoteste":
        sys.exit(autoteste())
    coleta(Path(sys.argv[1]),
           RAIZ / "dados" / f"n3_fichas_{date.today():%Y%m%d}.json")
