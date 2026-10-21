<!--
Versão de trabalho de 20/10/2026. Texto do Projeto Capstone I (TCC I).
Contém: elementos de identificação, resumo, abstract, introdução, metodologia
das etapas já executadas, plano de atividades e referências. A formatação final
segue o modelo ABNT da instituição; este arquivo guarda o conteúdo.
-->

**INSTITUTO BRASILEIRO DE ENSINO, DESENVOLVIMENTO E PESQUISA (IDP)**
**Bacharelado em Ciência da Computação**

**CLAUDIO MEIRELES**

# QUEM MAIS ESTÁ DENTRO DO APLICATIVO? Rastreamento por terceiros e soberania de dados em aplicativos móveis governamentais brasileiros

Projeto de pesquisa apresentado à disciplina Projeto Capstone I do curso de
Bacharelado em Ciência da Computação do Instituto Brasileiro de Ensino,
Desenvolvimento e Pesquisa (IDP), como requisito parcial para a aprovação no
Trabalho de Conclusão de Curso.

Orientador: Prof. Eduardo Arthur Izycki

Brasília, 2026

---

## RESUMO

Aplicativos móveis do governo brasileiro concentram serviços para os quais o
cidadão não tem alternativa, como previdência, saúde e documentos digitais, e
parte deles trata dado pessoal sensível nos termos da Lei Geral de Proteção de
Dados Pessoais (LGPD). A literatura sobre aplicativos comerciais mostra que a
maioria embarca bibliotecas de rastreamento de terceiros, mas os estudos
consultados não examinam o parque governamental brasileiro nem comparam a
população estudada com uma linha de base pareada. Este trabalho mede a presença
de rastreadores de terceiros em aplicativos governamentais brasileiros e a
compara com a de aplicativos comerciais de mesma categoria e porte, por análise
estática de pacotes de instalação fixados por hash no acervo AndroZoo. Nesta
primeira etapa, foram construídos um corpus de 396 aplicativos candidatos, de
71 publicadores públicos das três esferas de governo, e um grupo de controle de
190 aplicativos comerciais, e foi verificado, antes de qualquer download, se
cada hipótese dispõe de instrumento e de tamanho amostral suficientes. O
principal resultado obtido até aqui é que nenhum dos 396 aplicativos
governamentais declara exibir anúncios na Google Play (IC95% de 0% a 1,0%),
contra 33,2% dos aplicativos do controle (IC95% de 26,9% a 40,1%). Como a
declaração de anúncios é um limite inferior do rastreamento, o resultado não
estima a prevalência de rastreadores, mas indica sua natureza: se houver
rastreamento nesses aplicativos, ele vem de bibliotecas de análise de uso e de
infraestrutura, e não de monetização, o que desloca o problema da
comercialização de dados para a soberania de dados. Um segundo resultado é
metodológico: a inspeção do código do MobSF mostrou que sua detecção de
rastreadores aplica a base de assinaturas do Exodus Privacy com a mesma regra de
casamento, de modo que as duas ferramentas não são detectores independentes, e o
instrumento de comparação entre detectores foi redefinido.

**Palavras-chave:** rastreamento por terceiros; aplicativos governamentais;
privacidade; LGPD; análise estática.

---

## ABSTRACT

Brazilian government mobile applications concentrate services for which citizens
have no alternative, such as social security, health care and digital
documents, and some of them process sensitive personal data as defined by the
Brazilian General Data Protection Law (LGPD). Research on commercial
applications shows that most of them embed third-party tracking libraries, but
the studies reviewed neither examine Brazilian government applications nor
compare the studied population against a matched baseline. This work measures
the presence of third-party trackers in Brazilian government applications and
compares it with that of commercial applications of the same category and size,
through static analysis of installation packages pinned by hash in the AndroZoo
collection. In this first stage, a corpus of 396 candidate applications from 71
public-sector publishers across the three levels of government and a control
group of 190 commercial applications were built, and, before any download, it
was verified whether each hypothesis has an adequate instrument and sample size.
The main result obtained so far is that none of the 396 government applications
declares showing ads on Google Play (95% CI from 0% to 1.0%), against 33.2% of
the control applications (95% CI from 26.9% to 40.1%). Since the ad declaration
is a lower bound for tracking, this result does not estimate tracker prevalence,
but it indicates its nature: if these applications contain tracking, it comes
from usage analytics and infrastructure libraries rather than monetization,
which shifts the problem from the sale of data to data sovereignty. A second
result is methodological: an inspection of the MobSF source code showed that its
tracker detection applies the Exodus Privacy signature database with the same
matching rule, so the two tools are not independent detectors, and the
instrument for comparing detectors was redefined.

**Keywords:** third-party tracking; government applications; privacy; LGPD;
static analysis.

---

## 1 INTRODUÇÃO

### 1.1 Tema

Boa parte do atendimento ao cidadão no Brasil passou a acontecer por
aplicativos móveis. O pedido de benefício previdenciário, a carteira de
vacinação, o documento de habilitação e o agendamento em unidade de saúde estão
em aplicativos publicados por órgãos federais, estaduais e municipais na
Google Play. Dois deles, Meu INSS e Meu SUS Digital, registravam mais de 50
milhões de instalações cada um na coleta feita para este trabalho em setembro de
2026.

