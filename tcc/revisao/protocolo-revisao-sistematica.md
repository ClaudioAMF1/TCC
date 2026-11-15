# Protocolo da revisão sistemática

**Versão 1.7, 15/11/2026.** Segue as diretrizes de Kitchenham e Charters (2007)
para revisões sistemáticas em engenharia de software, com bola de neve conforme
Wohlin (2014) e relato do fluxo conforme o PRISMA 2020 (PAGE et al., 2021).

**Estado:** escrito, aguardando a revisão do orientador. Depois da primeira
busca, toda alteração entra na Seção 12, com data e motivo, e a versão sobe.

---

## 1 Contexto e objetivo

O projeto de pesquisa apresenta uma lacuna (Seção 1.3 e referencial teórico) e apoia quatro
hipóteses em resultados de outros trabalhos. A revisão existe para confirmar ou
corrigir essa lacuna e para dar a cada hipótese a base de comparação que ela
precisa: como outros detectam rastreadores (H4), que taxas encontram e contra
que linha de base (H1), como confrontam o detectado com o declarado (H2) e o
que já se sabe de aplicativos de governo (H1 e H3). Ela também fornece os
critérios jurídicos que o plano prevê para a LGPD.

**Busca exploratória.** Antes deste protocolo, uma busca exploratória achou
Samarasinghe et al. (2022), que analisaram 1.166 aplicativos Android de governo
de 71 países. Esse trabalho não estava entre os consultados quando a lacuna foi
escrita, e a lacuna foi revista por causa dele. É o motivo de a QR4 cobrir
aplicativos de governo de qualquer país, e não só do Brasil, e um sinal de que
a busca não pode se limitar aos trabalhos já conhecidos.

---

## 2 Questões de pesquisa

| QR | Pergunta | Serve a | String |
|---|---|---|---|
| QR1 | Como os estudos detectam SDKs de rastreamento e bibliotecas de terceiros em aplicativos Android, e como verificam a validade dessas detecções (verdade de referência, conferência manual, concordância entre ferramentas)? | H4 | S1 |
| QR2 | Que proporção de aplicativos com ao menos um rastreador os estudos reportam, em que populações, com que fonte de pacotes e contra que linha de base? | H1 | S2 |
| QR3 | Como os estudos confrontam os SDKs ou os fluxos de dados detectados com a política de privacidade ou com os rótulos de privacidade da loja, e que taxas de inconsistência encontram? | H2 | S3 |
| QR4 | Que estudos examinam rastreamento por terceiros ou privacidade em aplicativos publicados por governos, inclusive os de enfrentamento da COVID-19, e o que encontram? | H1, H3, lacuna | S4a, S4b |
| QR5 | Que trabalhos tratam do rastreamento ou da privacidade em aplicativos no Brasil ou à luz da LGPD, ou da transferência internacional de dados coletados por aplicativos? | Discussão jurídica; critérios dos Arts. 7º, 11 e 33 | S5a, S5b |

**PICOC** (KITCHENHAM; CHARTERS, 2007):

| Elemento | Definição |
|---|---|
| População | Aplicativos móveis, com prioridade para Android |
| Intervenção | Detecção ou medida de rastreamento por terceiros: SDKs, bibliotecas, domínios, fluxos de dados |
| Comparação | Entre populações (governo e comercial, categorias), entre ferramentas, entre o declarado e o detectado |
| Resultados | Prevalência; precisão, revocação e concordância dos detectores; taxa de inconsistência; destinos e jurisdição |
| Contexto | Estudos publicados de 2015 a 2026, de qualquer país; governo e Brasil com destaque |

---

## 3 Fontes

| Fonte | Por que entra | Strings |
|---|---|---|
| Scopus | Maior base multidisciplinar; indexa a maior parte dos anais da ACM e do IEEE e periódicos de direito e de políticas públicas. É a base principal. | S1 a S5b |
| ~~ACM Digital Library~~ | **Saiu na versão 1.1** (Seção 12.3): sem acesso à exportação. Os anais da ACM ficam cobertos pelo Scopus | (S1 a S4b) |
| IEEE Xplore | Anais e periódicos do IEEE (S&P, EuroS&P, TDSC, TSE) | S1 a S4b |
| SBC OpenLib (SOL) | Anais do SBSeg, do WebMedia e do SBES e o JISA, onde se publica a pesquisa brasileira da área | SOL1 a SOL3 |
| BDTD (IBICT) | Teses e dissertações brasileiras | BDTD1, BDTD2 |
| Bola de neve | Para trás (referências) e para a frente (quem cita), a partir dos incluídos | Seção 7.4 |

O Google Acadêmico não é base de busca, porque o resultado não é reproduzível;
ele é usado só na bola de neve para a frente ("Citado por") e para localizar
texto completo.

**Contingência.** Se não houver acesso ao Scopus pelo Portal de Periódicos da
CAPES, as strings S5a e S5b rodam no Google Acadêmico, com os 200 primeiros
resultados por relevância registrados, e o desvio entra na Seção 12.

---

## 4 Strings de busca

### 4.1 Como foram construídas

Os termos saem do PICOC e das palavras-chave dos estudos do conjunto de
controle (Seção 5). Cada string tem um bloco de aplicativo, um bloco do
fenômeno e, quando o fenômeno sozinho traz ruído, um bloco de contexto. Três
escolhas evitam ruído conhecido:

