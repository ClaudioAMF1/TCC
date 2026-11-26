# TCC — Projeto Capstone I (IDP, 2026.2)

**Rastreamento por terceiros em aplicativos móveis governamentais brasileiros: SDKs embarcados e transparência das declarações de privacidade.** Ciência da Computação, IDP. Orientador: Prof. Eduardo Arthur Izycki.

O projeto de pesquisa (Capstone I) está em [`tcc/`](tcc/README.md). O que falta até a entrega de 03/12 está em [`tcc/conformidade.md`](tcc/conformidade.md).

## Pastas

| Pasta | Conteúdo |
|---|---|
| `tcc/` | O projeto (LaTeX e PDF), a apresentação, o protocolo da revisão sistemática e os critérios da LGPD |
| `dados/` | Corpus de aplicativos, grupo de controle e planilhas da revisão sistemática |
| `scripts/` | Programas de coleta, piloto e revisão |
| `disciplina/` | Plano de ensino, regulamento do TCC e modelos do IDP (monografia e slides) |

## Dados

| Arquivo | Conteúdo |
|---|---|
| `dados/n3_corpus_20260917.csv` | Os 396 candidatos, com a classificação preliminar: 376 oficiais, esfera e tratamento de dado sensível |
| `dados/n3_relatorio_20260917.json` | Metadados da coleta e controle original (190 aplicativos) |
| `dados/controle_ampliado_20261104.json` | Controle ampliado (252 aplicativos) e cobertura por categoria e faixa |
| `dados/revisao/` | Exportações das buscas, triagem, leitura completa (F2), amostra da conferência cega e as restrições das versões 2.0 e 2.1 do protocolo (312 registros triados na 2.1) |

## Scripts

| Script | O que faz |
|---|---|
| `teste_viabilidade_n3.py` | Busca aplicativos governamentais na Google Play por termo e pelo catálogo de cada órgão |
| `teste_viabilidade_n3_robusto.py` | Coleta a ficha de cada app e verifica, antes de baixar APKs, se cada hipótese tem instrumento |
| `fichas_publicadores.py` | Obtém o nome jurídico do publicador, evidência para a classificação |
| `ampliar_controle.py` | Procura aplicativos comerciais nas células de categoria e faixa sem controle |
| `piloto_androzoo.py` | Piloto: cobertura do AndroZoo, download de 20 APKs, três detectores e concordância. Passo a passo em `tcc/piloto-passo-a-passo.md` |
| `coleta_google_play.py` | Baixa APKs da Google Play e registra SHA-256 e versão. Passo a passo em `tcc/coleta-passo-a-passo.md` |
| `revisao_triagem.py` | Revisão sistemática: junta as buscas, tira duplicatas, compara a conferência cega (`concordancia`) e dá os números do PRISMA (`prisma`). Passo a passo em `tcc/revisao/buscas-passo-a-passo.md` |

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Regras

- O repositório deve ficar **privado**: `dados/revisao/` traz resumos de artigos que as bases não permitem redistribuir.
- Chaves e tokens (AndroZoo, Google Play) ficam só em variáveis de ambiente, nunca em arquivo.
- Não se versionam APKs, PDFs de artigos nem dados pessoais. As fichas dos publicadores (`n3_fichas_*.json`) ficam fora do repositório porque trazem contatos; o script `fichas_publicadores.py` gera de novo.