Aplicativos Android raramente são escritos do zero. Eles incorporam kits de
desenvolvimento (SDKs) de terceiros para medir uso, registrar falhas, enviar
notificações e exibir anúncios, e esses componentes podem coletar
identificadores do dispositivo e enviá-los aos servidores de quem os fornece. A
literatura mede esse fenômeno há quase uma década. A análise de 959 mil
aplicativos da Google Play mostrou que a maioria embarca rastreadores de
terceiros, que poucos rastreadores dominantes respondem por grande parte dessa
presença e que muitos deles operam fora da jurisdição europeia (BINNS et al.,
2018). O tráfego real de aplicativos revelou serviços de rastreamento ausentes
das listas usadas para identificá-los (RAZAGHPANAH et al., 2018). Estudos
posteriores ao Regulamento Geral de Proteção de Dados europeu (GDPR)
observaram que o rastreamento pouco mudou com a nova regra, que poucas grandes
empresas continuam concentrando a capacidade de rastrear e que o consentimento
exigido raramente é obtido de forma válida (KOLLNIG et al., 2021a; KOLLNIG et
al., 2021b; NGUYEN; BACKES; STOCK, 2022).

O tema deste trabalho é o rastreamento por terceiros em aplicativos móveis
publicados por órgãos públicos brasileiros, examinado do ponto de vista da
proteção de dados e da soberania sobre os dados dos cidadãos.

### 1.2 Problema de pesquisa

**Enunciado.** Os aplicativos móveis oficiais do governo brasileiro embarcam
SDKs de rastreamento de terceiros, e em que medida esse comportamento difere do
de aplicativos comerciais de mesma categoria e porte?

**Lacuna.** A detecção de SDKs de rastreamento por análise estática é método
consolidado e já foi aplicada a aplicativos de diversos domínios comerciais. Os
trabalhos consultados até aqui têm duas lacunas em comum: estudam aplicativos
comerciais ou de saúde privada, e não o parque de aplicativos governamentais
brasileiros, que está sujeito a um regime jurídico distinto; e reportam a taxa
de rastreamento de uma população sem uma linha de base pareada, o que impede
dizer se a taxa observada é alta, baixa ou típica. A revisão sistemática
prevista no plano de atividades (Seção 3) vai confirmar ou corrigir essa
avaliação.

**Relevância.** O cidadão pode trocar de aplicativo de banco, mas não pode trocar
de aplicativo do INSS. A falta de alternativa muda o peso de qualquer coleta
feita por terceiros dentro de um serviço público, e é um argumento que a
literatura sobre aplicativos comerciais não tem como fazer.

### 1.3 Justificativa

O trabalho se justifica em três planos.

**Jurídico.** A LGPD define como sensível o dado referente à saúde e o dado
biométrico (Art. 5º, II), restringe as hipóteses de seu tratamento (Art. 11),
vincula o tratamento feito pelo poder público à sua finalidade pública
(Art. 23) e limita a transferência internacional de dados pessoais a casos
específicos (Art. 33) (BRASIL, 2018). Se um aplicativo de saúde publicado por um
órgão público envia identificadores a um terceiro, a base legal desse envio
precisa existir e ser demonstrável.

**Soberania de dados.** O rastreamento em aplicativos se concentra em poucas
grandes empresas estrangeiras, como Google e Facebook (BINNS et al., 2018;
KOLLNIG et al., 2021a). Dados de cidadãos gerados no uso de
um serviço público essencial podem, por dependência técnica assumida por padrão
no desenvolvimento Android, ser processados sob outra jurisdição. Medir a
extensão dessa dependência é condição para discuti-la.

**Metodológico.** Taxas de rastreamento publicadas por estudos diferentes são
produzidas por ferramentas diferentes. Se essas ferramentas discordam entre si,
as taxas não são comparáveis. Medir a concordância entre detectores sobre os
mesmos aplicativos dá ao trabalho uma contribuição que vai além do caso
brasileiro.

### 1.4 Objetivos

**Objetivo geral.** Medir a prevalência de SDKs de rastreamento de terceiros em
aplicativos móveis governamentais brasileiros e compará-la com a de aplicativos
comerciais pareados por categoria e faixa de instalações.

**Objetivos específicos.**

1. Consolidar e validar manualmente o corpus de aplicativos governamentais,
   documentando os critérios de inclusão e a taxa de erro da classificação
   automática.
2. Quantificar, por aplicativo, os SDKs de rastreamento detectados por análise
   estática, por esfera de governo e por tratamento de dado sensível.
3. Confrontar os SDKs detectados com o que a política de privacidade e a seção
   "Segurança dos dados" da Google Play declaram.
4. Determinar, em uma subamostra sob análise dinâmica, para quais destinos e
   jurisdições os aplicativos efetivamente transmitem dados.
5. Medir a concordância entre detectores de rastreadores e o efeito da escolha
   da ferramenta sobre a taxa reportada.

### 1.5 Hipóteses

