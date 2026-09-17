# Protocolo de busca e planilha de métricas

**Preencha este arquivo ENQUANTO busca, não depois.** O slide 4 pede o passo a passo
da seleção, e esse é o único item da atividade que é **impossível de reconstruir**:
se você achar o artigo e só depois tentar lembrar quantos resultados a busca
devolveu, o número vai ser inventado — e inventar número na metodologia é
exatamente o oposto do que a disciplina cobra.

Leve print de cada tela. A professora pode pedir.

---

## 1. Acesso

O acesso é pelo **portal da CAPES via CAFe**, com a credencial do IDP. Os tutoriais
estão em `material-fornecido/Como acessar a CAPES.pdf` e
`material-fornecido/Tutorial Plataformas Digitais 2024.pdf`.

### ⚠️ A busca TEM que ser numa base da CAFe

O item 1 do enunciado nomeia as bases: **Web of Science, ScienceDirect, ACM, Scopus,
IEEE Xplore**, entre outras. O **Google Scholar não está na lista**.

O Scholar aparece no enunciado só no **item 2**, e só para o **h5**. Buscar o artigo
no Scholar e apresentar isso como o passo a passo da seleção contraria o item 1 —
mesmo que você acabe no mesmo artigo.

**Faça a busca na ACM DL e/ou no Scopus, e registre a tela.**

☐ **Testar o acesso hoje.** Se a credencial não funcionar, você precisa de tempo
para resolver com a biblioteca — e descobrir isso no dia 28 é fatal.

---

## 2. A busca

Execute e registre. Se fizer mais de uma tentativa, registre **todas**, inclusive as
que não deram certo: refinar a string é parte do método e mostra rigor.

### Tentativa 1

| Campo | Preencher |
|---|---|
| Base (WoS · ScienceDirect · ACM · Scopus · IEEE Xplore) | |
| Acesso via CAFe confirmado? | |
| Data da consulta | |
| String exata | |
| Filtros aplicados (ano, tipo, idioma) | |
| Resultados devolvidos | |

### Tentativa 2

| Campo | Preencher |
|---|---|
| Base (WoS · ScienceDirect · ACM · Scopus · IEEE Xplore) | |
| Acesso via CAFe confirmado? | |
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

| | Métrica | Valor | Data | Onde consultei |
|---|---|---|---|---|
| ✅ | **Citações — ACM DL** | **42** | 17/09/2026 | `dl.acm.org/doi/10.1145/3548606.3560564` |
| ✅ | **Citações — Scopus** | **52** | 17/09/2026 | Scopus via CAFe, busca `DOI 10.1145/3548606.3560564` |
| ✅ | **Citações — Google Acadêmico** | **99** (9 versões) | 17/09/2026 | busca pelo DOI |
| ✅ | Downloads — ACM DL | 1.539 | 17/09/2026 | mesma tela |
| ✅ | Ano de publicação | 2022 (07/11) | | página do artigo |
| ☐ | Escala do estudo (nº de apps) | | | ler no artigo |
| ☐ | Artefato público disponível? | | | `github.com/cispa/consent-notices` |

### Dados da citação, conferidos na página do artigo (17/09/2026)

| | |
|---|---|
| Autores | Trung Tin Nguyen · Michael Backes · Ben Stock |
| Título | Freely Given Consent?: Studying Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps |
| Publicação | CCS '22: Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security |
| **Páginas** | **2369–2383** |
| Publicado em | 07 de novembro de 2022 |
| DOI | `10.1145/3548606.3560564` |
| Acesso | FREE ACCESS · tipo: RESEARCH-ARTICLE |

> **"RESEARCH-ARTICLE" na etiqueta do ACM** é confirmação independente de que é
> artigo original, não revisão — exatamente o que o item 1 do enunciado exige. Vale
> mencionar: é a própria base classificando, não interpretação sua.

### A divergência entre bases — já medida

| Base | Citações | Data |
|---|---|---|
| ACM Digital Library | **42** | 17/09/2026 |
| Scopus | **52** | 17/09/2026 |
| **Google Acadêmico** | **99** | 17/09/2026 |

**O Scopus conta 10 a mais que a própria editora do artigo.** Não é erro de
nenhuma das duas: a ACM conta o que está indexado no acervo da ACM, e o Scopus
indexa também IEEE, Springer, Elsevier e periódicos fora da ACM. Um artigo citado
por um trabalho publicado na IEEE aparece no Scopus e não aparece na ACM DL.

E o Google Acadêmico conta **99** — mais que o dobro da ACM. A razão está na própria
tela: ele indica **"Todas as 9 versões"**. O Scholar agrupa nove versões do mesmo
trabalho (preprint, repositório institucional, página do CISPA) e soma as citações
de todas, além de contar citações vindas de teses, relatórios técnicos e preprints
que Scopus e ACM não indexam.

