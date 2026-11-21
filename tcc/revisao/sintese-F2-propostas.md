# Síntese da leitura completa (F2): propostas de inclusão

Gerado em 15/11/2026 a partir de `dados/revisao/leitura_F2_registro_20261113.csv` e da aba Leitura de `dados/revisao/leitura_F2_para_preencher.xlsx`.

São as **71 propostas de inclusão** da rodada de 13/11, agrupadas pela questão de pesquisa (QR) provável. A Seção 2.7 do projeto já resume estes estudos, com um quadro e um parágrafo por QR. Use esta lista para escolher e ler os principais de cada grupo e ajustar aquele texto com as suas palavras.

| QR | Propostas |
|---|---|
| QR1: detecção de bibliotecas ou SDKs de terceiros | 22 |
| QR2: rastreadores ou dados enviados a terceiros por apps | 20 |
| QR3: confronto entre o declarado (política, rótulo) e o que o app faz | 15 |
| QR4: apps de governo | 4 |
| QR4: apps de governo da COVID-19 | 6 |
| QR5: LGPD ou Brasil | 2 |
| QR5: soberania ou transferência internacional de dados | 2 |
| **Total** | **71** |

Como usar na redação: para cada QR, diga o que os estudos mediram, com qual método e o que encontraram; destaque o que sustenta ou contradiz H1 a H3 e o que continua em aberto para o caso brasileiro. Não some taxas de estudos diferentes (Seção 3.7, Síntese).

## QR1: detecção de bibliotecas ou SDKs de terceiros

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0209 | Kajiwara, Naoya et al. (2015) | Detection of Android ad library focusing on HTTP connections and view object redraw behaviors | Avalia detecção de publicidade por tráfego HTTP e redesenho de interface | Seções V–VI e Tabela II; p. 5–7 |
| R0895 | J. Rubin et al. (2015) | Covert Communication in Mobile Applications (T) | Analisa comunicação de aplicativos com terceiros e compara detecção à referência manual | Método e seção IV.A, Tabela IV; p. 1, 7–8 |
| R0077 | Soh, Charlie et al. (2016) | LibSift: Automated detection of third-party libraries in android applications | Avalia separação de bibliotecas em 300 aplicativos com conferência manual | Seção III e Tabela I; p. 5 |
| R0105 | Backes, Michael et al. (2016) | Reliable third-party library detection in Android and its security applications | Detecta bibliotecas e mede sua presença em aplicativos Android | Seções 4–6 e Tabelas 2–3; p. 5–8 |
| R0312 | Continella, Andrea et al. (2017) | Obfuscation-Resilient Privacy Leak Detection for Mobile Apps Through Differential Analysis | Detecta vazamentos por análise diferencial de tráfego e compara ferramentas | Seção VI e Tabelas I–II; p. 8–10 |
| R0030 | Zhang, Yuan et al. (2018) | Detecting third-party libraries in Android applications with high precision and recall | Avalia precisão e revocação do LibPecker com conjuntos de referência | Seção IV e Tabelas II–III; p. 7–8 |
| R0093 | Wang, Yan et al. (2018) | ORLIS: Obfuscation-resilient library detection for Android | Avalia ORLIS com aplicativos ofuscados e referência derivada dos registros de transformação | Seção 4.1 e Tabela 3; p. 6–7 |
| R0399 | Su, Ming-Yang et al. (2018) | Using ad-related network behavior to distinguish ad libraries | Analisa bibliotecas de publicidade por grafos de comportamento de rede | Seções 3–4 e Tabelas 1–3; p. 6, 9–15 |
| R0070 | Zhang, Jiexin et al. (2019) | LibiD: Reliable identification of obfuscated third-party android libraries | Avalia LibID com aplicativos sintéticos e bibliotecas conhecidas sob ofuscação | Seção 5.1 e Tabela 2; p. 6–7 |
| R0088 | Feichtner, Johannes et al. (2019) | Obfuscation-resilient code recognition in android apps | Avalia reconhecimento de código e bibliotecas Android sob diferentes ofuscações | Seção 5 e Tabela 1; p. 7, 9 |
| R0064 | Li, Menghao et al. (2020) | Large-Scale Third-Party Library Detection in Android Markets | Avalia LibD em aplicativos Android e compara detecções com conferência manual | Seções III–IV e Tabelas I–IV; p. 1, 6–7 |
| R0019 | Zhan, Xian et al. (2021) | ATVHunter: Reliable version detection of third-party libraries for vulnerability identification in android applications | Avalia ATVHunter com bibliotecas e versões de referência em aplicativos Android | Seção IV e Tabela I; p. 6–7 |
| R0007 | Zhan, Xian et al. (2022) | A Systematic Assessment on Android Third-Party Library Detection Tools | Compara cinco ferramentas de detecção com conjuntos de referência e métricas quantitativas | Seções 5–6 e Tabela 2; p. 2, 9–11 |
| R0071 | Domínguez-Álvarez, Daniel et al. (2023) | LibKit: Detecting Third-Party Libraries in iOS Apps | Avalia detecção de bibliotecas em aplicativos iOS com referência e métricas | Seções 4–5 e Tabela 2; p. 8–9 |
| R0076 | Wu, Yafei et al. (2023) | LibScan: Towards More Precise Third-Party Library Identification for Android Applications | Avalia LibScan com aplicativos e versões de bibliotecas de referência | Seções 5.1–5.3 e Tabelas 5–6; p. 8–9 |
| R0109 | Huang, Jianjun et al. (2023) | Scalably Detecting Third-Party Android Libraries With Two-Stage Bloom Filtering | Avalia LIBLOOM com bibliotecas de referência e diferentes ofuscadores | Seções 5.1–5.3 e Tabelas 2 e 4; p. 7–9 |
| R0055 | Xie, Zifan et al. (2024) | How Does Code Optimization Impact Third-party Library Detection for Android Applications? | Avalia o impacto da otimização e o desempenho do detector LibHunter | Método, seção 5 e Tabela 3; p. 3, 9–10 |
| R0845 | J. Samhi et al. (2024) | AndroLibZoo: A Reliable Dataset of Libraries Based on Software Dependency Analysis | Constrói e caracteriza base de bibliotecas Android a partir de dependências | Seções 2–4, Figura 1 e Tabela 1; p. 1–4 |
| R0094 | Pan, Dahan et al. (2025) | Pay Your Attention on Lib! Android Third-Party Library Detection via Feature Language Model | Avalia LibAttention com referência de dependências e divisão treino e teste | Seção IV e Tabela III; p. 6–8 |
| R0129 | Zhou, Bolin et al. (2025) | Version-level Third-Party Library Detection in Android Applications via Class Structural Similarity | Avalia SAD e compara identificação de bibliotecas e versões | Seção 4 e Tabelas 2–3; p. 6–7 |
| R0414 | Liu, Wei et al. (2025) | WTDetect: a third-party website tracking detection framework for android applications | Analisa rastreamento de terceiros em WebViews de aplicativos Android | Design and implementation, Evaluation e Tabela 4; p. 1, 4–6, 11–12 |
| R0015 | Pan, Dahan et al. (2026) | An Empirical Study on the Robustness of Android Third-Party Library Detection Tools Against Advanced Obfuscation | Avalia detecção de bibliotecas sob ofuscação com referência construída pela compilação | Seção 4 e Tabela 5; p. 6–8 |