- `tracker*` sozinho traz "fitness tracker", "eye tracker" e "symptom tracker".
  Por isso ele só aparece junto de um bloco que o restringe (privacidade na S2,
  política de privacidade na S3, governo na S4a, Brasil na S5a) ou é trocado
  por frases (S1, S4b).
- `tracking` sozinho traz rastreamento de objetos e de localização. Ele só
  aparece em frase ("third-party track*").
- A S4b, de aplicativos da COVID-19, não usa `privacy`, porque o desenho de
  protocolos de rastreamento de contatos é uma literatura grande e fora do
  escopo; ela exige bibliotecas de terceiros, vazamento ou análise de código.

No Scopus, o hífen é ignorado dentro de frases entre aspas, então
`"third-party"` também acha "third party". Na ACM e no IEEE as duas formas são
escritas.

### 4.2 Scopus (busca avançada)

Toda string do Scopus termina com o filtro **F**:

```
AND PUBYEAR > 2014 AND PUBYEAR < 2027 AND ( DOCTYPE ( ar ) OR DOCTYPE ( cp ) OR DOCTYPE ( re ) ) AND ( LANGUAGE ( english ) OR LANGUAGE ( portuguese ) )
```

**S1, métodos de detecção (QR1):**

```
TITLE-ABS-KEY ( ( android OR app OR apps OR "mobile application*" ) AND ( "third-party librar*" OR "third-party SDK*" OR "third-party component*" OR "third-party track*" OR "tracking librar*" OR "tracking SDK*" OR ( tracker* W/3 ( detect* OR identif* ) ) OR "librar* detection" OR "SDK detection" ) AND ( detect* OR identif* OR recogni* ) AND ( evaluat* OR compar* OR accura* OR precision OR recall OR "ground truth" OR benchmark* OR agreement OR "false positive*" OR reliab* ) )
```

**S2, prevalência (QR2):**

```
TITLE-ABS-KEY ( ( app OR apps OR android OR "mobile application*" OR smartphone* OR "mobile ecosystem" ) AND ( "third-party track*" OR tracker* OR "tracking librar*" OR "tracking SDK*" OR "advertising librar*" OR "ad librar*" OR "analytics librar*" OR "analytics SDK*" ) AND ( privacy OR "personal data" OR "data protection" OR gdpr OR lgpd OR consent OR "third-part*" ) )
```

**S3, declarado e detectado (QR3):**

```
TITLE-ABS-KEY ( ( app OR apps OR android OR "mobile application*" ) AND ( "privacy polic*" OR "data safety" OR "privacy label*" OR "nutrition label*" ) AND ( "third-part*" OR tracker* OR sdk* OR librar* OR "data flow*" OR code ) AND ( inconsisten* OR discrepanc* OR mismatch* OR complian* OR violat* ) )
```

**S4a, aplicativos de governo (QR4):**

```
TITLE-ABS-KEY ( ( government* OR "e-government" OR "m-government" OR "public sector" OR "public service*" OR "public administration" ) AND ( app OR apps OR android OR "mobile application*" ) AND ( tracker* OR "third-part*" OR "personal data" OR leak* OR "privacy polic*" OR "privacy analys*" OR "privacy assessment*" OR "static analys*" OR "dynamic analys*" ) )
```

**S4b, aplicativos da COVID-19 (QR4):**

```
TITLE-ABS-KEY ( ( "contact tracing" OR "contact-tracing" OR covid* OR coronavirus OR "sars-cov-2" ) AND ( app OR apps OR android OR "mobile application*" ) AND ( "third-part* librar*" OR "third-part* SDK*" OR "third-part* track*" OR "third-part* service*" OR "data leak*" OR "privacy leak*" OR "static analys*" OR "dynamic analys*" ) )
```

**S5a, Brasil e LGPD (QR5):**

```
TITLE-ABS-KEY ( ( lgpd OR "Lei Geral de Proteção de Dados" OR "General Data Protection Law" OR brazil* OR brasil* ) AND ( app OR apps OR android OR "mobile application*" OR aplicativo* ) AND ( privacy OR privacidade OR tracker* OR rastreador* OR "personal data" OR "dados pessoais" OR "third-part*" OR "data protection" OR "proteção de dados" ) )
```

**S5b, soberania e transferência internacional (QR5):**

```
TITLE-ABS-KEY ( ( "data sovereignty" OR "digital sovereignty" OR "data localization" OR "data localisation" OR "cross-border data" OR "international data transfer*" OR "transborder data" ) AND ( app OR apps OR android OR "mobile application*" OR tracker* OR "third-part* track*" ) )
```

### 4.3 ACM Digital Library e IEEE Xplore

As mesmas strings, sem curinga dentro de aspas (as duas bases não aceitam ou
não documentam isso) e com as variantes escritas. Na ACM, a string vai inteira
na caixa **Edit Query** da busca avançada, com o campo `Abstract`. No IEEE, ela
vai no **Command Search**, sem o prefixo `Abstract:(...)`, com o campo padrão
*All Metadata*. O período (2015 a 2026) é aplicado pelo filtro de data de cada
base.

**S1:**

```
Abstract:((android OR app OR apps OR "mobile application" OR "mobile applications") AND ("third-party library" OR "third-party libraries" OR "third party library" OR "third party libraries" OR "third-party SDK" OR "third-party SDKs" OR "third-party tracking" OR "tracker detection" OR "library detection") AND (detect* OR identif*) AND (evaluat* OR compar* OR accura* OR precision OR recall OR "ground truth" OR benchmark*))
```

