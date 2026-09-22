# Plano até a apresentação

**Atualizado:** 22/09/2026 · **Apresentação:** 29/09 ou 01/10, ordem alfabética
**Sobrenome:** Meireles → provavelmente **29/09**. Prepare-se para a primeira data.

---

## Onde a atividade está

| Item do enunciado | Estado |
|---|---|
| **1** — passo a passo da seleção | ✅ funil 131 → 70 → 39 → 5 → 1, com um print por degrau |
| **1** — relevância | ✅ qualitativa, e quantitativa com 42 · 52 · 99 citações |
| **2** — h5 · Qualis · CORE | ✅ 90 · A1 · A\*, cada um com print e data |
| **3** — análise da estrutura | ✅ slides 5 a 22, discussão no 19 |
| Apresentação | ✅ **versão final** em `apresentacao/` |
| Teste no Google Slides | ⬜ **falta** |
| Ensaio | ⬜ **falta** |

**O conteúdo está fechado.** O que falta depende só de você: ver o deck no aplicativo
em que vai apresentar e ensaiar.

---

## Como a versão final foi feita

A revisão de 22/09 encontrou nove problemas no deck. Todos foram corrigidos, e o
`apresentacao/relatorio-de-revisao.pdf` registra cada um com o texto de antes e de
depois.

| Slide | Problema | Como ficou |
|---|---|---|
| **4** | Qualis "não determinável" | **A1**, pelo Qualis Eventos da Computação 2017–2020, p. 9 |
| **2** | Funil de 3 degraus, com o 5 atribuído às palavras-chave | 4 degraus, **131 → 70 → 39 → 5**, com o termo `consent` como último corte |
| **8** | *"Do these ... can be legally justified"* | *"Can these ... be legally justified"*, que é o texto da versão da ACM |
| **24** | WhisperTest entre os finalistas | o artigo sobre *cookie banners* (LNCS, 2025) |
| **24** | SOUPS como "CORE B" | "Veículo ICORE A (2026)", mesma edição usada para a CCS |
| 3 | relevância sem citações | 42 · 52 · 99, com data |
| 4 e 25 | h5 "sem nova confirmação" | posição 5 na subárea, consulta em 17/09/2026 |
| 25 | fontes sem o Qualis Eventos | relatório da CAPES incluído |
| 1 a 25 | texto abaixo de 12 pt, slide 1 sem número | tudo com 12 pt ou mais, numeração 01 a 23 |

**Conferido depois, direto no arquivo:** os slides 5 a 23 têm o mesmo texto do deck
anterior, exceto a pergunta do slide 8. Todos os números do artigo batem com o PDF.
As 17 citações em inglês estão no PDF da ACM, palavra por palavra. As páginas e
figuras citadas estão nas páginas indicadas. Nenhum travessão no meio de frase.

Uma única mudança foi feita depois do relatório: a nota do apresentador do slide 23
citava como fonte um arquivo do repositório que foi removido nesta organização. O
link saiu; a outra fonte da mesma nota, a proposta do N3, tem os números que ela usa.
Slides e PDF não mudaram.

---

## 1. Ver no aplicativo em que vai apresentar — 20 min

A revisão renderizou os 25 slides e conferiu cortes e alinhamento, mas **não testou
no Google Slides nem no PowerPoint**. Importação muda fonte e espaçamento.

☐ Abrir o `.pptx` no aplicativo da apresentação e passar os 25 slides
☐ Conferir em especial o slide 2 (quatro imagens lado a lado), o 4 (três caixas) e o
  24 (tabela)
☐ Se algo quebrar, apresentar pelo `.pdf`, que é fiel ao layout

---

## 2. Ler o artigo — 2h

Se ainda não leu inteiro, esta ordem rende mais em menos tempo. Use o PDF da ACM
(DOI 10.1145/3548606.3560564): as páginas do deck seguem ele.

| | O quê | Tempo |
|---|---|---|
| 1 | Só os títulos de seção. Conte as páginas de cada uma | 10 min |
| 2 | Resumo | 5 min |
| 3 | Introdução. Ache as três perguntas de pesquisa e a lista de contribuições | 20 min |
| 4 | Método. Siga o funil 239.381 → 13.082 → 2.688 | 30 min |
| 5 | Resultados. Repare que **não há grupo de controle** | 20 min |
| 6 | Discussão, Seção 6 | 15 min |
| 7 | Conclusão. Compare *"violate"* no resumo com *"potentially violate"* aqui | 10 min |

---

## 3. Ensaiar com cronômetro — 1h, duas vezes

Em voz alta. **Não leia os trechos em inglês.** Aponte o trecho e fale a análise.

**O roteiro, slide a slide, está em [`roteiro.md`](roteiro.md)**: o que falar, onde apontar e o
relógio acumulado ao fim de cada slide. Total: **14 min 35 s**, sobram 25 s.

As notas do apresentador no `.pptx` têm o texto de apoio de cada slide.

**Se estourar**, passe mais rápido pelos slides 9, 10 e 14. Não
corte 5, 12, 13 e 19, que são o esqueleto do item 3. Não encurte 21+22: o contraste
*"violate"* × *"potentially violate"* é o melhor argumento da apresentação.

---

## 4. As perguntas prováveis

**"Por que este artigo e não um mais recente?"**
> Recência e citações se excluem por construção. Um artigo de 2026 teria perto de
> zero citações; a própria busca trouxe um, do IEEE S&P, com zero. Este tem 99 em
> quatro anos. E o item 2 avalia o veículo, que independe da idade do artigo.

**"Por que as três bases dão números diferentes?"**
> É a cobertura de cada uma. A ACM conta só o próprio acervo: 42. O Scopus acrescenta
> outras editoras: 52. O Google Acadêmico agrupa nove versões e conta teses e
> relatórios: 99.

**"O enunciado pede Qualis Periódicos. Por que Qualis Eventos?"**
> Procurei a CCS no Qualis Periódicos, nos quadriênios 2017–2020 e 2021–2024, e ela
> não aparece, porque é conferência e essa lista é de revistas. Para conferências de
> Computação, a CAPES publica o Qualis Eventos, e nele a CCS é A1.

**"E converter o h5 em Qualis Periódicos?"**
> O Documento Técnico põe a Computação no agrupamento QR1. Nele, o h5 só vira
> percentil por uma regressão com coeficientes de cada área, nas páginas 11 e 12, e
> o documento não publica esses coeficientes. Então não dá para fazer a conta sem
> inventar número.

**"Por que não o artigo da SOUPS?"**
> Mesmo tema, mas 34 citações contra 52, e a SOUPS é A no ICORE2026 contra A\* da
> CCS, na mesma edição. Era B até o CORE2023.

**"O que você faria diferente do que eles fizeram?"**
> Duas coisas que o artigo não tem: grupo de controle pareado e recorte
> governamental. São exatamente as contribuições do meu TCC.

---

## 5. Véspera

☐ Um ensaio corrido
☐ `.pptx` e `.pdf` no computador da apresentação, num pendrive e no e-mail
☐ A pasta `pesquisa/` à mão, caso ela peça para ver um print

**Não mexa no deck na véspera.** Erro entra nessa hora.
