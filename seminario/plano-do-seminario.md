# Seminário — Análise de Artigo Científico

**Datas:** 29/09 e 01/10/2026 · ordem alfabética · **15 minutos** por apresentação
**Peso:** 4 dos 6 pontos da AV1 (a Lista 01 vale 2) — é a maior nota do bimestre
**Hoje:** 15/09 → **duas semanas**

---

## 1. O problema do tema indefinido — e como resolvê-lo

A atividade exige justificar a relevância do artigo **para o seu TCC**. Você ainda não tem
tema fechado, só a área. Três saídas possíveis:

| Saída | Avaliação |
|---|---|
| Escolher um artigo genérico de cibersegurança | ❌ A justificativa fica vaga. "É da minha área" não é critério. |
| Esperar fechar o tema antes de escolher o artigo | ❌ Duas semanas. Não dá. |
| **Assumir o candidato mais forte como tema de trabalho e escolher o artigo que é o precedente metodológico dele** | ✅ |

### Por que a terceira funciona

O `N3 — rastreadores em apps móveis governamentais` é o único candidato com **corpus
verificado**: 396 aplicativos de 71 publicadores públicos distintos. Assumi-lo como tema de
trabalho não é chute; é a conclusão de um processo de teste documentado.

E há uma segunda camada: **o artigo escolhido é relevante mesmo que o tema mude.** O que
você vai reaproveitar não é o objeto estudado, é o **método** — análise estática de APKs em
escala, detecção de SDKs de rastreamento e confronto entre o comportamento observado e o
que o app declara. Esse método serve a quase qualquer tema de medição em cibersegurança.

### O diferencial que quase ninguém vai ter

Você tem **dois temas testados e rejeitados com dados**:

- **N1 (infraestrutura crítica exposta):** descartado porque os mesmos hosts respondem em
  Modbus, IEC-104 e EtherNet/IP simultaneamente — comportamento de honeypot e de nuvem, não
  de equipamento industrial. A variável independente era inobservável.
- **CT (abuso de marca em Certificate Transparency):** descartado porque, em 20.007 entradas
  de log, não apareceu nenhuma imitação real — phishing moderno raramente põe a marca no
  domínio, o que impõe teto de recall por construção.

Gaste **30 segundos** disso no slide de justificativa. É demonstração direta do que a
Aula 04 chama de maturidade em pesquisa e do que a Aula 07 chama de evitar o fundamento
vazio. Numa sala de apresentações de 15 minutos, é o tipo de coisa que distingue.

> ⚠️ Antes de fechar: **alinhe com o orientador.** Se ele apontar outra direção, troque o
> artigo — ainda há tempo. O que não dá é chegar no dia 29 sem tema assumido.

---

## 2. Artigo recomendado

### Escolha principal