**S2:**

```
Abstract:((app OR apps OR android OR "mobile application" OR "mobile applications" OR smartphone*) AND ("third-party tracking" OR "third party tracking" OR tracker* OR "tracking library" OR "tracking libraries" OR "tracking SDK" OR "advertising libraries" OR "ad libraries" OR "analytics libraries") AND (privacy OR "personal data" OR GDPR OR LGPD OR consent OR "third-party" OR "third party"))
```

**S3:**

```
Abstract:((app OR apps OR android) AND ("privacy policy" OR "privacy policies" OR "data safety" OR "privacy label" OR "privacy labels" OR "nutrition label" OR "nutrition labels") AND ("third-party" OR "third party" OR tracker* OR SDK* OR librar* OR "data flow" OR "data flows" OR code) AND (inconsisten* OR discrepanc* OR mismatch* OR complian* OR violat*))
```

**S4a:**

```
Abstract:((government* OR "e-government" OR "m-government" OR "public sector" OR "public service" OR "public services") AND (app OR apps OR android OR "mobile application" OR "mobile applications") AND (tracker* OR "third-party" OR "third party" OR "personal data" OR leak* OR "privacy policy" OR "privacy analysis" OR "static analysis" OR "dynamic analysis"))
```

**S4b:**

```
Abstract:(("contact tracing" OR covid* OR coronavirus) AND (app OR apps OR android OR "mobile application" OR "mobile applications") AND ("third-party libraries" OR "third party libraries" OR "third-party SDKs" OR "third-party tracking" OR "third-party trackers" OR "data leak" OR "data leaks" OR "static analysis" OR "dynamic analysis"))
```

### 4.4 SOL e BDTD

As duas aceitam AND, OR, aspas e curinga no fim da palavra. Os anais da SBC
têm artigos em português e em inglês, por isso há uma string em cada língua.

| Id | Base | String |
|---|---|---|
| SOL1 | SOL | `(rastreador* OR "bibliotecas de terceiros" OR "SDKs de terceiros") AND (aplicativo* OR android)` |
| SOL2 | SOL | `(tracker* OR "third-party libraries" OR "third-party tracking") AND (app OR apps OR android)` |
| SOL3 | SOL | `(LGPD OR "proteção de dados") AND (aplicativo* OR android OR app OR apps)` |
| BDTD1 | BDTD | `(aplicativo* OR android OR "aplicações móveis") AND (rastreador* OR "bibliotecas de terceiros" OR "SDKs de terceiros")` |
| BDTD2 | BDTD | `(aplicativo* OR android) AND (LGPD OR "Lei Geral de Proteção de Dados") AND (governo OR "setor público" OR "administração pública" OR "dados pessoais")` |

---

## 5 Conjunto de controle

As strings são validadas contra um conjunto de estudos que precisam ser
achados, conforme a ideia de padrão quase-ouro de Zhang, Babar e Tell (2011).
Os estudos foram escolhidos antes da busca, entre os já citados no projeto e os
achados na busca exploratória.

| Id | Estudo | Tem de ser achado por |
|---|---|---|
| C01 | Binns et al. (2018), WebSci | S2 |
| C02 | Razaghpanah et al. (2018), NDSS | S2 |
| C03 | Kollnig et al. (2021a), Internet Policy Review | S2 |
| C04 | Kollnig et al. (2021b), SOUPS | S2 |
| C05 | Nguyen, Backes e Stock (2022), CCS | S2 |
| C06 | Zhan et al. (2020), ASE | S1 |
| C07 | Zimmeck et al. (2019), PoPETs | S3 |
| C08 | Slavin et al. (2016), ICSE | S3 |
| C09 | Samarasinghe et al. (2022), WWW | S4a, S2 |
| C10 | Serrano, Betarte e Campo (2023), LADC | S4a, S4b |
| C11 | Serrano, Betarte e Campo (2024), JISA | S4b |

**Regra.** Depois da busca, o script `scripts/revisao_triagem.py controle`
mostra quais estudos de controle foram recuperados e por qual string. Para cada
estudo não recuperado:

1. busca-se o título exato na base;
2. se a base **indexa** o estudo e a string não o achou, a string falha: o termo
   que faltou é acrescentado, a mudança vai para a Seção 12 e a string roda de
   novo, em todas as bases;
3. se a base **não indexa** o estudo, é limite de cobertura e não de string; o
   estudo entra pela bola de neve e o caso é reportado.

A revocação reportada é o número de estudos achados dividido pelo número de
estudos indexados em ao menos uma base. A meta é 100% antes de seguir para a
triagem. S5a e S5b não têm estudo de controle conhecido; são exploratórias, e
isso é declarado.

**Refinamento previsto.** Se, depois de tirar as duplicatas, sobrarem mais de
1.500 registros, a string com mais resultados é limitada às áreas de Ciência da
Computação, Ciências Sociais e Engenharia do Scopus (`SUBJAREA ( comp OR soci OR engi )`),
desde que o conjunto de controle continue inteiro. A decisão e as contagens de
antes e de depois vão para a Seção 12.

---

## 6 Critérios de inclusão e exclusão

Um registro é incluído quando atende a **todos** os critérios de inclusão e a
**nenhum** de exclusão.