## QR2: rastreadores ou dados enviados a terceiros por apps

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0648 | Huckvale, Kit et al. (2015) | Unaddressed privacy risks in accredited health and wellness apps: A cross-sectional systematic assessment | Confronta políticas e transmissões de apps de saúde, incluindo serviços terceiros | Methods e Results, Tabela 1; p. 2–3, 5–6 |
| R0057 | Liu, Minxing et al. (2016) | Identifying and analyzing the privacy of apps for kids | Mede bibliotecas de publicidade e outros terceiros em aplicativos infantis | Avaliação e análise de privacidade, Tabela 4; p. 1, 3–5 |
| R0248 | Demetriou, Soteris et al. (2016) | Free for All! Assessing User Data Exposure to Advertising Libraries on Android | Avalia exposição de dados de usuários a bibliotecas publicitárias em aplicativos reais | Seção IV e Tabelas I–II; p. 4–6 |
| R0138 | Ikram, Muhammad et al. (2017) | A first look at mobile Ad-Blocking apps | Mede bibliotecas de rastreamento em bloqueadores Android e compara controles | Método e Tabela IV; p. 1, 3, 5 |
| R0168 | Razaghpanah, Abbas et al. (2018) | Apps, Trackers, Privacy, and Regulators A Global Study of the Mobile Tracking Ecosystem | Analisa tráfego de aplicativos e identifica serviços de publicidade e rastreamento | Seções III–IV e Tabela II; p. 1, 3, 5 |
| R0292 | Binns, Reuben et al. (2018) | Measuring third-party tracker power across web and mobile | Mede presença e concentração de rastreadores em apps e sites | Seção 5 e Tabela 1; p. 8–9, 12 |
| R0376 | Binns, Reuben et al. (2018) | Third party tracking in the mobile ecosystem | Mede presença de domínios de rastreadores no código de aplicativos Android | Seções 3–4 e Tabela 1; p. 3, 5 |
| R0184 | Hu, Boyang et al. (2019) | Characterizing Location-based Mobile Tracking in Mobile Ad Networks | Mede dados pessoais enviados a redes de anúncios por aplicativos em diferentes locais | Método de captura e seção V, Tabela III; p. 1, 4–5 |
| R0136 | Kollnig, Konrad et al. (2021) | A fait accompli? An empirical study into the absence of consent to third-party tracking in Android apps | Mede conexões a rastreadores antes e depois do consentimento em apps Android | Seção 4 e Tabela 1; p. 1, 6–7 |
| R0178 | Kollnig, Konrad et al. (2021) | Before and after GDPR: Tracking in mobile apps | Compara presença de rastreadores em aplicativos antes e depois da GDPR | Methodology e Tabela 1; p. 9–10, 17 |
| R0249 | Nguyen, Trung Tin et al. (2022) | Freely Given Consent?: Studying Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps | Compara avisos de consentimento com transmissão de dados a terceiros | Método e análise de tráfego da Seção 4.4; p. 1, 4–5, 7, 9 |
| R0567 | Saini, Shalini et al. (2022) | Mobile Mental Health Apps: Alternative Intervention or Intrusion? | Analisa tráfego e políticas de privacidade de aplicativos de saúde mental | Seções V–VI e Tabelas III–V; p. 4–6, 8–9 |
| R1145 | M. Ahasanuzzaman et al. (2022) | Studying Ad Library Integration Strategies of Top Free-to-Download Apps | Mede integração de bibliotecas publicitárias e distingue analytics de exibição de anúncios | Método de identificação e Tabelas 1–3; p. 1, 3–4 |
| R0579 | Iwaya, Leonardo Horn et al. (2023) | On the privacy of mental health apps: An empirical investigation and its implications for app development | Combina análise estática, tráfego e políticas de aplicativos de saúde mental | Seções 3–4 e Tabela 2; p. 9, 12, 16–17 |
| R0047 | Dong, Zikan et al. (2024) | Exploring Covert Third-party Identifiers through External Storage in the Android New Era | Detecta e atribui identificadores persistentes a SDKs de rastreamento Android | Método, atribuição manual e Tabelas 1–2; p. 1–2, 5–6, 8, 10 |
| R0060 | Liu, Dexin et al. (2024) | iHunter: Hunting Privacy Violations at Scale in the Software Supply Chain on iOS | Analisa fluxos de dados e práticas de SDKs iOS contra políticas | Análise de fluxo, avaliação e Tabela 3; p. 2, 7, 10–11 |
| R0085 | Zhang, Yifan et al. (2024) | Navigating the Privacy Compliance Maze: Understanding Risks with Privacy-Configurable Mobile SDKs | Avalia configuração de privacidade de SDKs e riscos em aplicativos Android | PICOSCAN, Tabela 3 e medição da Seção 6; p. 2, 7, 11–12 |
| R0092 | Heid, Kris et al. (2026) | Opportunistic Permission Exploitation of Third-Party Libraries in Android Apps | Mede aproveitamento de permissões por bibliotecas em mil aplicativos Android | Método estático e Evaluation, Figura 3; p. 1, 4, 16–17 |
| R0120 | Aljedaani, Bakheet (2026) | Third-Party Service Categories in Android Mobile Gaming Apps: A Static Empirical Analysis | Mede categorias de SDKs de terceiros em jogos Android | Seções 3.3–3.4 e Tabela 2; p. 1, 8–9, 12 |
| R0705 | Pybu, Jennifer et al. (2026) | Extraction-by-design: Auditing infrastructures of datafication in baby-tracking apps | Analisa SDKs e declarações de privacidade em 14 aplicativos de acompanhamento infantil | Methodology e achados da auditoria; p. 8–11, 13, 15–16 |

