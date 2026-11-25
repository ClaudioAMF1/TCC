# Projeto Capstone I

A entrega do Capstone I é um **projeto de pesquisa**: introdução, referencial teórico e procedimentos metodológicos, com recursos e cronograma. A coleta principal e os testes das hipóteses ficam para o Capstone II. O estado e o que falta estão em [conformidade.md](conformidade.md).

**Revisão de 25/11/2026 (comentários da simulação de defesa):** título sem pergunta; uma única hipótese (H1: ao menos 10% dos pares aplicativo–SDK sem declaração compatível), baseada em Andow et al. (2020), Samarasinghe et al. (2022), Carlsson et al. (2022) e Kollnig et al. (2022); a comparação de dados sensíveis (antiga H2) saiu do projeto. O texto foi reescrito em prosa, com seis quadros, e os procedimentos seguem a ordem das seis etapas do método. A análise dinâmica usa o emulador do Android Studio com o mitmproxy, sem celular Android. A revisão sistemática passou à versão 2.0 do protocolo, com termo do tema obrigatório no título (552 registros, 413 triados, 210 à leitura completa, 55 propostas de inclusão). Os slides atuais são [apresentacao/apresentacao-defesa-final.pptx](apresentacao/apresentacao-defesa-final.pptx), com o [roteiro](apresentacao/roteiro-defesa-final.md).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [latex/main.pdf](latex/main.pdf) | O projeto, no modelo do IDP |
| [latex/main.docx](latex/main.docx) | O mesmo projeto em Word, gerado a partir do `main.tex`. Mudanças feitas no Word não voltam para o LaTeX |
| [latex/main.tex](latex/main.tex) | Fonte do texto |
| [latex/referencias.bib](latex/referencias.bib) | Referências |
| [apresentacao/simulacao-defesa-rascunho.pptx](apresentacao/simulacao-defesa-rascunho.pptx) | 14 slides no modelo do IDP, com a fala de cada slide nas notas |
| [apresentacao/roteiro-simulacao.md](apresentacao/roteiro-simulacao.md) | Fala de cada slide, tempos e perguntas prováveis |
| [revisao/protocolo-revisao-sistematica.md](revisao/protocolo-revisao-sistematica.md) | Protocolo e registros da revisão sistemática |
| [revisao/sintese-F2-propostas.md](revisao/sintese-F2-propostas.md) | As propostas de inclusão por questão de pesquisa (lista anterior à versão 2.0, com 71; a síntese atual da Seção 2.7 usa as 55 que continuam após a restrição pelo título) |
| [revisao/buscas-passo-a-passo.md](revisao/buscas-passo-a-passo.md) | Como as buscas e a triagem foram feitas e como seguir |
| [metodologia/criterios-lgpd.md](metodologia/criterios-lgpd.md) | Matriz de dez critérios documentais da LGPD |
| [piloto-passo-a-passo.md](piloto-passo-a-passo.md), [coleta-passo-a-passo.md](coleta-passo-a-passo.md) | Como rodar o piloto e a coleta direta |

## Compilação

No Overleaf, envie `main.tex`, `referencias.bib` e `logo-idp.png` para o mesmo projeto e clique em Recompile. O arquivo funciona com qualquer compilador do Overleaf:

- **XeLaTeX (recomendado):** Menu > Compiler > XeLaTeX. Usa Times New Roman se o ambiente tiver essa fonte e, se não tiver, a TeX Gyre Termes, uma Times que vem com o TeX Live.
- **pdfLaTeX:** usa a Times do próprio LaTeX.

No computador: `xelatex main.tex`, `bibtex main`, `xelatex main.tex`, `xelatex main.tex`.

Depois de qualquer mudança, gere o PDF de novo e substitua `latex/main.pdf`. O `main.docx` também precisa ser gerado de novo para acompanhar o texto.
