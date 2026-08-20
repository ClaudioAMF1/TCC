# T3 — Desenho Experimental

**Título provisório (EN):** *Does a Stricter Legal Regime Change Anything? Measuring
Third-Party Tracking on Brazilian Health Websites Under LGPD Article 11*

Documento de trabalho para levar ao orientador. Complementa `TEMAS-PROPOSTOS-TCC1.md` e
`ESTADO-DA-ARTE-TEMAS.md`.

---

## 1. A ideia em um parágrafo

A LGPD trata dado de saúde como **dado pessoal sensível** (Art. 11) e impõe a ele um
regime mais estrito que o dos dados comuns (Art. 7): exige consentimento **específico e
destacado**, ou o enquadramento em uma lista curta de exceções. A pergunta é se esse
regime jurídico mais rigoroso produz **qualquer diferença técnica observável**. Sites de
hospitais, planos de saúde e laboratórios brasileiros rastreiam menos seus visitantes do
que sites comuns de porte equivalente — ou o regime especial do Art. 11 é letra morta na
camada técnica?

A hipótese de trabalho é que **não há diferença** — e demonstrar isso com medição é a
contribuição.

---

## 2. Quadrante metodológico

**Tema.** Conformidade técnica com o regime de dados pessoais sensíveis da LGPD em
serviços de saúde na web brasileira.

**Problema.** O regime mais estrito do Art. 11 da LGPD para dados sensíveis se traduz em
comportamento técnico distinguível — menos rastreadores de terceiros, consentimento mais
rigoroso, menos vazamento de URL sensível — quando comparado ao regime geral do Art. 7?

**Hipóteses.**

- **H1** — Não há diferença estatisticamente significativa na prevalência de rastreadores
  de terceiros pré-consentimento entre sites sujeitos ao Art. 11 (saúde) e sites de
  controle sujeitos ao Art. 7, controlando por porte e uso de plataforma de consentimento.
- **H2** — A maioria dos sites de saúde brasileiros **não atende ao critério explícito da
  ANPD** de oferecer botão de recusa facilmente visível, e uma fração relevante dos que
  oferecem recusa **não a respeita tecnicamente** — continua carregando rastreadores após
  a recusa.
- **H3** — Ocorre vazamento de URL semanticamente sensível (páginas de especialidade
  médica, busca de sintomas, agendamento) para domínios de terceiros, configurando
  transmissão de dado de saúde inferível sem base legal adequada.

**Marco teórico.** Três corpos que hoje não se conversam:

1. **Medição de conformidade de consentimento** — a literatura europeia sobre GDPR
   (estudo longitudinal de 4 anos, taxonomia de *dark patterns* de Nouwens et al. na CHI,
   análise automatizada em larga escala na USENIX Security 2024, Cookiescanner).
2. **Rastreamento em sites de saúde** — a literatura norte-americana, robusta e de alto
   impacto: estudo em *Health Affairs* com 6.162 sites de hospitais dos EUA concluindo que
   **98,6%** transmitiam informação sensível a terceiros; investigação do The Markup sobre
   o Meta Pixel; pesquisa da Rutgers ligando pixels de rastreamento a **46% mais risco de
   vazamento**.
3. **Regime jurídico brasileiro** — LGPD Arts. 7 e 11, e o **Guia Orientativo "Cookies e
   Proteção de Dados Pessoais"** da ANPD (out/2022).

---

## 3. Por que este tema resiste à checagem de estado da arte

**O que já está feito.** O fenômeno é bem documentado — nos **Estados Unidos**, sob a
**HIPAA**. A metodologia de medição é madura e replicável. A conformidade brasileira com a
LGPD já foi medida uma vez, mas de forma agregada, num estudo de 10 países e 9.488 sites
que concluiu que a LGPD é pouco efetiva por ausência de fiscalização.

**O que não está feito, e é o seu espaço:**

1. **Ninguém mediu o Brasil sob o Art. 11.** Nenhum estudo isolou o regime de dado sensível
   brasileiro nem testou se ele produz efeito observável.
