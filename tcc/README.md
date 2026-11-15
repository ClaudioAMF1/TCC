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

Use **XeLaTeX**, com `main.tex`, `referencias.bib` e `logo-idp.png` na mesma pasta.

- **Overleaf:** envie os três arquivos e escolha Menu > Compiler > XeLaTeX.
- **No computador:** `xelatex main.tex`, `bibtex main`, `xelatex main.tex`, `xelatex main.tex`.

O texto usa a fonte Times New Roman, como pede o modelo do IDP. Se o ambiente não a tiver, troque a linha `\setmainfont{Times New Roman}` por `\setmainfont{TeX Gyre Termes}`, uma Times equivalente que vem com o TeX Live. O fluxograma PRISMA é desenhado com TikZ, que também vem com o TeX Live.

Depois de qualquer mudança, gere o PDF de novo e substitua `latex/main.pdf`.
