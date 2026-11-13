# Quem mais está dentro do aplicativo?: rastreamento por terceiros e soberania de dados em aplicativos móveis governamentais brasileiros

Claudio da Aparecida Meireles Filho  
Orientador: Prof. Eduardo Arthur Izycki  
Universidade IDP — Bacharelado em Ciência da Computação  
Projeto Capstone I — Brasília-DF, 2026

Espelho de leitura atualizado em 13/11/2026 a partir de [main.tex](latex/main.tex). Para entrega e paginação, usar [main.pdf](latex/main.pdf). As referências são as mesmas da compilação do PDF.

## Resumo

Este projeto investiga a presença de SDKs de rastreamento de terceiros em aplicativos Android publicados por órgãos e entidades públicas brasileiras e propõe compará-la com a de aplicativos comerciais de mesma categoria e faixa de instalações. A literatura documenta rastreamento em diferentes populações de aplicativos, divergências entre detecção técnica e declarações de privacidade e limitações dos instrumentos de medição. A proteção de dados pessoais e a soberania de dados orientam a discussão dos resultados. O desenho é quantitativo, observacional e comparativo, com análise estática de pacotes identificados por hash, confronto com políticas de privacidade e observação dinâmica de uma subamostra. As etapas preparatórias produziram 396 candidatos governamentais, dos quais 376 foram mantidos na classificação registrada, ainda sujeita à validação pessoal, e 252 controles comerciais. Na coleta de metadados, nenhum dos 376 aplicativos mantidos declarou anúncios, contra 63 dos 190 controles originais. Essa declaração não mede a presença de rastreadores. Uma consulta histórica ao AndroZoo localizou 92 dos 396 candidatos governamentais e 160 dos 190 controles, indicando a necessidade de testar uma fonte complementar de pacotes. Em um piloto com 20 aplicativos, a proporção com detecções variou de 75% a 95% entre três detectores, e a adjudicação mostrou a importância de distinguir assinaturas de código de referências a domínios. A revisão sistemática recuperou 1.531 registros, manteve 1.249 após a deduplicação e encaminhou 357 à leitura completa, com 71 propostas de inclusão e 8 de exclusão, ainda sujeitas à validação pessoal. O projeto define recursos, critérios documentais da LGPD, procedimentos de reteste e cronograma. A coleta principal e os testes das hipóteses permanecem previstos para o Projeto Capstone II.

**Palavras-chave:** rastreamento por terceiros; aplicativos governamentais; privacidade; LGPD; análise estática.

## Abstract

This research project investigates third-party tracking SDKs in Android applications published by Brazilian public bodies and proposes a comparison with commercial applications matched by category and installation range. Previous studies document tracking across application populations, discrepancies between technical findings and privacy disclosures, and limitations of measurement tools. Personal data protection and data sovereignty guide the interpretation of the results. The study adopts a quantitative, observational and comparative design, combining static analysis of packages identified by cryptographic hashes, comparison with privacy policies and dynamic observation of a subsample. Preparatory work identified 396 government candidates, of which 376 were retained in the recorded classification, still awaiting the author's personal validation, and 252 commercial controls. In the metadata collection, none of the 376 retained applications declared advertisements, compared with 63 of the 190 original controls. This declaration does not measure tracker presence. A historical AndroZoo lookup found 92 of the 396 government candidates and 160 of the 190 controls, indicating the need to test an additional package source. In a pilot involving 20 applications, the proportion with detections ranged from 75% to 95% across three detectors, and adjudication demonstrated the importance of distinguishing code signatures from domain references. The systematic search retrieved 1,531 records, retained 1,249 after deduplication and advanced 357 to full-text assessment, with 71 proposed inclusions and 8 proposed exclusions, still awaiting personal validation. The project specifies resources, documentary criteria for analysing the Brazilian General Data Protection Law, retest procedures and a schedule. Main data collection and hypothesis testing remain planned for Capstone Project II.

**Keywords:** third-party tracking; government applications; privacy; LGPD; static analysis.

## 1 Introdução

Boa parte do atendimento ao cidadão no Brasil passou a acontecer por aplicativos móveis. O pedido de benefício previdenciário, a carteira de vacinação, o documento de habilitação e o agendamento em unidade de saúde estão em aplicativos publicados por órgãos federais, estaduais e municipais na Google Play. Dois deles, Meu INSS e Meu SUS Digital, registravam mais de 50 milhões de instalações cada um na coleta feita para este trabalho em setembro de 2026.

Aplicativos Android incorporam kits de desenvolvimento (SDKs) de terceiros, que podem coletar identificadores do dispositivo e enviá-los a quem os fornece. A literatura mostra que a maioria dos aplicativos comerciais embarca esses rastreadores, e um estudo com 1.166 aplicativos de governo de 71 países observou envio de dados do dispositivo a rastreadores conhecidos em 269 deles (23,1%) (Samarasinghe et al., 2022). Nos estudos examinados nesta síntese, não foi identificada uma comparação do conjunto governamental brasileiro com controles comerciais pareados por categoria e porte (Seção 2.5).

O tema deste trabalho é o rastreamento por terceiros em aplicativos móveis publicados por órgãos públicos brasileiros, examinado do ponto de vista da proteção de dados e da soberania sobre os dados dos cidadãos.

O problema, as hipóteses e a justificativa estão nas Seções 1.3 a 1.5. A Seção 2 apresenta o referencial teórico, e a Seção 3, os procedimentos metodológicos, os resultados esperados, o cronograma e os riscos. Os resultados das etapas já executadas estão na Seção 3.8.

### 1.1 Objetivo geral

Medir a prevalência de SDKs de rastreamento de terceiros em aplicativos móveis governamentais brasileiros e compará-la com a de aplicativos comerciais pareados por categoria e faixa de instalações.

### 1.2 Objetivos específicos

1.  Consolidar e validar manualmente o corpus de aplicativos governamentais, documentando os critérios de inclusão e a taxa de erro da classificação automática.

2.  Quantificar, por aplicativo, os SDKs de rastreamento detectados por análise estática, por esfera de governo e por tratamento de dado sensível.

3.  Confrontar os SDKs detectados com o que a política de privacidade e a seção “Segurança dos dados” da Google Play declaram.

4.  Determinar, em uma subamostra sob análise dinâmica, para quais destinos e jurisdições os aplicativos efetivamente transmitem dados.

5.  Medir a concordância entre detectores de rastreadores e o efeito da escolha da ferramenta sobre a taxa reportada.

### 1.3 Problema

Os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros, e em que medida esse comportamento difere do de aplicativos comerciais de mesma categoria e porte?

A lacuna que motiva a pergunta está detalhada na Seção 2.5: o estudo mais próximo, de Samarasinghe et al. (2022), não oferece a comparação aqui proposta entre aplicativos brasileiros e controles comerciais pareados, com avaliação da concordância entre detectores sobre as mesmas versões dos pacotes.

**Relevância.** O prestador responsável por um benefício público não pode ser livremente substituído pelo cidadão, embora possam existir canais presenciais ou digitais alternativos. Essa dependência institucional torna relevante examinar a necessidade e a transparência da participação de terceiros no aplicativo.

### 1.4 Hipóteses

As hipóteses abaixo orientam a coleta principal. Os critérios foram refinados durante a preparação e o piloto e deverão ser congelados, com data e versão, antes da análise principal. Os resultados do piloto não constituem teste confirmatório dessas hipóteses. A não rejeição de H1 não demonstra equivalência entre os grupos.

**Quadro 1 — Hipóteses e critérios de rejeição**

| **Hipótese** | **Enunciado**                                                                                                                        | **Critério de rejeição**                                                                                                                                                        |
|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| H1           | A prevalência de aplicativos com ao menos um SDK de rastreamento é igual entre governo e controle comercial pareado (hipótese nula). | Razão de prevalências ajustada por categoria e faixa de instalações com IC95% que exclua 1.                                                                                     |
| H2           | Fração relevante dos SDKs detectados não está declarada na política de privacidade.                                                  | Proporção de SDKs não declarados com limite superior do IC95% abaixo de 10%.                                                                                                    |
| H3           | Aplicativos que tratam dado sensível não apresentam menor prevalência de SDKs de rastreamento que os demais governamentais.          | Limite superior do IC95% da razão de prevalências sensível/não sensível abaixo de 1, com ajuste por esfera, categoria e porte quando houver suporte.                            |
| H4           | A concordância entre detectores sobre o mesmo pacote é baixa, de modo que a taxa reportada depende da ferramenta escolhida.          | Limite inferior do IC95% do $\kappa$ de Fleiss (Fleiss, 1971) maior ou igual a 0,6. O $\tau$ de Kendall (Kendall, 1938) será complementar, sem limiar indefinido de valor alto. |

