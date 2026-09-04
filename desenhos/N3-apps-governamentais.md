# N3 — Desenho Experimental

**Título provisório (EN):** *Who Else Is in the App? Third-Party Tracking, Security Posture
and Data Sovereignty in Brazilian Government Mobile Applications*

Documento para levar ao orientador. É o único dos temas considerados que passou no teste de
viabilidade sem precisar de reformulação.

---

## 1. Viabilidade — já verificada

| Medida | Resultado (03/09/2026) |
|---|---|
| Aplicativos distintos localizados | 590 |
| Com publicador de órgão público | **396** |
| Publicadores oficiais distintos | **71** |
| Corte mínimo estabelecido no protocolo | 60 |

As três esferas estão representadas, com o publicador identificado **na origem** — o campo
de desenvolvedor diz "Prefeitura Municipal de Curitiba", "Tribunal de Justiça de
Pernambuco", "SERPRO". **Não há trabalho de atribuição a fazer**, que é exatamente o que
inviabilizou o tema N1 (ver `../descartados/N1-infraestrutura-critica.md`).

Subconjunto de dado sensível confirmado e substancial: Meu SUS Digital (50 mi+), família
e-SUS, Meu INSS (50 mi+), Saúde Já Curitiba, e-saudeSP, Portal do Paciente HC, Carteira
Digital de Enfermagem e o Biovalid do SERPRO, que trata **biometria**.

---

## 2. Quadrante metodológico

**Tema.** Rastreamento por terceiros, postura de segurança e soberania de dados em
aplicativos móveis governamentais brasileiros.

**Problema de pesquisa** — nas três partes exigidas pela Aula 05/06:

1. **Enunciado.** Aplicativos móveis oficiais do governo brasileiro — inclusive os que
   tratam dado pessoal sensível — embarcam SDKs de rastreamento de terceiros que transmitem
   identificadores a infraestrutura estrangeira, e em que medida esse comportamento difere
   do de aplicativos comerciais equivalentes?

2. **Lacuna, com referência à literatura.** A metodologia de detecção de SDKs por análise
   estática está consolidada e replicada em vários domínios — aplicativos de terapia, de
   saúde mental, de condicionamento físico, de controle parental, de rastreamento de
   contato —, com achado recorrente de SDKs **não declarados** nas políticas de
   privacidade. Nenhum desses trabalhos cobre o parque de aplicativos governamentais
   brasileiros, e nenhum deles adota grupo de controle pareado.

3. **Por que importa.** Duas camadas. A jurídica: o Art. 11 da LGPD impõe regime mais
   estrito ao dado sensível, e boa parte do corpus trata saúde, biometria e dados
   previdenciários. A de soberania: identificadores de cidadãos brasileiros interagindo com
   serviço público fluindo para infraestrutura sob jurisdição estrangeira.

**Objetivo geral.** **Medir** a prevalência de SDKs de rastreamento de terceiros e de
falhas de configuração de segurança em aplicativos móveis governamentais brasileiros, e
**comparar** esse comportamento com o de aplicativos comerciais pareados.

> Verbos escolhidos conforme a Aula 05/06: *medir* e *comparar* são verificáveis ao final.
> *Propor*, *estudar* e *apresentar* são apontados na aula como inadequados.

**Objetivos específicos.**
1. Consolidar e validar manualmente o corpus de aplicativos governamentais brasileiros.
2. Quantificar SDKs de rastreamento, permissões perigosas e falhas de configuração.
3. Confrontar os SDKs detectados com o que a política de privacidade declara.
4. Determinar a jurisdição dos destinos de rede observados.
5. Medir a concordância entre os detectores empregados.

**Marco teórico.** Três corpos: análise estática de segurança e privacidade em Android;
ecossistema de SDKs de rastreamento; e o regime jurídico brasileiro (LGPD Arts. 7 e 11,
mais a discussão de soberania de dados).

---

## 3. Hipóteses

- **H1 — comparativa (principal).** Aplicativos governamentais embarcam SDKs de
  rastreamento em proporção **estatisticamente indistinguível** da de aplicativos
  comerciais pareados, apesar de submetidos a regime jurídico distinto.

- **H2 — transparência.** Uma fração relevante dos SDKs detectados **não está declarada**
  na política de privacidade do aplicativo.

- **H3 — dado sensível.** Aplicativos que tratam dado sensível (Art. 11) **não apresentam**
  postura de proteção superior à dos demais aplicativos governamentais.