## QR3: confronto entre o declarado (política, rótulo) e o que o app faz

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0641 | Slavin, Rocky et al. (2016) | Toward a framework for detecting privacy policy violations in android application code | Compara fluxos estáticos de dados com políticas de aplicativos Android | Framework de fluxos; Seção 5.2 e Tabela 1; p. 1, 4, 7 |
| R0468 | Zimmeck, Sebastian et al. (2017) | Automated Analysis of Privacy Requirements for Mobile Apps | Confronta práticas de coleta e compartilhamento com políticas de apps | Anotações da Tabela I e validação da análise estática na Tabela IV; p. 1, 6, 9 |
| R0417 | Kununka, Sophia et al. (2018) | A comparative study of android and iOS mobile applications’ data handling practices versus compliance to privacy policy | Confronta dados enviados a terceiros com políticas de apps Android e iOS | Seção 3, Tabela 1 e Figuras 2–3; p. 1, 4, 7 |
| R0442 | Andow, Benjamin et al. (2020) | Actions speak louder than words: Entity-sensitive privacy policy and data flow analysis with policheck | Confronta fluxos observados e destinatários com políticas de aplicativos Android | Seção 4, Tabelas 2–3 e caracterização da Seção 5; p. 2–3, 9–10 |
| R0449 | Fan, Ming et al. (2020) | An empirical evaluation of GDPR compliance violations in android mhealth apps | Confronta fluxos de dados de saúde com declarações das políticas de apps | Seções III–IV e Tabelas I–III; p. 4, 7–8 |
| R0581 | Verderame, Luca et al. (2020) | On the (Un)Reliability of Privacy Policies in Android Apps | Monitora acesso a dados por aplicativos e bibliotecas confrontando políticas | Implementação 3PDroid e Tabela IV; p. 1, 5–6 |
| R0600 | Zimmeck, Sebastian et al. (2021) | PrivacyFlash Pro: Automating Privacy Policy Generation for Mobile Apps | Compara bibliotecas presentes com políticas geradas e avalia detecção estática | Tabelas IV–V e Seções III–IV; p. 1, 5, 7, 10 |
| R0500 | Zhao, Kaifa et al. (2023) | Demystifying Privacy Policy of Third-Party Libraries in Mobile Apps | Analisa fluxos de dados em bibliotecas e inconsistências nas políticas | Método ATPChecker e Tabela IV; p. 3, 6–7 |
| R0527 | Achilleos, Georgios et al. (2023) | Exploring Personal Data Processing in Video Conferencing Apps | Combina Exodus e Lumen para comparar rastreadores, tráfego e políticas | Seção 4.3, Tabela 1 e Seção 5.2; p. 1, 6–9 |
| R0552 | Xiao, Yue et al. (2023) | Lalaine: Measuring and Characterizing Non-Compliance of Apple Privacy Labels | Compara fluxos de dados de aplicativos iOS com rótulos de privacidade | Arquitetura, Tabela 4 e avaliação da Seção 4.4; p. 1, 5, 9 |
| R0643 | Jain, Vijayanta et al. (2023) | Towards Fine-Grained Localization of Privacy Behaviors | Localiza comportamentos de processamento, compartilhamento, publicidade e análise em código Android | Seções 3–6 e Tabela 2; p. 1, 4–6, 9–11 |
| R0005 | Cory, Thomas et al. (2024) | A Qualitative Analysis Framework for mHealth Privacy Practices | Confronta rastreadores, tráfego e rótulos de privacidade em 152 apps de saúde | Seções 4–5 e Tabela 1; p. 3–4, 6 |
| R0545 | Tu, Tengfei et al. (2024) | Intelligent analysis of android application privacy policy and permission consistency | Confronta permissões de aplicativos e SDKs com políticas de privacidade | Seção 4.1 e Tabela 4 da avaliação; p. 1, 8, 16–17 |
| R0504 | Baalous, Rawan et al. (2025) | Detecting the Inconsistency between Android Apps’ Data Collection and Google Play’s Data Safety Using Static Analysis | Confronta indicadores estáticos de coleta com rótulos Data Safety | Método e Figuras 7–8; p. 6, 11–12 |
| R0436 | Khedkar, Mugdha et al. (2026) | A study of privacy-related data collected by Android apps | Compara coleta identificada estaticamente com declarações de segurança de dados | Seções 5–6, comparação de formulários e código; p. 13–15 |

