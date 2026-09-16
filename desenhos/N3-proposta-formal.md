# Proposta de TCC — Projeto Capstone I

**Aluno:** Claudio Meireles · Ciência da Computação · IDP
**Orientador pretendido:** Prof. Eduardo Arthur Izycki
**Semestre:** 2026.2 · **Modalidade:** monografia
**Data:** 16/09/2026

**Título (PT):** Quem mais está dentro do aplicativo? Rastreamento por terceiros,
postura de segurança e soberania de dados em aplicativos móveis governamentais
brasileiros

**Título (EN, para o texto final — Art. 32, §3º):** *Who Else Is in the App?
Third-Party Tracking, Security Posture and Data Sovereignty in Brazilian
Government Mobile Applications*

---

## 1. Quadrante metodológico

O Art. 31, I do Regulamento coloca o quadrante **tema–problema–hipótese–marco
teórico** como primeiro critério de avaliação da banca. Ele abre este documento
por isso.

| Vértice | Conteúdo |
|---|---|
| **Tema** | Rastreamento por terceiros, postura de segurança e soberania de dados em aplicativos móveis publicados por órgãos públicos brasileiros. |
| **Problema** | Aplicativos móveis oficiais do governo brasileiro — inclusive os que tratam dado pessoal sensível — embarcam SDKs de rastreamento de terceiros que transmitem identificadores a infraestrutura estrangeira? E em que medida esse comportamento difere do de aplicativos comerciais pareados por categoria e porte? |
| **Hipóteses** | H1 a H4, na Seção 3. Todas falsificáveis, todas com instrumento e critério de decisão definidos antes da coleta. |
| **Marco teórico** | Três corpos: (a) análise estática de segurança e privacidade em Android; (b) o ecossistema de SDKs de rastreamento e sua economia; (c) o regime jurídico brasileiro — LGPD Arts. 7º e 11 — e a discussão de soberania de dados. |

---

## 2. Problema de pesquisa, nas três partes

A Aula 05/06 exige que o problema seja enunciado em três partes. São elas:

### 2.1 Enunciado

Aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento
de terceiros que transmitem identificadores a infraestrutura sob jurisdição
estrangeira, e em que medida esse comportamento difere do de aplicativos
comerciais equivalentes?

### 2.2 A lacuna, com referência à literatura

A detecção de SDKs de rastreamento por análise estática é **metodologia
consolidada**, replicada em vários domínios: aplicativos de terapia, de saúde
mental, de condicionamento físico, de controle parental e de rastreamento de
contato. O achado recorrente dessa literatura é a presença de SDKs **não
declarados** nas políticas de privacidade.

Dois vazios persistem nesse conjunto:

1. **Nenhum desses trabalhos cobre o parque de aplicativos governamentais
   brasileiros.** O objeto é sempre o aplicativo comercial ou de saúde privada.
2. **Nenhum deles adota grupo de controle pareado.** Reportam a taxa de
   rastreamento de um domínio isoladamente, sem linha de base — o que impede
   dizer se a taxa observada é alta, baixa ou típica.

> **Sobre o "fundamento vazio" (Aula 07/08).** A ausência de estudo anterior não
> é, por si só, justificativa — a disciplina é explícita quanto a isso. O que
> sustenta esta proposta não é o vazio, e sim o que a literatura **já
> estabeleceu**: que a metodologia funciona, que o achado de SDK não declarado
> se repete em todo domínio onde foi procurado, e que o setor público brasileiro
> opera sob um regime jurídico **distinto** do que essa literatura estudou. A
> contribuição é aplicar instrumento validado a uma população sob regra
> diferente, com a linha de base que os trabalhos anteriores não tinham.

### 2.3 Por que importa

**Camada jurídica.** O Art. 11 da LGPD impõe regime mais estrito ao dado pessoal
sensível. Parte substancial do corpus trata saúde, biometria e dados
previdenciários — Meu SUS Digital (50 mi+ instalações), a família e-SUS, Meu
INSS (50 mi+), o Biovalid do SERPRO, que faz prova de vida por reconhecimento
facial. Se há SDK de terceiro nesses aplicativos, a questão de base legal é
imediata.