| Código | Critério de inclusão |
|---|---|
| IC1 | Estudo primário que mede, detecta ou analisa rastreamento por terceiros, bibliotecas ou SDKs de terceiros, ou fluxos de dados pessoais em aplicativos móveis (QR1 a QR4); ou trabalho que analisa a LGPD ou a transferência internacional de dados aplicada a aplicativos ou serviços digitais (QR5) |
| IC2 | Publicado em periódico ou evento com revisão por pares, ou tese ou dissertação defendida |
| IC3 | Escrito em inglês ou português |
| IC4 | Publicado de 2015 a 2026 (vale para a busca nas bases; ver 7.4) |

| Código | Critério de exclusão |
|---|---|
| EC1 | Duplicata ou versão anterior de estudo incluído. Fica a versão mais completa; a de evento e a de periódico do mesmo estudo são registradas juntas |
| EC2 | Não trata de aplicativos móveis (só web, só desktop, dispositivo sem aplicativo). Exceção: trabalhos jurídicos da QR5 |
| EC3 | "Rastreamento" em outro sentido: localização física, olhar, objetos, contatos sem análise do aplicativo, acompanhamento de saúde ou de atividade física sem medida de terceiros |
| EC4 | Usa a detecção de bibliotecas só como meio para outro fim (malware, reempacotamento, clones), sem medir rastreamento e sem avaliar a detecção |
| EC5 | Mede só a percepção ou a intenção de uso das pessoas (questionário, entrevista, modelo de aceitação), sem nenhuma medida sobre os aplicativos |
| EC6 | Resumo, pôster, artigo curto de até 4 páginas, editorial, tutorial ou palestra; preprint sem revisão por pares (exceção: 7.4) |

Texto completo não obtido não é critério de exclusão. O texto é procurado pelos
links da planilha, pelo Portal de Periódicos da CAPES (Acesso CAFe) e por cópias
dos autores; sem nenhuma dessas fontes, o registro é contado como "não
recuperado" no fluxograma do PRISMA 2020 e listado por `id`, sem pedido ao
autor. Na `triagem_20261106.csv`, fica com `decisao_f2` vazia e `NR` em
`criterio_f2`. O código EC7, que previa esse pedido, saiu na versão 1.6 sem ter sido
aplicado.

Um registro que não atende a um critério de inclusão é excluído com o código
desse critério (IC1 a IC4). Quando mais de um código se aplica, usa-se o mais
específico: um estudo de malware que usa bibliotecas só como filtro é EC4, e
não IC1; o IC1 fica para o que está fora do tema e não cabe em EC2 a EC5.

Revisões da literatura que aparecerem na busca não são incluídas como estudo
primário; elas são registradas com a marca `R` e servem de ponto de partida da
bola de neve.

---

## 7 Procedimento de seleção

### 7.1 Fases

| Fase | O que se lê | Decisão |
|---|---|---|
| F0 | Nada: junção das exportações e remoção de duplicatas pelo script | Automática, por DOI e por título normalizado |
| F1 | Título, resumo e palavras-chave | `I` inclui, `E` exclui (com critério), `T` talvez e `R` revisão para bola de neve. Na dúvida, `T`. `I` e `T` seguem para F2 |
| F2 | Texto completo | `I` ou `E`, com o código do critério |
| F3 | Bola de neve a partir dos incluídos em F2 | Os novos achados passam por F1 e F2 |

Cada decisão de exclusão leva o código de um único critério, o mais
específico (Seção 6). Isso permite contar os excluídos por critério no
fluxograma do PRISMA.

### 7.2 Confiabilidade com um revisor

A seleção tem um revisor responsável. Como a classificação F1 registrada não foi produzida inteiramente pelo autor (Seção 7.3), a consistência da triagem é examinada por uma **conferência cega por amostra**, e não por teste e reteste.

1. **Conferência cega.** O autor classifica, sem consultar as decisões registradas, uma amostra aleatória de 10% dos registros, no mínimo 30. Para 1.249 registros, o arredondamento para cima resulta em **125**. A amostra foi preparada em 13/11/2026 com semente **20261116**, usando `random.Random(20261116).sample` sobre a ordem do CSV e ordenação dos sorteados por `id`. O arquivo `dados/revisao/reteste_F1_20261116.xlsx` (o nome foi mantido para não romper o manifesto) contém apenas os dados bibliográficos e campos de resposta vazios. O manifesto registra a versão da fonte, o algoritmo e os identificadores. Não há intervalo mínimo: a conferência pode ser feita assim que possível.
2. **Conferência do orientador.** Se houver disponibilidade, decidir os 20 registros de `dados/revisao/conferencia_orientador_20261110.xlsx`, sem consultar as respostas do autor. Se não ocorrer, registrar essa limitação; não apresentar a etapa como executada.

Após o preenchimento, comparar com `decisao_f1` por `id` (`python3 scripts/revisao_triagem.py concordancia dados/revisao/reteste_F1_20261116.xlsx`) e reportar matriz de contingência, acordo observado, κ de Cohen (COHEN, 1960), tamanho da amostra e divergências. A comparação principal será **I/T versus E/R**, isto é, segue ou não para F2 como estudo primário. Também serão descritas as quatro categorias. Cada divergência é examinada; a decisão final fica registrada com a decisão anterior, a nova e o motivo. Se κ < 0,6, uma segunda amostra de 125 registros, sorteada com nova semente, será conferida da mesma forma, e a limitação será reportada. O limiar é uma regra operacional do protocolo, não garantia de validade. Se κ for indefinido por ausência de variação, reportar isso, sem atribuir zero ou um arbitrariamente.

### 7.3 Versões das decisões