**A ordem 42 < 52 < 99 não é ruído — é a hierarquia de cobertura das bases.** Diga
os três com a data e explique a escada. Escolher o maior sem dizer de onde veio é o
erro que esse item existe para pegar; explicar por que eles diferem é a resposta
completa.

☐ Escolher **um** número para a justificativa e declarar qual base e qual data. O
  mais defensável é o do Scopus, que é base multieditora e curada — mas qualquer um
  serve, desde que declarado.

### O Scopus também confirmou dois dados do item 2

| | |
|---|---|
| Tipo de documento | **Conference Paper** |
| Subject area | Computer Science |
| Source | Proceedings of the ACM Conference on Computer and Communications Security |

**"Conference Paper"** é a terceira fonte independente confirmando que o ramo
correto do item 2 é o de conferência — junto com a etiqueta `RESEARCH-ARTICLE` do
ACM e a entrada no CORE.

E note o nome da fonte no Scopus: *Proceedings of the ACM Conference on Computer
and Communications Security*. É a **quarta** variação do nome do mesmo veículo
(Scholar: *ACM Symposium*; ACM: *ACM SIGSAC Conference*; CORE: *ACM Conference*).
Reforça por que a verificação de identidade do veículo era necessária.

---

## 4. Métricas do veículo

O item 2 da atividade avalia a classificação do **veículo**, não do artigo.

A atividade define **três itens obrigatórios**, e quais são depende do tipo de
veículo. Não são opcionais e não se substituem entre si.

### Se for CONFERÊNCIA (é o caso da CCS) — os três obrigatórios

| | Métrica | Valor | Data | Onde |
|---|---|---|---|---|
| ✅ | **h5-index** | **90** (mediana 146) | 17/09/2026 | Google Scholar Metrics |
| ✅ | **Qualis correspondente ao h5** | **A1** — ver o argumento do limiar | 17/09/2026 | Figura 6, p. 13 |
| ✅ | **Rank CORE** | **A\*** | 17/09/2026 | `portal.core.edu.au/conf-ranks/12/` |

**Os três itens obrigatórios estão levantados.**

#### h5 — levantado

Google Acadêmico → Principais publicações → Categorias → *Engineering & Computer
Science* → **Computer Security & Cryptography**, em **17/09/2026**:

| Posição | Publicação | h5 | Mediana h5 |
|---|---|---|---|
| 1 | USENIX Security Symposium | 116 | 170 |
| 2 | Computers & Security *(periódico)* | 112 | 164 |
| 3 | IEEE Symposium on Security and Privacy | 110 | 195 |
| 4 | IEEE Trans. on Information Forensics and Security *(periódico)* | 100 | 140 |
| **5** | **ACM Symposium on Computer and Communications Security** | **90** | **146** |
| … | | | |
| 13 | Proceedings on Privacy Enhancing Technologies | 56 | 75 |

**Observação que rende:** a lista **mistura periódicos e conferências**. Entre as
**conferências**, a CCS é a **3ª** — atrás só da USENIX Security e da IEEE S&P.
Dizer isso é mais preciso que "5º lugar", e mostra que você leu a tabela em vez de
copiar a linha.

#### ⚠️ Confirme que a linha é o MESMO veículo do artigo

Os nomes não batem entre as fontes, e há uma conferência homônima na mesma lista:

| Onde | Como aparece | h5 |
|---|---|---|
| Scholar, posição **5** | ACM **Symposium** on Computer and Communications Security | **90** |
| Atas do artigo | ACM **SIGSAC Conference** on Computer and Communications Security (CCS '22) | — |
| Scholar, posição **19** | ACM **Asia Conference** on Computer and Communications Security | **41** |

A da posição 19 é a **AsiaCCS**, evento **diferente**, com menos da metade do h5.
Pegar a linha errada significa apresentar 41 no lugar de 90.

**Verificação primária, 30 segundos:** no Google Acadêmico, **clique no número do
h5**. Ele abre a lista dos artigos que compõem o índice. Se aparecerem trabalhos do
CCS — idealmente o próprio artigo escolhido —, o veículo está confirmado.

☐ Cliquei no h5 e confirmei que os artigos listados são do CCS
☐ Anotei a **janela de anos** que o Scholar declara para o h5 (são os 5 anos
  completos mais recentes; se ela incluir o ano do artigo, as citações dele entram
  no índice — vale dizer)
☐ Conferi que o CORE aponta `dblp.uni-trier.de/db/conf/ccs` e **não** `/asiaccs`

> **Vocabulário:** o h5 é **do veículo**, nunca do artigo. Artigo tem citações;
> veículo tem h5. Misturar os dois é erro fácil de a banca pegar.

Complementares, se sobrar tempo: mediana h5, taxa de aceitação do ano.

#### CORE — levantado, com dois detalhes que valem mais que o rank

Conferido no ICORE Conference Portal em **17/09/2026**:

| | |
|---|---|
| Conferência | ACM Conference on Computer and Communications Security |
| Acrônimo | CCS |
| **Rank (ICORE2026)** | **A\*** |
| Field of Research | **4604 — Cybersecurity and privacy** |
| Fonte DBLP | `dblp.uni-trier.de/db/conf/ccs` |

**1. O rank é estável há quase duas décadas.** A mesma página lista CORE2023,
2021, 2020, 2018, 2017, 2014, 2013 e 2008 — **A\* em todas**. A única exceção é o
ERA2010, que deu A. Dizer "é A\* desde 2008, com uma única exceção em 2010" é muito
mais forte que "é A\*": mostra que a classificação não é ruído de uma edição.

**2. O FoR 4604 resolve a pergunta do conjunto de referência.** O CORE classifica a
CCS em *Cybersecurity and privacy*. Quando você for converter o h5 em percentil, o
conjunto de referência natural é a subárea equivalente no Scholar Metrics —
*Computer Security & Cryptography*. **Os dois instrumentos concordam sobre qual é o
campo**, e é isso que justifica a escolha da lista em vez de ser arbitrária.

> Guarde o print desta página. É fonte primária e responde o item 2 inteiro na
> parte do CORE.

#### Convertendo o h5 em percentil — é este o passo que falta

O Qualis trabalha com **percentil**, não com h5 bruto. A conversão:

| Passo | O que fazer | Anote |
|---|---|---|
| 1 | Google Scholar → Metrics → Categories → *Engineering & Computer Science* → **Computer Security & Cryptography** | |
| 2 | h5 do veículo | |
| 3 | Posição na lista | ___ de 20 |
| 4 | Percentil — **leia a armadilha abaixo antes** | |
| 5 | Estrato, pela tabela da Figura 6 | |

### ⚠️ A armadilha do denominador

O Scholar publica **só as 20 primeiras** de cada subárea. **Isso é uma lista
truncada, não a população da área.**

Dividir a posição por 20 subestima o percentil de forma grosseira. Se o veículo é o
3º entre os 20 que o Scholar exibe, ele não é o 3º entre 20 — é o **3º entre todos
os veículos da área**, que são centenas. A conta ingênua daria
(20 − 3) ÷ 20 × 100 = 85 → **A2**, o que colocaria uma das principais conferências
de segurança do mundo abaixo do topo. O erro está no denominador.

**É exatamente o problema que o Documento Técnico descreve (p. 12):** a base do
Google Scholar não fornece percentis dentro dos agrupamentos temáticos, e por isso a
CAPES teve de montar uma base ampliada por área — o **"Universo"** — para obter a
posição real.

**O argumento do limiar — é ele que fecha o item.**

A CCS está na **posição 5**. Com N = 20 (a lista truncada), o percentil seria
(20 − 5) ÷ 20 × 100 = **75**, o que dá **A2** — na borda inferior. Mas esse 75 é um
**piso por construção**: qualquer universo maior que 20 empurra o percentil para
cima, nunca para baixo.

E dá para saber exatamente quando ele cruza para A1:

> (N − 5) ÷ N ≥ 0,875  →  0,125 · N ≥ 5  →  **N ≥ 40**

| Tamanho do universo | Percentil | Estrato |
|---|---|---|
| 20 (lista truncada) | 75,0 | A2 — **piso** |
| 30 | 83,3 | A2 |
| **40** | **87,5** | **A1 — limiar** |
| 100 | 95,0 | A1 |
| 500 | 99,0 | A1 |

**Basta o universo da área ter 40 veículos para a CCS ser A1.** A subárea *Computer
Security & Cryptography* tem centenas — as 20 exibidas são só o topo do que o Scholar
indexa. Logo, **A1**, e o que se afirma não é uma estimativa chutada: é um limite.

**Como dizer isso:**

> "A CCS aparece na posição 5 da lista de *Computer Security & Cryptography*, com h5
> de 90 e mediana 146. O Scholar publica só as vinte primeiras, então essa lista é
> truncada. Com vinte no denominador o percentil seria 75, que dá A2 — mas esse valor
> é um piso por construção, porque qualquer universo maior empurra para cima. O
> limiar do A1 é 87,5, e a posição 5 atinge isso a partir de um universo de quarenta
> veículos. A subárea tem centenas. Portanto o estrato é **A1**, e isso não é
> estimativa: é um limite inferior."

Isso é a resposta completa: você calcula, aponta o limite do instrumento, e diz de
que lado o erro cai. Muito mais forte que entregar um número sem ressalva.

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