*Fonte: Elaborado pelo autor (2026).*

### 1.5 Justificativa

O trabalho se justifica em três planos.

**Jurídico.** A LGPD define como sensível o dado referente à saúde e o dado biométrico (Art. 5º, II), restringe as hipóteses de seu tratamento (Art. 11), vincula o tratamento feito pelo poder público à sua finalidade pública (Art. 23) e limita a transferência internacional de dados pessoais a casos específicos (Art. 33) (Brasil, 2018). Se um aplicativo de saúde publicado por um órgão público envia identificadores a um terceiro, a base legal desse envio precisa existir e ser demonstrável.

**Soberania de dados.** O rastreamento em aplicativos se concentra em poucas grandes empresas estrangeiras, como Google e Facebook (Binns et al., 2018; Kollnig et al., 2021a). Dados de cidadãos gerados no uso de um serviço público essencial podem, por dependência técnica assumida por padrão no desenvolvimento Android, ser processados sob outra jurisdição. Medir a extensão dessa dependência é condição para discuti-la.

**Metodológico.** Taxas de rastreamento publicadas por estudos diferentes são produzidas por ferramentas diferentes. Se essas ferramentas discordam entre si, as taxas não são comparáveis. Medir a concordância entre detectores sobre os mesmos aplicativos dá ao trabalho uma contribuição que vai além do caso brasileiro.

## 2 Referencial teórico

Esta seção apresenta os conceitos e os trabalhos em que o projeto se apoia. A Seção 2.1 define o rastreamento por terceiros e resume o que se sabe sobre sua presença em aplicativos móveis; a Seção 2.2, o que os estudos observaram depois das leis de proteção de dados; a Seção 2.3, como bibliotecas e rastreadores são detectados e por que a escolha da ferramenta importa; a Seção 2.4, os trabalhos que confrontam o que o aplicativo declara com o que ele faz; a Seção 2.5, os estudos sobre aplicativos de governo e a lacuna que deixam; e a Seção 2.6, o marco jurídico brasileiro. A síntese parte dos 11 estudos do conjunto de controle da revisão sistemática (Seção 3.9) e incorpora trabalhos complementares sobre validação, políticas e soberania digital. Ela será ampliada com os estudos incluídos após a leitura completa; as referências desta seção não são o resultado final da revisão sistemática.

### 2.1 Bibliotecas de terceiros e rastreamento em aplicativos móveis

Aplicativos Android raramente são escritos do zero. Eles incorporam bibliotecas e kits de desenvolvimento (SDKs) de terceiros, que facilitam o desenvolvimento e oferecem funções como análise de uso, integração com redes sociais e monetização por anúncios (Razaghpanah et al., 2018). Quando esses componentes coletam dados de comportamento e permitem identificar o usuário e acompanhá-lo em vários serviços digitais, fala-se em rastreamento por terceiros (Binns et al., 2018). Como funcionam dentro do aplicativo, esses serviços são, em grande parte, invisíveis para o usuário e podem rastreá-lo sem consentimento, inclusive entre aplicativos diferentes (Razaghpanah et al., 2018).

Binns et al. (2018) mediram a presença de rastreadores em 959 mil aplicativos das lojas da Google Play dos Estados Unidos e do Reino Unido. A maioria dos aplicativos contém rastreamento de terceiros. A distribuição é de cauda longa: poucos rastreadores dominantes respondem por grande parte da cobertura. A intensidade varia por categoria, e aplicativos de notícias e infantis estão entre os que mais embarcam rastreadores. O estudo mostra ainda que o rastreamento é transnacional, com muitos rastreadores operando em jurisdições fora da União Europeia.

Razaghpanah et al. (2018) partiram do tráfego real de usuários, coletado por um aplicativo de monitoramento instalado nos próprios aparelhos, e desenvolveram métodos para detectar serviços de publicidade e rastreamento no nível da rede. Identificaram 2.121 desses serviços, dos quais 233 não constavam das listas de bloqueio mais usadas. Ao analisar as políticas de privacidade dos maiores fornecedores, concluíram que compartilhar os dados coletados com subsidiárias e afiliadas é a norma. O resultado expõe um limite das medições baseadas em listas: elas só encontram o que já conhecem.

### 2.2 Rastreamento e regulação da proteção de dados

Estudos anteriores e posteriores a mudanças regulatórias permitem descrever tendências, mas não isolam, por si só, o efeito causal de uma lei. Kollnig et al. (2021a) compararam quase dois milhões de aplicativos Android de antes e de depois da entrada em vigor do Regulamento Geral de Proteção de Dados europeu (GDPR), em 2018, e observaram pouca mudança na presença de rastreadores e a persistência da concentração da capacidade de rastrear em poucas grandes empresas.

Kollnig et al. (2021b) mostraram que a legislação da União Europeia e do Reino Unido exige consentimento para o rastreamento por terceiros, mas que a maioria dos aplicativos analisados rastreia e poucos obtêm o consentimento antes de fazê-lo. As próprias bibliotecas de rastreamento atribuem ao desenvolvedor do aplicativo a tarefa de obter o consentimento, sem oferecer meios robustos para isso.

Nguyen; Backes; Stock (2022) estudaram os avisos de consentimento em 239.381 aplicativos. Encontraram 30.160 aplicativos que compartilhavam dados pessoais com terceiros sem sequer tentar obter consentimento e, entre os 13.082 que exibiam aviso, 2.688 (20,54%) que violavam ao menos um requisito do GDPR, por exemplo ao continuar transmitindo dados depois de o usuário recusar.

### 2.3 Detecção de bibliotecas e de rastreadores

A presença de bibliotecas e os fluxos que podem produzir são examinados por abordagens complementares. A análise estática examina o pacote de instalação (APK) sem executá-lo: lista as classes do código compilado e os textos que ele contém e os compara com assinaturas conhecidas. A análise dinâmica executa o aplicativo e observa o que ele de fato transmite, como fizeram Razaghpanah et al. (2018). A primeira mostra que o código está no pacote, mas não que ele é executado; a segunda mostra o envio, mas exige executar cada aplicativo.

Para a análise estática de bibliotecas existem várias ferramentas. Zhan et al. (2020) compararam todas as ferramentas de detecção de bibliotecas de terceiros em Android disponíveis publicamente, quanto à eficácia, à eficiência, à resistência à ofuscação de código e à facilidade de uso, e nenhuma foi a melhor em todos os critérios: o LibScout foi o mais eficaz; o LibRadar, o mais rápido e o mais fácil de usar; e o LibPecker, o que melhor resistiu à ofuscação. Ferramentas diferentes podem, portanto, dar respostas diferentes para o mesmo aplicativo, e é esse efeito que a H4 mede.

Para rastreadores, uma base usada por ferramentas abertas é a do Exodus Privacy, que associa a cada rastreador conhecido uma assinatura de código, um padrão nos nomes das classes do aplicativo, e uma assinatura de rede, um padrão nos domínios que ele contata (Exodus Privacy, 2026). Outras listas, como a da Disconnect, classificam domínios por finalidade, como publicidade, análise de uso e coleta de impressão digital do aparelho (Disconnect, 2026). Ferramentas de análise de aplicativos, como o MobSF (MobSF, 2026), e bibliotecas de extração, como o Androguard (Androguard, 2026), permitem aplicar essas bases a um pacote. A Seção 3.7 mostra que essas ferramentas não são todas independentes entre si. A avaliação ampliada de Zhan et al. (2022) também considera precisão, revocação, identificação de versões e resistência à ofuscação. A combinação de ferramentas exige comparar unidades equivalentes e documentar as dependências entre bases, métodos de extração e critérios de adjudicação.

A fonte dos pacotes também importa para a reprodutibilidade. O AndroZoo é um acervo acadêmico com milhões de pacotes Android, no qual cada versão de um aplicativo é obtida pelo seu hash SHA-256 (Alecci et al., 2024; Allix et al., 2016). A disponibilidade na loja pode mudar com atualizações e restrições de distribuição; o estudo registrará a origem e a versão de cada pacote.

### 2.4 O que o aplicativo declara e o que ele faz

