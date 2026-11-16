# TCC — Projeto Capstone I (IDP, 2026.2)

Repositório do Trabalho de Conclusão de Curso em Ciência da Computação no IDP.

**Tema:** *Quem mais está dentro do aplicativo? Rastreamento por terceiros e soberania de dados em aplicativos móveis governamentais brasileiros.* Orientador: Prof. Eduardo Arthur Izycki. O texto é em português.

**Estado em 15/11/2026:** projeto de pesquisa escrito no modelo do IDP, com as 71 propostas de inclusão da revisão sistemática resumidas no referencial, e slides da simulação prontos. O que falta até 03/12 está em [`tcc/conformidade.md`](tcc/conformidade.md).

## Onde está cada coisa

| Pasta | Conteúdo |
|---|---|
| [`tcc/`](tcc/README.md) | **O projeto** (LaTeX e PDF), a apresentação, o protocolo da revisão, os critérios da LGPD e a pauta do orientador |
| `dados/` | Corpus, controle, fichas e planilhas da revisão sistemática. APKs, PDFs de artigos e listas grandes ficam fora (ver `.gitignore`) |
| `scripts/` | Coleta, piloto, revisão e testes de viabilidade |
| `disciplina/` | Plano de ensino, regulamento, aulas, listas, normas ABNT e modelos do IDP |
| `seminario/` | Seminário de análise de artigo (AV1), concluído |
| `temas/`, `desenhos/`, `descartados/` | Histórico da escolha do tema: catálogo, testes de viabilidade e propostas |

## O trabalho, etapa por etapa

| Etapa | Como foi feita | Resultado |
|---|---|---|
| Escolha do tema | Seis temas testados com scripts antes do desenho | N3 (este tema) escolhido; ver `temas/` e `descartados/` |
| Corpus | `scripts/teste_viabilidade_n3.py`: 21 termos na Google Play e catálogo de cada órgão (setembro); `scripts/fichas_publicadores.py`: nome jurídico do publicador | 396 candidatos; 376 oficiais na classificação preliminar (85 federais, 199 estaduais, 92 municipais); 100 com dado sensível |
| Controle comercial | `scripts/teste_viabilidade_n3_robusto.py` e `scripts/ampliar_controle.py` (04/11) | 190 → 252 aplicativos |
| Pacotes | `scripts/piloto_androzoo.py` (AndroZoo, acesso concedido em 17/09) | Acervo cobre 23,2% do governo e 84,2% do controle |
| Piloto dos detectores | 20 APKs; A = Exodus por código, B = Exodus por domínio, C = Disconnect | 75%, 95% e 80%; κ 0,52, ou 0,69 sem os falsos positivos de B |
| Revisão sistemática | `scripts/revisao_triagem.py`: 17 buscas (Scopus, IEEE Xplore, BDTD, SBC OpenLib), deduplicação, triagem | 1.531 → 1.249 → 357 para leitura completa; 79 propostas (71 I, 8 E) até 13/11 |
| Texto e apresentação | LaTeX (abnTeX2) no modelo do IDP; 14 slides no modelo do IDP | `tcc/latex/main.pdf`; `tcc/apresentacao/` |

As classificações registradas, de aplicativos e de artigos, serão conferidas pelo autor no início do Capstone II, junto com a leitura dos registros da revisão ainda em aberto.

## Scripts

Todos leem fontes públicas. Nenhum acessa área autenticada de terceiros nem explora falha.

| Script | O que faz |
|---|---|
| `teste_viabilidade_n3.py` | Enumera aplicativos governamentais na Google Play por termo e por catálogo de publicador |
| `teste_viabilidade_n3_robusto.py` | Verifica, antes de baixar APK, se cada hipótese tem instrumento: pareamento, políticas acessíveis, células e potência |
| `fichas_publicadores.py` | Ficha de cada app e nome jurídico do publicador, evidência para a classificação |
| `ampliar_controle.py` | Procura comerciais nas células categoria × faixa em que o controle falta |
| `piloto_androzoo.py` | Piloto da H4: cobertura do AndroZoo, sorteio de 20 apps, três detectores, κ e τ. Passo a passo em `tcc/piloto-passo-a-passo.md` |
| `coleta_google_play.py` | Baixa APKs direto da Google Play e registra SHA-256 e versão. Passo a passo em `tcc/coleta-passo-a-passo.md` |
| `revisao_triagem.py` | Revisão sistemática: junta as exportações, tira duplicatas, confere o conjunto de controle, compara a conferência cega (`concordancia`) e dá os números do PRISMA (`prisma`). Passo a passo em `tcc/revisao/buscas-passo-a-passo.md` |
| `segundo_avaliador.py` | Compara classificações de avaliadores diferentes (κ de Cohen e de Fleiss) |
| `teste_viabilidade_n1.py`, `ct_direto.py`, `teste_viabilidade_malware.py`, `teste_viabilidade_s3.py` | Testes de viabilidade dos temas descartados |

### Como rodar

> O projeto fica em `~/Projetos/TCC`, fora do iCloud: na pasta Documentos sincronizada, o macOS tira arquivos do disco e o git falha com `mmap failed`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 scripts/revisao_triagem.py prisma          # números do fluxograma PRISMA
python3 scripts/revisao_triagem.py concordancia dados/revisao/reteste_F1_20261116.xlsx
python3 scripts/piloto_androzoo.py autoteste        # sem rede
```

Para compilar o projeto, veja [`tcc/README.md`](tcc/README.md).

## Regras do repositório

- O repositório é **privado**. As normas ABNT em `disciplina/normas/` são exemplares licenciados com dados de quem comprou, e `dados/revisao/` traz resumos que as bases não permitem redistribuir: os dois saem antes de qualquer publicação.
- Chaves e tokens (AndroZoo, Google Play, Shodan, MalwareBazaar) ficam só em variáveis de ambiente, nunca em arquivo versionado.
- APKs e PDFs de artigos (`dados/revisao/pdf/`) nunca são versionados nem redistribuídos.
- Dados pessoais e tráfego identificável não entram no repositório.