- **H4 — validade da medição.** A concordância entre detectores de SDK sobre o mesmo APK é
  baixa (κ < 0,6), de modo que a taxa reportada por um estudo depende da ferramenta
  escolhida — e taxas de estudos diferentes não são diretamente comparáveis.

**H4 é o eixo que eleva o trabalho.** Sem ele, isto é mais uma medição. Com ele, o trabalho
também diz algo sobre **como o campo mede** — o mesmo movimento meta-metodológico que
sustentaria o tema T1.

E há precedente empírico próprio para suspeitar da medição automática: durante a montagem
do corpus, dois classificadores heurísticos independentes falharam pelo mesmo motivo
(casamento por substring), incluindo o Yandex Maps entre órgãos públicos e excluindo o
publicador do gov.br federal. Isso está registrado no histórico do repositório e vira
argumento na seção de validade.

---

## 4. Corpus e amostragem

### Grupo A — governamental (regime declarado)

Base: os 396 candidatos, submetidos a **validação manual** de vínculo institucional.
Estimativa conservadora após validação: 250 a 320 aplicativos.

Estratificação em dois eixos:
- **Esfera**: federal / estadual / municipal
- **Sensibilidade**: trata ou não dado do Art. 11 (saúde, biometria, previdência)

### Grupo B — controle comercial

Aplicativos comerciais **pareados** por:
- faixa de instalações (em escala logarítmica: 10³–10⁴, 10⁴–10⁵, …)
- categoria da loja

O pareamento é o que impede a crítica óbvia — comparar um app municipal de 500 instalações
com um portal comercial de 100 milhões não mede nada.

### Fonte dos APKs

**AndroZoo** (acesso acadêmico) como fonte primária — é a fonte correta para pesquisa
reprodutível, e permite fixar a versão analisada. Coleta direta da loja como complemento
para os aplicativos ausentes, com o hash registrado.

---

## 5. Instrumentos e medidas

| Dimensão | Instrumento | Medida |
|---|---|---|
| SDKs de rastreamento | MobSF, Androguard, base de assinaturas Exodus | nº e identidade dos rastreadores |
| Permissões | manifesto | nº de permissões perigosas |
| Configuração de rede | `network_security_config`, manifesto | tráfego em claro permitido? |
| Segredos embutidos | varredura estática | chaves e tokens no pacote |
| Criptografia | análise estática | uso de primitivas fracas |
| Destino de rede | subamostra dinâmica | domínios contactados e sua jurisdição |
| Declaração | política de privacidade | SDKs declarados × detectados |
| **Concordância** | os três detectores em paralelo | κ de Fleiss |

**Análise dinâmica em subamostra.** Dispositivo/emulador próprio, conta própria,
interceptação de TLS. Serve para responder o que a análise estática não responde:
**presença de SDK não é transmissão**. Medir essa lacuna é contribuição de validade.

---

## 6. Plano de análise

| Hipótese | Método |
|---|---|
| **H1** | Regressão — contagem de rastreadores modelada por binomial negativa (há sobredispersão), com `grupo` como preditor e faixa de instalação e categoria como controles. Reportar razão de taxas com intervalo de confiança e **tamanho de efeito**, não só valor-p. |
| **H2** | Proporção de SDKs não declarados, com intervalo de confiança; comparação entre esferas. |
| **H3** | Dentro do Grupo A: sensível × não sensível, controlando por esfera e porte. |
| **H4** | κ de Fleiss entre os três detectores; e o teste decisivo — o **ordenamento** dos aplicativos por "quantidade de rastreamento" muda conforme a ferramenta? (τ de Kendall entre ordenamentos). |

**Congele o plano de análise antes de olhar os resultados** e registre isso no texto.
Análise pré-registrada é sinal de rigor barato de dar e caro de ignorar.

---

## 7. Ética e limites legais

Precisa estar escrito desde o Capstone I. A banca vai perguntar.

**O que o trabalho faz.** Analisa **artefatos de software publicamente distribuídos**. O
objeto de estudo é o aplicativo, não pessoas.

**O que não faz, em nenhuma hipótese:**
- ❌ Não coleta dado pessoal de terceiros. A análise dinâmica usa **dispositivo próprio e
  conta própria**.
- ❌ Não acessa área restrita de terceiros nem contorna autenticação de sistema alheio.
- ❌ Não explora falha, não faz varredura de infraestrutura, não é pentest.
- ❌ Não publica segredo embutido que ainda esteja ativo.

**Divulgação responsável.** Achado grave e atribuível a órgão específico é comunicado à
instituição — e, se couber, ao CTIR Gov e à ANPD — **antes** da publicação. Os resultados
são reportados de forma agregada; a identificação individual de aplicativo só ocorre para
achados já corrigidos ou já públicos. Definir o prazo de espera com o orientador e
registrá-lo no texto.