Uma linha de trabalhos confronta o que o aplicativo declara com o que ele faz. Slavin et al. (2016) propuseram um arcabouço semiautomático que liga frases da política de privacidade aos métodos da API do Android que produzem informação sensível e usa análise de fluxo de informação para encontrar desalinhamentos. Nos 477 aplicativos mais populares avaliados, encontraram 341 possíveis violações da política. Zimmeck et al. (2019) levaram esse tipo de análise de conformidade à escala de cerca de um milhão de aplicativos, com o sistema MAPS, que compara a política de privacidade com as práticas de dados identificadas no código. Esses trabalhos fundamentam a H2, que confronta os SDKs detectados com a política de privacidade e com a seção “Segurança dos dados” da Google Play. Andow et al. (2020) acrescentam uma distinção importante com o PoliCheck: identificar o destinatário do dado, e não somente sua categoria. Na análise de 13.796 aplicativos, encontraram declarações ausentes ou incorretas em até 42,4% dos casos. Para este projeto, a implicação é registrar separadamente componente, destinatário e finalidade, sem tratar a simples menção a dados pessoais como declaração suficiente de qualquer compartilhamento.

### 2.5 Aplicativos de governo

Aplicativos de governo também já foram medidos. Samarasinghe et al. (2022) analisaram 1.166 aplicativos Android governamentais de 71 países e observaram envio de dados do dispositivo, como modelo e identificador, a rastreadores conhecidos em 269 deles (23,1%).

Diferentemente dos sites comerciais, os serviços de governo são financiados com dinheiro público, tratam dados sensíveis e raramente aparecem nas listas dos sites mais acessados, de onde costumam sair as amostras dos estudos de rastreamento (Samarasinghe et al., 2022). A análise dos aplicativos combinou MobSF e LiteRadar com tráfego capturado por mitmproxy durante eventos gerados pelo Monkey. A Seção 5 do estudo informa 611 ocorrências de SDKs do Google entre 1.647 ocorrências de SDKs rastreadores (37,1%). Como a discussão usa outra redação para esse percentual, ele não é tratado aqui como proporção de aplicativos. A coleta dinâmica não abrangeu aplicativos com fixação de certificado que impediu a interceptação do tráfego.

Na versão ampliada de seu estudo sobre aplicativos da COVID-19, Serrano, Betarte e Campo (2024) identificaram rastreadores em 402 de 595 aplicativos por assinaturas do Exodus e examinaram o código de bibliotecas para caracterizar a coleta e o envio de dados. Os pacotes vieram da Google Play, do AndroZoo, de um conjunto no Zenodo e de repositórios alternativos. Essa combinação evidencia a necessidade de registrar origem e versão dos pacotes. O artigo também apresenta o SAPITO, ferramenta para apoiar a identificação de fluxos de dados em bibliotecas. A publicação anterior (Serrano, Betarte e Campo, 2023) descreve o mesmo conjunto e será substituída pela versão ampliada na seleção F2, evitando dupla contagem. A presença estática de uma assinatura e a análise de código de uma biblioteca não demonstram que todos os aplicativos transmitiram dados em execução.

A detecção de SDKs de rastreamento por análise estática é método consolidado e já foi aplicada a aplicativos de diversos domínios comerciais e, no estudo de Samarasinghe et al. (2022), a aplicativos de governo de vários países. Esse estudo deixa em aberto três pontos, que são os deste trabalho.

1.  **O caso brasileiro.** A amostra internacional foi montada a partir de links para a Google Play encontrados em sites de governo, com o governo identificado pelo domínio `.gov.` no e-mail ou no site do desenvolvedor. O Brasil aparece só em exemplos isolados, como um dos sete aplicativos que enviavam credenciais sem criptografia. Não há separação por esfera de governo nem identificação dos aplicativos que tratam dado sensível, que são o recorte da H3.

2.  **A linha de base.** Os resultados não são comparados com aplicativos comerciais equivalentes e, por isso, não dizem se o governo rastreia mais, menos ou o mesmo que o mercado. A comparação do projeto será restrita às categorias e faixas de instalações com suporte nos dois grupos, sem estender a conclusão a todo o mercado. A ausência de estudo equivalente na síntese atual permanece sujeita à leitura completa e à bola de neve.

3.  **O instrumento.** O estudo combinou análise estática e dinâmica, incluindo MobSF, LiteRadar e verificação de Firebase. Portanto, não se trata de um estudo com uma única ferramenta. O recorte proposto aqui é comparar saídas de detectores sobre as mesmas versões, com unidades harmonizadas, adjudicação de divergências e medidas explícitas de concordância. Essa é uma questão metodológica específica da H4, e não a alegação de que o estudo anterior ignorou validação.

Os autores relatam ainda que parte significativa dos aplicativos de governo não pôde ser baixada por restrição de região. É a mesma hipótese levantada aqui para a baixa cobertura do AndroZoo (Seção 3.8), e um motivo para coletar os pacotes com conta e região brasileiras. A revisão sistemática, cujo protocolo está descrito na Seção 3.9, vai confirmar ou corrigir essa avaliação.

### 2.6 Proteção de dados pessoais e soberania de dados

No Brasil, o tratamento de dados pessoais é regido pela Lei Geral de Proteção de Dados Pessoais (Brasil, 2018). A lei define dado pessoal como a informação relacionada a pessoa natural identificada ou identificável e dado pessoal sensível como, entre outros, o dado referente à saúde e o dado genético ou biométrico, quando vinculado a uma pessoa natural (Art. 5º, I e II). O tratamento só pode ocorrer nas hipóteses previstas em lei (Art. 7º), e as hipóteses para dados sensíveis são mais restritas (Art. 11). O tratamento feito pelo poder público deve atender à sua finalidade pública, na persecução do interesse público (Art. 23). A transferência internacional de dados, definida como a transferência de dados pessoais para país estrangeiro ou organismo internacional (Art. 5º, XV), só é permitida nos casos que a lei enumera (Art. 33).

Essas regras dão os critérios para discutir os resultados. O guia da ANPD para o poder público orienta a análise de bases legais, finalidades e compartilhamentos (Autoridade Nacional de Proteção de Dados, 2023). Para a dimensão internacional, a Resolução CD/ANPD nº 19/2024 distingue transferência e coleta internacional e disciplina mecanismos de transferência (Autoridade Nacional de Proteção de Dados, 2024). Os estudos da Seção 2.1 mostram que o rastreamento se concentra em poucas empresas e opera em várias jurisdições (Binns et al., 2018; Kollnig et al., 2021a). A presença de fornecedores externos torna relevante investigar a governança dessa dependência, sem presumir que o órgão desconheça a decisão técnica ou que todo SDK envie dados ao exterior. Pohle; Thiel (2020) discutem a soberania digital em termos de capacidades de decisão de Estados, organizações e indivíduos, destacando que o conceito tem sentidos distintos. Neste projeto, a soberania de dados é um recorte operacional dessa discussão: a capacidade de o Estado saber e decidir para onde vão os dados gerados no uso dos seus serviços. Medir a presença desses SDKs é a condição para discutir essa dependência; examinar destinos observados exige a análise dinâmica, e caracterizar uma transferência internacional também exige identificar os agentes e a operação, conforme o quarto objetivo específico (Seção 1.2).

## 3 Procedimentos metodológicos

A pesquisa é quantitativa, observacional e comparativa: mede características de artefatos de software publicamente distribuídos, sem intervir neles, e compara dois grupos. Os procedimentos são, em ordem:

1.  construção do corpus governamental a partir de buscas na Google Play e da expansão pelo catálogo de cada publicador oficial;

2.  caracterização dos aplicativos por metadados públicos e montagem de um grupo de controle comercial;

3.  verificação de viabilidade de cada hipótese antes do download dos pacotes;

4.  obtenção dos pacotes no AndroZoo (Alecci et al., 2024; Allix et al., 2016) e, para os que não estão no acervo, direto da Google Play, sempre com o hash registrado;

5.  detecção de rastreadores por mais de um detector e medida de concordância;

6.  confronto com as declarações dos publicadores;

7.  análise dinâmica de uma subamostra com dispositivo e conta próprios;

8.  análise estatística conforme plano congelado antes da análise principal, distinguindo os ajustes motivados pelo piloto.

Todos os scripts citados estão no repositório do trabalho, na pasta `scripts/`. A construção inicial do corpus, do controle e os testes de viabilidade foram executados; a validação pessoal das classificações está pendente. A obtenção e a detecção foram ensaiadas em 20 pacotes, ainda sem execução no corpus completo. Os resultados preliminares estão na Seção 3.8, e as etapas restantes, no cronograma (Seções 3.15 e 3.16).

### 3.1 Escolha do tema por testes de viabilidade

Antes da escolha deste tema, outros três foram testados empiricamente e descartados com base nos dados obtidos. O critério comum foi verificar, antes de fixar o desenho, se a variável principal de cada tema podia ser observada.

