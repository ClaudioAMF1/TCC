# Projeto Capstone I

A entrega do Capstone I é um **projeto de pesquisa** no modelo LaTeX oficial do Capstone do IDP, em cinco seções: introdução, revisão bibliográfica, metodologia (com recursos e cronograma), resultados e discussão (resultados preliminares, resultados esperados e limitações) e conclusão. A coleta principal e os testes das hipóteses ficam para o Capstone II. O estado e o que falta estão em [conformidade.md](conformidade.md).

**Revisão de 25/11/2026 (comentários da simulação de defesa):** título sem pergunta; uma única hipótese (H1: ao menos 10% dos pares aplicativo–SDK sem declaração compatível, decidida pela proporção observada em todos os aplicativos oficiais, com IC95% como medida de precisão), baseada em Andow et al. (2020), Samarasinghe et al. (2022), Carlsson et al. (2022) e Kollnig et al. (2022); a comparação de dados sensíveis (antiga H2) saiu do projeto. O texto foi reescrito em prosa, com seis quadros, e os procedimentos seguem a ordem das seis etapas do método. A análise dinâmica usa o emulador do Android Studio com o mitmproxy, sem celular Android. A revisão sistemática passou à versão 2.1 do protocolo, com termo do tema obrigatório no título, período de 2018 a 2026 e sem a questão sobre detecção de bibliotecas (396 registros, 312 triados, 148 à leitura completa, 31 propostas de inclusão). Os slides atuais são [apresentacao/apresentacao-defesa-final.pptx](apresentacao/apresentacao-defesa-final.pptx), com o [roteiro](apresentacao/roteiro-defesa-final.md).

**Modelo do Capstone (26/11/2026):** o texto passou para o modelo oficial ([lucasmauricio/capstone-latex-template](https://github.com/lucasmauricio/capstone-latex-template)), com XeLaTeX, fonte Arial e citações numéricas no padrão IEEE, que a classe do modelo define. Os resultados preparatórios (seleção dos aplicativos, cobertura do AndroZoo, piloto dos detectores, declarações e andamento da revisão) saíram da metodologia e foram para a Seção 4, Resultados e discussão. A pasta `configs/` do modelo não foi alterada; os ajustes estão em [latex/README.md](latex/README.md).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [latex/main.pdf](latex/main.pdf) | O projeto, no modelo do Capstone do IDP |
| [latex/main.tex](latex/main.tex) | Dados do trabalho e ordem das seções; o texto de cada seção está em [latex/partes/](latex/partes/) |
| [latex/README.md](latex/README.md) | Como compilar e o que foi ajustado no modelo |
| [latex/referencias.bib](latex/referencias.bib) | Referências |
| [apresentacao/simulacao-defesa-rascunho.pptx](apresentacao/simulacao-defesa-rascunho.pptx) | 14 slides no modelo do IDP, com a fala de cada slide nas notas |
| [apresentacao/roteiro-simulacao.md](apresentacao/roteiro-simulacao.md) | Fala de cada slide, tempos e perguntas prováveis |
| [revisao/protocolo-revisao-sistematica.md](revisao/protocolo-revisao-sistematica.md) | Protocolo e registros da revisão sistemática |
| [revisao/sintese-F2-propostas.md](revisao/sintese-F2-propostas.md) | As propostas de inclusão por questão de pesquisa (lista anterior à versão 2.0, com 71; a síntese atual, na Seção 2.2.4, traz as 31 propostas da versão 2.1 do protocolo) |
| [revisao/buscas-passo-a-passo.md](revisao/buscas-passo-a-passo.md) | Como as buscas e a triagem foram feitas e como seguir |
| [metodologia/criterios-lgpd.md](metodologia/criterios-lgpd.md) | Matriz de dez critérios documentais da LGPD |
| [piloto-passo-a-passo.md](piloto-passo-a-passo.md), [coleta-passo-a-passo.md](coleta-passo-a-passo.md) | Como rodar o piloto e a coleta direta |

## Compilação

No Overleaf: compacte a pasta `latex/` (sem o `main.pdf`), use Novo projeto > Enviar projeto e escolha Menu > Compilador > **XeLaTeX**. O modelo usa a fonte Arial e não compila com pdfLaTeX.

No computador: `make` dentro de `latex/` (XeLaTeX e BibTeX), com o TeX Live e a fonte Arial instalados.

Depois de qualquer mudança, gere o PDF de novo e substitua `latex/main.pdf`.
