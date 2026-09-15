# Protocolo e registro de seleção

## Pergunta e recorte

Como diferentes sistemas de pontuação ou decisão influenciam a priorização de vulnerabilidades de software?

Área: cibersegurança. Recorte provisório para o seminário: gestão de vulnerabilidades. O tema final do TCC continua em definição.

## Procedimento realizado

1. Consultar o histórico do TCC e delimitar a priorização de vulnerabilidades como recorte exploratório. A descoberta pública e a leitura da versão aberta precederam a confirmação na base institucional.
2. Abrir o [Portal CAPES, Acesso CAFe](https://www.periodicos.capes.gov.br/index.php/acesso-cafe.html) e selecionar **IDP - INSTITUTO BRASILEIRO DE ENSINO, DESENVOLVIMENTO E PESQUISA**.
3. Concluir a autenticação institucional e verificar o cabeçalho **“Você está acessando esse portal por: IDP”**. Uma sessão inicial expirou; o fluxo foi reiniciado e o reconhecimento institucional foi confirmado.
4. Abrir **Lista de bases e coleções** e, no registro **ACM Digital Library**, usar o link **Acesse**. Destino institucional: `https://dl-acm-org.ez279.periodicos.capes.gov.br/`.
5. Executar `"vulnerability prioritization" AND (CVSS OR EPSS OR SSVC)` na busca simples da ACM. A interface confirmou a interpretação em **All / todos os campos**, na **ACM Full-Text Collection**.
6. Registrar **44 resultados**, com a primeira página mostrando itens 1–20. A interface exibia **Basic Edition** e os filtros como **Premium feature**. Não foram aplicados filtros Premium nem parâmetros ocultos. O período **2021–2026**, texto completo e pesquisa original foram critérios de triagem manual.
7. Inspecionar entradas da primeira página pelos títulos e trechos de resumo. O artigo escolhido apareceu nessa página, com autoria, CCS 2025, páginas 1904–1918 e DOI.
8. Abrir o artigo pelo resultado e confirmar **research-article**, **Open access**, metadados e resumo. A análise integral usa **arXiv:2508.13644v1**. Não foi feita comparação integral entre essa versão e o PDF final da editora.
9. Justificar a escolha pela comparação de quatro sistemas, amostra de 600 CVEs, método explícito, artefato público e relação com o recorte do TCC.
10. Preservar expressão, contagem, limites da triagem e capturas. Não apresentar a busca como revisão sistemática dos 44 resultados.

## Consulta efetivamente executada

| Campo | Registro |
|---|---|
| Data | 15/09/2026 |
| Acesso | CAPES → CAFe → IDP → Lista de bases e coleções → ACM |
| Coleção | ACM Full-Text Collection |
| Expressão | `"vulnerability prioritization" AND (CVSS OR EPSS OR SSVC)` |
| Campos | All / todos os campos |
| Contagem | **44 resultados** antes de triagem manual |
| Página inspecionada | Primeira página, itens 1–20; sem alegação de leitura integral desses 20 trabalhos |
| Filtros executados na interface | Nenhum; a interface indicava filtros como recurso Premium |
| Triagem manual | 2021–2026, pesquisa original, texto completo, comparação ou priorização de vulnerabilidades |
| Selecionado | Koscinski et al. (2025), DOI `10.1145/3719027.3765210` |
| Versão integral analisada | arXiv v1; metadados e resumo confirmados na ACM |

[Consulta institucional registrada](https://dl-acm-org.ez279.periodicos.capes.gov.br/action/doSearch?AllField=%22vulnerability+prioritization%22+AND+%28CVSS+OR+EPSS+OR+SSVC%29). O link depende do acesso CAFe; a contagem pode variar com a atualização da base.

## Critérios de escolha

| Tipo | Critério |
|---|---|
| Inclusão | Pesquisa original com dados ou análises próprios |
| Inclusão | Relação direta com priorização ou avaliação de vulnerabilidades |
| Inclusão | Texto completo e identificação do veículo |
| Preferência | Procedimento inspecionável e artefato público |
| Preferência | Contribuição compreensível e criticável em até 15 minutos |
| Exclusão para artigo principal | Revisão, tutorial, opinião ou resumo sem estudo empírico completo |

É uma seleção exploratória para o seminário. Não há amostra bibliográfica exaustiva nem fluxo PRISMA.

## Entradas consideradas na triagem exploratória

| Entrada observada na ACM | Relação com a escolha |
|---|---|
| **Conflicting Scores, Confusing Signals** (2025), DOI 10.1145/3719027.3765210 | Selecionado: comparação de quatro sistemas, método e dados inspecionáveis |
| **Exploit Prediction Scoring System (EPSS)** (2021), DOI 10.1145/3436242 | Referência para um dos sistemas; escopo diferente da comparação entre quatro instrumentos |
| **Adaptive Vulnerability Prioritization under Active Exploitation Using the CISA Known Exploited Vulnerabilities Catalog** (2026), DOI 10.1145/3807501.3808240 | Alternativa recente sobre priorização; deve integrar revisão futura antes de alegar originalidade para uma extensão temporal |

A comparação usa títulos e trechos de resumo da listagem. Apenas o artigo escolhido recebeu análise integral. A não seleção das outras entradas não é uma avaliação negativa de sua qualidade.

## Evidências

- [Reconhecimento do acesso CAFe pelo IDP](evidencias/2026-09-15-cafe-idp.png).
- [Busca na ACM e 44 resultados](evidencias/2026-09-15-acm-busca.png).
- [Página oficial do artigo selecionado](evidencias/2026-09-15-acm-artigo.png).

As capturas registram o conteúdo visível em 15/09/2026 e não contêm credenciais.

## Outras verificações e pendências

| Etapa | Resultado |
|---|---|
| Repositório de partida | `ClaudioAMF1/TCC`, main, commit `b1990d78a13fcfb2c2cf4f1e2ddf5a0d450f913c` |
| Novas aulas | Aulas 11, 12 e 13–14 consultadas |
| Anexos específicos | Não localizados nas duas branches consultadas nem na busca por arquivos anexados |
| Artefato dos autores | Repositório e README inspecionados; experimentos não reexecutados |
| CORE | A*, edição ICORE2026, consulta confirmada |
| Qualis | A1 na lista oficial de eventos 2017–2020; corte por h5 também conferido no relatório 2021–2024 |
| h5 atual | Google Scholar bloqueou a consulta automatizada; valor, edição e janela ainda precisam de confirmação |

Antes da entrega, atualizar o slide 6 com o h5 confirmado e conferir os cinco anexos específicos da professora. A busca via CAFe já está concluída e documentada.