**Quadro 2 — Temas testados antes da escolha**

| **Tema testado**                                   | **Teste**                                                 | **Resultado**                                                                                                                                                                       |
|:---------------------------------------------------|:----------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sistemas de controle industrial expostos no Brasil | Contagens e facetas no Shodan                             | Descartado. Os mesmos hosts respondiam em vários protocolos industriais ao mesmo tempo, padrão de honeypot e de nuvem. O setor do operador, variável principal, não era observável. |
| Abuso de marca em Certificate Transparency         | entradas de log, casamento por token                      | Descartado. Nenhuma imitação real encontrada; a marca raramente aparece no domínio de phishing.                                                                                     |
| Genealogia de malware bancário brasileiro          | imphash de 1.764 amostras brasileiras e 2.104 de controle | Inconclusivo. 85% do acervo brasileiro eram containers, nos quais o imphash não se aplica.                                                                                          |
| Aplicativos governamentais (este)                  | Busca e expansão por catálogo na Google Play              | Viável. O publicador vem identificado pela própria loja.                                                                                                                            |

*Fonte: Elaborado pelo autor (2026).*

A diferença decisiva do tema escolhido é que a variável que separa os grupos, o publicador do aplicativo, vem declarada na fonte. A identificação do publicador na Google Play oferece um ponto de partida, mas o nome exibido precisa ser confrontado com o nome jurídico e o vínculo institucional; um nome de serviço público não garante oficialidade.

### 3.2 Construção do corpus governamental

**Fonte e ferramenta.** Os metadados foram obtidos da Google Play com a biblioteca `google-play-scraper` (JOMINGYU, 2024), com país Brasil e idioma português. O script é `scripts/teste_viabilidade_n3.py`.

**Busca.** Foram usados 21 termos ligados a serviço público: “gov.br”, “governo federal”, “governo do estado”, “prefeitura”, “ministério da saúde”, “receita federal”, “INSS”, “SUS”, “detran”, “tribunal”, “SERPRO”, “Dataprev”, “carteira digital”, “cadastro único”, “meu INSS”, “secretaria estadual”, “secretaria municipal”, “defensoria”, “polícia militar”, “corpo de bombeiros” e “procon”, com até 30 resultados por termo.

**Classificação do publicador.** Um aplicativo foi considerado candidato quando o nome do publicador contém um sinal de órgão público, como “prefeitura”, “secretaria”, “tribunal”, “ministério” ou “detran”, ou quando o publicador consta de uma lista de órgãos conhecidos cujo nome não tem esses sinais. Essa lista existe porque o publicador do portal gov.br federal, responsável por Meu INSS e Meu SUS Digital, se chama “Serviços e Informações do Brasil”, e as empresas públicas de tecnologia, como a Celepar (Paraná) e a Prodam (município de São Paulo), também não têm sinal no nome. O casamento é feito por palavra inteira, e não por trecho de texto: a primeira versão, que casava trechos, incluiu um aplicativo da Yandex entre os órgãos públicos e excluiu o publicador do gov.br. O erro foi corrigido e está registrado no histórico do repositório.

**Expansão por catálogo.** Para cada publicador classificado como oficial, foi feita uma busca pelo nome exato do publicador, mantendo apenas os aplicativos cujo publicador coincide exatamente. A busca por termo encontra uma amostra; a busca pelo publicador encontra o catálogo dele.

**Resultado (3 de setembro de 2026).** Foram localizados 590 aplicativos distintos. Destes, 396 têm publicador classificado como órgão público, de 71 publicadores distintos. Esses 396 são candidatos: a validação manual do vínculo institucional é a primeira atividade do plano (Seção 3.15).

### 3.3 Caracterização do corpus

Em 17 de setembro de 2026, a ficha completa de cada um dos 396 candidatos foi obtida na Google Play, sem nenhuma remoção. O script é `scripts/teste_viabilidade_n3_robusto.py`, e cada aplicativo recebeu três classificações automáticas.

**Esfera de governo**, pelo nome do publicador, testando primeiro os sinais municipais, depois os estaduais e por último os federais, porque “municipal” é menos ambíguo que “secretaria”. Resultado: 85 federais, 206 estaduais, 95 municipais e 10 indeterminados (2,5%). A validação manual encontrou um erro de regra, já corrigido: os aplicativos do STJ, tribunal da União, saíam estaduais (Seção 3.8). Na conferência dos 396, a esfera conferida difere da automática em 18 dos 376 aplicativos oficiais, 7 deles indeterminados pela regra automática.

**Tratamento de dado sensível**, por palavras-chave no título e na descrição, em quatro grupos: saúde, biometria, previdência e assistência social. Resultado: 152 aplicativos (38,4%) em ao menos um grupo; 125 em saúde, 28 em previdência, 17 em biometria e 5 em assistência social (um aplicativo pode estar em mais de um grupo). O critério automático é mais amplo que o da LGPD: previdência e assistência social não são, por si, dado sensível no sentido do Art. 5º, II. Na comparação com a classificação registrada (Seção 3.8), houve divergência em 28,7% dos 376 aplicativos mantidos como oficiais, nos dois sentidos. A H3 usará a classificação após validação pessoal; por enquanto, 100 desses 376 foram marcados como tratando dado de saúde ou biométrico.

**Faixa de instalações**, em escala logarítmica, pela ordem de grandeza do número mínimo de instalações informado pela loja ($10^{0}$, $10^{1}$, …, $10^{9}$). Dois aplicativos não informam instalações.

### 3.4 Grupo de controle comercial

Para cada categoria da loja presente no corpus governamental, foram buscados aplicativos comerciais com o nome da categoria combinado a termos genéricos (“app”, “grátis”, “brasil”, “online”, “digital”, “fácil”), percorrendo os resultados alternadamente pelo início e pelo fim da lista. Aplicativos de publicadores oficiais foram excluídos. Foram aceitos até 8 aplicativos por categoria, com no máximo 2 por faixa de instalações, para espalhar o controle ao longo das faixas.

A busca da loja ordena por relevância e quase nunca devolve um aplicativo comercial com poucas instalações. Para cobrir as faixas de $10^{2}$ a $10^{5}$, o controle foi complementado com aplicativos de publicadores não oficiais encontrados na busca inicial, até 12 por faixa. O controle original tem 190 aplicativos, 22 deles vindos desse complemento. Como esses 22 foram encontrados por termos ligados a governo, o controle não é amostra aleatória do mercado, e isso entra nas limitações (Seção 3.11).

### 3.5 Ampliação do controle por categoria

Em 4 de novembro de 2026, o controle foi ampliado dentro de cada categoria, com o script `scripts/ampliar_controle.py`. Para cada célula de categoria e faixa de instalações em que havia aplicativo governamental e menos de dois comerciais, o script buscou na Google Play pelo nome da categoria, por termos genéricos e pelas palavras mais frequentes nos títulos dos aplicativos governamentais daquela categoria, que trazem aplicativos comerciais do mesmo assunto. Foram aceitos apenas aplicativos de publicador não oficial, da mesma categoria e de uma das faixas em falta, com teto de 80 fichas lidas por categoria. As faixas abaixo de $10^{2}$ ficaram de fora, porque os aplicativos governamentais nelas já saem da H1 pela restrição ao suporte comum.

**Tabela 1 — Cobertura do controle antes e depois da ampliação por categoria**

| **Medida**                                                           | **Antes**       | **Depois**     |
|:---------------------------------------------------------------------|:----------------|:---------------|
| Aplicativos comerciais no controle                                   |                 |                |
| Governo dentro da amplitude de faixas do controle da mesma categoria | de 394 (77,9%)  | de 394 (89,1%) |
| Governo com comercial na mesma categoria e na mesma faixa            | de 394 (57,9%)  | de 394 (87,3%) |
| Comerciais em falta para dois por célula                             | , em 44 células |                |

*Fonte: Elaborado pelo autor (2026).*

As 18 vagas restantes estão, na maioria, na faixa de $10^{2}$ instalações, em que a busca da loja quase não devolve aplicativo comercial. Com 252 aplicativos de controle, a menor diferença detectável no pior caso, com taxa de base de 50%, cai de 12,3 para 11,4 pontos percentuais. Os 62 aplicativos novos ainda não foram cruzados com o AndroZoo; como a coleta completa vai baixar governo e controle direto da Google Play, isso não bloqueia a etapa seguinte.

### 3.6 Acesso ao AndroZoo