As hipóteses foram formuladas de modo a poderem ser rejeitadas, com o critério
de decisão fixado antes da coleta dos pacotes.

| Hipótese | Enunciado | Critério de rejeição |
|---|---|---|
| H1 | Aplicativos governamentais embarcam rastreadores em taxa estatisticamente indistinguível da de aplicativos comerciais pareados, apesar do regime jurídico distinto. | Razão de taxas, no modelo ajustado por categoria e faixa de instalações, com intervalo de confiança de 95% que exclua 1. |
| H2 | Fração relevante dos SDKs detectados não está declarada na política de privacidade. | Proporção de SDKs não declarados com limite superior do IC95% abaixo de 10%. |
| H3 | Aplicativos que tratam dado sensível não apresentam menos rastreadores que os demais aplicativos governamentais. | Diferença significativa a favor dos aplicativos sensíveis, controlando por esfera e porte. |
| H4 | A concordância entre detectores sobre o mesmo pacote é baixa, de modo que a taxa reportada depende da ferramenta escolhida. | κ de Fleiss (FLEISS, 1971) maior ou igual a 0,6 e τ de Kendall (KENDALL, 1938) alto entre os ordenamentos de aplicativos produzidos por cada detector. |

Fonte: elaborado pelo autor (2026).

### 1.6 Resultados esperados

Ao final do trabalho, espera-se obter:

1. a prevalência de rastreadores no parque governamental, com intervalo de
   confiança, por esfera e por tratamento de dado sensível;
2. a razão entre as taxas de rastreadores dos aplicativos governamentais e dos
   comerciais pareados, com tamanho de efeito;
3. a proporção de SDKs detectados que não constam da declaração do publicador;
4. a medida de concordância entre detectores e o efeito da ferramenta sobre a
   taxa reportada;
5. um conjunto de dados reprodutível, com a lista dos aplicativos, os hashes dos
   pacotes analisados e os scripts de coleta e análise.

### 1.7 Limitações

- A análise estática mostra que o código de um SDK está presente no pacote, não
  que ele é executado nem que transmite dados. A subamostra dinâmica mede essa
  diferença em parte dos aplicativos.
- O estudo cobre apenas aplicativos Android distribuídos pela Google Play.
- A versão analisada é a disponível no AndroZoo, que pode ser anterior à versão
  vigente na loja. A defasagem é medida e reportada.
- O grupo de controle não é amostra aleatória do mercado comercial: foi montado
  a partir de buscas na loja por categoria, com complemento de aplicativos de
  publicadores não oficiais encontrados nas buscas iniciais.
- A declaração de anúncios na Google Play é feita pelo próprio publicador.
- A discussão jurídica identifica pontos de atenção à luz da LGPD; ela não
  substitui uma análise jurídica do caso concreto.

### 1.8 Procedimentos metodológicos

A pesquisa é quantitativa, observacional e comparativa: mede características de
artefatos de software publicamente distribuídos, sem intervir neles, e compara
dois grupos. Os procedimentos são, em ordem:

1. construção do corpus governamental a partir de buscas na Google Play e da
   expansão pelo catálogo de cada publicador oficial;
2. caracterização dos aplicativos por metadados públicos e montagem de um grupo
   de controle comercial;
3. verificação de viabilidade de cada hipótese antes do download dos pacotes;
4. obtenção dos pacotes no AndroZoo, fixados por hash (ALLIX et al., 2016;
   ALECCI et al., 2024);
5. detecção de rastreadores por mais de um detector e medida de concordância;
6. confronto com as declarações dos publicadores;
7. análise dinâmica de uma subamostra com dispositivo e conta próprios;
8. análise estatística conforme plano fixado antes da observação dos
   resultados.

As etapas 1 a 3 estão concluídas e são descritas no Capítulo 2. As demais estão
planejadas no Capítulo 3.

### 1.9 Estrutura do trabalho

Este documento tem dois capítulos além desta introdução. O Capítulo 2 descreve a
metodologia das etapas já executadas e os resultados que elas produziram. O
Capítulo 3 apresenta o plano de atividades até a defesa do Projeto Capstone I e
para o Projeto Capstone II, com os riscos identificados. Na versão final da
monografia, a revisão bibliográfica, o desenvolvimento e as conclusões serão
acrescentados como capítulos próprios.

---

## 2 METODOLOGIA DAS ETAPAS EXECUTADAS

Este capítulo descreve o que foi feito até 20 de outubro de 2026. Todos os
scripts citados estão no repositório do trabalho, na pasta `scripts/`.

### 2.1 Escolha do tema por testes de viabilidade

Antes da escolha deste tema, outros três foram testados empiricamente e
descartados com base nos dados obtidos. O critério comum foi verificar, antes de
fixar o desenho, se a variável principal de cada tema podia ser observada.