2. **O desenho comparativo não existe.** Os estudos americanos mediram hospitais *sozinhos*
   — sem grupo de controle. Sem controle, não se sabe se 98,6% é ruim ou se é simplesmente
   o comportamento padrão da web inteira. **Adicionar o grupo de controle é a sua
   contribuição metodológica**, e ela também vale para a literatura internacional.
3. **A ANPD deu um critério objetivo que ninguém verificou.** O Guia Orientativo diz que o
   usuário deve ter **botão facilmente visível para recusar cookies não necessários**. Isso
   é um requisito nacional, concreto e automaticamente mensurável — e não há medição
   publicada de quantos sites brasileiros o cumprem.

**Você tem ainda uma linha de base numérica de comparação pronta: 98,6%.** Poder dizer "nos
EUA sob HIPAA foi 98,6%; no Brasil sob LGPD Art. 11 foi X" é o tipo de frase que sustenta
um trabalho inteiro.

---

## 4. Corpus

Desenho **caso–controle pareado**. Alvo: ~500 sites por grupo.

### Grupo A — regime Art. 11 (dado sensível)

| Estrato | Fonte do cadastro |
|---|---|
| Hospitais públicos e privados | CNES / DataSUS (cadastro nacional, público) |
| Operadoras de planos de saúde | ANS (lista pública de operadoras ativas) |
| Laboratórios e clínicas diagnósticas | cadastros setoriais + busca estruturada |
| Farmácias online e telemedicina | listagem por setor |

Estratificar por **público vs. privado** — a hipótese secundária de que o setor público se
comporta diferente do privado é interessante por si só e defende bem em banca.

### Grupo B — controle, regime Art. 7

Sites brasileiros de porte comparável, **pareados** por posição em ranking de tráfego
(lista Tranco) e, quando possível, por CMS e por presença de plataforma de gestão de
consentimento. O pareamento é o que impede a crítica óbvia — "você comparou hospital
pequeno com portal grande".

---

## 5. Cenários de medição

Cada site é visitado em quatro condições. **É aqui que mora o rigor do trabalho.**

| Cenário | O que mede |
|---|---|
| **C1 — sem interação** | O que carrega **antes de qualquer consentimento**. É o teste central: rastreador presente aqui é tratamento sem base legal. |
| **C2 — após aceitar tudo** | Linha de base do que o site pretende carregar. |
| **C3 — após recusar tudo** | Mede se a recusa é **tecnicamente respeitada**. É onde a literatura europeia encontra as falhas mais graves. |
| **C4 — navegação interna** | Visita a página de especialidade médica ou busca de sintoma. Onde o vazamento é mais grave: a própria URL revela condição de saúde. |

O C4 é o cenário que diferencia este trabalho de mais um estudo de banner de cookie. Uma
URL como `/oncologia/tratamento` transmitida a um domínio de publicidade **é, ela própria,
dado de saúde inferível sobre o visitante**.

---

## 6. Variáveis

**Dependentes:**

- Presença de rastreador de terceiro em C1 (binária) — desfecho primário
- Número de domínios de terceiros distintos contactados
- Presença de rastreadores específicos de alto impacto (Meta Pixel, Google Analytics/Ads,
  TikTok, LinkedIn)
- Cookies depositados antes do consentimento, por categoria
- Vazamento de URL sensível em C4 (binária + contagem)
- Existência de banner de consentimento
- **Recusa em um clique disponível** (critério explícito da ANPD)
- **Recusa efetivamente respeitada** (comparação C3 × C1)
- Existência de política de cookies acessível

**Independente principal:** grupo (A = Art. 11 vs. B = Art. 7).

**Controles:** porte/ranking, público vs. privado, uso de plataforma de consentimento,
país de hospedagem, CMS.

---

## 7. Ferramental

| Função | Ferramenta |
|---|---|
| Automação de navegador | **Playwright** com Chromium — captura de requisições de rede, cookies e DOM |
| Identificação de rastreadores | EasyPrivacy, EasyList, DuckDuckGo Tracker Radar, Disconnect |
| Classificação de cookies | Open Cookie Database |
| Ranking de tráfego para pareamento | lista Tranco |
| Corpus de saúde | CNES/DataSUS, cadastro de operadoras da ANS |
| Análise | Python (pandas, statsmodels) |