O AndroZoo é um acervo acadêmico de pacotes Android que permite obter uma versão específica de um aplicativo pelo hash SHA-256 (Alecci et al., 2024; Allix et al., 2016). O hash permite identificar a versão analisada, e o acervo oferece uma via de recuperação por pesquisadores autorizados. Na coleta direta, a possibilidade de obter novamente a mesma versão depende de sua disponibilidade posterior; registrar o hash não garante acesso futuro. O acesso foi solicitado em 16 de setembro de 2026 e concedido em 17 de setembro de 2026. A chave de acesso é individual, não é compartilhada e não é gravada no repositório; os scripts a leem de uma variável de ambiente. A cobertura do acervo para o corpus deste trabalho foi medida no piloto e está na Seção 3.8.

### 3.7 Verificação dos detectores de rastreadores

A proposta previa três ferramentas para a H4: MobSF, Androguard e Exodus Privacy (Exodus Privacy, 2026). Antes do piloto, o código de cada uma foi examinado para saber se elas são, de fato, detectores independentes. Duas constatações mudaram o desenho.

**O MobSF usa a base do Exodus.** No MobSF 4.5.3 (MobSF, 2026), a detecção de rastreadores está em `mobsf/MalwareAnalyzer/views/Trackers.py`. O módulo baixa a base de rastreadores da API do Exodus Privacy, lista as classes de cada arquivo DEX e aplica a cada classe as expressões regulares de assinatura de código dessa base. É a mesma base e a mesma regra de casamento do Exodus, e o pacote do MobSF inclui a licença do exodus-core, a biblioteca de análise do próprio Exodus. A cópia da base distribuída com o pacote tem 432 rastreadores: 428 com assinatura de código e 260 com assinatura de rede. Comparar MobSF e Exodus mede apenas diferenças de implementação, e a concordância entre eles tende a ser alta por construção.

**O Androguard não é detector.** O Androguard (Androguard, 2026) extrai classes, textos e recursos de um pacote; ele não tem base de rastreadores. Ele é o extrator sobre o qual os detectores trabalham.

**Instrumento redefinido para a H4.** Para que a comparação separe o efeito da base de assinaturas do efeito do método de detecção, o piloto usa três detectores:

**Quadro 3 — Detectores usados no piloto**

| **Detector** | **Base**                                                     | **Método**                                                     |
|:-------------|:-------------------------------------------------------------|:---------------------------------------------------------------|
| A            | Exodus Privacy                                               | assinatura de código nas classes do DEX                        |
| B            | Exodus Privacy                                               | assinatura de rede nos domínios presentes nos textos do pacote |
| C            | Disconnect (Disconnect, 2026), mantida por outra organização | lista de domínios aplicada aos mesmos textos de B              |

*Fonte: Elaborado pelo autor (2026).*

A diferença entre A e B mede o efeito do método com a base fixa; a diferença entre B e C mede o efeito da base com o método fixo. O MobSF entra como verificação de implementação do detector A. A lista da Disconnect é usada nas categorias de publicidade, análise de uso e impressão digital invasiva; as categorias de conteúdo e redes sociais ficam de fora porque incluem domínios de uso geral, como `google.com` e `facebook.com`, que gerariam falso positivo em quase todo aplicativo. Essa escolha é parâmetro do script e é reportada, porque ela própria afeta a taxa.

O ensaio do pipeline já mostrou um efeito de método. Na base do Exodus, a assinatura de rede do rastreador “Google Ads” é a expressão `\.google\.com`, que casa com qualquer subdomínio do Google. Em um dos APKs de teste, um link para `maps.google.com` bastou para o detector B apontar “Google Ads”, enquanto o detector A, que procura o código do SDK, não encontrou nada. Por isso o script registra, para cada detecção, a classe ou o domínio que a produziu, e as detecções do piloto foram conferidas uma a uma (Seção 3.8).

### 3.8 Verificação de viabilidade, piloto e validação do corpus

As etapas já executadas produziram os resultados que orientam o método da coleta completa.

**Viabilidade.** Antes de baixar qualquer pacote, foi verificado se cada hipótese tem instrumento, com critérios escritos antes da rodada completa. As quatro hipóteses têm: com a classificação conferida, a menor célula esfera $\times$ sensibilidade tem 26 aplicativos e há 100 aplicativos com dado sensível (H3); 364 de 394 aplicativos governamentais (92,4%) estão dentro da amplitude de faixas de instalações coberta pelo controle (H1); e 323 de 396 (81,6%) têm política de privacidade acessível (H2).

**Anúncios declarados.** Nenhum dos 376 aplicativos oficiais declara exibir anúncios na Google Play (IC95% de 0% a 1,0%), contra 33,2% dos 190 aplicativos do controle (IC95% de 26,9% a 40,1%), com os intervalos calculados pelo método de Wilson (1927). A declaração é feita pelo próprio publicador e trata só de anúncios: não indica quais SDKs o aplicativo embarca nem para onde os dados vão.

**Fonte dos pacotes.** Na consulta histórica, o AndroZoo continha 92 dos 396 candidatos governamentais (23,2%), contra 160 dos 190 controles originais (84,2%). Esses denominadores antecedem a redução do corpus a 376 e a ampliação do controle a 252. Na mesma faixa de instalações, a razão de chances de Mantel; Haenszel (1959) de um aplicativo governamental estar no acervo é de 0,13 (IC95% de 0,07 a 0,24). Por isso, a maior parte do corpus será baixada direto da Google Play, com o hash registrado.

**Piloto dos detectores.** Em 20 aplicativos do AndroZoo, a proporção com ao menos um rastreador foi de 75%, 95% e 80% conforme o detector (A, B e C), e o $\kappa$ de Fleiss sobre a presença de rastreador foi de 0,52. A conferência das 223 detecções pela evidência que as produziu mostrou que 72% das detecções do detector B eram falsas, porque as assinaturas de rede tomam qualquer domínio do Google ou do Facebook por um SDK; sem esses falsos positivos, o $\kappa$ passa a 0,69. Daí a proposta, ainda sujeita à orientação, de usar A como medida principal, C como comparação com outra base e B para examinar o efeito do método. B e C procuram domínios em textos do APK, não tráfego observado. A adjudicação usa a evidência dos próprios detectores e não constitui uma verdade de referência independente; a mudança do $\kappa$ é uma análise de sensibilidade do piloto.

**Validação do corpus.** A conferência de 4 de novembro de 2026 abrangeu 30 aplicativos sorteados sistematicamente e dois casos adicionais. Entre os 30, dois publicadores eram privados (6,7%); entre os 28 oficiais dessa parte da amostra, oito classificações de sensibilidade divergiram (28,6%), o que levou à conferência dos 396 candidatos. Com o nome jurídico que a Google Play mostra em “Sobre o desenvolvedor” como evidência, ficaram 376 aplicativos oficiais (85 federais, 199 estaduais e 92 municipais), dos quais 100 tratam dado de saúde ou biométrico. Saíram 20: 13 de empresas privadas que publicam com nome de serviço público e 7 publicados numa conta registrada em nome de pessoa física. Entre os 376, a classificação por palavra-chave e a classificação registrada divergiram em 108 casos de sensibilidade (28,7%). Esses são os resultados da classificação registrada, ainda sujeitos à validação pessoal do autor (Seção 3.10). As divergências com a regra automática não substituem a validação com evidência independente.

### 3.9 Protocolo da revisão sistemática

A revisão segue Kitchenham; Charters (2007), com bola de neve conforme Wohlin (2014) e relato do fluxo conforme o PRISMA 2020 (Page et al., 2021). O protocolo completo está no repositório do trabalho, em `tcc/revisao/protocolo-revisao-sistematica.md`; esta seção resume as decisões.

**Origem.** Uma busca exploratória feita na preparação do protocolo encontrou Samarasinghe et al. (2022), estudo de aplicativos de governo de 71 países que não estava entre os consultados quando a lacuna foi escrita na proposta. A lacuna foi reescrita (Seção 2.5), e o episódio fixou duas decisões: a revisão cobre aplicativos de governo de qualquer país, e as strings de busca são validadas contra estudos que precisam ser achados.

**Questões.** São cinco, uma por necessidade do projeto: QR1, métodos de detecção e sua validação (H4); QR2, prevalência e linha de base (H1); QR3, confronto entre o declarado e o detectado (H2); QR4, aplicativos de governo, inclusive os de enfrentamento da COVID-19 (H1, H3 e lacuna); QR5, Brasil, LGPD e transferência internacional de dados (discussão jurídica).

