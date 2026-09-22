# Registro da busca e das métricas

Itens 1 e 2 do enunciado: como o artigo foi encontrado, por que ele é relevante e
como o veículo é classificado. Cada número aqui tem data e um print em
`pesquisa/`. Conferido tela a tela em 22/09/2026.

---

## 1. Acesso

**Portal de Periódicos da CAPES, via CAFe, com a credencial do IDP.** O item 1 exige
base acessada pela CAFe e cita Web of Science, ScienceDirect, ACM, Scopus e IEEE
Xplore. O Google Scholar não está nessa lista: ele aparece só no item 2, para o h5.
Por isso a busca foi no **Scopus**.

O endereço nas telas é `www-scopus-com.ez279.periodicos.capes.gov.br`. O prefixo
`ez279` é o proxy institucional da CAPES, e é a prova de que o acesso foi pela CAFe.

Prints: `pesquisa/0-acesso/`.

---

## 2. A busca — 21/09/2026, das 08:46 às 09:11

### As três tentativas

| | String | Resultados | Prints |
|---|---|---|---|
| 1 | `"third-party tracking" AND consent AND android` | **4** | `busca-1/` |
| 2 | `"third party" AND tracking AND android AND (consent OR GDPR)` | **12** (9 com filtro de área e tipo) | `busca-2/` |
| **3** | `"third-party tracking"`, depois refinada com `consent` | **131 → 5** | `busca-3/` |

Todas no campo *Article title, Abstract, Keywords*.

**As duas primeiras foram estreitas demais.** Expressão exata mais três termos
obrigatórios devolve 4 documentos, o que não mostra triagem nenhuma. A terceira abre
para 131 e depois estreita, que é como uma busca sistemática deve ser.

### O funil

```
131   "third-party tracking", sem filtro                          print 18 · 09:07
 ↓    ano 2018–2026 · Computer Science · Conference paper + Article
 70                                                               print 20 · 09:09
 ↓    palavras-chave Third Parties e Third-party Tracking
 39                                                               print 21 · 09:10
 ↓    acrescenta o termo consent à string · ano passa a 2018–2025
  5   finalistas                                                  print 23 · 09:11
 ↓    leitura de título e resumo
  1   selecionado
```

**O último corte é uma decisão de método, não um filtro de interface.** O recorte do
TCC é consentimento, então o termo entra na string. O print 23 mostra a caixa de busca
com `consent` e o total na mesma tela.

### Os cinco finalistas

| # | Artigo | Veículo | Ano | Cit. | Decisão |
|---|---|---|---|---|---|
| 1 | An Empirical Measurement of Cookie Banners Potential Legal Violations in EU vs US Websites | LNCS 15995 | 2025 | 0 | ❌ é web, não Android |
| 2 | A Comprehensive Study on Third-Party User Tracking in Mobile Applications | ACM ICPS | 2023 | 10 | ❌ menos citado |
| **3** | **Freely Given Consent?** — Nguyen, Backes, Stock | **CCS** | **2022** | **52** | ✅ **selecionado** |
| 4 | A fait accompli? An empirical study into the absence of consent to third-party tracking in Android apps | SOUPS | 2021 | 34 | ❌ ICORE A (2026), abaixo do A\* da CCS |
| 5 | Protecting privacy on the web: A study of HTTPS and Google Analytics implementation in academic library websites | Online Information Review | 2018 | 23 | ❌ é web, não Android |

Item 1 no print 23; itens 2 a 5 no print 24.

**Critérios.** Incluir: artigo original com medição empírica, rastreamento por
terceiros em Android, veículo revisado por pares. Excluir: revisão de literatura,
foco só em web ou iOS, preprint.

Aplicados aos cinco, dois saem por serem web (1 e 5). Dos três Android, o da CCS tem
mais citações e o veículo de classificação mais alta.

**A alternativa mais séria é o Kollnig et al. (SOUPS 2021).** Poder dizer
*"considerei e descartei, com o número"* vale mais que apresentar um artigo isolado:
34 citações contra 52, e SOUPS **A** contra CCS **A\*** na mesma edição do ICORE.