| Tema testado | Teste | Resultado |
|---|---|---|
| Sistemas de controle industrial expostos no Brasil | Contagens e facetas no Shodan | Descartado. Os mesmos hosts respondiam em vários protocolos industriais ao mesmo tempo, padrão de honeypot e de nuvem. O setor do operador, variável principal, não era observável. |
| Abuso de marca em Certificate Transparency | 20.007 entradas de log, casamento por token | Descartado. Nenhuma imitação real encontrada; a marca raramente aparece no domínio de phishing. |
| Genealogia de malware bancário brasileiro | imphash de 1.764 amostras brasileiras e 2.104 de controle | Inconclusivo. 85% do acervo brasileiro eram containers, nos quais o imphash não se aplica. |
| Aplicativos governamentais (este) | Busca e expansão por catálogo na Google Play | Viável. O publicador vem identificado pela própria loja. |

Fonte: elaborado pelo autor (2026).

A diferença decisiva do tema escolhido é que a variável que separa os grupos, o
publicador do aplicativo, vem declarada na fonte. A Google Play informa que o
aplicativo é publicado por "Prefeitura Municipal de Curitiba" ou "SERPRO", e não
há trabalho de atribuição a fazer.

### 2.2 Construção do corpus governamental

**Fonte e ferramenta.** Os metadados foram obtidos da Google Play com a
biblioteca `google-play-scraper` (JOMINGYU, 2024), com país Brasil e idioma
português. O script é `scripts/teste_viabilidade_n3.py`.

**Busca.** Foram usados 21 termos ligados a serviço público: "gov.br", "governo
federal", "governo do estado", "prefeitura", "ministério da saúde", "receita
federal", "INSS", "SUS", "detran", "tribunal", "SERPRO", "Dataprev", "carteira
digital", "cadastro único", "meu INSS", "secretaria estadual", "secretaria
municipal", "defensoria", "polícia militar", "corpo de bombeiros" e "procon",
com até 30 resultados por termo.

**Classificação do publicador.** Um aplicativo foi considerado candidato quando
o nome do publicador contém um sinal de órgão público, como "prefeitura",
"secretaria", "tribunal", "ministério" ou "detran", ou quando o publicador
consta de uma lista de órgãos conhecidos cujo nome não tem esses sinais. Essa
lista existe porque o publicador do portal gov.br federal, responsável por Meu
INSS e Meu SUS Digital, se chama "Serviços e Informações do Brasil", e as
empresas públicas de tecnologia, como a Celepar (Paraná) e a Prodam (município de
São Paulo), também não têm sinal no nome. O casamento é feito por palavra inteira, e não por trecho de texto: a
primeira versão, que casava trechos, incluiu um aplicativo da Yandex entre os
órgãos públicos e excluiu o publicador do gov.br. O erro foi corrigido e está
registrado no histórico do repositório.

**Expansão por catálogo.** Para cada publicador classificado como oficial,
foi feita uma busca pelo nome exato do publicador, mantendo apenas os
aplicativos cujo publicador coincide exatamente. A busca por termo encontra uma
amostra; a busca pelo publicador encontra o catálogo dele.

**Resultado (3 de setembro de 2026).** Foram localizados 590 aplicativos
distintos. Destes, 396 têm publicador classificado como órgão público, de 71
publicadores distintos. Esses 396 são candidatos: a validação manual do vínculo
institucional é a primeira atividade do plano (Seção 3.1).

### 2.3 Caracterização do corpus

Em 17 de setembro de 2026, a ficha completa de cada um dos 396 candidatos foi
obtida na Google Play, sem nenhuma remoção. O script é
`scripts/teste_viabilidade_n3_robusto.py`, e cada aplicativo recebeu três
classificações automáticas.

**Esfera de governo**, pelo nome do publicador, testando primeiro os sinais
municipais, depois os estaduais e por último os federais, porque "municipal" é
menos ambíguo que "secretaria". Resultado: 85 federais, 206 estaduais, 95
municipais e 10 indeterminados (2,5%).

**Tratamento de dado sensível**, por palavras-chave no título e na descrição,
em quatro grupos: saúde, biometria, previdência e assistência social. Resultado:
152 aplicativos (38,4%) em ao menos um grupo; 125 em saúde, 28 em previdência,
17 em biometria e 5 em assistência social (um aplicativo pode estar em mais de
um grupo). O critério automático é mais amplo que o da LGPD: previdência e
assistência social não são, por si, dado sensível no sentido do Art. 5º, II. A
validação manual vai aplicar a definição legal e reportar as duas contagens.
Mesmo pelo critério estrito, o grupo de saúde sozinho tem 125 aplicativos.

**Faixa de instalações**, em escala logarítmica, pela ordem de grandeza do
número mínimo de instalações informado pela loja (10⁰, 10¹, …, 10⁹). Dois
aplicativos não informam instalações.

### 2.4 Grupo de controle comercial

Para cada categoria da loja presente no corpus governamental, foram buscados
aplicativos comerciais com o nome da categoria combinado a termos genéricos
("app", "grátis", "brasil", "online", "digital", "fácil"), percorrendo os
resultados alternadamente pelo início e pelo fim da lista. Aplicativos de
publicadores oficiais foram excluídos. Foram aceitos até 8 aplicativos por
categoria, com no máximo 2 por faixa de instalações, para espalhar o controle ao
longo das faixas.