**Fontes e strings.** O Scopus é a base principal; o IEEE Xplore recebe as strings das QR1 a QR4; a SBC OpenLib e a BDTD cobrem a produção nacional; e a bola de neve parte dos incluídos, para trás e para a frente. A ACM Digital Library estava prevista e saiu na versão 1.1 do protocolo: a exportação dos resultados exige uma assinatura que a instituição não tem, e os anais da ACM são em grande parte indexados pelo Scopus. São 17 buscas, de 2015 a 2026, em inglês e português.

**Validação das strings.** Onze estudos conhecidos formam um conjunto de controle, na linha do padrão quase-ouro de Zhang; Babar; Tell (2011). Cada string tem de recuperar os estudos de controle que a base indexa; se não recuperar, o termo que faltou é acrescentado e a busca é refeita, com a mudança registrada no protocolo. As buscas recuperaram os 10 estudos de controle que o Scopus indexa; o décimo primeiro não está no Scopus.

**Seleção e qualidade.** Há quatro critérios de inclusão e sete de exclusão. A triagem é feita por título e resumo e depois pelo texto completo, e cada exclusão leva o código do critério que a motivou. Como a seleção tem um revisor responsável, a consistência será examinada pelo reteste de 10% das decisões e, se o orientador aceitar, por sua conferência em 20 registros, com o $\kappa$ de Cohen (Cohen, 1960) e o mesmo limiar de 0,6 usado na H4. A qualidade é avaliada por oito perguntas, das quais duas, a reprodutibilidade e a validação da detecção, medem o que a H4 discute; a nota não exclui estudos.

**Execução da triagem.** As 17 buscas de 6 de novembro de 2026 retornaram 1.531 registros. Após a remoção de 282 duplicatas, os 1.249 registros receberam decisões de F1: 886 exclusões, 6 revisões reservadas para a bola de neve e 357 encaminhamentos ao texto completo (214 inclui e 143 talvez). Esses 357 registros são candidatos, não o total final de estudos incluídos. Em 13 de novembro de 2026, a busca de textos dos 214 registros I da F1 obteve 80 publicações correspondentes. O exame de resumo, método e resultados pertinentes produziu 71 propostas I e 7 propostas E; outra exclusão EC1 foi sustentada pela declaração de ampliação no artigo posterior, totalizando 8 propostas E. Permanecem 278 decisões em aberto: 131 por acesso, 2 por divergência de versão, 2 por dúvida de escopo e os 143 registros T que aguardam definição do orientador. As propostas têm páginas e justificativas registradas e dependem de validação pessoal. A extração completa e a avaliação de qualidade ainda não estão concluídas; nenhuma exclusão por indisponibilidade (EC7) foi aplicada.

**Reteste preparado.** Foi sorteada uma amostra de 125 registros, correspondente ao arredondamento para cima de 10% dos 1.249, com a semente 20261116 prevista no script. O arquivo contém título, resumo, palavras-chave e campos de decisão vazios, sem as classificações anteriores. O reteste deverá ocorrer pelo menos sete dias depois da primeira conferência pessoal. A data de 16 de novembro é uma previsão e será adiada se esse intervalo não tiver sido cumprido. Sem uma primeira avaliação pessoal datada, a comparação com a versão existente será apenas uma comparação de versões, não uma medida de estabilidade intra-avaliador. O $\kappa$ será calculado somente depois do preenchimento e da identificação das duas avaliações. A conferência de 20 registros pelo orientador depende de sua disponibilidade. Para a decisão binária, I e T seguem para F2; E e R não seguem como estudos primários. Também serão reportadas as quatro categorias separadamente.

**Síntese.** É narrativa e organizada por questão, sem metanálise: as taxas da literatura vêm de detectores e populações diferentes, e juntá-las seria assumir o que a H4 testa.

### 3.10 Aspectos éticos e validação

As etapas executadas usaram metadados públicos da Google Play, políticas de privacidade divulgadas pelos publicadores e pacotes obtidos do AndroZoo, analisados estaticamente nos termos de uso do acervo. A análise dinâmica ainda não foi realizada. O objeto da pesquisa são os aplicativos e seus componentes, sem recrutamento de participantes nesta etapa.

As classificações registradas nas planilhas ainda dependem da validação pessoal do autor, no escopo combinado com o orientador. As decisões, suas datas e eventuais alterações serão preservadas por identificador, sem sobrescrever a avaliação anterior usada no reteste. A conferência do orientador e o reteste ainda não produziram resultados. Testes futuros usarão dispositivo e conta próprios e registrarão somente a evidência necessária, com remoção de credenciais, tokens e identificadores antes de qualquer publicação.

### 3.11 Limitações

- A análise estática mostra que o código de um SDK está presente no pacote, não que ele é executado nem que transmite dados. A subamostra dinâmica mede essa diferença em parte dos aplicativos.

- O estudo cobre apenas aplicativos Android distribuídos pela Google Play.

- Na consulta histórica, o AndroZoo continha 92 de 396 candidatos governamentais (23,2%) (Seção 3.8). Os demais são coletados direto da Google Play, com o hash registrado, e quem repetir o estudo só consegue obter a mesma versão dos que estão no acervo. Para estes, a versão pode ser anterior à vigente na loja; a defasagem é medida e reportada.

- O grupo de controle não é amostra aleatória do mercado comercial: foi montado a partir de buscas na loja por categoria, com complemento de aplicativos de publicadores não oficiais encontrados nas buscas iniciais.

- A declaração de anúncios na Google Play é feita pelo próprio publicador.

- A discussão jurídica identifica pontos de atenção à luz da LGPD; ela não substitui uma análise jurídica do caso concreto.

### 3.12 Resultados esperados

Ao final do trabalho, espera-se obter:

1.  a prevalência de rastreadores no parque governamental, com intervalo de confiança, por esfera e por tratamento de dado sensível;

2.  a razão de prevalências de aplicativos com rastreadores entre governo e controle pareado, com tamanho de efeito;

3.  a proporção de SDKs detectados que não constam da declaração do publicador;

4.  a medida de concordância entre detectores e o efeito da ferramenta sobre a taxa reportada;

5.  um conjunto de dados reprodutível, com a lista dos aplicativos, os hashes dos pacotes analisados e os scripts de coleta e análise.

**Plano de análise principal.** A presença de ao menos um SDK é uma variável binária. H1 e H3 serão analisadas por razões de prevalências, com regressão de Poisson e variância robusta (Zou, 2004), ajustadas pelas variáveis com suporte nos dados. A contagem de SDKs será um desfecho secundário, com modelo binomial negativo se houver sobredispersão. Serão informados estimativas, IC95%, perdas de pacotes e células sem controle; não rejeitar diferença não será interpretado como provar igualdade. O detector principal, o tratamento de versões, as regras para políticas genéricas e a multiplicidade das comparações serão fixados com o orientador antes da análise principal. A concordância entre detectores será reportada junto dos acordos positivo e negativo; concordância não mede, sozinha, acurácia contra uma verdade de referência.

### 3.13 Recursos necessários

A execução requer recursos humanos, computacionais e de acesso às fontes. O planejamento prevê o reaproveitamento de equipamento do pesquisador e o uso de programas de código aberto. A disponibilidade e a configuração do dispositivo para a etapa dinâmica ainda precisam ser registradas; não se pressupõe a aquisição de equipamento nem a contratação de serviços pagos.

**Quadro 4 — Recursos necessários e situação de acesso**

| **Recurso**                   | **Finalidade**                                                                              | **Situação e previsão**                                                                                                      |
|:------------------------------|:--------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------|
| Pesquisador e orientação      | Leitura, classificação, coleta, análise e revisão metodológica                              | Trabalho individual; encontros e validação de decisões pelo orientador conforme o calendário da disciplina                   |
| Computador e armazenamento    | Executar scripts, extrair APKs, guardar resultados e cópias de segurança                    | Dimensionamento a confirmar com o teste de coleta e extração; separar dados brutos, resultados e cópia de segurança          |
| Dispositivo Android e conexão | Instalar a subamostra e observar os cenários da análise dinâmica                            | Usar dispositivo e conta próprios, compatíveis com os apps; registrar sistema, versão e limitações de acesso                 |
| Programas de análise          | Python, Androguard, MobSF, bases Exodus e Disconnect, ferramentas de inspeção de rede e Git | Fixar versões e hashes das bases antes da coleta principal; observar as licenças e condições de uso                          |
| Fontes bibliográficas         | Scopus, IEEE Xplore, SBC OpenLib, BDTD e textos completos                                   | Acesso institucional quando disponível e repositórios abertos; registrar indisponibilidade e tentativas de obtenção          |
| Pacotes e metadados           | AndroZoo e Google Play na região brasileira                                                 | Acesso acadêmico ao AndroZoo obtido; a coleta direta ainda depende do teste em cinco aplicativos                             |
| Documentação e edição         | Planilhas, leitor de PDF, editor de texto/LaTeX e repositório                               | Guardar decisões por identificador estável e manter histórico de versões; não publicar credenciais nem tráfego identificável |