Os arquivos preservam a classificação inicial sugerida e a versão posteriormente revista na conferência das planilhas. A versão consultada contém decisões para os 1.249 registros. A conferência cega da Seção 7.2 estima o quanto essas decisões coincidem com as do autor.

As alterações devem manter identificador, data, decisão anterior, nova decisão, critério e motivo. Uma concordância entre versões não equivale à concordância entre avaliadores independentes.

### 7.4 Bola de neve

Segue Wohlin (2014): para cada incluído em F2, examinam-se as referências (para
trás) e os trabalhos que o citam no Google Acadêmico e no Scopus (para a
frente). Os achados novos passam por F1 e F2. A iteração se repete até não
surgir estudo novo, com limite de duas iterações por causa do prazo; se o
limite for atingido com estudos novos ainda aparecendo, isso é reportado como
ameaça.

Na bola de neve, um estudo anterior a 2015 ou um preprint sem versão revisada
pode ser incluído se atender ao IC1 e for citado por ao menos dois estudos já
incluídos. É a forma de não perder os trabalhos fundadores da área.

---

## 8 Avaliação de qualidade

Cada estudo empírico incluído recebe uma nota por pergunta: 1 (sim), 0,5 (em
parte) ou 0 (não).

| Código | Pergunta |
|---|---|
| QA1 | O objetivo e as perguntas do estudo estão explícitos? |
| QA2 | A população de aplicativos está descrita: fonte, critério de seleção, tamanho e data da coleta? |
| QA3 | Os pacotes analisados são identificáveis (versão, hash ou lista publicada)? |
| QA4 | O método de detecção é reproduzível: ferramenta, versão, base de assinaturas e regra de casamento? |
| QA5 | A detecção foi validada (verdade de referência, conferência manual ou comparação entre ferramentas), com números? |
| QA6 | Há inferência: intervalo de confiança, teste ou comparação com linha de base? |
| QA7 | As ameaças à validade são discutidas? |
| QA8 | Os dados ou o código estão disponíveis? |

A nota vai de 0 a 8. Ela **não** exclui estudos: aparece na tabela dos
incluídos e é usada na síntese da QR2, que é reportada com e sem os estudos de
nota menor que 4. Trabalhos não empíricos da QR5 (análises jurídicas) não
recebem nota; são identificados como tal e usados na discussão jurídica.

As perguntas QA4 e QA5 medem diretamente o que a H4 discute. A distribuição das
notas nelas é, por si, um resultado da revisão.

---

## 9 Extração de dados

O formulário é uma planilha com uma linha por estudo incluído:

| Campo | Conteúdo |
|---|---|
| id, referência | Identificador da triagem e referência ABNT |
| QR | Quais perguntas o estudo responde |
| população | Domínio dos aplicativos, país ou loja, tamanho, governo ou não |
| fonte dos pacotes | Google Play, AndroZoo, outra; data da coleta |
| tipo de análise | Estática, dinâmica ou as duas |
| detector | Ferramenta, versão, base de assinaturas, unidade de detecção (classe, domínio, fluxo) |
| validação | Se houve, como, e os números (precisão, revocação, concordância) |
| prevalência | Proporção de aplicativos com ao menos um rastreador; média por aplicativo; principais rastreadores |
| linha de base | Se houve grupo de comparação e como foi pareado |
| declarado e detectado | Fonte da declaração (política, rótulo da loja) e taxa de inconsistência |
| destinos e jurisdição | Se mediu para onde os dados vão e em que país |
| marco legal | GDPR, LGPD, CCPA ou nenhum; artigos usados |
| limitações | As declaradas pelos autores |
| QA1 a QA8 | Notas da Seção 8 |
| uso no TCC | Qual hipótese o estudo apoia ou contesta, e onde será citado |

---

## 10 Síntese

A síntese é narrativa e organizada por QR, com uma tabela por pergunta. Não há
metanálise: as ferramentas, as bases de assinaturas e as populações diferem
entre os estudos, e essa heterogeneidade é justamente o objeto da H4. Juntar
taxas produzidas por detectores diferentes seria assumir o que a H4 testa.

| QR | Produto da síntese |
|---|---|
| QR1 | Tabela ferramenta × forma de validação × números; quantos estudos validam a detecção |
| QR2 | Tabela de prevalência por estudo, com população, fonte, detector e linha de base; quantos estudos têm linha de base |
| QR3 | Taxas de inconsistência entre o declarado e o detectado, com o método de cada estudo |
| QR4 | Tabela dos estudos de governo: países, número de aplicativos, método, principais achados, o que fica em aberto |
| QR5 | Lista dos artigos da LGPD discutidos e dos critérios propostos, que alimenta a atividade de 17/11 a 23/11 do plano |

O último produto é o confronto com a lacuna da Seção 1.2 do projeto: cada um
dos pontos que ela afirma em aberto é confirmado ou corrigido, com os estudos
que sustentam a decisão.

---

## 11 Cronograma das etapas pendentes

Situação em 13/11/2026: a F1 tem decisões registradas; a F2 tem **79 propostas em 357 registros: 71 I e 8 E**, ainda não conferidas pelo autor. Restam 278 decisões em aberto: 131 por acesso, duas por versão divergente, duas por dúvida de escopo e 143 T cujo tratamento será definido com o orientador. Foram obtidos 80 textos correspondentes. R0375 é a exclusão adicional por duplicidade comprovada em R0192, sem texto próprio obtido. Não houve contato com autores. Desde a versão 1.6, texto não obtido conta como não recuperado, sem exclusão (Seção 6). A revisão sistemática, a extração e a avaliação de qualidade permanecem em andamento. Ver `dados/revisao/LEIA-ME_leitura_F2_20261113.md` e o registro por ID.