**Custo: zero.** Tudo aberto e gratuito. **Hardware: irrelevante** — a sua máquina é muito
mais do que suficiente; isto roda em qualquer notebook.

**Volume:** ~1.000 sites × 4 cenários = ~4.000 visitas. A ~30 s por visita, com 8 execuções
paralelas, são cerca de **4 a 6 horas de coleta**. Prevendo repetições e falhas, reserve
alguns dias — não semanas.

---

## 8. Plano de análise

| Hipótese | Método |
|---|---|
| **H1** | Comparação de proporções entre grupos (qui-quadrado / exato de Fisher), seguida de **regressão logística** com os controles da Seção 6. O que interessa é o coeficiente do grupo: ele sobrevive ao controle por porte e por uso de plataforma de consentimento? Reportar razão de chances com intervalo de confiança. |
| **H2** | Estatística descritiva da conformidade com o critério da ANPD; e a comparação C3 × C1 para medir **recusa desrespeitada**, que é o achado com mais impacto prático. |
| **H3** | Classificação das URLs de C4 por sensibilidade semântica (protocolo de codificação escrito), cruzada com transmissão a terceiros. Validação manual de amostra. |
| Comparação internacional | Confronto direto do número brasileiro com os 98,6% do estudo norte-americano, discutindo as diferenças de regime (HIPAA × LGPD) e de desenho amostral. |

**Congele o plano de análise antes de olhar os dados** e registre isso no texto.

---

## 9. Ética e limites legais — leia antes de escrever uma linha de código

Esta seção não é formalidade. Ela **precisa** estar no projeto desde o Capstone I, porque
a banca vai perguntar, e porque delimita o que você pode fazer.

**O que o trabalho faz:** visita páginas **públicas** com um navegador automatizado e
observa quais requisições de rede o próprio site dispara. É medição passiva — exatamente o
que qualquer visitante provoca ao abrir a página.

**O que o trabalho NÃO faz, em nenhuma hipótese:**

- ❌ **Não autentica em portal de paciente.** Os estudos americanos encontraram Meta Pixel
  *dentro* de portais autenticados. Você **não vai** replicar essa parte. Acesso a área
  restrita sem autorização é invasão de dispositivo informático (Lei 12.737/2012).
- ❌ Não coleta dado pessoal real de terceiros. O sujeito observado é o **site**, não
  pessoas. O único "usuário" é o crawler.
- ❌ Não explora falha, não testa injeção, não faz varredura de porta. Não é pentest.
- ❌ Não submete formulário com dado real, nem realiza agendamento.

**Divulgação responsável.** Se a medição identificar vazamento grave e atribuível a uma
instituição específica, o caminho correto é notificar a instituição — e possivelmente a
ANPD — **antes** da publicação, e reportar os resultados de forma agregada ou anonimizada.
Discuta o critério com o orientador e registre a decisão no texto. Essa discussão, aliás,
é conteúdo acadêmico legítimo e valoriza o trabalho.

**Robots.txt e taxa de requisição.** Respeite; limite a frequência; identifique o
*user-agent* como pesquisa acadêmica. Documente essas escolhas.

---

## 10. Ameaças à validade

| Ameaça | Tratamento |
|---|---|
| **Robustez do crawler** — sites quebram, exigem CAPTCHA, detectam automação | Amostra com folga (colete mais que o alvo); **registre as falhas explicitamente** e reporte a taxa de perda. Falha registrada é dado; falha silenciosa é viés. |
| **Detecção e interação com banner** | Banners variam muito. Combine heurísticas de seletor com listas de plataformas de consentimento conhecidas e valide manualmente uma amostra da detecção. |
| **Pareamento imperfeito** entre grupos | Justifique os critérios; rode análise de sensibilidade com pareamentos alternativos. |
| **Geolocalização** | O comportamento muda conforme o país do visitante. Colete de IP brasileiro e declare isso — medir da Europa daria outro resultado. |
| **Instantâneo temporal** | A web muda. Colete em janela curta e registre as datas. Se der, repita a coleta ao fim para medir estabilidade. |
| **Classificação de sensibilidade em C4** é subjetiva | Protocolo escrito, validação manual, e — se possível — segundo codificador em subamostra. |

