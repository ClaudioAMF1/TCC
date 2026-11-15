# Projeto Capstone I

A entrega do Capstone I é um **projeto de pesquisa**: introdução, referencial teórico e procedimentos metodológicos, com recursos e cronogramas. A coleta principal e os testes das hipóteses ficam para o Capstone II. O estado e o que falta estão em [conformidade.md](conformidade.md).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [latex/main.pdf](latex/main.pdf) | O projeto, no modelo do IDP |
| [latex/main.tex](latex/main.tex) | Fonte do texto |
| [latex/referencias.bib](latex/referencias.bib) | Referências |
| [apresentacao/simulacao-defesa-rascunho.pptx](apresentacao/simulacao-defesa-rascunho.pptx) | 14 slides no modelo do IDP, com a fala de cada slide nas notas |
| [apresentacao/roteiro-simulacao.md](apresentacao/roteiro-simulacao.md) | Fala de cada slide, tempos e perguntas prováveis |
| [revisao/protocolo-revisao-sistematica.md](revisao/protocolo-revisao-sistematica.md) | Protocolo e registros da revisão sistemática |
| [revisao/sintese-F2-propostas.md](revisao/sintese-F2-propostas.md) | As 71 propostas de inclusão por questão de pesquisa, base da síntese da Seção 2 |
| [revisao/buscas-passo-a-passo.md](revisao/buscas-passo-a-passo.md) | Como as buscas e a triagem foram feitas e como seguir |
| [metodologia/criterios-lgpd.md](metodologia/criterios-lgpd.md) | Matriz de dez critérios documentais da LGPD |
| [orientacao/pauta-proximo-encontro.md](orientacao/pauta-proximo-encontro.md) | Decisões a tomar com o orientador |
| [piloto-passo-a-passo.md](piloto-passo-a-passo.md), [coleta-passo-a-passo.md](coleta-passo-a-passo.md) | Como rodar o piloto e a coleta direta |

## Compilação

No Overleaf, envie `main.tex`, `referencias.bib` e `logo-idp.png` para o mesmo projeto e clique em Recompile. O arquivo funciona com qualquer compilador do Overleaf:

- **XeLaTeX (recomendado):** Menu > Compiler > XeLaTeX. Usa Times New Roman se o ambiente tiver essa fonte e, se não tiver, a TeX Gyre Termes, uma Times que vem com o TeX Live.
- **pdfLaTeX:** usa a Times do próprio LaTeX.

No computador: `xelatex main.tex`, `bibtex main`, `xelatex main.tex`, `xelatex main.tex`.

Depois de qualquer mudança, gere o PDF de novo e substitua `latex/main.pdf`.