## QR4: apps de governo

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0229 | Samarasinghe, Nayanamana et al. (2022) | Et tu, Brute? Privacy Analysis of Government Websites and Mobile Apps | Mede SDKs e tráfego de dados em aplicativos governamentais | Seções 3.4, 3.5 e 5; Tabela 2; p. 3, 5, 7–8 |
| R0662 | Carlsson, Robin et al. (2022) | Where Does Your Data Go? Comparing Network Traffic and Privacy Policies of Public Sector Mobile Applications | Compara tráfego de aplicativos públicos finlandeses com políticas e destinatários | Seção 3, Tabela 1 e Seção 4.2; p. 1, 4–5, 7 |
| R0743 | Firmino, Rodrigo Jose et al. (2022) | Smart Pandemic Surveillance?: A Neo-Materialist Analysis of the “Monitora Covid-19” Application in Brazil | Analisa aplicativo público brasileiro, rastreadores, documentação e proteção de dados | Método, governança do Monitora Covid-19 e Figura 1; p. 1, 5–8, 11–12 |
| R0584 | Jiang, Jiayi et al. (2023) | Personal Information Protection and Privacy Policy Compliance of Health Code Apps in China: Scale Development and Content Analysis | Avalia políticas de aplicativos públicos incluindo requisitos de transferência internacional | Método, Tabela 1 e resultados de transmissão transfronteiriça; p. 1, 3–5 |