> **A comparação usa a mesma edição para os dois.** A SOUPS era **B** no CORE2020, no
> CORE2021 e no CORE2023, e subiu para **A** no ICORE2026 (print
> `metricas/11-core-portal-soups-a-icore2026`). Como o rank da CCS citado é o do
> ICORE2026, o da SOUPS também tem de ser. O registro anterior dizia "CORE B", o que
> misturava edições.

> **O artigo de 2026 no IEEE S&P** sobre plataformas de gestão de consentimento, com
> **0 citações**, aparece na busca 2 (print 10). É a prova de que recência e citações
> se excluem por construção: um artigo novo não teve tempo de ser citado.

### Duas correções de registro, feitas em 22/09

1. O funil registrado antes era `131 → 70 → 5`, com o corte final atribuído às
   palavras-chave. Os prints mostram o degrau de **39** e o termo `consent`.
2. A tabela de finalistas tinha o **WhisperTest** (CCS 2025, iOS), que é das buscas 1
   e 2. O quinto finalista é o artigo sobre *cookie banners*.

Os dois erros foram de registro, não de busca. As telas sempre mostraram o certo.

---

## 3. Métricas do artigo — relevância quantitativa

| Base | Citações | Data | Print |
|---|---|---|---|
| ACM Digital Library | **42** | 17/09/2026 | `metricas/01` |
| Scopus | **52** | 17/09/2026 | `metricas/04` |
| Google Acadêmico | **99** (9 versões) | 17/09/2026 | `metricas/05` |

Downloads na ACM: 1.539, na mesma tela.

**A ordem 42 < 52 < 99 é a cobertura de cada base, não erro.** A ACM conta só o
próprio acervo. O Scopus acrescenta IEEE, Springer, Elsevier e outros. O Google
Acadêmico agrupa nove versões do mesmo trabalho e conta teses, relatórios e preprints.

**No Scopus, o DOI tem de ir em *All fields*.** No campo de título e resumo ele
devolve zero (`metricas/03`), porque DOI não é título.

### Por que é artigo original

O item 1 define original como o que relata pela primeira vez uma pesquisa inédita.
Três fontes independentes confirmam:

| Fonte | O que diz | Print |
|---|---|---|
| ACM Digital Library | etiqueta **RESEARCH-ARTICLE** | `metricas/02` |
| Scopus | tipo de documento **Conference Paper** | `metricas/04` |
| O próprio artigo | corpus de 239.381 apps e ferramenta construídos pelos autores | — |

### O veículo tem quatro nomes