> **Privacy Settings of Third-Party Libraries in Android Apps: A Study of Facebook SDKs.**
> **Proceedings on Privacy Enhancing Technologies (PoPETs)**, v. 2025, n. 1.
> [petsymposium.org/popets/2025/popets-2025-0056.php](https://petsymposium.org/popets/2025/popets-2025-0056.php)
>
> ⚠️ Confirme autores, paginação e número da edição ao baixar o PDF — não copie daqui.

**Por que este:**

- **É estado da arte.** 2025. A Aula 05/06 é explícita: *"é importante que um trabalho de
  pesquisa se relacione principalmente com conhecimentos que sejam inerentes ao estado da
  arte, ou seja, que sejam recentes"*. Em privacidade móvel, um artigo de 2020 já não
  atende — o Android mudou permissões, armazenamento com escopo e Privacy Sandbox desde lá.
- **PoPETs é o veículo principal da área de privacidade.** Não é conferência genérica de
  segurança: é onde essa literatura específica acontece.
- **O método é o do seu TCC, com um item a mais.** Mais de 6.000 apps analisados para
  detectar SDKs, verificar como o desenvolvedor configurou as opções de privacidade, e
  **confrontar isso com o que o app declara nos rótulos e na política de privacidade**.
  Essa última parte é exatamente a hipótese H2 do `desenhos/N3-apps-governamentais.md`.
- **É acesso aberto.** O PDF baixa sem CAFe e sem paywall. Isso resolve o gargalo prático:
  você consegue o texto completo hoje, sem depender da credencial institucional funcionar.
- **A lacuna continua lá:** corpus de apps populares comerciais, sem recorte governamental,
  sem grupo de controle pareado, sem contexto brasileiro.

### Alternativas

| Artigo | Veículo / ano | Quando preferir |
|---|---|---|
| Fingerprinting SDKs for Mobile Apps and Where to Find Them | ACM CCS 2025 · [DOI](https://dl.acm.org/doi/10.1145/3719027.3744877) | Se quiser o veículo mais prestigiado. Tema mais estreito (fingerprinting). |
| A Comprehensive Study on Third-Party User Tracking in Mobile Applications (Paci, Pizzoli & Zannone) | ARES 2023 · [DOI](https://dl.acm.org/doi/10.1145/3600160.3605079) | 400 apps; metade contata rastreadores sem consentimento. Meio-termo de recência. |
| Betrayed by the Guardian (Ali et al.) | ACSAC 2020 · [DOI](https://dl.acm.org/doi/abs/10.1145/3427228.3427287) | **Não como artigo analisado** — 2020 é antigo demais. Use como citação de apoio na justificativa, por ser o precedente metodológico. |
| Third Party Tracking in the Mobile Ecosystem (Binns et al.) | WebSci 2018 · Best Paper | Citação de apoio para dimensionar o fenômeno (959 mil apps). |

> **A lição, que vale para o TCC inteiro:** um artigo pode ser ótimo como *precedente
> metodológico* e ruim como *estado da arte*. São funções diferentes. Na revisão
> bibliográfica você vai precisar dos dois tipos — e saber distinguir é o que a Aula 07
> cobra quando fala em relacionar o trabalho ao que é recente.

## 3. Planilha de levantamento — o que buscar e onde

**Estes valores você precisa levantar.** Não aceite número de segunda mão: a professora pode
pedir a tela. Anote a **data de consulta** de cada um; indicador muda.

### Acesso

CAFe pelo Portal de Periódicos da CAPES → escolher **IDP** como instituição → login
institucional. O passo a passo está em `material-fornecido/Como acessar a CAPES.pdf` e
`Tutorial Plataformas Digitais 2024.pdf`.

> ⚠️ **Atenção — qual caminho se aplica a cada recomendação:**
> **PoPETs é PERIÓDICO**, não conferência. Se ficar com a escolha principal, use o
> caminho **(a)**: JIF Percentile no JCR + Highest Percentile no Scopus + Qualis de cada um.
> As alternativas CCS 2025 e ARES 2023 são conferências e usam o caminho **(b)**.
> Confirme o tipo do veículo antes de levantar as métricas — errar o caminho custa nota.
>
> Se o PoPETs não estiver indexado no JCR, **isso é um achado a reportar**, não um problema:
> informe que só há Scopus e explique por quê. Reportar a ausência de um indicador é mais
> correto do que omitir o item.

### a) Se você escolher um artigo de **revista**

| Indicador | Onde | O que anotar |
|---|---|---|
| **JIF Percentile** | Web of Science → Journal Citation Reports (JCR) → busque a revista → aba *Rank* | o percentil, a categoria e o ano |
| **Highest Percentile** | Scopus → Sources → busque a revista → *CiteScore rank & trend* | o maior percentil entre as categorias |
| **Qualis** | tabela da Seção 4, aplicada a cada percentil | dois estratos, um por indicador |

### b) Se você escolher um artigo de **conferência**

| Indicador | Onde | O que anotar |
|---|---|---|
| **h5-index** | Google Scholar → *Metrics* → busque a sigla da conferência | valor do h5 e o h5-mediana |
| **Qualis via h5** | tabela da Seção 4 | o estrato correspondente |
| **CORE Rank** | [portal.core.edu.au/conf-ranks](https://portal.core.edu.au/conf-ranks/) — **aberto, sem CAFe** | rank (A*, A, B, C) e o ano do ranking |

> Sobre o Qualis a partir do h5: o Documento Técnico (p. 12) explica que, para veículos sem
> CiteScore/JCR, o percentil é **estimado** por um modelo de regressão CiteScore–h5. Ou seja,
> o estrato obtido por essa via é uma aproximação. **Diga isso na apresentação** — mostra
> que você leu o documento e não só aplicou a tabela.

### c) Critérios de relevância do artigo (o item 1 pede quantitativos e/ou qualitativos)

**Quantitativos** — número de citações (Google Scholar, Scopus, Web of Science; anote os
três, eles divergem), ano de publicação, métricas do veículo acima.

**Qualitativos** — e aqui você tem munição que ninguém mais tem:
- o método do artigo é o que você vai reusar;
- o corpus dele não cobre o recorte que você vai estudar;
- **você já verificou que o seu corpus existe: 396 aplicativos de 71 publicadores públicos.**

Esse último ponto transforma "acho relevante" em "é relevante, e eu medi".

---

## 4. Tabela Qualis — percentil → estrato

Extraída da Figura 6, p. 13 do `Documento Tecnico do Qualis Periodicos.pdf`.
Imagem em `qualis-faixas-de-percentil.png` — **use ela no slide**, é fonte primária.

| Estrato | Faixa de percentil | | Estrato | Faixa de percentil |
|---|---|---|---|---|
| **A1** | percentil ≥ 87,5 | | **B1** | 37,5 ≤ percentil < 50 |
| **A2** | 75 ≤ percentil < 87,5 | | **B2** | 25 ≤ percentil < 37,5 |
| **A3** | 62,5 ≤ percentil < 75 | | **B3** | 12,5 ≤ percentil < 25 |
| **A4** | 50 ≤ percentil < 62,5 | | **B4** | 0 ≤ percentil < 12,5 |

Classes de **12,5% de amplitude**. O estrato **C** é dos periódicos que não possuem nenhum
dos indicadores do modelo e/ou não atendem às boas práticas editoriais (referência: COPE).

Dois detalhes do documento que rendem pergunta de banca:
- Quando o periódico tem mais de um indicador, considera-se **o maior percentil**.
- As áreas podem ajustar até 30% dos estratos (20% em 1 nível, 10% em 2 níveis), então o
  estrato final publicado pode não bater exatamente com o que a tabela devolve.

---

## 5. Roteiro da apresentação (15 minutos)

Estrutura que segue a ordem exigida no enunciado.

| # | Slide | Tempo |
|---|---|---|
| 1 | Capa — título, seu nome, disciplina, data | — |
| 2 | **Contexto:** área do TCC e o tema de trabalho assumido | 1 min |
| 3 | **Como cheguei aqui:** os dois temas testados e rejeitados, com o número de cada teste | 1 min |
| 4 | **Passo a passo da seleção:** base usada, string de busca, filtros, critério de inclusão, quantos resultados → quantos lidos → 1 escolhido | 2 min |
| 5 | **O artigo:** citação completa + por que é original e não revisão | 1 min |
| 6 | **Relevância — quantitativa:** citações nas três bases, métricas do veículo | 1,5 min |
| 7 | **Relevância — qualitativa:** o método que eu reuso + a lacuna que ele deixa + meu corpus de 396 apps | 1,5 min |
| 8 | **Métricas e Qualis:** h5, estrato, CORE rank + a tabela da Figura 6 | 2 min |
| 9–14 | **Análise da estrutura** (Seção 6) | 5 min |
| 15 | Fechamento: o que este artigo muda no meu TCC | 0,5 min |

**Prove o tempo em voz alta antes.** Quinze minutos passam rápido, e a análise da estrutura
é o que mais rende nota — não deixe para correr no fim.

---

## 6. Análise da estrutura — o formato que ela espera

O `Exemplo de Analise da Estrutura de Artigo.pdf` mostra exatamente o que fazer: **reproduzir
o texto real do artigo e anotar, ao lado, a função retórica de cada trecho.** Não é resumir
o artigo — é mostrar como ele foi construído.

Os dois exemplos do arquivo seguem seis blocos:

**1. Análise da estrutura** — reproduza o sumário do artigo (seções e subseções) e marque à
direita o que é o quê: *"Desenvolvimento do trabalho"*, *"Procedimento metodológico"*,
*"Resultados obtidos"*, *"Infere a partir dos dados obtidos"*.

**2. Análise do resumo** — cole o abstract e marque: *Objetivos* · *Método empregado* ·
*Apresentação dos resultados*. Inclua as palavras-chave.

**3. Análise da introdução** — cole os parágrafos e marque: *Contextualiza o trabalho* ·
*Descreve a problemática* · *Objetivo e contribuição da proposta* · *Estrutura e organização
do artigo*.

**4. Análise do método** — qual é o procedimento metodológico, seção a seção. Repare que, no
segundo exemplo, o avaliador anotou: *"apesar do método empregado não estar explicitamente
descrito, o trabalho segue a seguinte metodologia..."* — ou seja, **apontar o que falta na
estrutura também é análise**, e é o tipo de observação que rende nota.

**5. Análise dos resultados** — o que foi obtido e como foi validado.

**6. Análise da conclusão** — cole e marque: *Inferência a partir dos dados obtidos*.

### Aplicando ao artigo do PoPETs

Duas coisas para observar quando ler, e que rendem comentário na análise:

- **Onde fica o método.** Em artigo de periódico de privacidade, a seção de metodologia
  costuma ser explícita — diferente do exemplo de robótica fornecido pela professora, em que
  o avaliador precisou reconstruir o método a partir do texto. **Compare os dois casos na
  apresentação:** dizer por que um artigo tem seção metodológica explícita e o outro não é
  análise comparativa, que vale mais que descrição.
- **O confronto declarado × detectado.** O artigo compara a configuração real dos SDKs com o
  que o app declara nos rótulos e na política de privacidade. Marque essa parte com atenção
  — é exatamente a hipótese H2 do seu desenho, e é o gancho natural para o slide de
  fechamento.

## 7. O que fazer nesta semana

| Ordem | Ação |
|---|---|
| 1 | Testar o acesso CAFe **hoje** — se a credencial não funcionar, você precisa de tempo para resolver com a biblioteca |
| 2 | Baixar o PDF do artigo pelo ACM DL via CAFe e **ler inteiro** (não só o abstract) |
| 3 | Levantar as métricas e anotar valor + data + print de cada tela |
| 4 | Registrar o passo a passo da busca enquanto faz — base, string, filtros, nº de resultados. O slide 4 depende disso e é impossível reconstruir depois |
| 5 | Montar a análise da estrutura seguindo o formato da Seção 6 |
| 6 | Ensaiar cronometrado |

**O passo 4 é o que todo mundo esquece.** A atividade pede o *passo a passo* da seleção, não
só o resultado. Anote enquanto pesquisa.