## QR4: apps de governo da COVID-19

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0216 | Kouliaridis, Vasileios et al. (2021) | Dissecting contact tracing apps in the Android platform | Detecta rastreadores em aplicativos oficiais europeus de rastreamento de contatos | Seção 2 e análise de rastreadores em 4.3; p. 1, 4, 15 |
| R0423 | Samhi, Jordan et al. (2021) | A first look at Android applications in Google Play related to COVID-19 | Analisa fluxos de dados de aplicativos COVID-19 com conferência manual | Seção 3.3 e Tabela 10; p. 1, 6–7, 10, 12, 35–36, 40–41 |
| R0433 | Hatamian, Majid et al. (2021) | A privacy and security analysis of early-deployed COVID-19 contact tracing Android apps | Analisa acesso efetivo a dados e políticas de 28 aplicativos COVID-19 | Desenho, monitoramento em execução e Tabela 4; p. 1, 6, 15, 24, 34 |
| R0476 | Flood, Robert et al. (2022) | Checking Contact Tracing App Implementations with Bespoke Static Analysis | Mede bibliotecas de rastreamento em aplicativos COVID-19 com MobSF | Método e Tabelas 2–5; p. 1, 6, 11–12 |
| R0471 | Jordanoski, Zoran et al. (2023) | Balancing privacy at the time of pandemic: global observation | Analisa dados pessoais declarados por aplicativos reais da COVID-19 | Seção 3.1, Tabela 1 e Seção 4.1; p. 1, 3, 6 |
| R0192 | Serrano, Nicolás et al. (2024) | COVID-19 Mobile Applications: A Study of Trackers and Data Leaks | Analisa rastreadores e coleta de dados em aplicativos da COVID-19 | Método 3.1, Tabela 2 e relação com Serrano et al. 2023c; p. 1–4, 6, 20 |

## QR5: LGPD ou Brasil

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0693 | Dos Reis, Valéria Quadros et al. (2023) | Data practices in apps from Brazil: What do privacy policies inform us about? | Analisa políticas de aplicativos no Brasil sob a LGPD | Corpus APP-BR, Tabela 3 e Seção 6; p. 1, 3–5 |
| R0760 | Rodrigues, Anna Luísa Braz (2024) | (UN)PROTECTION OF SENSITIVE PERSONAL DATA IN "GRINDR'S" TERMS OF USE: THE VULNERABILITY OF LGBTQIAPN+ USERS IN ROMANTIC AND SEXUAL RELATIONSHIP APPLICATIONS; [A (DES)PROTEÇÃO DE DADOS PESSOAIS SENSÍVEIS NOS TERMOS DE USO DO “GRINDR”: A VULNERABILIDADE DE USUÁRIOS LGBTQIAPN+ EM APLICATIVOS DE RELACIONAMENTOS AMOROSOS E SEXUAIS] | Analisa LGPD aplicada ao tratamento de dados sensíveis em aplicativo | Seção 3: termos do Grindr à luz da LGPD; p. 1, 13, 16 |

## QR5: soberania ou transferência internacional de dados

| ID | Autores (ano) | Título | Contribuição registrada | Evidência |
|---|---|---|---|---|
| R0710 | Jia, Lianrui et al. (2020) | Going global: Comparing chinese mobile applications’ data and user privacy governance at home and abroad | Compara regras e destinos declarados de transferência internacional em aplicativos | Método e Tabelas 1–2; p. 1, 6, 10–11 |
| R0668 | Sterling, Rogena et al. (2024) | A Māori data governance assessment of the NZ COVID Tracer app | Examina governança e armazenamento internacional de dados do NZ COVID Tracer | Método e critérios de proteção e compartilhamento; p. 1, 3–6 |