| Prazo previsto | Atividade | Condição |
|---|---|---|
| Até 23/11 | Conferência cega dos 125 registros (Seção 7.2) | Calcular κ só depois do preenchimento; examinar cada divergência |
| Até 23/11 | Definir com o orientador o tratamento dos 143 T | Registrar a decisão e a justificativa |
| 16/11 a 01/12 | Obter os textos pelo Portal de Periódicos da CAPES; conferir as 79 propostas; decidir os 4 casos pendentes; ler os demais; extração e qualidade | Não chamar proposta de inclusão final antes da conferência |
| 25/11 a 02/12 | Bola de neve a partir dos incluídos; síntese por QR na Seção 2 do projeto; fluxograma PRISMA final | Explicitar no texto o que ficar pendente |
| A combinar | Conferência de 20 registros pelo orientador | Opcional, conforme disponibilidade |
| Até 03/12 | Entregar o projeto com o estado real da revisão | Não apresentar etapas futuras como concluídas |

O prazo não dispensa a fundamentação e revisão bibliográfica exigidas pelo Art. 25, §3º. O orientador deverá avaliar a suficiência da síntese para a entrega; o cronograma não equivale a dispensa institucional.

---

## 12 Registros

### 12.1 Buscas executadas

| Data | Base | String | Resultados | Arquivo | Observação |
|---|---|---|---|---|---|
| 06/11/2026 | Scopus | S1 | 135 | `scopus_S1_20261106.csv` | 133 únicos. As 2 duplicatas são da própria exportação: um artigo com o mesmo DOI nos anais do PLDI e no SIGPLAN Notices, e um estudo com versão de evento (2018) e de periódico (2019) com o mesmo título |
| 06/11/2026 | Scopus | S2 | 299 | `scopus_S2_20261106.csv` | Junto com a S1: 434 registros, 18 duplicatas, 416 únicos |
| 06/11/2026 | Scopus | S3 | 83 | `scopus_S3_20261106.csv` | |
| 06/11/2026 | Scopus | S4a | 173 | `scopus_S4a_20261106.csv` | |
| 06/11/2026 | Scopus | S4b | 29 | `scopus_S4b_20261106.csv` | S1 a S4b juntas: 719 registros, 54 duplicatas, 665 únicos |
| 06/11/2026 | Scopus | S5a | 43 | `scopus_S5a_20261106.csv` | |
| 06/11/2026 | Scopus | S5b | 63 | `scopus_S5b_20261106.csv` | Scopus completo: 825 registros, 62 duplicatas, 763 únicos, todos com resumo |
| 06/11/2026 | IEEE Xplore | S1 | 152 | `ieee_S1_20261106.csv` | 96 fora do Scopus |
| 06/11/2026 | IEEE Xplore | S2 | 191 | `ieee_S2_20261106.csv` | 129 fora do Scopus |
| 06/11/2026 | IEEE Xplore | S3 | 85 | `ieee_S3_20261106.csv` | 54 fora do Scopus |
| 06/11/2026 | IEEE Xplore | S4a | 220 | `ieee_S4a_20261106.csv` | 178 fora do Scopus |
| 06/11/2026 | IEEE Xplore | S4b | 20 | `ieee_S4b_20261106.csv` | Scopus e IEEE juntos: 1.493 registros, 279 duplicatas, 1.214 únicos. O IEEE traz mais ruído: o campo *All Metadata* inclui os termos de indexação do IEEE e a base aplica radicalização ("governance" casa com `government*`). Só um terço dos registros do IEEE satisfaz a string em título, resumo e palavras-chave do autor sem esses dois efeitos. Um filtro automático foi testado e descartado, porque excluiria registros relevantes, como um estudo de aplicativos de *e-governance*. O ruído fica para a triagem |
| 06/11/2026 | ACM | S1 | 52 | (não exportado) | A busca roda na edição gratuita, mas a exportação de citações exige assinatura que o IDP não tem. Ver 12.3 |
| 06/11/2026 | BDTD | BDTD1 | 7 | `bdtd_BDTD1_20261106.csv` | Pela API pública da BDTD (`bdtd.ibict.br/vufind/api/v1/search`, campo AllFields, filtro 2015 a 2026) |
| 06/11/2026 | BDTD | BDTD2 | 16 | `bdtd_BDTD2_20261106.csv` | Idem. Scopus, IEEE e BDTD juntos: 1.516 registros, 279 duplicatas, 1.237 únicos |
| 06/11/2026 | SOL | SOL1 | 1 | `sol_SOL1_20261106.csv` | Transcrito da tela de resultados, que o site não exporta |
| 06/11/2026 | SOL | SOL2 | 5 | `sol_SOL2_20261106.csv` | Idem; inclui C11 |
| 06/11/2026 | SOL | SOL3 | 9 | `sol_SOL3_20261106.csv` | Idem. **Fim das buscas: 1.531 registros (Scopus 825, IEEE 668, BDTD 23, SOL 15), 282 duplicatas, 1.249 únicos para a triagem.** Conjunto de controle: 10 de 11 recuperados; o que falta (C07) não é indexado pelo Scopus e entra pela bola de neve |

### 12.2 Conjunto de controle