*Fonte: Planejamento da pesquisa (2026).*

O piloto ocupou aproximadamente 518 MB para 20 pacotes. Uma extrapolação apenas para dimensionamento dos 628 candidatos à coleta principal (376 governamentais e 252 controles) resulta em cerca de 16,3 GB de APKs, antes de extração, logs e cópias. Esse valor não é uma medição do corpus completo. Prevê-se reservar inicialmente 100 GB livres para o trabalho e uma cópia de segurança separada, revendo a estimativa após o teste de coleta direta. Quantidade de memória, tempo de processamento e compatibilidade do dispositivo serão registrados nesse teste, sem tratá-los como requisitos já validados.

Não há orçamento de compra aprovado. O plano inicial não prevê pagamento de licenças dos programas indicados nem compra individual de artigos; eventuais despesas de equipamento, armazenamento, conectividade ou acesso excepcional serão cotadas e combinadas com o orientador antes da contratação. Internet, energia e equipamento reaproveitado constituem recursos empregados, mesmo quando não geram uma despesa adicional registrada no projeto.

### 3.14 Critérios de análise da LGPD

A análise jurídica será operacionalizada por uma matriz documental, associada à evidência técnica de cada versão do aplicativo. A unidade de registro reúne aplicativo, hash do pacote, destinatário, categoria de dado, finalidade e cenário de execução. A presença estática de um SDK será distinguida da transmissão observada e da declaração encontrada na política. A matriz é uma proposta a validar com o orientador antes da coleta principal, não uma avaliação já aplicada ao corpus.

Serão examinados três eixos: a hipótese legal indicada para a operação com dados pessoais (Art. 7º), o enquadramento específico quando houver dado sensível (Art. 11) e a caracterização e o mecanismo de eventual transferência internacional (Art. 33) (Brasil, 2018). O consentimento não será exigido indistintamente de todas as operações do poder público. A finalidade do serviço, a competência do órgão e os compartilhamentos serão examinados com apoio no guia da ANPD (Autoridade Nacional de Proteção de Dados, 2023). A base legal do tratamento e o mecanismo de transferência internacional serão registrados em campos separados, conforme a Resolução CD/ANPD nº 19/2024 (Autoridade Nacional de Proteção de Dados, 2024).

Cada item receberá um resultado: *documentado*, *indício de inconsistência*, *não verificável* ou *não aplicável*, acompanhado da evidência e da justificativa. Documento ausente ou inacessível será marcado como não verificável, sem presumir inexistência de base legal ou de contrato. Um resultado documentado tampouco certifica a conformidade integral do aplicativo.

Para a H2, serão contados pares aplicativo–SDK, com distinção entre menção nominal, declaração por categoria, ausência de menção e política indisponível. O denominador incluirá apenas pares com detecção confirmada e política recuperada; políticas indisponíveis serão informadas à parte. Declarações genéricas serão objeto de análise de sensibilidade. A expressão fluxo não declarado será reservada aos casos em que o fluxo foi observado, enquanto a detecção estática produzirá uma comparação documental.

Na análise dinâmica, país do ponto de rede, país da entidade destinatária e localização documentada de tratamento serão campos distintos. A nacionalidade do fornecedor e a geolocalização de um IP não demonstram, isoladamente, uma transferência internacional. A matriz separará transferência, coleta internacional direta e situação indeterminada, observando as distinções da Resolução nº 19/2024 (Autoridade Nacional de Proteção de Dados, 2024). O roteiro completo, com dez critérios e ficha de evidências, está em `tcc/metodologia/criterios-lgpd.md`.

### 3.15 Cronograma até a defesa do Projeto Capstone I

As datas da disciplina são as do plano de ensino: simulação de defesa em 24/11, 26/11 ou 01/12, conforme a ordem da turma, com 15 minutos de apresentação e 10 de arguição; entrega da redação no Canvas até 03/12; defesa final em 08/12, 10/12 ou 15/12, com 15 minutos de apresentação e 15 de arguição. O regulamento exige cinco encontros de orientação registrados no bimestre. As atividades já concluídas estão descritas nas seções anteriores; o quadro abaixo traz só o que falta.

**Quadro 5 — Cronograma até a defesa do Projeto Capstone I**

| **Período**                      | **Atividade**                                                                                                                                              | **Produto**                                                  |
|:---------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------|
| 11/11 a 16/11                    | Encontro de orientação: eixo da discussão, escopo da revisão, recursos, critérios e detector principal                                                     | Decisões registradas; ficha de orientação                    |
| 11/11 a 16/11                    | Testar a coleta direta da Google Play, com hash registrado, em cinco aplicativos fora do AndroZoo                                                          | Procedimento de coleta direta definido                       |
| 16/11, condicionado ao intervalo | Reteste cego de 125 registros, pelo menos sete dias após a primeira conferência pessoal                                                                    | Decisões datadas e $\kappa$ após preenchimento               |
| 11/11 a 23/11                    | Leitura do texto completo, bola de neve e extração da revisão sistemática, no escopo combinado com o orientador; seção de revisão bibliográfica            | Lista de trabalhos incluídos; seção de revisão bibliográfica |
| até 23/11                        | Validação das classificações dos artigos e dos aplicativos pelo autor, no escopo combinado com o orientador                                                | Validação registrada no repositório                          |
| 17/11 a 23/11                    | Validar com o orientador a matriz de critérios da LGPD e os recursos; congelar o protocolo e o plano de análise com data; revisar e ensaiar a apresentação | Protocolo congelado; slides da simulação                     |
| 24/11 a 01/12                    | Simulação de defesa                                                                                                                                        | Apresentação e sugestões da avaliadora                       |
| até 03/12                        | Incorporar as sugestões e entregar a redação no modelo ABNT                                                                                                | Redação entregue; ficha de orientação                        |
| 08/12 a 15/12                    | Defesa final do Projeto Capstone I                                                                                                                         | Apresentação                                                 |

*Fonte: Elaborado pelo autor (2026).*

### 3.16 Cronograma do Projeto Capstone II (2027.1)

**Quadro 6 — Cronograma do Projeto Capstone II**

| **Mês**   | **Atividade**                                                                                                                                                                                                                                       |
|:----------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fevereiro | Download e detecção em todo o corpus validado e no controle ampliado: AndroZoo para os aplicativos do acervo, Google Play direta para os demais                                                                                                     |
| Março     | Confronto com as políticas de privacidade e com a seção “Segurança dos dados” (H2); comparação entre aplicativos sensíveis e não sensíveis (H3)                                                                                                     |
| Abril     | Análise dinâmica da subamostra com dispositivo e conta próprios: destinos, jurisdição e taxa de bloqueio por *certificate pinning*                                                                                                                  |
| Maio      | Análise estatística conforme o plano congelado: razões de prevalências para H1 e H3, proporções com IC para H2 e concordância para H4; contagens como análise secundária. Comunicação de achados graves aos órgãos responsáveis antes da publicação |
| Junho     | Redação final, publicação do conjunto de dados e defesa                                                                                                                                                                                             |

*Fonte: Elaborado pelo autor (2026).*

### 3.17 Riscos e contingências

**Quadro 7 — Riscos e contingências**

| **Risco**                                                                | **Efeito**                                                                              | **Contingência**                                                                                                                       |
|:-------------------------------------------------------------------------|:----------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| Cobertura baixa do AndroZoo (ocorreu: 23,2% do governo)                  | Fonte do pacote diferente entre os grupos; reconstrução parcial do corpus por terceiros | Coleta direta da loja com SHA-256 registrado; fonte registrada por aplicativo e usada em análise de sensibilidade; limitação declarada |
| Versão do AndroZoo muito anterior à da loja                              | Resultado desatualizado                                                                 | Reportar a defasagem; usar a coleta direta para os mais defasados                                                                      |
| Prevalência muito alta ou muito baixa                                    | $\kappa$ instável mesmo com acordo alto                                                 | Reportar, junto do $\kappa$, as proporções de concordância positiva e negativa                                                         |
| Células de porte pequeno sem controle (18 vagas, na maioria em $10^{2}$) | Ajuste por categoria na H1 sem sustentação nessas células                               | Restringir a H1 às células com suporte e reportar a análise com e sem a restrição                                                      |
| Achado grave atribuível a um órgão                                       | Risco ao cidadão se publicado antes da correção                                         | Comunicação prévia ao órgão e, se couber, ao CTIR Gov e à ANPD, com prazo definido com o orientador                                    |
| Atraso nos encontros de orientação                                       | Reprovação por falta de encontros                                                       | Agendar os cinco encontros já no primeiro deles                                                                                        |