A busca da loja ordena por relevância e quase nunca devolve um aplicativo
comercial com poucas instalações. Para cobrir as faixas de 10² a 10⁵, o controle
foi complementado com aplicativos de publicadores não oficiais encontrados na
busca inicial, até 12 por faixa. O controle final tem 190 aplicativos, 22 deles
vindos desse complemento. Como esses 22 foram encontrados por termos ligados a
governo, o controle não é amostra aleatória do mercado, e isso entra nas
limitações (Seção 1.7).

### 2.5 Verificação de viabilidade por hipótese

Antes de baixar qualquer pacote, foi verificado se cada hipótese tem
instrumento. Os critérios foram escritos no script antes da rodada completa.

| Condição | Hipótese | Critério | Resultado |
|---|---|---|---|
| Fichas obtidas | todas | não aplicável | 396 de 396 |
| Menor célula esfera × sensibilidade, nos três níveis de esfera | H3 | ≥ 5 | 35 |
| Aplicativos com dado sensível | H3 | ≥ 30 | 152 (38,4%) |
| Aplicativos governamentais dentro da amplitude de faixas coberta pelo controle | H1 | ≥ 60% | 364 de 394 (92,4%) |
| Política de privacidade acessível (resposta HTTP 200) | H2 | ≥ 60% | 323 de 396 (81,6%) |

Fonte: elaborado pelo autor (2026).

As quatro hipóteses têm instrumento. Três ressalvas acompanham esse resultado.

**Suporte comum.** As duas populações têm portes diferentes, e isso é
propriedade do mundo, não do coletor: um aplicativo de prefeitura de cidade
pequena tem poucas centenas de instalações.

| Faixa de instalações | Governo | Controle |
|---|---|---|
| 10⁰ a 10¹ | 30 | 0 |
| 10² a 10⁵ | 308 | 63 |
| 10⁶ a 10⁹ | 56 | 127 |
| Total | 394 | 190 |

Fonte: elaborado pelo autor (2026).

Os 30 aplicativos abaixo de qualquer controle (7,6%) ficam fora da comparação da
H1, pelo procedimento de restrição ao suporte comum, e permanecem na H3, que
compara aplicativos governamentais entre si. O critério da tabela considera
apenas a faixa. Exigida a sobreposição dentro de cada categoria, a cobertura
registrada cai para 27,4%. Ampliar o controle dentro das categorias mais
frequentes é atividade do plano (Seção 3.1).

**Políticas de privacidade.** Das 323 políticas acessíveis, 321 estão em HTML e
uma em PDF. Entre as que falharam, 27 responderam HTTP 403 e 15 com
redirecionamento, o que indica bloqueio do agente automático ou mudança de
endereço, e não ausência de documento. A conferência manual tende a elevar a
taxa.

**Poder estatístico.** A menor diferença detectável entre duas proporções, com
poder de 80% e α de 0,05 bilateral, foi calculada por aproximação normal com os
364 aplicativos governamentais em suporte comum e os 190 do controle. Ela
depende da taxa de base, que ainda não é conhecida:

| Taxa de base | 10% | 30% | 50% | 70% | 90% |
|---|---|---|---|---|---|
| Menor diferença detectável | 9,2 p.p. | 12,1 p.p. | 12,3 p.p. | 10,5 p.p. | 6,0 p.p. |

Fonte: elaborado pelo autor (2026).

O valor de 5,1 pontos percentuais registrado na proposta usava taxa de base de
1%, que vem da proporção de anúncios e é otimista para rastreadores em geral. O
pior caso é 12,3 pontos. Diferenças menores que isso não serão detectadas com o
tamanho atual, e essa limitação será declarada.

### 2.6 Sinal preliminar: declaração de anúncios

A Google Play informa, para cada aplicativo, se ele contém anúncios. Exibir
anúncio exige SDK de publicidade, que é rastreador; a recíproca não vale, porque
um SDK de análise de uso não exibe anúncio. A declaração é, portanto, um limite
inferior do rastreamento.

| Grupo | Com anúncio | Proporção | IC95% (Wilson) |
|---|---|---|---|
| Governo (n = 396) | 0 | 0,0% | 0,0% a 1,0% |
| Controle comercial (n = 190) | 63 | 33,2% | 26,9% a 40,1% |

Fonte: elaborado pelo autor (2026).

Os intervalos foram calculados pelo método de Wilson (1927), adequado a
proporções próximas de zero. Eles não se sobrepõem. O resultado não testa a H1,
que trata de rastreadores em geral, mas informa a natureza do que se espera
encontrar: se os aplicativos governamentais tiverem rastreadores, eles serão de
análise de uso, registro de falhas e infraestrutura, e não de publicidade. Isso
descarta o enquadramento de que o governo vende dados do cidadão e concentra o
trabalho na questão de soberania: dados gerados no uso de um serviço público
sendo enviados a terceiros sem finalidade comercial, por dependência técnica.

### 2.7 Correções feitas no instrumento

A verificação de viabilidade reprovou duas hipóteses, H1 e H3, por defeito do
próprio instrumento, e não por falta de dados. Foram três correções:

1. **Controle concentrado nas faixas altas.** A primeira versão do critério da
   H1 exigia par exato por célula de categoria e faixa e reprovou com 45,8%. As
   falhas estavam todas nas faixas baixas, porque a busca da loja não devolvia
   aplicativos comerciais pequenos. A coleta passou a percorrer o fim da lista de
   resultados e ganhou o complemento descrito na Seção 2.4.
2. **Critério mais estrito que a análise.** A H1 será testada por regressão com
   categoria e faixa como covariáveis, que exige sobreposição entre as
   distribuições, e não par exato. O critério foi alinhado ao plano de análise, e
   os dois números (por faixa e por categoria) são reportados lado a lado.
3. **Categoria residual no mínimo.** A menor célula da H3 era "indeterminado ×
   sensível", com 3 aplicativos. "Indeterminado" não é nível do fator esfera, e
   sim o que a heurística não classificou. Entre os três níveis reais, a menor
   célula tem 35.

A lição registrada é que um critério de decisão pode reprovar por defeito
próprio, e que a defesa contra isso é inspecionar a distribuição das falhas, e
não apenas o valor agregado. Como os critérios 1 e 2 foram alterados depois da
primeira rodada, os valores anteriores e posteriores são reportados, e o
protocolo da etapa seguinte será congelado antes do download dos pacotes.

### 2.8 Acesso ao AndroZoo

O AndroZoo é um acervo acadêmico de pacotes Android que permite obter uma versão
específica de um aplicativo pelo hash SHA-256 (ALLIX et al., 2016; ALECCI et
al., 2024). Isso torna o corpus reconstruível por outros pesquisadores, o que a
coleta direta da loja não permite, porque a loja substitui o pacote a cada
atualização. O acesso foi solicitado em 16 de setembro de 2026 e concedido em
17 de setembro de 2026. A chave de acesso é individual, não é compartilhada e
não é gravada no repositório; os scripts a leem de uma variável de ambiente.

### 2.9 Verificação dos detectores de rastreadores

A proposta previa três ferramentas para a H4: MobSF, Androguard e Exodus
Privacy (EXODUS PRIVACY, 2026). Antes do piloto, o código de cada uma foi examinado para saber se elas
são, de fato, detectores independentes. Duas constatações mudaram o desenho.

**O MobSF usa a base do Exodus.** No MobSF 4.5.3 (MOBSF, 2026), a detecção de
rastreadores está em `mobsf/MalwareAnalyzer/views/Trackers.py`. O módulo baixa
a base de rastreadores da API do Exodus Privacy, lista as classes de cada
arquivo DEX e aplica a cada classe as expressões regulares de assinatura de
código dessa base. É a mesma base e a mesma regra de casamento do Exodus, e o
pacote do MobSF inclui a licença do exodus-core, a biblioteca de análise do
próprio Exodus. A cópia da base distribuída com o pacote tem 432 rastreadores: 428 com assinatura
de código e 260 com assinatura de rede. Comparar MobSF e Exodus mede apenas
diferenças de implementação, e a concordância entre eles tende a ser alta por
construção.

**O Androguard não é detector.** O Androguard (ANDROGUARD, 2026) extrai classes,
textos e recursos de um pacote; ele não tem base de rastreadores. Ele é o
extrator sobre o qual os detectores trabalham.

**Instrumento redefinido para a H4.** Para que a comparação separe o efeito da
base de assinaturas do efeito do método de detecção, o piloto usa três
detectores:

| Detector | Base | Método |
|---|---|---|
| A | Exodus Privacy | assinatura de código nas classes do DEX |
| B | Exodus Privacy | assinatura de rede nos domínios presentes nos textos do pacote |
| C | Disconnect (DISCONNECT, 2026), mantida por outra organização | lista de domínios aplicada aos mesmos textos de B |

Fonte: elaborado pelo autor (2026).

A diferença entre A e B mede o efeito do método com a base fixa; a diferença
entre B e C mede o efeito da base com o método fixo. O MobSF entra como
verificação de implementação do detector A. A lista da Disconnect é usada nas
categorias de publicidade, análise de uso e impressão digital invasiva; as
categorias de conteúdo e redes sociais ficam de fora porque incluem domínios de
uso geral, como `google.com` e `facebook.com`, que gerariam falso positivo em
quase todo aplicativo. Essa escolha é parâmetro do script e é reportada, porque
ela própria afeta a taxa.

O ensaio do pipeline já mostrou um efeito de método. Na base do Exodus, a
assinatura de rede do rastreador "Google Ads" é a expressão `\.google\.com`,
que casa com qualquer subdomínio do Google. Em um dos APKs de teste, um link
para `maps.google.com` bastou para o detector B apontar "Google Ads", enquanto
o detector A, que procura o código do SDK, não encontrou nada. Por isso o
script registra, para cada detecção, a classe ou o domínio que a produziu, e as
detecções do piloto serão conferidas à mão.

### 2.10 Piloto do pipeline de análise

O piloto previsto para o Projeto Capstone I passa 20 aplicativos pelos
detectores e produz números preliminares de concordância. O script
`scripts/piloto_androzoo.py` foi escrito e testado de duas formas: um autoteste
com dados sintéticos, que cobre a leitura da lista do AndroZoo, os três
detectores, o sorteio e as medidas de concordância, com os valores de
referência conferidos nas bibliotecas SciPy e statsmodels; e um ensaio de
todas as etapas com dois APKs públicos de teste do projeto Androguard. Ele executa cinco etapas:

1. **Cobertura:** lê a lista pública do AndroZoo, verifica quais aplicativos do
   corpus e do controle estão no acervo e escolhe, para cada um, a versão de
   maior código de versão vinda da Google Play;
2. **Amostra:** sorteia, com semente fixa, 14 aplicativos governamentais
   estratificados por esfera e sensibilidade e 6 do controle;
3. **Download:** baixa cada pacote pelo hash e confere o SHA-256 do arquivo
   recebido;
4. **Detecção:** aplica os detectores A, B e C a cada pacote;
5. **Concordância:** calcula o κ de Fleiss sobre a presença de ao menos um
   rastreador e o τ de Kendall entre os ordenamentos de aplicativos por número
   de rastreadores.

O ambiente em que este texto foi preparado não tem acesso de rede ao AndroZoo
nem à API do Exodus, e o piloto ainda não foi executado. A execução é a primeira
atividade do plano.

### 2.11 Aspectos éticos das etapas executadas

As etapas executadas usaram apenas metadados públicos da Google Play e uma
requisição GET à política de privacidade divulgada pelo próprio publicador, com
agente identificado como pesquisa acadêmica. Nenhum aplicativo foi instalado,
nenhuma área autenticada foi acessada e nenhum dado pessoal foi coletado. O
objeto de estudo é o aplicativo, não pessoas.

---

## 3 PLANO DE ATIVIDADES

### 3.1 Até a defesa do Projeto Capstone I

As datas da disciplina são as do plano de ensino: simulação de defesa em 24/11,
26/11 ou 01/12, conforme a ordem da turma, com 15 minutos de apresentação e 10
de arguição; entrega da redação no Canvas até 03/12; defesa final em 08/12,
10/12 ou 15/12, com 15 minutos de apresentação e 15 de arguição. O regulamento
exige cinco encontros de orientação registrados no bimestre.

| Período | Atividade | Produto |
|---|---|---|
| 20/10 a 26/10 | Rodar a etapa de cobertura do piloto. Primeiro encontro de orientação: apresentar este texto e a mudança de detectores da H4 | Tabela de cobertura do AndroZoo; ficha de orientação 1 |
| 27/10 a 02/11 | Validação manual do corpus na planilha gerada pelo script: vínculo oficial, esfera e dado sensível pelo Art. 5º, II | Corpus validado; taxa de erro da classificação automática |
| 27/10 a 09/11 | Piloto: amostra, download, detecção e concordância nos 20 aplicativos | Números preliminares da H4; ficha de orientação 2 |
| 03/11 a 16/11 | Revisão sistemática conforme Kitchenham e Charters (2007): protocolo, termos, bases (Scopus, ACM DL, IEEE Xplore), seleção | Protocolo e lista de trabalhos selecionados |
| 10/11 a 16/11 | Ampliar o controle nas categorias com menor cobertura | Cobertura por categoria recalculada; ficha de orientação 3 |
| 17/11 a 23/11 | Traduzir os Arts. 7º, 11 e 33 da LGPD em critérios verificáveis; congelar o protocolo e o plano de análise com data registrada no repositório; preparar a apresentação | Protocolo congelado; slides da simulação; ficha de orientação 4 |
| 24/11 a 01/12 | Simulação de defesa | Apresentação e sugestões da avaliadora |
| até 03/12 | Incorporar as sugestões e entregar a redação no modelo ABNT | Redação entregue; ficha de orientação 5 |
| 08/12 a 15/12 | Defesa final do Projeto Capstone I | Apresentação |

Fonte: elaborado pelo autor (2026).

### 3.2 Projeto Capstone II (2027.1)

| Mês | Atividade |
|---|---|
| Fevereiro | Download e detecção em todo o corpus validado e no controle ampliado |
| Março | Confronto com as políticas de privacidade e com a seção "Segurança dos dados" (H2); comparação entre aplicativos sensíveis e não sensíveis (H3) |
| Abril | Análise dinâmica da subamostra com dispositivo e conta próprios: destinos, jurisdição e taxa de bloqueio por *certificate pinning* |
| Maio | Análise estatística conforme o plano congelado: regressão binomial negativa para a H1, proporções com IC para H2 e H3, concordância para a H4. Comunicação de achados graves aos órgãos responsáveis antes da publicação |
| Junho | Redação final, publicação do conjunto de dados e defesa |

Fonte: elaborado pelo autor (2026).

### 3.3 Riscos e contingências

| Risco | Efeito | Contingência |
|---|---|---|
| Cobertura baixa do AndroZoo para aplicativos pequenos | Corpus analisável menor que o planejado | Coleta direta da loja com SHA-256 registrado, declarada como ameaça à validade |
| Versão do AndroZoo muito anterior à da loja | Resultado desatualizado | Reportar a defasagem; usar a coleta direta para os mais defasados |
| Prevalência muito alta ou muito baixa | κ instável mesmo com acordo alto | Reportar, junto do κ, as proporções de concordância positiva e negativa |
| Cobertura por categoria continuar baixa | Ajuste por categoria na H1 sem sustentação | Restringir a H1 às categorias com suporte e reportar a análise com e sem a restrição |
| Achado grave atribuível a um órgão | Risco ao cidadão se publicado antes da correção | Comunicação prévia ao órgão e, se couber, ao CTIR Gov e à ANPD, com prazo definido com o orientador |
| Atraso na orientação ou no termo de aceite | Reprovação por falta de encontros | Agendar os cinco encontros já no primeiro deles |