| Id | Achado? | Por qual base e string | Se não: a base indexa? | Ação |
|---|---|---|---|---|
| C01 a C05 | Sim | Scopus, S2 | | |
| C06 | Sim | Scopus, S1 | | |
| C09 a C11 | Sim | Scopus, S2 (antes das S4a e S4b) | | |
| C08 | Sim | Scopus, S3 | | |
| C07 | Não | | Não. `TITLE ( "scaling privacy compliance analysis" )` sem filtro deu 0 documentos em 06/11 | Limite de cobertura, não de string: entra pela bola de neve. Revocação no Scopus: 10 de 10 estudos indexados |

### 12.3 Alterações do protocolo

| Data | Versão | O que mudou | Por quê |
|---|---|---|---|
| 04/11/2026 | 1.0 | Versão inicial | |
| 06/11/2026 | 1.1 | A ACM Digital Library sai das fontes | A busca funciona na edição gratuita (a S1 deu 52 resultados), mas exportar as citações é recurso pago e o IDP não dá acesso à ACM. A cobertura dos anais da ACM fica com o Scopus: os seis estudos de controle publicados pela ACM (C01, C05, C06, C08, C09 e C10) foram todos recuperados nele. Trabalhos da ACM fora do Scopus entram pela bola de neve. **Pendente: concordância do orientador** |
| 06/11/2026 | 1.1 | BDTD consultada pela API pública | Mesma string e mesmo filtro de anos da interface; a API devolve o resumo, o que dispensa copiar à mão |
| 06/11/2026 | 1.1 | SOL feita à mão | O site da SBC OpenLib recusa acesso automatizado |
| 06/11/2026 | 1.1 | O texto do TCC (Seção 2.13) ainda cita a ACM e 22 buscas | Será atualizado com os números finais, ao fim das buscas |
| 06/11/2026 | 1.2 | Códigos IC1 a IC4 para exclusão por falta de critério de inclusão; regra do código mais específico | A tabela de EC não cobria o que está fora do tema sem se encaixar em EC2 a EC5 |
| 06/11/2026 | 1.2 | Classificação inicial da F1 e armazenamento de versões separadas | Preservar o histórico de decisões para conferência |
| 10/11/2026 | 1.2 | Atualização do texto com a retirada da ACM, as 17 buscas e os números da F1 | Corrigir a descrição das etapas executadas |
| 10/11/2026 | 1.3 | Separação entre a versão revista das classificações e a validação pessoal, ainda pendente | Evitar confundir versão registrada com avaliação pessoal |
| 13/11/2026 | 1.4 | Reteste cego de 125 preparado, datas condicionadas ao intervalo, comparação I/T × E/R, F2 e cronograma atualizados | Registrar a preparação sem afirmar execução ou concordância ainda não medidas |
| 13/11/2026 | 1.5 | Rodada documental F2: 71 propostas I, 8 E e registro de acesso e evidências; 143 T preservados | Distinguir propostas da validação pessoal, conferir versões e evitar exclusão por falha de acesso sem cumprir EC7 |
| 15/11/2026 | 1.6 | EC7 retirado: texto não obtido pelos links, pela CAPES (CAFe) ou por cópias dos autores conta como "não recuperado" no PRISMA, sem pedido ao autor | O PRISMA 2020 já tem essa categoria; a espera de sete dias por resposta não cabe no prazo de 03/12. Nenhum registro havia sido excluído por EC7 |
| 15/11/2026 | 1.7 | O reteste vira conferência cega por amostra, sem intervalo de sete dias e sem conferência integral prévia; κ < 0,6 leva a uma segunda amostra; Seções 7.2, 7.3, 11, 12.5 e 13 atualizadas | A classificação F1 registrada não foi produzida inteiramente pelo autor; a comparação útil é entre a avaliação cega do autor e essa classificação, e o prazo de 03/12 não comporta a conferência integral dos 1.249 registros |

### 12.4 Triagem por título e resumo (F1)

Decisões registradas em 10/11/2026, ainda sujeitas à validação pessoal, sobre os 1.249 registros de `dados/revisao/triagem_20261106.csv`.

| Decisão | Registros |
|---|---|
| I (inclui) | 214 |
| T (talvez) | 143 |
| R (revisão, para a bola de neve) | 6 |
| E (exclui) | 886: IC1 527, EC3 118, EC2 114, EC5 89, EC4 30, EC6 5, EC1 3 |
| Seguem para o texto completo (I + T) | 357 |

Entre as versões armazenadas, 148 decisões mudaram (11,8%), 125 de E para T; o κ binário entre versões é 0,712, conforme o cálculo existente em `scripts/revisao_triagem.py sugestao`. Esse resultado descreve as versões e não substitui o reteste pessoal nem a conferência do orientador.

### 12.5 Preparação da conferência cega

Em 13/11/2026, foram produzidos o XLSX, o CSV cego e o manifesto de `reteste_F1_20261116`, preparados como reteste e usados, desde a versão 1.7, como conferência cega por amostra (Seção 7.2). Fonte: commit `236470418f16b979606bb115375fdab03fcc0039`, com 1.249 registros. Os 125 campos de decisão estão vazios. κ: **não calculado**. A preparação não altera as decisões da F1.

---

## 13 Ameaças à validade da revisão

