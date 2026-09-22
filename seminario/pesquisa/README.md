# Evidência da seleção e das métricas

Prints do item 1 (seleção e relevância do artigo) e do item 2 (métricas do veículo).
**Todos foram conferidos tela a tela em 22/09/2026**, e os nomes dizem o que cada um
mostra.

**Base: Scopus, pelo portal da CAPES via CAFe**, em **21/09/2026, das 08:46 às
09:11**. O endereço nas telas é `www-scopus-com.ez279.periodicos.capes.gov.br`. O
prefixo `ez279` é o proxy institucional, e prova o acesso pela CAFe que o item 1 do
enunciado exige.

```
pesquisa/
├── 0-acesso/              como entrei no Scopus
├── busca-1/               string estreita, 4 resultados
├── busca-2/               string intermediária, 12 resultados
├── busca-3/               string ampla, 131 → 70 → 39 → 5   ← é a que vai ao slide
├── metricas/              citações do artigo (item 1) e h5, Qualis, CORE (item 2)
└── recortes-para-slide/   os quatro degraus do funil, comprimidos para o deck
```

A numeração dos prints da busca (01 a 24) é a ordem em que foram tirados e continua
a mesma entre as pastas. Os dois `00a` e `00b` são de 17/09, anteriores à busca.

---

## O funil que vai ao slide

```
131   "third-party tracking", sem filtro                          18 · 09:07
 ↓    ano 2018–2026 · Computer Science · Conference paper + Article
 70                                                               20 · 09:09
 ↓    palavras-chave Third Parties e Third-party Tracking
 39                                                               21 · 09:10
 ↓    acrescenta consent à string · ano passa a 2018–2025
  5   finalistas                                                  23 · 09:11
 ↓    leitura de título e resumo
  1   selecionado
```

**O degrau que muda tudo é o último.** De 39 para 5 não foi filtro de interface: foi
acrescentar **`consent`** à string, porque consentimento é o recorte do TCC. O print
23 mostra a caixa de busca com o termo e o resultado na mesma tela.

## Os cinco finalistas

| # | Artigo | Veículo | Ano | Cit. | Decisão |
|---|---|---|---|---|---|
| 1 | An Empirical Measurement of Cookie Banners Potential Legal Violations in EU vs US Websites | LNCS | 2025 | 0 | web, não Android |
| 2 | A Comprehensive Study on Third-Party User Tracking in Mobile Applications | ACM ICPS | 2023 | 10 | menos citado |
| **3** | **Freely Given Consent?** — Nguyen, Backes, Stock | **CCS** | **2022** | **52** | **selecionado** |
| 4 | A fait accompli? An empirical study into the absence of consent to third-party tracking in Android apps | SOUPS | 2021 | 34 | veículo CORE B |
| 5 | Protecting privacy on the web: HTTPS and Google Analytics in academic library websites | Online Information Review | 2018 | 23 | web, não Android |

Item 1 está no print 23; itens 2 a 5 no print 24.

> **Duas correções de 22/09**, feitas ao rever os prints um a um:
>
> 1. O funil registrado antes era `131 → 70 → 5`. Faltava o degrau de **39**, e o
>    corte para 5 estava atribuído às palavras-chave, quando foi o termo `consent`.
> 2. A tabela de finalistas tinha o **WhisperTest** (CCS 2025, iOS) no lugar do artigo
>    sobre *cookie banners*. O WhisperTest é das buscas 1 e 2, não dos 5 da busca 3.
>
> Os dois erros foram de registro, não de busca: as telas sempre disseram isto.

---

## Os arquivos

### `0-acesso/`
| Arquivo | O que mostra |
|---|---|
| `00a-capes-portal-busca-pela-base-scopus` | 17/09 · Portal de Periódicos da CAPES, *"Você está acessando esse portal por: IDP"*, via CAFe |
| `00b-capes-lista-de-bases-scopus-proxy-ez279` | 17/09 · Lista A-Z de bases da CAPES, já pelo proxy `ez279` |
| `01-capes-ficha-scopus-acesso-cafe` | 21/09 · Ficha da base Scopus no portal da CAPES, com "Acesso CAFe" e a instituição identificada como IDP |
| `02-scopus-formulario-da-busca-1` | 21/09 · Formulário do Scopus com a primeira string digitada |

### `busca-1/` — `"third-party tracking" AND consent AND android`
| Arquivo | O que mostra |
|---|---|
| `03-sem-filtro-4-resultados` | **4 documentos**, sem filtro |
| `04-sem-filtro-candidatos-2-a-4` | Paci 2023 (10 cit.), Nguyen 2022 (52), Kollnig 2021 (34) |
| `05-filtros-ano-area-tipo` | Aplicando ano, área e tipo de documento |
| `06-filtrada-4-candidatos` | Os 4 com filtro 2021–2025, Computer Science, Conference paper |
| `07-resumo-whispertest-2025` | Resumo do WhisperTest aberto: é **iOS** |
| `08-resumo-paci-2023` | Resumo do Paci 2023 aberto: 400 apps, 200 Android |
| `09-resumo-nguyen-2022-selecionado` | Resumo do artigo escolhido: 239.381 apps, 13.082 com aviso, 2.688 (20,54%) |

