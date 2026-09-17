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

### Se for conferência (é o caso da CCS)

| Métrica | Valor | Data | Onde |
|---|---|---|---|
| h5-index | | | Google Scholar Metrics |
| Mediana h5 | | | Google Scholar Metrics |
| CORE rank | | | portal CORE |
| Taxa de aceitação do ano | | | site da conferência |

### Se fosse periódico

| Métrica | Valor | Data | Onde |
|---|---|---|---|
| Percentil / quartil | | | Scopus (CiteScore) ou JCR |
| Fator de impacto | | | JCR |
| ISSN | | | site do periódico |

### Qualis

O `material-fornecido/Documento Tecnico do Qualis Periodicos.pdf` define a conversão
de percentil em estrato; a Figura 6 está extraída em `qualis-faixas-de-percentil.png`.

| | Preencher |
|---|---|
| Percentil apurado | |
| Estrato correspondente | |
| Faixa da tabela usada | |

> Atenção: o Qualis é definido para **periódicos**. Se o veículo for conferência,
> diga isso na apresentação em vez de forçar um estrato — apontar que o instrumento
> não se aplica ao caso é análise, não falha. Use o CORE como classificação
> equivalente e explique a substituição.

---

## 5. Conferência final da citação

☐ Autores, na ordem exata do PDF
☐ Título completo, com subtítulo
☐ Nome completo do evento ou periódico
☐ Ano, páginas, DOI
☐ Formatada em ABNT

**Nunca copie referência de segunda mão**, nem deste repositório. Abra o PDF e
confira. É o erro mais fácil de a banca pegar e o mais bobo de cometer.