*Fonte: Elaborado pelo autor (2026).*

## Referências

ALECCI, M. et al. AndroZoo: a retrospective with a glimpse into the future. In: **Proceedings of the 21st International Conference on Mining Software Repositories**. New York: ACM, 2024. p. 389–393. DOI: 10.1145/3643991.3644863.

ALLIX, K. et al. AndroZoo: collecting millions of Android apps for the research community. In: **Proceedings of the 13th International Conference on Mining Software Repositories**. New York: ACM, 2016. p. 468–471. DOI: 10.1145/2901739.2903508.

ANDOW, B. et al. Actions speak louder than words: entity-sensitive privacy policy and data flow analysis with PoliCheck. In: **29th USENIX Security Symposium**. Berkeley: USENIX Association, 2020. p. 985–1002. Disponı́vel em: <https://www.usenix.org/conference/usenixsecurity20/presentation/andow>. Acesso em: 13 nov. 2026.

ANDROGUARD. **Androguard**. 2026. Versão 4.1.4. Disponı́vel em: <https://pypi.org/project/androguard/4.1.4/>. Acesso em: 20 out. 2026.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Tratamento de dados pessoais pelo Poder Público: guia orientativo**. Brasília, DF: ANPD, 2023. Versão 2.0. Disponı́vel em: <https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-poder-publico-anpd-versao-final.pdf>. Acesso em: 13 nov. 2026.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Resolução CD/ANPD nº 19, de 23 de agosto de 2024**. 2024. Regulamento de Transferência Internacional de Dados e cláusulas-padrão contratuais. Texto consolidado. Disponı́vel em: <https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024>. Acesso em: 13 nov. 2026.

BINNS, R. et al. Third party tracking in the mobile ecosystem. In: **Proceedings of the 10th ACM Conference on Web Science**. New York: ACM, 2018. p. 23–31. DOI: 10.1145/3201064.3201089.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018: Lei Geral de Proteção de Dados Pessoais (LGPD)**. 2018. Diário Oficial da União: seção 1, Brasília, DF, 15 ago. 2018. Disponı́vel em: <https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html>. Acesso em: 13 nov. 2026.

COHEN, J. A coefficient of agreement for nominal scales. **Educational and Psychological Measurement**, v. 20, n. 1, p. 37–46, 1960. DOI: 10.1177/001316446002000104.

DISCONNECT. **Disconnect tracking protection**. 2026. Lista de serviços de rastreamento, licença CC BY-NC-SA 4.0. Disponı́vel em: <https://github.com/disconnectme/disconnect-tracking-protection>. Acesso em: 20 out. 2026.

EXODUS PRIVACY. **$\varepsilon$xodus: trackers**. 2026. Base de assinaturas de rastreadores. Disponı́vel em: <https://reports.exodus-privacy.eu.org/en/trackers/>. Acesso em: 28 out. 2026.

FLEISS, J. L. Measuring nominal scale agreement among many raters. **Psychological Bulletin**, v. 76, n. 5, p. 378–382, 1971. DOI: 10.1037/h0031619.

JOMINGYU. **google-play-scraper**. 2024. Versão 1.2.7. Disponı́vel em: <https://pypi.org/project/google-play-scraper/>. Acesso em: 20 out. 2026.

KENDALL, M. G. A new measure of rank correlation. **Biometrika**, v. 30, n. 1-2, p. 81–93, 1938. DOI: 10.1093/biomet/30.1-2.81.

KITCHENHAM, B.; CHARTERS, S. **Guidelines for performing systematic literature reviews in software engineering**. Keele: Keele University; Durham University, 2007. (Technical Report EBSE-2007-01).

KOLLNIG, K. et al. Before and after GDPR: tracking in mobile apps. **Internet Policy Review**, v. 10, n. 4, 2021a. DOI: 10.14763/2021.4.1611.

KOLLNIG, K. et al. A fait accompli? An empirical study into the absence of consent to third-party tracking in Android apps. In: **Proceedings of the 17th Symposium on Usable Privacy and Security**. Berkeley: USENIX Association, 2021b. p. 181–196.

MANTEL, N.; HAENSZEL, W. Statistical aspects of the analysis of data from retrospective studies of disease. **Journal of the National Cancer Institute**, v. 22, n. 4, p. 719–748, 1959.

MOBSF. **Mobile Security Framework (MobSF)**. 2026. Versão 4.5.3. Disponı́vel em: <https://pypi.org/project/mobsf/4.5.3/>. Acesso em: 20 out. 2026.

NGUYEN, T. T.; BACKES, M.; STOCK, B. Freely given consent? Studying consent notice of third-party tracking and its violations of GDPR in Android apps. In: **Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security**. New York: ACM, 2022. p. 2369–2383. DOI: 10.1145/3548606.3560564.

PAGE, M. J. et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. **BMJ**, v. 372, 2021. Art. n71. DOI: 10.1136/bmj.n71.

POHLE, J.; THIEL, T. Digital sovereignty. **Internet Policy Review**, v. 9, n. 4, 2020. DOI: 10.14763/2020.4.1532.

RAZAGHPANAH, A. et al. Apps, trackers, privacy, and regulators: a global study of the mobile tracking ecosystem. In: **Proceedings of the Network and Distributed System Security Symposium**. Reston: Internet Society, 2018. DOI: 10.14722/ndss.2018.23353.

SAMARASINGHE, N. et al. Et tu, Brute? Privacy analysis of government websites and mobile apps. In: **Proceedings of the ACM Web Conference 2022**. New York: ACM, 2022. p. 564–575. DOI: 10.1145/3485447.3512223.

SERRANO, N.; BETARTE, G.; CAMPO, J. D. Third-party trackers in COVID-19 mobile applications can enable privacy leaks. In: **Proceedings of the 12th Latin-American Symposium on Dependable and Secure Computing**. New York: ACM, 2023. p. 80–89. DOI: 10.1145/3615366.3615426.

SERRANO, N.; BETARTE, G.; CAMPO, J. D. COVID-19 mobile applications: a study of trackers and data leaks. **Journal of Internet Services and Applications**, v. 15, n. 1, p. 139–159, 2024. DOI: 10.5753/jisa.2024.3882.

SLAVIN, R. et al. Toward a framework for detecting privacy policy violations in Android application code. In: **Proceedings of the 38th International Conference on Software Engineering**. New York: ACM, 2016. p. 25–36. DOI: 10.1145/2884781.2884855.

WILSON, E. B. Probable inference, the law of succession, and statistical inference. **Journal of the American Statistical Association**, v. 22, n. 158, p. 209–212, 1927. DOI: 10.1080/01621459.1927.10502953.

WOHLIN, C. Guidelines for snowballing in systematic literature studies and a replication in software engineering. In: **Proceedings of the 18th International Conference on Evaluation and Assessment in Software Engineering**. New York: ACM, 2014. p. 1–10. DOI: 10.1145/2601248.2601268.

ZHAN, X. et al. A systematic assessment on Android third-party library detection tools. **IEEE Transactions on Software Engineering**, v. 48, n. 11, p. 4249–4273, 2022. DOI: 10.1109/TSE.2021.3115506.

ZHAN, X. et al. Automated third-party library detection for Android applications: are we there yet? In: **Proceedings of the 35th IEEE/ACM International Conference on Automated Software Engineering**. New York: ACM, 2020. p. 919–930. DOI: 10.1145/3324884.3416582.

ZHANG, H.; BABAR, M. A.; TELL, P. Identifying relevant studies in software engineering. **Information and Software Technology**, v. 53, n. 6, p. 625–637, 2011. DOI: 10.1016/j.infsof.2010.12.010.

ZIMMECK, S. et al. MAPS: scaling privacy compliance analysis to a million apps. **Proceedings on Privacy Enhancing Technologies**, v. 2019, n. 3, p. 66–86, 2019. DOI: 10.2478/popets-2019-0037.

ZOU, G. A modified Poisson regression approach to prospective studies with binary data. **American Journal of Epidemiology**, v. 159, n. 7, p. 702–706, 2004. DOI: 10.1093/aje/kwh090.
