# Texto do TCC I no modelo LaTeX do Capstone do IDP

O texto segue o modelo oficial do Projeto Capstone dos cursos de tecnologia do IDP
([lucasmauricio/capstone-latex-template](https://github.com/lucasmauricio/capstone-latex-template),
versão de 1º/7/2026; a classe é a mesma do [modelo no Overleaf](https://pt.overleaf.com/read/srgxtbvdbdng#effe2a)).

## Como compilar

- **No Overleaf:** criar um projeto a partir do zip com estes arquivos e escolher o compilador
  **XeLaTeX** em File > Settings > Compiler (ou no ícone de engrenagem, no canto inferior
  esquerdo). O modelo usa a fonte Arial e não compila com pdfLaTeX; por garantia, o arquivo
  `latexmkrc` faz o Overleaf chamar o XeLaTeX mesmo que o compilador escolhido seja o pdfLaTeX.
- **No computador:** `make` (XeLaTeX e BibTeX), com o TeX Live e a fonte Arial instalados.

## Organização

| Arquivo | Conteúdo |
|---|---|
| `main.tex` | dados do trabalho (autor, título, orientador, banca, palavras-chave) e ordem das seções |
| `partes/resumo.tex`, `partes/abstract.tex` | resumo e abstract (nomes fixos exigidos pelo modelo) |
| `partes/introducao.tex` | 1 Introdução: problema, justificativa, objetivos, hipótese e estrutura do trabalho |
| `partes/revisao-bibliografica.tex` | 2 Revisão bibliográfica: fundamentação teórica e trabalhos correlatos |
| `partes/metodologia.tex` | 3 Metodologia: etapas, revisão sistemática, ética, recursos e cronograma |
| `partes/resultados-e-discussao.tex` | 4 Resultados e discussão: resultados preliminares, esperados e limitações |
| `partes/conclusao.tex` | 5 Conclusão |
| `referencias.bib` | referências, no estilo IEEE definido pela classe do modelo |
| `pacotes/pacotes.tex` | pacotes extras e ajustes deste trabalho |
| `pacotes/rotulos-em-portugues.tex` | textos fixos da classe (folha de rosto, folha de aprovação, referências) em português |
| `latexmkrc` | faz a compilação usar o XeLaTeX, que o modelo exige |
| `configs/` | arquivos do modelo, **sem nenhuma alteração** |

## O que foi ajustado sem mexer em `configs/`

- O idioma principal é o português (linha `\PassOptionsToPackage{main=portuguese}{babel}` no
  início do `main.tex`), o que ativa os títulos em português que a própria classe prevê:
  Sumário, Lista de Figuras e Lista de Tabelas.
- Os textos que a classe escreve em inglês (folha de rosto, folha de aprovação e referências)
  estão em português em `pacotes/rotulos-em-portugues.tex`. Para voltar aos textos originais
  do modelo, basta comentar a linha `\input{pacotes/rotulos-em-portugues}` em `pacotes/pacotes.tex`.
- No sumário, a classe deixava o número da subsubseção colado ao título; `pacotes/pacotes.tex`
  repete a definição de `\subsubsecao` com o espaço corrigido.