**Camada de soberania.** Identificadores de cidadãos brasileiros interagindo com
serviço público fluindo para infraestrutura sob jurisdição estrangeira. É a
camada que conecta o trabalho à linha de pesquisa do orientador pretendido, e é
o que diferencia este trabalho de um estudo de conformidade com a LGPD.

**Camada de escolha ausente.** O cidadão pode trocar de aplicativo de banco. Não
pode trocar de INSS. A ausência de alternativa altera o peso normativo do achado
e é argumento que a literatura de apps comerciais não tem como fazer.

---

## 3. Hipóteses

Todas enunciadas de modo que possam ser **rejeitadas** por um resultado
específico, com o critério fixado antes da coleta.

| # | Hipótese | Como se rejeita |
|---|---|---|
| **H1** | Aplicativos governamentais embarcam SDKs de rastreamento em proporção **estatisticamente indistinguível** da de aplicativos comerciais pareados, apesar do regime jurídico distinto. | Razão de taxas com intervalo de confiança que **exclua** 1, no modelo ajustado por categoria e faixa de instalação. |
| **H2** | Fração relevante dos SDKs detectados **não está declarada** na política de privacidade. | Proporção de não declarados com IC95% cujo limite superior fique abaixo de 10%. |
| **H3** | Aplicativos que tratam dado sensível (Art. 11) **não apresentam** postura de proteção superior à dos demais aplicativos governamentais. | Diferença significativa a favor dos sensíveis, controlando por esfera e porte. |
| **H4** | A concordância entre detectores de SDK sobre o mesmo APK é **baixa** (κ de Fleiss < 0,6), de modo que a taxa reportada depende da ferramenta escolhida. | κ ≥ 0,6 **e** τ de Kendall alto entre os ordenamentos produzidos por cada ferramenta. |

**H4 é o eixo que eleva o trabalho.** Sem ela, isto é mais uma medição de
prevalência. Com ela, o trabalho também diz algo sobre **como o campo mede** — e
se as taxas publicadas por estudos diferentes são sequer comparáveis entre si.

Na escala de maturidade de Wazlawick, H1 a H3 situam o trabalho no nível de
**"reconhecidamente melhor"** por evidência empírica comparativa; H4 acrescenta
uma contribuição de **validade de instrumento**, que é o que distingue uma
medição de uma contribuição metodológica.

**Precedente empírico próprio para suspeitar da medição automática.** Durante a
montagem do corpus, dois classificadores heurísticos independentes falharam pelo
mesmo motivo — casamento por substring —, incluindo o Yandex Maps entre órgãos
públicos e excluindo o publicador do gov.br federal. O mesmo erro reapareceu no
coletor de Certificate Transparency. Está registrado no histórico do
repositório e entra na seção de validade como evidência de primeira mão.

---

## 4. Objetivos

**Geral.** **Medir** a prevalência de SDKs de rastreamento de terceiros e de
falhas de configuração de segurança em aplicativos móveis governamentais
brasileiros, e **comparar** esse comportamento com o de aplicativos comerciais
pareados.

> Os verbos são escolha deliberada. A Aula 05/06 aponta *propor*, *estudar* e
> *apresentar* como inadequados por não serem verificáveis ao final. *Medir* e
> *comparar* são verificáveis: ou a medida existe, ou não existe.

**Específicos.**

1. Consolidar e **validar manualmente** o corpus de aplicativos governamentais
   brasileiros, documentando os critérios de inclusão e a taxa de erro do
   classificador automático.
2. **Quantificar** SDKs de rastreamento, permissões perigosas e falhas de
   configuração de rede por aplicativo.
3. **Confrontar** os SDKs detectados com o que a política de privacidade e a
   seção "Segurança dos dados" da loja declaram.
4. **Determinar** a jurisdição dos destinos de rede efetivamente contactados, em
   subamostra sob análise dinâmica.
5. **Medir** a concordância entre os detectores empregados e o efeito da escolha
   de ferramenta sobre o ordenamento dos aplicativos.

---

## 5. Base empírica já construída

Esta proposta não chega como intenção. Quatro temas foram testados
empiricamente antes desta escolha, e **três foram descartados com dados**.

