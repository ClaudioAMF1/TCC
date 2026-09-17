# Protocolo de busca e planilha de métricas

**Preencha este arquivo ENQUANTO busca, não depois.** O slide 4 pede o passo a passo
da seleção, e esse é o único item da atividade que é **impossível de reconstruir**:
se você achar o artigo e só depois tentar lembrar quantos resultados a busca
devolveu, o número vai ser inventado — e inventar número na metodologia é
exatamente o oposto do que a disciplina cobra.

Leve print de cada tela. A professora pode pedir.

---

## 1. Acesso

O acesso à ACM Digital Library e ao Scopus é pelo **CAFe**, com a credencial do IDP.
O tutorial está em `material-fornecido/Como acessar a CAFe.pdf`.

☐ **Testar o acesso hoje.** Se a credencial não funcionar, você precisa de tempo
para resolver com a biblioteca — e descobrir isso no dia 28 é fatal.

---

## 2. A busca

Execute e registre. Se fizer mais de uma tentativa, registre **todas**, inclusive as
que não deram certo: refinar a string é parte do método e mostra rigor.

### Tentativa 1

| Campo | Preencher |
|---|---|
| Base | |
| Data da consulta | |
| String exata | |
| Filtros aplicados (ano, tipo, idioma) | |
| Resultados devolvidos | |

### Tentativa 2

| Campo | Preencher |
|---|---|
| Base | |
| Data da consulta | |
| String exata | |
| Filtros aplicados | |
| Resultados devolvidos | |

### String sugerida como ponto de partida

```
("third-party" OR "third party") AND (tracking OR tracker OR SDK)
AND (android OR "mobile app") AND (privacy OR consent OR GDPR)
```

Ajuste à sintaxe de cada base — a ACM DL e o Scopus não usam a mesma. **Registre a
string que você de fato usou**, não esta.

### Critérios de inclusão e exclusão

Declare antes de olhar os resultados. É o que separa seleção de conveniência.

**Incluir:** artigo original com medição empírica · rastreamento por terceiros em
Android · veículo indexado e revisado por pares · texto completo acessível.

**Excluir:** revisão de literatura ou survey · posicionamento sem dado · foco em iOS
ou web sem componente Android · publicado apenas como preprint.

### O funil

| | Quantos |
|---|---|
| Resultados devolvidos | |
| Após ler título e resumo | |
| Lidos na íntegra | |
| **Selecionado** | 1 |

---

## 3. Métricas do artigo

Cada célula precisa de **valor + data**. Indicador muda; número sem data não vale.

| Métrica | Valor | Data | Onde consultei |
|---|---|---|---|
| Citações — Google Scholar | | | |
| Citações — Scopus | | | |
| Citações — ACM DL | | | |
| Ano de publicação | | | |
| Escala do estudo (nº de apps) | | | |
| Artefato público disponível? | | | |

> As três bases vão divergir. **Isso não é erro** — elas indexam conjuntos
> diferentes. Reportar a divergência, em vez de escolher o número maior, é uma
> observação metodológica que rende ponto.

---

## 4. Métricas do veículo

O item 2 da atividade avalia a classificação do **veículo**, não do artigo.

A atividade define **três itens obrigatórios**, e quais são depende do tipo de
veículo. Não são opcionais e não se substituem entre si.

### Se for CONFERÊNCIA (é o caso da CCS) — os três obrigatórios

| ☐ | Métrica | Valor | Data | Onde |
|---|---|---|---|---|
| ☐ | **h5-index** | | | Google Scholar Metrics |
| ☐ | **Qualis correspondente ao h5** | | | tabela de percentis (ver abaixo) |
| ☐ | **Rank CORE** | | | `portal.core.edu.au/conf-ranks/` |

Complementares, se sobrar tempo: mediana h5, taxa de aceitação do ano.

#### Convertendo o h5 em percentil — é este o passo que falta

O Qualis trabalha com **percentil**, não com h5 bruto. A conversão:

| Passo | O que fazer | Anote |
|---|---|---|
| 1 | Google Scholar → Metrics → Categories → *Engineering & Computer Science* → **Computer Security & Cryptography** | |
| 2 | h5 do veículo | |
| 3 | Posição dele na lista, e o tamanho da lista | ___ de ___ |
| 4 | Percentil = (total − posição) ÷ total × 100 | |
| 5 | Estrato, pela tabela da Figura 6 | |

Exemplo da conta: 3º lugar numa lista de 20 → (20 − 3) ÷ 20 × 100 = **85** → **A2**.

> **Fonte primária, e é ela que dá a resposta.** O Documento Técnico, p. 12,
> reconhece o problema e diz como a CAPES o resolve:
>
> > *"No caso do QR2, o índice h é a referência para o cálculo dos estratos. Porém,
> > a base do Google Scholar **não fornece diretamente os valores dos percentis
> > dentro dos agrupamentos temáticos**. Para contornar, foi necessário criar uma
> > base ampliada de periódicos pertinentes a cada área, denominada **Universo**,
> > para que se tivesse a real posição dos títulos utilizados pelos programas dentro
> > desse conjunto de veículos potenciais da área."*
>
> Dois pontos que isso te dá:
>
> 1. **O percentil do h5 é posição dentro de um conjunto de referência.** Não é
>    propriedade do veículo. Você não tem acesso ao "Universo" da CAPES, então usa a
>    lista da subárea do Google Scholar Metrics e **declara** que foi essa.
> 2. **O documento prevê um segundo caminho** (p. 11–12): para veículos sem
>    CiteScore nem JCR, um modelo de **regressão linear CiteScore–h5** estima o
>    CiteScore, e o percentil sai da ordenação desses valores estimados. Mencione que
>    existe — mostra que você leu o documento inteiro, não só a Figura 6.

### Se fosse PERIÓDICO — os outros três obrigatórios

| ☐ | Métrica | Valor | Data | Onde |
|---|---|---|---|---|
| ☐ | **JIF Percentile** | | | JCR |
| ☐ | **Highest Percentile** | | | Scopus |
| ☐ | **Qualis de ambos** | | | tabela da Figura 6 |

> São **dois** indicadores e **dois** estratos a informar. O Documento Técnico manda
> considerar **o maior percentil** quando há mais de um indicador — diga isso ao
> apresentar, mostra que você leu o documento e não só aplicou a tabela.

### A tabela de conversão

`material-fornecido/Documento Tecnico do Qualis Periodicos.pdf`, Figura 6, p. 13.
Imagem em `qualis-faixas-de-percentil.png` — **use ela no slide**, é fonte primária.

| Estrato | Percentil | | Estrato | Percentil |
|---|---|---|---|---|
| **A1** | ≥ 87,5 | | **B1** | 37,5 – 50 |
| **A2** | 75 – 87,5 | | **B2** | 25 – 37,5 |
| **A3** | 62,5 – 75 | | **B3** | 12,5 – 25 |
| **A4** | 50 – 62,5 | | **B4** | 0 – 12,5 |

---

## 5. Conferência final da citação

☐ Autores, na ordem exata do PDF
☐ Título completo, com subtítulo
☐ Nome completo do evento ou periódico
☐ Ano, páginas, DOI
☐ Formatada em ABNT

**Nunca copie referência de segunda mão**, nem deste repositório. Abra o PDF e
confira. É o erro mais fácil de a banca pegar e o mais bobo de cometer.