---

## 11. Divisão entre Capstone I e Capstone II

### Capstone I — entrega em **03/12/2026**

1. Revisão sistemática dos **três** corpos teóricos da Seção 2 — é o capítulo mais denso e
   o que o orientador pode revisar com autoridade.
2. Análise jurídico-técnica: o que exatamente os Arts. 7 e 11 da LGPD e o Guia Orientativo
   da ANPD exigem, **traduzido em critérios verificáveis automaticamente**. Essa tradução
   é, sozinha, uma contribuição — e é o coração do encaixe com um orientador de formação
   jurídica.
3. Protocolo de medição completo e congelado, com plano de análise.
4. Seção de ética e limites legais escrita.
5. **Piloto**: crawler funcionando ponta a ponta em ~50 sites, com os quatro cenários.

### Capstone II — 2027.1

Coleta completa, análise estatística, comparação internacional, discussão e publicação do
conjunto de dados como artefato.

---

## 12. Por que este tema encaixa com o orientador

Se a escolha for o professor Izycki, o encaixe é direto e verificável no currículo:

- **Graduação em Direito (UFPR) e especialização em Direito Eletrônico** — a metade
  jurídica do trabalho (Seção 11, item 2) é o terreno dele.
- **Leciona disciplinas híbridas de segurança cibernética para alunos de Direito e Relações
  Internacionais no IDP** — a interface direito/tecnologia é literalmente o que ele ensina.
- **Quinze anos de análise de risco em infraestrutura crítica no GSI/PR** — dá substância à
  discussão de impacto, especialmente para os hospitais públicos do corpus.

A divisão de trabalho fica natural: ele orienta a tradução jurídica e o enquadramento; você
executa a medição. É exatamente o que o Art. 22, §2º do Regulamento define como papel do
orientador — marco teórico e produção do texto.

---

## 13. Primeiros passos

| Quando | O quê |
|---|---|
| Esta semana | Ler o **Guia Orientativo da ANPD** (out/2022) inteiro e extrair dele a lista de requisitos que dá para verificar automaticamente. É a base do trabalho. |
| Esta semana | Montar um piloto de crawler com Playwright em ~20 sites e confirmar que você consegue capturar requisições de terceiros e detectar banner. |
| Esta semana | Verificar a acessibilidade dos cadastros CNES e ANS — é o equivalente aqui do "teste de corpus" que recomendei para o T2. Faça antes de fechar o tema. |
| Até 25/08 | Levar este documento ao orientador, junto com o piloto. |
| Oficina de 01–03/09 | Usar a oficina de bases para montar a busca sistemática dos três corpos teóricos. |
| Seminário de 29/09 | Apresentar o estudo do *Health Affairs* ou o da USENIX Security 2024 — cumpre a atividade avaliativa e adianta a revisão. |

---

## Referências iniciais

- [Guia Orientativo: Cookies e Proteção de Dados Pessoais — ANPD (out/2022)](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf/@@download/file)
- [Automated Large-Scale Analysis of Cookie Notice Compliance (USENIX Security 2024)](https://www.usenix.org/system/files/usenixsecurity24-bouhoula.pdf)
- [Dark Patterns after the GDPR: Scraping Consent Pop-ups and Demonstrating their Influence (CHI 2020)](https://dl.acm.org/doi/fullHtml/10.1145/3313831.3376321)
- [Facebook Is Receiving Sensitive Medical Information from Hospital Websites — The Markup](https://themarkup.org/pixel-hunt/2022/06/16/facebook-is-receiving-sensitive-medical-information-from-hospital-websites)
- [Beyond the click: Pixel tracking technologies and patient data security in hospitals](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12687351/)
- [Invisible Codes on Hospital Websites Put Patient Data at Risk — Rutgers](https://research.rutgers.edu/news/invisible-codes-hospital-websites-put-patient-data-risk)
- [Cookiescanner: An Automated Tool for Detecting and Evaluating GDPR Consent Notices](https://arxiv.org/pdf/2309.06196)
- [Estudo comparativo de 10 países incluindo Brasil (2026)](https://arxiv.org/html/2604.18633)