| Tema | Teste | Resultado |
|---|---|---|
| ICS exposta no Brasil | Contagens e facetas no Shodan | ❌ Os mesmos hosts respondem em Modbus, IEC‑104 e EtherNet/IP simultaneamente — honeypot e nuvem, não equipamento industrial. A variável independente (o setor do operador) é inobservável. |
| Abuso de marca em Certificate Transparency | 20.007 entradas de log, casamento por token | ❌ Zero imitações reais. O phishing moderno raramente põe a marca no domínio: teto de recall por construção. |
| Genealogia do malware bancário BR | imphash de 1.764 amostras BR × 2.104 de controle | ⚠️ Inconclusivo. O rótulo de família marca a campanha, não o payload; 85% do acervo brasileiro são containers, onde imphash não existe. Conclusão exigiria desempacotar malware vivo. |
| **Apps governamentais (este)** | Busca e expansão por catálogo na Play Store | ✅ **396 aplicativos, 71 publicadores públicos distintos, três esferas representadas, publicador identificado na origem.** |

O que torna este tema diferente dos três anteriores é uma propriedade só:
**a variável independente vem rotulada na fonte**. A Play Store declara o
publicador — "Prefeitura Municipal de Curitiba", "Tribunal de Justiça de
Pernambuco", "SERPRO". Não há trabalho de atribuição a fazer, que foi exatamente
o que matou o primeiro tema.

Os descartes não são tempo perdido: sustentam a seção de metodologia e
demonstram a postura que as Aulas 04 a 08 cobram — hipótese falsificável,
verificação empírica, e disposição de abandonar o que não se sustenta.

### 5.1 Segunda rodada de verificação

Um teste mais exigente foi escrito (`scripts/teste_viabilidade_n3_robusto.py`)
para medir, **antes de baixar o primeiro APK**, se cada hipótese tem instrumento:

| Porta | O que mede | Hipótese em risco |
|---|---|---|
| 1 | Corpus efetivo após a ficha completa | todas |
| 2 | Povoamento das células esfera × sensibilidade | H3 |
| 3 | Existência de controle comercial na mesma categoria e faixa de instalação | H1 |
| 4 | Política de privacidade publicada e acessível | H2 |
| 5 | Sinal preliminar da variável dependente (`containsAds` como limite inferior) | H1 |
| 6 | Menor diferença detectável com o n disponível | H1, H3 |

Cada porta tem desfecho de contingência escrito no próprio script: se o
pareamento não existir, a comparação vira interna (entre esferas); se a política
não for acessível, a fonte de declaração muda para a seção estruturada da loja;
se as células sensíveis forem pequenas, a estratificação cai e o contraste
principal permanece. **Nenhum desfecho mata o tema — todos mudam o desenho**, e é
por isso que o teste vem antes de congelar o protocolo.

---

## 6. Método

**Corpus.** Grupo A: aplicativos governamentais, estratificados por esfera
(federal/estadual/municipal) e por sensibilidade do dado (Art. 11 ou não).
Grupo B: comerciais **pareados** por categoria da loja e faixa logarítmica de
instalação. O pareamento impede a crítica óbvia — comparar um app municipal de
500 instalações com um portal comercial de 100 milhões não mede nada.

**Fonte dos APKs.** AndroZoo (acesso acadêmico) como primária, por permitir
fixar a versão analisada e tornar o estudo reprodutível; coleta direta da loja
como complemento, com hash registrado.

**Instrumentos.** MobSF, Androguard e a base de assinaturas do Exodus, aplicados
em paralelo — a paralelização não é redundância, é o instrumento da H4.
Subamostra sob análise dinâmica com dispositivo próprio e conta própria, para
medir a lacuna entre **presença** de SDK e **transmissão** efetiva.

**Análise.** H1 por regressão binomial negativa (há sobredispersão na contagem
de rastreadores), com `grupo` como preditor e categoria e faixa como controles;
reportando razão de taxas com IC e **tamanho de efeito**, não só valor‑p. H2 e
H3 por proporção com IC. H4 por κ de Fleiss mais τ de Kendall entre ordenamentos.

**O plano de análise é congelado antes de olhar os resultados** e esse
congelamento é registrado no texto. Análise pré‑registrada é rigor barato de dar
e caro de ignorar.