| Onde | Como aparece |
|---|---|
| Atas do artigo | ACM **SIGSAC Conference** on Computer and Communications Security (CCS '22) |
| Scopus | Proceedings of the **ACM Conference** on Computer and Communications Security |
| Google Scholar Metrics e CAPES | **ACM Symposium** on Computer and Communications Security |
| ICORE | ACM Conference on Computer and Communications Security |

A sigla **CCS** é o que amarra os quatro. E há um evento diferente com nome parecido,
a **AsiaCCS** (*ACM Asia Conference on...*), com h5 41. Pegar a linha errada seria
apresentar 41 no lugar de 90.

---

## 4. Métricas do veículo — item 2

A CCS é **conferência**. O enunciado dá dois caminhos, e o tipo de veículo decide
qual vale. Para conferência: h5 no Google Scholar, Qualis correspondente e rank no
CORE.

| Métrica | Valor | Data | Print |
|---|---|---|---|
| **h5** | **90** (mediana 146), posição 5 | 17/09/2026 | `metricas/06` |
| **Qualis** | **A1** (Qualis Eventos, Computação, 2017–2020) | 22/09/2026 | `metricas/07` |
| **CORE** | **A\*** (ICORE2026) | 17/09/2026 | `metricas/09` |

### h5

Google Acadêmico → Principais publicações → *Engineering & Computer Science* →
**Computer Security & Cryptography**:

| Posição | Publicação | h5 | Mediana |
|---|---|---|---|
| 1 | USENIX Security Symposium | 116 | 170 |
| 2 | Computers & Security *(periódico)* | 112 | 164 |
| 3 | IEEE Symposium on Security and Privacy | 110 | 195 |
| 4 | IEEE Trans. on Information Forensics and Security *(periódico)* | 100 | 140 |
| **5** | **ACM Symposium on Computer and Communications Security** | **90** | **146** |
| 19 | ACM Asia Conference on Computer and Communications Security | 41 | 66 |

A lista mistura periódicos e conferências. **Entre as conferências, a CCS é a 3ª**,
atrás só da USENIX Security e da IEEE S&P.

O h5 é **do veículo**, não do artigo. Artigo tem citações; veículo tem h5.

### Qualis

A CAPES classifica a CCS diretamente:

| | |
|---|---|
| Documento | *Relatório Reunião — Qualis Eventos — Computação*, quadriênio **2017–2020** |
| Endereço | `gov.br/capes/pt-br/centrais-de-conteudo/documentos/avaliacao/09012022_RELATORIOQUALISEVENTOS20172020COMPUTACAO.PDF` |
| Página | **9** de 44 |
| Linha | CCS · ACM Symposium on Computer and Communications Security · **A1** |

**Duas ressalvas para dizer antes que ela pergunte:**

1. **É o Qualis Eventos, não o Qualis Periódicos.** O enunciado pede "Qualis
   Periódicos correspondente ao índice h5". O Periódicos classifica revistas, e a CCS
   é conferência. Para conferências da Computação, o instrumento da CAPES é o Qualis
   Eventos, com a mesma escala de estratos (A1 a B4).
2. **O A1 é do quadriênio 2017–2020.** Ele não é uma conversão do h5 90 de hoje.

**Por que não converter o h5 em percentil.** Seria o caminho literal do enunciado, e
ele não se sustenta com o que está disponível. O Scholar publica só as 20 primeiras
de cada subárea: a posição 5 numa lista truncada não dá o percentil dentro do
conjunto real de veículos da área. O próprio Documento Técnico do Qualis Periódicos
(p. 12) reconhece o problema. A CAPES montou uma base ampliada, o "Universo", para
ter a posição real, e essa base não é pública. Qualquer conversão feita aqui
dependeria do tamanho de um universo que não foi demonstrado. Por isso o estrato
apresentado é o que a CAPES publicou, com a fonte, e não um percentil calculado.

A escala de estratos do Qualis Periódicos (Figura 6, p. 13 do Documento Técnico) está
em `metricas/08`, para referência.

### CORE

ICORE Conference Portal, `portal.core.edu.au/conf-ranks/12/`:

| | |
|---|---|
| Acrônimo | CCS |
| **Rank ICORE2026** | **A\*** |
| Field of Research | 4604 — Cybersecurity and privacy |
| Fonte DBLP | `dblp.uni-trier.de/db/conf/ccs` (não `asiaccs`) |

**A\* em todas as edições desde 2008**, com uma exceção: o ERA2010 deu A. A
classificação é estável, não um acaso de uma edição.

### O caminho de periódico não se aplica

JIF Percentile e Highest Percentile são métricas de **revista**. No Scopus *Sources*,
que busca veículos e não artigos, a busca pelo título do artigo devolve zero
(`metricas/10`). A CCS não é periódico, então esse ramo do enunciado não se aplica.

---

## 5. Referência

NGUYEN, Trung Tin; BACKES, Michael; STOCK, Ben. Freely Given Consent? Studying
Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps.
In: ACM SIGSAC CONFERENCE ON COMPUTER AND COMMUNICATIONS SECURITY (CCS '22), 2022,
Los Angeles. **Proceedings** [...]. New York: ACM, 2022. p. 2369–2383. DOI:
10.1145/3548606.3560564.

**Versão usada: a da ACM** (PDF `3548606.3560564`, 15 páginas). A cópia dos autores
no CISPA tem pelo menos uma diferença de texto: a segunda pergunta de pesquisa diz
*"Do these ... can be"*, e a versão da ACM diz *"Can these ... be"*. As citações e
páginas da apresentação seguem a ACM.
