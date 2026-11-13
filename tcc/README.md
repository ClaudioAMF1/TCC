# Projeto Capstone I

Versão revista em **13/11/2026**. A entrega é um projeto de pesquisa: introdução, referencial teórico e procedimentos metodológicos, com recursos e cronogramas. Os resultados descritos são preparatórios e do piloto. A coleta principal e os testes das hipóteses permanecem previstos para o Capstone II.

## Arquivos principais

| Arquivo | Conteúdo |
|---|---|
| [latex/main.pdf](latex/main.pdf) | Projeto diagramado no modelo do IDP |
| [latex/main.tex](latex/main.tex) | Fonte principal do texto |
| [latex/referencias.bib](latex/referencias.bib) | Referências bibliográficas, editadas neste arquivo |
| [tcc1-projeto-de-pesquisa.md](tcc1-projeto-de-pesquisa.md) | Espelho de leitura do texto, gerado da fonte LaTeX |
| [apresentacao/simulacao-defesa-rascunho.pptx](apresentacao/simulacao-defesa-rascunho.pptx) | 14 slides editáveis no modelo do IDP, com notas |
| [apresentacao/roteiro-simulacao.md](apresentacao/roteiro-simulacao.md) | Roteiro correspondente aos slides |
| [metodologia/criterios-lgpd.md](metodologia/criterios-lgpd.md) | Dez critérios documentais da LGPD, versão 0.1 para orientação |
| [revisao/protocolo-revisao-sistematica.md](revisao/protocolo-revisao-sistematica.md) | Protocolo e registros atualizados, versão 1.4 |
| [../dados/revisao/reteste_F1_20261116.xlsx](../dados/revisao/reteste_F1_20261116.xlsx) | Reteste cego de 125 registros, sem respostas anteriores |
| [orientacao/pauta-proximo-encontro.md](orientacao/pauta-proximo-encontro.md) | Perguntas e espaço para registrar decisões do orientador |
| [conformidade.md](conformidade.md) | Exigências atendidas e pendências verificáveis |

## Compilação no Overleaf ou no computador

Use **XeLaTeX**, com `main.tex`, `referencias.bib` e `logo-idp.png` na mesma pasta. São necessários abnTeX2, os pacotes indicados no preâmbulo e a fonte **Times New Roman** instalada ou disponível no projeto com licença de uso. A fonte não é distribuída neste repositório. Se o ambiente não a encontrar, disponibilize a fonte licenciada; não substitua silenciosamente antes da entrega.

No Overleaf, envie os três arquivos e selecione XeLaTeX. Em uma instalação local configurada: `xelatex main.tex`, `bibtex main`, `xelatex main.tex`, `xelatex main.tex`. As referências não ficam mais embutidas no `main.tex`: edite `referencias.bib`. Após qualquer mudança, regenere o PDF e o espelho Markdown.

## Estado da revisão

As buscas produziram 1.531 registros; 282 duplicatas foram removidas. Dos 1.249 restantes, a F1 registra 886 E, 6 R e **357 candidatos à F2** (214 I e 143 T). A F2 consultada em 13/11 está sem decisões preenchidas. Não há número final de estudos incluídos. A lista de referências do documento também contém leis, métodos e ferramentas; ela não equivale à amostra final da revisão.

O reteste está preparado, não realizado. Deve ocorrer no mínimo sete dias depois da primeira avaliação pessoal. O κ só será calculado com as duas avaliações identificadas. A validação pessoal das classificações e a leitura completa continuam pendentes.

## Decisões a confirmar

Confirmar com o orientador o escopo da revisão, detector principal, regras de análise das políticas, recursos e plano estatístico antes da coleta principal. Confirmar a data da simulação e ensaiar para o limite de 15 minutos. Completar titulação, terceiro membro e identificadores da banca; confirmar a aplicação da regra de idioma; entregar as fichas de orientação e o termo de aceite. A entrega no Canvas continua prevista para 03/12 e depende do autor.