Fonte: elaborado pelo autor (2026).

---

## REFERÊNCIAS

ALECCI, M. et al. AndroZoo: a retrospective with a glimpse into the future. In:
INTERNATIONAL CONFERENCE ON MINING SOFTWARE REPOSITORIES, 21., 2024, Lisboa.
**Proceedings** [...]. New York: ACM, 2024. p. 389-393. DOI:
10.1145/3643991.3644863.

ALLIX, K.; BISSYANDÉ, T. F.; KLEIN, J.; LE TRAON, Y. AndroZoo: collecting
millions of Android apps for the research community. In: INTERNATIONAL
CONFERENCE ON MINING SOFTWARE REPOSITORIES, 13., 2016, Austin. **Proceedings**
[...]. New York: ACM, 2016. p. 468-471. DOI: 10.1145/2901739.2903508.

ANDROGUARD. **Androguard**. Versão 4.1.4. [*S. l.*], 2026. Disponível em:
https://pypi.org/project/androguard/4.1.4/. Acesso em: 20 out. 2026.

BINNS, R. et al. Third party tracking in the mobile ecosystem. In: ACM
CONFERENCE ON WEB SCIENCE, 10., 2018, Amsterdam. **Proceedings** [...]. New
York: ACM, 2018. p. 23-31. DOI: 10.1145/3201064.3201089.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados
Pessoais (LGPD). **Diário Oficial da União**: seção 1, Brasília, DF, 15 ago.
2018. Disponível em:
https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm.
Acesso em: [preencher na consulta].

DISCONNECT. **Disconnect tracking protection**. [*S. l.*], 2026. Lista de
serviços de rastreamento, licença CC BY-NC-SA 4.0. Disponível em:
https://github.com/disconnectme/disconnect-tracking-protection. Acesso em: 20
out. 2026.

EXODUS PRIVACY. **εxodus**: trackers. [*S. l.*], 2026. Base de assinaturas de
rastreadores. Disponível em: https://reports.exodus-privacy.eu.org/en/trackers/.
Acesso em: [preencher na execução do piloto].

FLEISS, J. L. Measuring nominal scale agreement among many raters.
**Psychological Bulletin**, v. 76, n. 5, p. 378-382, 1971. DOI:
10.1037/h0031619.

JOMINGYU. **google-play-scraper**. Versão 1.2.7. [*S. l.*], 2024. Disponível
em: https://pypi.org/project/google-play-scraper/. Acesso em: 20 out. 2026.

KENDALL, M. G. A new measure of rank correlation. **Biometrika**, v. 30, n. 1-2,
p. 81-93, 1938. DOI: 10.1093/biomet/30.1-2.81.

KITCHENHAM, B.; CHARTERS, S. **Guidelines for performing systematic literature
reviews in software engineering**. Keele: Keele University; Durham: Durham
University, 2007. (Technical Report EBSE-2007-01).

KOLLNIG, K. et al. Before and after GDPR: tracking in mobile apps. **Internet
Policy Review**, v. 10, n. 4, 2021a. DOI: 10.14763/2021.4.1611.

KOLLNIG, K. et al. A fait accompli? An empirical study into the absence of
consent to third-party tracking in Android apps. In: SYMPOSIUM ON USABLE PRIVACY
AND SECURITY, 17., 2021. **Proceedings** [...]. Berkeley: USENIX Association,
2021b. p. 181-195.

MOBSF. **Mobile Security Framework (MobSF)**. Versão 4.5.3. [*S. l.*], 2026.
Disponível em: https://pypi.org/project/mobsf/4.5.3/. Acesso em: 20 out. 2026.

NGUYEN, T. T.; BACKES, M.; STOCK, B. Freely given consent? Studying consent
notice of third-party tracking and its violations of GDPR in Android apps. In:
ACM SIGSAC CONFERENCE ON COMPUTER AND COMMUNICATIONS SECURITY, 2022, Los
Angeles. **Proceedings** [...]. New York: ACM, 2022. p. 2369-2383. DOI:
10.1145/3548606.3560564.

RAZAGHPANAH, A. et al. Apps, trackers, privacy, and regulators: a global study
of the mobile tracking ecosystem. In: NETWORK AND DISTRIBUTED SYSTEM SECURITY
SYMPOSIUM, 2018, San Diego. **Proceedings** [...]. Reston: Internet Society,
2018. DOI: 10.14722/ndss.2018.23353.

WILSON, E. B. Probable inference, the law of succession, and statistical
inference. **Journal of the American Statistical Association**, v. 22, n. 158,
p. 209-212, 1927. DOI: 10.1080/01621459.1927.10502953.