**Engenharia reversa para pesquisa.** Análise estática de binários publicamente
distribuídos é prática consolidada na literatura acadêmica de segurança. Alinhar com o
orientador o enquadramento jurídico e citá-lo explicitamente.

---

## 8. Ameaças à validade

| Ameaça | Tratamento |
|---|---|
| ***Certificate pinning*** impede interceptação em parte dos apps | Limita a análise dinâmica a uma subamostra. **Reportar a taxa de bloqueio como resultado**, não escondê-la — é informação sobre a postura dos apps. |
| Presença estática ≠ execução | É exatamente o que a subamostra dinâmica mede. A lacuna entre os dois é achado, não ruído. |
| Apps municipais publicados por terceirizada | Documentar caso a caso; se o vínculo não for declarado, classificar como indeterminado e reportar o tamanho dessa fatia. Foi o que matou o N1 — aqui é minoria, mas precisa de tratamento explícito. |
| Versão do APK muda com o tempo | Fixar por hash; usar AndroZoo; registrar data de coleta. |
| Base de assinaturas de rastreadores incompleta | É parte da H4: a incompletude do detector **é** o objeto. |
| Metadados da loja mudam | Congelar o corpus com data e arquivar o JSON bruto. |

---

## 9. Divisão entre Capstone I e Capstone II

### Capstone I — entrega em **03/12/2026**

1. Revisão sistemática dos três corpos teóricos, com protocolo de Kitchenham (Aula 07/08).
2. Corpus consolidado e **validado manualmente**, com os critérios de inclusão documentados.
3. Tradução dos Arts. 7 e 11 da LGPD em critérios verificáveis automaticamente.
4. Protocolo experimental congelado, incluindo o plano de análise estatística.
5. Seção de ética escrita.
6. **Piloto**: 20 aplicativos passados ponta a ponta pelos três detectores, com números
   preliminares de concordância.
7. Acesso ao AndroZoo obtido.

O piloto é o que torna a qualificação forte: você não chega com promessa, chega com
pipeline funcionando e resultado preliminar.

### Capstone II — 2027.1

Execução completa, subamostra dinâmica, análise estatística, discussão, e publicação do
conjunto de dados como artefato.

---

## 10. Próximos passos imediatos

| Prazo | Ação |
|---|---|
| Hoje | Solicitar acesso acadêmico ao **AndroZoo** (`androzoo.uni.lu`). É o gargalo de prazo. |
| Esta semana | Validar manualmente a planilha: `OFICIAL_S_N`, `ESFERA`, `TRATA_DADO_SENSIVEL_S_N`. ~1 hora. |
| Esta semana | Instalar MobSF e rodar em 3 APKs para validar o encanamento. |
| Até 25/08* | Levar este documento ao orientador, junto do resultado negativo do N1. |
| Oficina 01–03/09 | Usar a oficina de bases para a busca sistemática dos três corpos. |
| Seminário 29/09 | Apresentar um dos estudos de rastreamento em apps de saúde — cumpre a atividade e adianta a revisão. |

\* A data de apresentação dos orientadores já passou; ajustar para a próxima reunião de
orientação disponível.

---

## 11. O que levar para a conversa de orientação

Três coisas, nesta ordem:

1. **Este desenho**, com o número de corpus verificado.
2. **O resultado negativo do N1** (`../descartados/N1-infraestrutura-critica.md`) — um tema testado e
   rejeitado com evidência quantitativa, na área de especialidade do próprio orientador.
3. **O registro do teste de CT** — segundo tema descartado, por teto de recall estrutural.

Chegar com um tema confirmado e dois refutados, todos com dados, demonstra exatamente a
postura que as Aulas 04 a 08 cobram: hipótese falsificável, verificação empírica, e
disposição de abandonar o que não se sustenta.

**Leitura inicial**
- [Speak Freely & Never Mind the Pesky Trackers: Privacy Analysis of Popular Therapy Apps](https://arxiv.org/html/2605.02016v2)
- [Security Analysis of Top-Ranked mHealth Fitness Apps: An Empirical Study](https://arxiv.org/pdf/2409.18528)
- [Third Party Tracking in the Mobile Ecosystem](https://arxiv.org/html/1804.03603v1)
- [Betrayed by the Guardian: Security and Privacy Risks of Parental Control Solutions](https://arxiv.org/pdf/2012.06502)
- OWASP **MASTG** — Mobile Application Security Testing Guide (gratuito)
