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
| `main.tex` | dados do trabalho (autor, título, tipo de trabalho, orientador, banca, palavras-chave) e ordem das seções |
| `partes/resumo.tex`, `partes/abstract.tex` | resumo e abstract (nomes fixos exigidos pelo modelo) |
| `partes/introducao.tex` | 1 Introdução: problema, justificativa, objetivos, hipótese e estrutura do trabalho |
| `partes/revisao-bibliografica.tex` | 2 Revisão bibliográfica: fundamentação teórica e trabalhos correlatos |
| `partes/metodologia.tex` | 3 Metodologia: etapas, revisão sistemática, ética, recursos e cronograma |
| `partes/resultados-e-discussao.tex` | 4 Resultados e discussão: resultados preliminares, esperados e limitações |
| `partes/conclusao.tex` | 5 Conclusão |
| `referencias.bib` | referências, no estilo IEEE definido pela classe do modelo |
| `pacotes/pacotes.tex` | pacotes extras e ajustes deste trabalho |
| `latexmkrc` | faz a compilação usar o XeLaTeX, que o modelo exige |
| `configs/` | arquivos do modelo; a classe `idp-model.cls` foi traduzida para o português |

## Classe traduzida (`configs/idp-model.cls`)

- O idioma principal é o português (`\RequirePackage[english,portuguese]{babel}`), o que ativa os
  títulos em português que a própria classe prevê: Sumário, Lista de Figuras e Lista de Tabelas.
  O inglês continua carregado para o abstract.
- Os textos que a classe escrevia em inglês estão em português: folha de rosto e folha de
  aprovação ("Orientador", "Aprovado em", "Banca examinadora"), referências, agradecimentos,
  dedicatória, apêndices e anexos. O texto de apresentação diz "\<tipo de trabalho\> como requisito
  parcial para a obtenção do título de bacharel em \<curso\> no Instituto Brasileiro de Ensino,
  Desenvolvimento e Pesquisa (IDP)"; o tipo de trabalho é definido no `main.tex` com
  `\tipotrabalho{...}` (padrão: "Trabalho de Conclusão de Curso apresentado").
- O abstract e as keywords continuam em inglês, como pede o modelo, e vêm antes do resumo e das
  palavras-chave em português.

## Outros ajustes, em `pacotes/pacotes.tex`

- No sumário, a classe deixava o número da subsubseção colado ao título; a definição de
  `\subsubsecao` é repetida com o espaço corrigido.
- Na classe, o título de subseção e de subsubseção podia ficar sozinho no pé da página; as
  definições de `\subsecao` e `\subsubsecao` são repetidas com `\Needspace`
  (pacote `needspace`), que leva o título para a página seguinte quando não cabe texto
  depois dele.
- Tabelas grandes ficam no alto de uma página com texto, e não sozinhas e centralizadas numa
  página só de tabelas (`\floatpagefraction` e `\@fptop`).
- A classe põe a capa, a folha de rosto, a folha de aprovação e os títulos de subseção em
  caixa alta. Para "SDKs" não virar "SDKS", o título usa o comando `\SDKs`.
- Nas referências, o pacote `xurl` deixa os endereços longos quebrarem em qualquer ponto, e a
  hifenização é a do inglês, língua de quase todas elas; as referências em português têm o
  campo `language = {portuguese}` no `referencias.bib`.