### `busca-2/` — `"third party" AND tracking AND android AND (consent OR GDPR)`
| Arquivo | O que mostra |
|---|---|
| `10-filtrada-area-tipo-9-resultados` | **9 documentos** com Computer Science e Conference paper. Topo: IEEE S&P 2026, 0 citações |
| `11-filtrada-itens-2-a-5` | WhisperTest, Paci 2023, Liu (WiSec 2023), Nguyen 2022 |
| `12-filtrada-itens-5-a-8` | Nguyen 2022, Kollnig 2021, Gamba (IEEE S&P 2020, 73 cit.), Monogios 2020 |
| `13-filtrada-itens-7-a-9-fim` | Fim da lista filtrada |
| `14-sem-filtro-12-resultados` | **12 documentos**, filtros removidos |
| `15-sem-filtro-itens-3-a-6` | Itens 3 a 6, com os contadores de área e tipo à esquerda |
| `16-sem-filtro-itens-7-a-10` | Itens 7 a 10. Inclui Kollnig, *Before and after GDPR* (2021, 40 cit.) |
| `17-sem-filtro-pagina-2` | Segunda página da lista de 12 |

### `busca-3/` — `"third-party tracking"` — **a que vai ao slide**
| Arquivo | O que mostra |
|---|---|
| `18-sem-filtro-131-resultados` | **131 documentos**, só a expressão exata |
| `19-escolhendo-ano-area-tipo` | Painel de filtros aberto, ano 2018–2026, ainda sem aplicar |
| `20-ano-area-tipo-70-resultados` | **70 documentos**: Computer Science 70, Conference paper 52, Article 18 |
| `21-palavras-chave-39-resultados` | **39 documentos** |
| `22-palavras-chave-39-filtros-visiveis` | Os mesmos 39, com os filtros de palavra-chave marcados à esquerda |
| `23-termo-consent-5-resultados` | String com **`consent`**, ano 2018–2025: **5 documentos**, itens 1 a 3 |
| `24-5-finalistas-itens-2-a-5` | Os mesmos 5, itens 2 a 5, com todos os filtros visíveis |

### `metricas/`
Prints de **17/09/2026**, exceto o 07 (22/09) e o 10 (21/09). O 08 é uma figura do PDF da CAPES, não print de tela.

**Item 1 — relevância quantitativa: citações do artigo**

| Arquivo | O que mostra |
|---|---|
| `01-acm-dl-42-citacoes-1539-downloads` | ACM Digital Library, painel *Bibliometrics*: **42 citações**, 1.539 downloads |
| `02-acm-dl-pagina-do-artigo-research-article` | Página do artigo na ACM: etiqueta **RESEARCH-ARTICLE** e FREE ACCESS, CCS '22, p. 2369–2383, publicado em 07/11/2022. É a prova de artigo original |
| `03-scopus-doi-no-campo-titulo-0-resultados` | Scopus com o DOI no campo *Article title, Abstract, Keywords*: 0 resultados. DOI não é título, então o campo estava errado |
| `04-scopus-doi-todos-os-campos-52-citacoes` | O mesmo DOI em *All fields*: **1 documento, 52 citações**, tipo *Conference Paper* |
| `05-google-academico-99-citacoes-9-versoes` | Google Acadêmico pelo DOI: **"Citado por 99"** e **"Todas as 9 versões"** |

**Item 2 — métricas do veículo**

| Arquivo | O que mostra |
|---|---|
| `06-google-scholar-metrics-h5-90-posicao-5` | *Computer Security & Cryptography*, lista completa das 20: CCS na **posição 5, h5 90, mediana 146**. Das quatro acima, duas são periódicos, então entre conferências a CCS é a 3ª. A AsiaCCS, que não é o mesmo evento, está na posição 19, com h5 41 |
| `07-qualis-eventos-computacao-2017-2020-ccs-a1` | **CAPES, Qualis Eventos da Computação 2017–2020, p. 9: CCS = A1.** Fonte primária do estrato |
| `08-qualis-periodicos-faixas-de-percentil` | Figura 6 do Documento Técnico do Qualis Periódicos: percentil → estrato. Base do argumento do limiar |
| `09-core-portal-ccs-a-estrela` | ICORE Conference Portal: **A\*** em ICORE2026, com o histórico inteiro (A\* desde 2008; só o ERA2010 deu A). FoR 4604, *Cybersecurity and privacy*. DBLP aponta `conf/ccs`, não `asiaccs` |
| `10-scopus-sources-busca-por-titulo-0-resultados` | Scopus *Sources* pesquisado pelo título do artigo: 0 resultados. *Sources* busca **veículos**, não artigos, e a CCS não é periódico. Por isso o ramo JIF / Highest Percentile do enunciado não se aplica |

### `recortes-para-slide/`
Recortes de 1200 × 694, sem barra de menu nem dock, para caber no deck.

| Arquivo | Recortado de |
|---|---|
| `funil-1-131.jpg` | print 18 |
| `funil-2-70.jpg` | print 20 |
| `funil-3-39.jpg` | print 21 |
| `funil-4-5.jpg` | print 23 — mostra a string com `consent` e o total na mesma imagem |

---

## O que ficou fora de propósito

**O e-mail de concessão do AndroZoo** (17/09) foi enviado na mesma leva de prints,
mas mostra a **chave da API** em texto aberto. A chave é de uso individual e vive só
em variável de ambiente. Não entra no repositório, nem recortada.

---

## Por que guardar isso

O item 1 do enunciado pede o **passo a passo da seleção**, não só o resultado. É o
único item da atividade impossível de reconstruir depois: quem busca primeiro e anota
depois acaba inventando o número. Estes prints provam que o funil
`131 → 70 → 39 → 5 → 1` aconteceu, na data declarada, na base declarada. E, como a
revisão de 22/09 mostrou, são eles que corrigem o registro quando o registro erra.