**Revisão da literatura.** Protocolo sistemático conforme Kitchenham & Charters,
com strings de busca, critérios de inclusão e exclusão e o fluxo de seleção
documentados. Três corpos teóricos, tratados separadamente.

---

## 7. Ética e limites

**O objeto de estudo é o aplicativo, não pessoas.** A análise incide sobre
artefatos de software publicamente distribuídos.

O trabalho **não** coleta dado pessoal de terceiros (a análise dinâmica usa
dispositivo e conta próprios), **não** acessa área restrita nem contorna
autenticação de sistema alheio, **não** explora falha, **não** faz varredura de
infraestrutura, e **não** publica segredo embutido que ainda esteja ativo.

**Divulgação responsável.** Achado grave e atribuível a órgão específico é
comunicado à instituição — e, cabendo, ao CTIR Gov e à ANPD — **antes** da
publicação. Resultados reportados de forma agregada; identificação individual
apenas para achado já corrigido ou já público. O prazo de espera será definido
com o orientador e registrado no texto.

---

## 8. Ameaças à validade

| Ameaça | Tratamento |
|---|---|
| *Certificate pinning* impede interceptação em parte dos apps | Limita a subamostra dinâmica. **A taxa de bloqueio é reportada como resultado** — é informação sobre a postura dos apps, não ruído a esconder. |
| Presença estática ≠ execução | É o que a subamostra dinâmica mede. A lacuna entre os dois é achado. |
| App municipal publicado por terceirizada sem vínculo declarado | Classificar como indeterminado e **reportar o tamanho dessa fatia**. Foi o que matou o tema ICS; aqui é minoria, mas precisa de tratamento explícito. |
| Versão do APK muda no tempo | Fixar por hash, usar AndroZoo, registrar data de coleta. |
| Base de assinaturas de rastreadores incompleta | Não é ameaça a contornar: **é o objeto da H4**. |
| Classificador heurístico de esfera e sensibilidade erra | A revisão manual mede a taxa de erro, e essa taxa entra no texto. |
| Metadados da loja mudam | Congelar o corpus com data e arquivar o JSON bruto. |

---

## 9. Entrega do Capstone I — 03/12/2026

1. Revisão sistemática dos três corpos, com protocolo de Kitchenham.
2. Corpus consolidado e **validado manualmente**, critérios documentados.
3. Arts. 7º e 11 da LGPD traduzidos em critérios verificáveis automaticamente.
4. Protocolo experimental congelado, **incluindo o plano de análise estatística**.
5. Seção de ética escrita.
6. **Piloto: 20 aplicativos ponta a ponta** pelos três detectores, com números
   preliminares de concordância.
7. Acesso ao AndroZoo obtido.

O piloto é o que torna a qualificação forte: a defesa não apresenta promessa,
apresenta pipeline funcionando e resultado preliminar.

**Capstone II (2027.1):** execução completa, subamostra dinâmica, análise
estatística, discussão, e publicação do conjunto de dados como artefato.

---

## 10. Pendências formais

| Item | Base | Situação |
|---|---|---|
| Termo de aceite do orientador | Art. 10 e Art. 15 | **pendente** |
| Verificar elegibilidade do orientador na lista da Coordenação | Art. 13, §1º e §6º (máx. 3 orientandos novos/semestre) | **a confirmar** |
| 5 encontros de orientação com ficha assinada | Art. 19, II e Art. 24 | a iniciar — reprova por si só se faltar |
| Modalidade | Art. 29, §1º | **monografia**. A modalidade artigo exige aceite em periódico Qualis ≥ B2, o que não está sob controle do aluno. |

---

## 11. Leitura inicial

- *Speak Freely & Never Mind the Pesky Trackers: Privacy Analysis of Popular Therapy Apps*
- *Security Analysis of Top-Ranked mHealth Fitness Apps: An Empirical Study*
- *Third Party Tracking in the Mobile Ecosystem*
- *Betrayed by the Guardian: Security and Privacy Risks of Parental Control Solutions*
- OWASP **MASTG** — Mobile Application Security Testing Guide

O desenho experimental detalhado está em `N3-apps-governamentais.md`, neste
mesmo diretório.
