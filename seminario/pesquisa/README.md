# Evidência da busca bibliográfica

Prints da seleção do artigo do seminário. **Base: Scopus, pelo portal da CAPES via
CAFe**, em **21/09/2026**. O endereço nas telas é
`www-scopus-com.ez279.periodicos.capes.gov.br` — o prefixo `ez279` é o proxy
institucional, e serve como prova do acesso pela CAFe, que o item 1 do enunciado
exige.

---

## As três buscas

| | String | Campo | Resultados |
|---|---|---|---|
| **1** | `"third-party tracking" AND consent AND android` | título, resumo, palavras-chave | **4** |
| **2** | `"third party" AND tracking AND android AND (consent OR GDPR)` | título, resumo, palavras-chave | **12** (9 com filtro de ano) |
| **3** | `"third-party tracking"` | título, resumo, palavras-chave | **131** |

A terceira é a que dá o topo do funil. As duas primeiras foram cirúrgicas demais: a
expressão exata combinada com três termos obrigatórios devolveu só 4 documentos, o
que não mostra trabalho de triagem. A terceira abre para 131 e depois estreita por
filtro, que é como uma busca sistemática deve parecer.

## O funil que vai ao slide

```
131  expressão exata, sem filtro
 ↓   ano 2018–2026, Computer Science, Conference paper e Article
 70
 ↓   palavras-chave Third Parties e Third-party Tracking, ano 2018–2025
  5  finalistas
 ↓   leitura de título e resumo
  1  selecionado
```

## Os finalistas

| Artigo | Veículo | Ano | Citações | Decisão |
|---|---|---|---|---|
| A Comprehensive Study on Third-Party User Tracking in Mobile Applications | ACM ICPS | 2023 | 10 | descartado, menos citado |
| **Freely Given Consent?** — Nguyen, Backes, Stock | **CCS** | **2022** | **52** | **selecionado** |
| A fait accompli? An empirical study into the absence of consent | SOUPS | 2021 | 34 | descartado, veículo CORE B |
| Protecting privacy on the web: HTTPS and Google Analytics em bibliotecas | Online Information Review | 2018 | 23 | descartado, é web e não Android |
| WhisperTest: A Voice-Control-based Library for iOS UI Automation | CCS | 2025 | 0 | descartado, é iOS |

> Vale registrar que a busca também trouxe um artigo de **2026 no IEEE Symposium on
> Security and Privacy** sobre riscos de privacidade em plataformas de gestão de
> consentimento, com **0 citações**. Ele é mais recente que o escolhido e está em
> veículo de topo, mas ainda não teve tempo de ser citado. É a demonstração viva de
> que recência e citações se excluem por construção.

---

## Os arquivos

Numerados na ordem em que foram feitos.

| Arquivo | O que mostra |
|---|---|
| `01-capes-base-scopus` | Ficha da base Scopus no portal da CAPES, com "Acesso CAFe" e a instituição identificada como IDP |
| `02-scopus-formulario-busca1` | Formulário do Scopus com a string da busca 1 digitada |
| `03-busca1-4-resultados` | Busca 1 sem filtro: **4 documentos** |
| `05-busca1-filtros-aplicados` | Busca 1 com filtros de ano, área e tipo de documento |
| `06-busca1-4-candidatos` | Busca 1 filtrada, com os 4 candidatos, ano e número de citações |
| `10-busca2-filtrada-9` | Busca 2 com filtro de ano: **9 documentos** |
| `14-busca2-12-resultados` | Busca 2 sem filtro: **12 documentos** |
| `17-busca2-pagina2` | Segunda página da lista de 12 |
| `18-busca3-131-resultados` | Busca 3, só a expressão exata: **131 documentos** |
| `20-busca3-filtrada-70` | Busca 3 após ano, área e tipo: **70 documentos** |
| `24-busca3-5-finalistas` | Busca 3 refinada por palavra-chave: **5 documentos**, os finalistas |
| `04`, `07` a `09`, `11` a `13`, `15`, `16`, `19`, `21` a `23` | Telas intermediárias da mesma sequência, guardadas como registro |
| `busca-scopus-resultados.jpg` | Recorte comprimido do print 06, usado no slide 4 |

**Os arquivos marcados como intermediários não foram conferidos um a um.** Estão
aqui porque fazem parte do registro da sessão de busca, não porque cada um carregue
um número usado na apresentação. Os números do funil saem dos prints nomeados
acima, todos conferidos na tela.

---

## Por que guardar isso

O item 1 do enunciado pede o **passo a passo da seleção**, não só o resultado. É o
único item da atividade que é impossível de reconstruir depois: quem busca primeiro
e anota depois acaba inventando o número. Estes prints são a prova de que o funil
`131 → 70 → 5 → 1` aconteceu, na data declarada, na base declarada.