- **Um revisor só.** Mitigação pela conferência cega por amostra e, se houver disponibilidade, pela conferência do orientador (Seção 7.2). Ainda não há κ dessas etapas.
- **Textos não recuperados.** Estudos sem texto completo acessível ficam fora da síntese; são listados por `id` e contados no fluxograma do PRISMA.
- **Cobertura das bases.** NDSS, USENIX Security, SOUPS e PoPETs podem não estar
  indexados por completo no Scopus, na ACM e no IEEE. O conjunto de controle
  mede isso (C02, C04, C07) e a bola de neve compensa.
- **Língua.** As strings das bases internacionais estão em inglês; trabalhos em
  português nelas podem escapar. SOL e BDTD cobrem a produção nacional.
- **Viés de publicação.** Estudos que não acham rastreadores tendem a ser menos
  publicados, o que puxa para cima as prevalências da QR2.
- **Recorte de 2015.** Trabalhos fundadores anteriores entram pela regra de 7.4.

---

## Referências

BINNS, R. et al. Third party tracking in the mobile ecosystem. In: ACM
CONFERENCE ON WEB SCIENCE, 10., 2018, Amsterdam. **Proceedings** [...]. New
York: ACM, 2018. p. 23-31. DOI: 10.1145/3201064.3201089.

COHEN, J. A coefficient of agreement for nominal scales. **Educational and
Psychological Measurement**, v. 20, n. 1, p. 37-46, 1960. DOI:
10.1177/001316446002000104.

KITCHENHAM, B.; CHARTERS, S. **Guidelines for performing systematic literature
reviews in software engineering**. Keele: Keele University; Durham: Durham
University, 2007. (Technical Report EBSE-2007-01).

KOLLNIG, K. et al. Before and after GDPR: tracking in mobile apps. **Internet
Policy Review**, v. 10, n. 4, 2021a. DOI: 10.14763/2021.4.1611.

KOLLNIG, K. et al. A fait accompli? An empirical study into the absence of
consent to third-party tracking in Android apps. In: SYMPOSIUM ON USABLE PRIVACY
AND SECURITY, 17., 2021. **Proceedings** [...]. Berkeley: USENIX Association,
2021b. p. 181-195.

NGUYEN, T. T.; BACKES, M.; STOCK, B. Freely given consent? Studying consent
notice of third-party tracking and its violations of GDPR in Android apps. In:
ACM SIGSAC CONFERENCE ON COMPUTER AND COMMUNICATIONS SECURITY, 2022, Los
Angeles. **Proceedings** [...]. New York: ACM, 2022. p. 2369-2383. DOI:
10.1145/3548606.3560564.

PAGE, M. J. et al. The PRISMA 2020 statement: an updated guideline for
reporting systematic reviews. **BMJ**, v. 372, art. n71, 2021. DOI:
10.1136/bmj.n71.

RAZAGHPANAH, A. et al. Apps, trackers, privacy, and regulators: a global study
of the mobile tracking ecosystem. In: NETWORK AND DISTRIBUTED SYSTEM SECURITY
SYMPOSIUM, 2018, San Diego. **Proceedings** [...]. Reston: Internet Society,
2018. DOI: 10.14722/ndss.2018.23353.

SAMARASINGHE, N. et al. Et tu, Brute? Privacy analysis of government websites
and mobile apps. In: ACM WEB CONFERENCE, 2022, Lyon. **Proceedings** [...]. New
York: ACM, 2022. p. 564-575. DOI: 10.1145/3485447.3512223.

SERRANO, N.; BETARTE, G.; CAMPO, J. D. Third-party trackers in COVID-19 mobile
applications can enable privacy leaks. In: LATIN-AMERICAN SYMPOSIUM ON
DEPENDABLE AND SECURE COMPUTING, 12., 2023, La Paz. **Proceedings** [...]. New
York: ACM, 2023. p. 80-89. DOI: 10.1145/3615366.3615426.

SERRANO, N.; BETARTE, G.; CAMPO, J. D. COVID-19 mobile applications: a study of
trackers and data leaks. **Journal of Internet Services and Applications**,
v. 15, n. 1, p. 139-159, 2024. DOI: 10.5753/jisa.2024.3882.

SLAVIN, R. et al. Toward a framework for detecting privacy policy violations in
Android application code. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING,
38., 2016, Austin. **Proceedings** [...]. New York: ACM, 2016. p. 25-36. DOI:
10.1145/2884781.2884855.

WOHLIN, C. Guidelines for snowballing in systematic literature studies and a
replication in software engineering. In: INTERNATIONAL CONFERENCE ON EVALUATION
AND ASSESSMENT IN SOFTWARE ENGINEERING, 18., 2014, London. **Proceedings**
[...]. New York: ACM, 2014. p. 1-10. DOI: 10.1145/2601248.2601268.

ZHAN, X. et al. Automated third-party library detection for Android
applications: are we there yet? In: IEEE/ACM INTERNATIONAL CONFERENCE ON
AUTOMATED SOFTWARE ENGINEERING, 35., 2020. **Proceedings** [...]. New York: ACM,
2020. p. 919-930. DOI: 10.1145/3324884.3416582.

ZHANG, H.; BABAR, M. A.; TELL, P. Identifying relevant studies in software
engineering. **Information and Software Technology**, v. 53, n. 6, p. 625-637,
2011. DOI: 10.1016/j.infsof.2010.12.010.

ZIMMECK, S. et al. MAPS: scaling privacy compliance analysis to a million apps.
**Proceedings on Privacy Enhancing Technologies**, v. 2019, n. 3, p. 66-86,
2019. DOI: 10.2478/popets-2019-0037.
