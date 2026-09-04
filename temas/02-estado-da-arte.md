# Estado da Arte dos Temas Propostos — Checagem de Viabilidade

Documento complementar a `01-catalogo-inicial.md`. Para cada tema proposto, foi feita
uma busca na literatura recente para responder a três perguntas:

1. O que **já foi feito** (e, portanto, não pode ser a sua contribuição)?
2. **Onde ainda há espaço** — qual reformulação salva o tema?
3. **Vale a pena?** — veredito honesto.

Cada seção termina com 3–5 artigos recentes para leitura de sondagem.

> **Data da checagem:** agosto de 2026. Em áreas quentes (T1, T7) a literatura muda em
> semanas — refaça a busca antes de fechar o tema com o orientador.

---

## O padrão geral

Em **todos** os nove temas, a formulação intuitiva já está publicada. Isso não é azar:
é o estado normal de qualquer área ativa. O que restou de contribuição possível tem
sempre uma destas duas formas:

**(a) Movimento meta-metodológico.** Em vez de responder a pergunta do campo, questionar
como o campo mede. *As conclusões se sustentam quando troco o instrumento de medida? Os
benchmarks concordam entre si? Qual a taxa de falso positivo do oráculo?* Este movimento
aparece como brecha viável em T1, T5, T7 e A1 — e é consistentemente a contribuição mais
forte disponível para escala de TCC, porque exige rigor, não recursos.

**(b) População não medida.** Brasil, língua portuguesa, setores sujeitos a regra
específica. Aparece em T2, T3, T6 e A1. Mais fácil de executar, contribuição mais modesta
— e sempre exposta à pergunta "e além de trocar a amostra, o que há de novo?".

Os temas mais fortes desta lista combinam **as duas**.

---

## T1 — Segurança do código gerado por LLMs

**Status: 🟢 VIÁVEL com reformulação (detalhada em conversa à parte).**

**Já feito.** Modelos × estratégias de prompting × taxa de CWE está saturado: pelo menos
cinco trabalhos de 2026 fazem exatamente isso, além dos benchmarks CWEval, SafeGenBench e
SecCodePLT.

**Brecha 1 — a literatura se contradiz.** Os efeitos reportados para prompting de
segurança vão de "redução de 56%" e "60%" a "nenhuma redução estatisticamente
significativa; prompting só redistribui as categorias de CWE". Resolver conflito de
literatura é contribuição de primeira classe e imune a ser furada por publicação nova.

**Brecha 2 — a régua é suspeita.** Quase todo esse campo mede vulnerabilidade via
CodeQL/Semgrep/Bandit. A literatura de análise estática reporta até 99,5% de falso
positivo em certas classes e apenas 8–30% de alertas relevantes nas avaliações SATE do
NIST. Ninguém quantificou sistematicamente **quanto a conclusão depende da ferramenta
escolhida como oráculo**.

**Reformulação.** Replicação rigorosa que mede simultaneamente (i) se prompting reduz de
fato a densidade de vulnerabilidades ou só muda sua composição, e (ii) o quanto a resposta
muda conforme o analisador adotado, com rotulagem manual de amostra estratificada para
estabelecer verdade de campo.

**Risco principal:** hardware para rodar modelos de pesos abertos.

**Leitura:**
- [An Empirical Evaluation of LLM-Generated Code Security Across Prompting Methods](https://arxiv.org/html/2605.24298v1)
- [On Fixing Insecure AI-Generated Code through Model Fine-Tuning and Prompting Strategies](https://arxiv.org/pdf/2605.05867)
- [Benchmarking Prompt Engineering Techniques for Secure Code Generation](https://arxiv.org/pdf/2502.06039)
- [LLMs Cannot Reliably Identify and Reason About Security Vulnerabilities (Yet?)](https://arxiv.org/pdf/2312.12575)
- [RealVuln: Benchmarking Rule-Based, General-Purpose LLM, and Security-Specialized Scanners on Real-World Code](https://arxiv.org/pdf/2604.13764)

---

## T2 — Cadeia de suprimentos / dependências vulneráveis

**Status: 🟡 VIÁVEL, mas condicionado a teste de corpus.**

**Já feito.** Patch lag e propagação de vulnerabilidade em ecossistemas de pacotes é um
dos assuntos mais estudados de engenharia de software empírica — npm, Maven, PyPI, Go
todos com medição consolidada. Novidade metodológica ≈ zero.

**Brecha.** O recorte brasileiro segue aberto: o trabalho existente sobre setor público
brasileiro mede infraestrutura (portas, SO, CVSS/EPSS), não cadeia de dependências.

**Risco que derruba o tema.** As organizações governamentais brasileiras no GitHub têm
**dezenas** de repositórios cada, não milhares, e boa parte é documentação e dados
abertos, sem manifesto de dependências. Abaixo de ~150 projetos analisáveis, a
estatística fica frágil. **Teste isso antes de qualquer outra coisa.**

**Reformulação.** Adicionar eixo comparativo (governo brasileiro vs. governo digital
estrangeiro) e eixo de alcançabilidade (que fração dos alertas é de fato acionável).

**Leitura:**
- [Research Directions in Software Supply Chain Security (ACM TOSEM)](https://dl.acm.org/doi/10.1145/3714464)
- [Lags in the release, adoption, and propagation of npm vulnerability fixes (EMSE)](https://link.springer.com/article/10.1007/s10664-021-09951-x)
- [Out of Sight, Still at Risk: The Lifecycle of Transitive Vulnerabilities in Maven](https://arxiv.org/pdf/2504.04803)
- [SoK: Taxonomy of Attacks on Open-Source Software Supply Chains](https://oaklandsok.github.io/papers/ladisa2023.pdf)

---

## T3 — Conformidade com a LGPD medida em escala

**Status: 🟢 VIÁVEL com reformulação setorial.**

**Já feito, e mais do que eu supunha.** A metodologia é madura no contexto europeu:
estudo longitudinal de 4 anos (49% dos sites depositam cookies antes do consentimento,
28% não oferecem mecanismo algum), taxonomia de *dark patterns* de Nouwens et al. na
CHI, análise automatizada em larga escala na USENIX Security 2024, ferramentas prontas
(Cookiescanner, CookieEnforcer).

**E o Brasil já foi medido** — um estudo de 2026 cobre 10 países e 9.488 sites,
incluindo o Brasil, e conclui que a LGPD é **pouco efetiva por falta de fiscalização**:
"uma lei de privacidade sem regulador ativo produz comportamento de rastreamento próximo
ao de não haver lei alguma". Ou seja: a pergunta "os sites brasileiros cumprem a LGPD?"
já tem resposta publicada, e ela é "não".

**Brecha.** O estudo existente é de grão grosso — 10 países, comparação agregada. Fica
aberto:
- **Setores com dado sensível.** O Art. 11 da LGPD impõe regime mais estrito para dados
  sensíveis (saúde, biometria, dados de crianças). Medir rastreadores de terceiros em
  sites de **saúde**, **educação básica** e **serviços públicos** brasileiros testa uma
  hipótese muito mais afiada: o regime jurídico mais rigoroso se reflete em algum
  comportamento técnico observável? A hipótese provável — e interessante — é que **não**.
- **Efeito da orientação da ANPD sobre cookies.** Se houver marco temporal de publicação
  ou de ação de fiscalização, dá um desenho quase-experimental antes/depois.

**Reformulação.** Não "o Brasil cumpre a LGPD" (respondido), mas: *o tratamento de dados
sensíveis previsto no Art. 11 produz comportamento técnico distinguível do tratamento de
dados comuns?* Isso é jurídico + técnico, mensurável, e ninguém fez.

**Risco:** baixo. Ferramental pronto, corpus infinito, custo zero.

**Leitura:**
- [Automated Large-Scale Analysis of Cookie Notice Compliance (USENIX Security 2024)](https://www.usenix.org/system/files/usenixsecurity24-bouhoula.pdf)
- [Dark Patterns after the GDPR: Scraping Consent Pop-ups and Demonstrating their Influence (CHI 2020)](https://dl.acm.org/doi/fullHtml/10.1145/3313831.3376321)
- [Large-scale web tracking and cookie compliance: one million websites under GDPR](https://www.sciencedirect.com/science/article/pii/S1084804525001195)
- [Estudo comparativo de 10 países incluindo Brasil (2026)](https://arxiv.org/html/2604.18633)
- [Cookiescanner: An Automated Tool for Detecting and Evaluating GDPR Consent Notices](https://arxiv.org/pdf/2309.06196)

---

## T4 — Detecção de intrusão sob concept drift

**Status: 🔴 NÃO RECOMENDADO. A pergunta já foi respondida.**

Este foi o resultado mais categórico da checagem. As duas pernas do tema estão publicadas:

**A generalização cruzada já foi medida.** Trabalho de 2024 estabelece que modelos com
desempenho quase perfeito intra-dataset caem para **desempenho comparável ao acaso** em
avaliação cruzada; outro mede queda média de **30,45% de AUROC**. Há ainda um estudo de
2026 sobre generalização temporal e semântica cruzada. A minha hipótese original ("o
desempenho degrada substancialmente") não é mais hipótese — é resultado conhecido.

**A crítica aos datasets também está feita, e com sobra.** Engelen et al. (2021), Liu et
al. (2022) e Lanvin et al. (2023) documentaram: implementação errada do ataque DoS Hulk,
incompreensão do TCP na construção de fluxos, 34 features mal calculadas, falha do
CICFlowMeter, **6,67% de corrupção de rótulos** no CIC-IDS2017 com algumas classes acima
de 75%.

**Sobra alguma coisa?** Uma pergunta estreita: os estudos de generalização cruzada usaram
os rótulos **defeituosos** — a conclusão sobrevive aos datasets corrigidos? É legítimo,
mas é uma fatia fina, exige domínio profundo de redes e o maior custo computacional da
lista. Não compensa para TCC.

**Leitura (para entender por que evitar):**
- [On the Cross-Dataset Generalization of Machine Learning for Network Intrusion Detection](https://arxiv.org/abs/2402.10974)
- [Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study](https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf)
- [Errors in the CICIDS2017 Dataset and the Significant Differences in Detection Performances It Makes](https://link.springer.com/chapter/10.1007/978-3-031-31108-6_2)
- [Cross-Dataset Temporal and Semantic Generalization of Intrusion Detection Models (2026)](https://www.mdpi.com/1999-5903/18/4/194)

---

## T5 — Más configurações em Infraestrutura como Código

**Status: 🟡 VIÁVEL como plano B. Seguro, pouco vistoso.**

**Já feito.** A linha de *security smells* é bem estabelecida: Rahman et al. ("The Seven
Sins", ICSE 2019) analisaram 15.232 scripts de 293 repositórios e catalogaram sete
smells com 21.201 ocorrências; houve replicação em Ansible e Chef; GLITCH estendeu para
múltiplas linguagens; uma taxonomia de 2025 expandiu para **62 categorias** cobrindo
Ansible, Terraform, Chef, Puppet, Pulumi, Saltstack e Vagrant. Medir prevalência está
esgotado — já se sabe que 84,5% dos repositórios Terraform têm ao menos um smell.

**Brecha.** O eixo de **concordância entre ferramentas e taxa de falso positivo** é
tratado quase só em blog de fornecedor, não em literatura acadêmica revisada. É o mesmo
movimento meta-metodológico do T1, aplicado a IaC — e vale pelo mesmo motivo.

**Fronteira nova (e arriscada).** IaC gerada por LLM: já surgiram em 2026 trabalhos sobre
*text-to-Terraform* seguro e sobre "correções enganosas" em Terraform assistido por LLM.
Muito recente para apostar, bom para citar.

**Por que continua sendo bom plano B:** é o tema com menor probabilidade de dar errado da
lista inteira. Custo zero, corpus abundante, metodologia estabelecida.

**Leitura:**
- [The Seven Sins: Security Smells in Infrastructure as Code Scripts (ICSE 2019)](https://akondrahman.github.io/files/papers/icse19_slic.pdf)
- [Security Smells in Ansible and Chef Scripts: A Replication Study](https://arxiv.org/pdf/1907.07159)
- [Security Smells in Infrastructure as Code Scripts: A Taxonomy (2025)](https://arxiv.org/pdf/2509.18761)
- [Exploring Security Practices in Infrastructure as Code: An Empirical Study](https://arxiv.org/pdf/2308.03952)
- [TerraProbe: Detecting Deceptive Fixes in LLM-Assisted Terraform (2026)](https://arxiv.org/pdf/2606.26590)

---

## T6 — Phishing: LLMs vs. ML clássico

**Status: 🟡 VIÁVEL só com reformulação para português.**

**Já feito, inclusive o eixo adversarial que eu propus.** Existe revisão sistemática de
2026 cobrindo LLMs tanto na *geração* quanto na *detecção* de phishing. ChatSpamDetector
com GPT-4 reporta 99,70% de acurácia. Já há trabalho específico sobre detecção robusta de
phishing convencional, gerado por LLM **e** adversarial. O eixo "e se o phishing for
escrito por IA?" está ocupado.

**Achado interessante, e contraintuitivo.** Em detecção de **URL**, a melhor configuração
de LLM chegou a F1 = 94,09% contra **95,35% de um Random Forest**. Ou seja: o baseline
clássico ganha. E o benefício de enriquecer features depende da capacidade do modelo —
ajuda muito os fracos e **degrada** os fortes. Isso é uma nuance que a narrativa
dominante ("LLM é melhor") esconde.

**Brecha real: português.** Praticamente toda essa literatura é anglófona, treinada e
avaliada em corpora em inglês. **Detectores treinados em inglês transferem para phishing
em português brasileiro?** A hipótese de que não transferem bem é plausível, testável e
localmente relevante — o Brasil é um dos alvos mais visados do mundo, com golpes de Pix e
tributação como iscas recorrentes.

**O risco que decide o tema.** Não existe corpus público consolidado de phishing em
português. Você teria que montá-lo (PhishTank filtrado por domínio/idioma, doações de
CERTs, honeypot de e-mail próprio), e isso pode virar o TCC inteiro. **Investigue a
disponibilidade de corpus antes de escolher** — é o mesmo tipo de risco que derrubou o T2.

**Leitura:**
- [A systematic literature review of LLMs in phishing attack generation and detection (2026)](https://www.sciencedirect.com/science/article/pii/S2590005626000986)
- [ChatSpamDetector: Leveraging LLMs for Effective Phishing Email Detection](https://arxiv.org/html/2402.18093v1)
- [Robust ML-based Detection of Conventional, LLM-Generated, and Adversarial Phishing Emails](https://arxiv.org/html/2510.11915v1)
- [PhishEmailLLM: A Meta Model Approach (ACSW 2025)](https://dl.acm.org/doi/full/10.1145/3727166.3727169)

---

## T7 — Segurança de agentes: injeção indireta de prompt

**Status: 🟠 MAIOR TETO, MAIOR RISCO. Só com pré-requisitos.**

**Já feito.** O campo tem infraestrutura madura e muita gente boa: AgentDojo (97 tarefas
realistas, 629 casos de teste de segurança, medindo utilidade e segurança **conjuntamente**
— exatamente o desenho que eu havia proposto como diferencial), MELON, ARGUS,
AgentSentry, CommandSans. Defesas por delimitação, sanduíche de prompt, classificadores e
filtragem de ferramentas já estão catalogadas com sua fronteira de trade-off.

**Brecha.** Surgiu em 2026 um trabalho de *taxonomia e análise de consistência* entre
benchmarks de segurança de agentes — sinal de que **os benchmarks discordam entre si**.
Aí mora a pergunta meta-metodológica: *uma defesa que vence no AgentDojo vence também em
BIPIA, InjecAgent e ASB — ou o ranking de defesas é artefato do benchmark escolhido?*
Mesmo movimento do T1, e igualmente valioso. Mas verifique se o trabalho de 2026 já não
respondeu isso.

**Pré-requisitos honestos:** familiaridade prévia com agentes e ferramentas, orçamento de
inferência, e um orientador confortável com o assunto. Sem os três, o T1 entrega apelo
semelhante com metade do risco.

**Leitura:**
- [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses](https://www.researchgate.net/publication/397198170_AgentDojo_A_Dynamic_Environment_to_Evaluate_Prompt_Injection_Attacks_and_Defenses_for_LLM_Agents)
- [MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents](https://arxiv.org/pdf/2502.05174)
- [Taxonomy and Consistency Analysis of Safety Benchmarks for AI Agents (2026)](https://arxiv.org/pdf/2605.16282)
- [ARGUS: Defending LLM Agents Against Context-Aware Prompt Injection](https://arxiv.org/pdf/2605.03378)

---

## A1 — Acessibilidade digital em serviços públicos brasileiros

**Status: 🟢 SURPRESA POSITIVA. Subiu muito na checagem.**

Eu havia listado este como alternativa de consolo. A literatura mostrou que ele é mais
forte do que quase todos os temas de cibersegurança da lista.

**Já feito, e é justamente o que dá a brecha.** Está bem estabelecido que **ferramentas
automáticas capturam apenas uma fração dos problemas reais**: um estudo de 2026 mediu que
a melhor ferramenta encontrou 62,8% dos problemas de uma auditoria manual, enquanto o
axe-core sozinho — o mais usado do mundo — encontrou **22,6%**. O teto por critério fica
entre 20% e 40%, e cerca de metade dos 87 critérios da WCAG exige julgamento humano.

Os estudos de sites governamentais existentes são **pequenos** (um deles com 21 sites) e
quase todos usam só ferramenta automática — ou seja, herdam exatamente o viés que a
literatura metodológica denuncia.

**Brecha, e ela é grande.** Ninguém fez, em escala, para o Brasil, com validação manual.
E o Brasil tem duas particularidades que dão substância jurídica ao trabalho: o **eMAG**
(padrão próprio de acessibilidade de governo eletrônico) e a **Lei Brasileira de Inclusão
(Lei 13.146/2015)**, que torna a acessibilidade de sites públicos uma obrigação legal, não
uma boa prática.

**Reformulação sugerida.** Medição em larga escala de serviços públicos digitais
brasileiros combinando varredura automatizada com auditoria manual em amostra
estratificada, para (i) estimar a conformidade real e (ii) **quantificar o quanto a
avaliação puramente automatizada subestima o problema** — número que hoje ninguém tem
para o contexto brasileiro e que tem consequência direta para política pública.

**Por que é forte:** corpus abundante (milhares de serviços no gov.br, ao contrário dos
poucos repositórios do T2), ferramental gratuito e maduro, hipótese falsificável, mesmo
movimento meta-metodológico do T1, impacto social evidente e defesa fácil perante banca.
**Não é cibersegurança** — mas se o que te atrai é o método empírico, é sério candidato.

**Leitura:**
- [WCAG-EM: Website Accessibility Conformance Evaluation Methodology (W3C)](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/)
- [Web accessibility automatic evaluation tools: to what extent can they be automated?](https://ouci.dntb.gov.ua/en/works/4vrZ2jK4/)
- [Accessibility evaluation of websites using WCAG tools and Cambridge Simulator](https://arxiv.org/pdf/2009.06526)
- [Investigation of COVID-19 Vaccine Information Websites Using Automated Accessibility Protocols](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8910771/)

---

## A2 — Impacto de assistentes de IA na qualidade de código

**Status: 🟡 VIÁVEL, mas sobrepõe o T1 e é mais engenharia de software que segurança.**

**Já feito, e com resultados contraditórios** — o que, como no T1, é a oportunidade. De um
lado, experimento de campo em empresas Fortune 100 mostra **26% mais tarefas concluídas**
por semana com Copilot, efeito maior em desenvolvedores juniores. De outro,
desenvolvedores experientes em repositórios familiares ficaram **mais lentos** com IA,
por esforço extra de revisão e correção. Um estudo de projetos que adotaram Cursor achou
ganho inicial seguido de **aumento substancial de alertas de análise estática e de
complexidade** — produtividade cedendo lugar a dívida técnica.

**Brecha.** O efeito de médio prazo sobre manutenibilidade, e a reconciliação das
contradições. Há também uma linha nova e prática: uso de IA **auto-declarado** em projetos
open source, que dá um sinal de rotulagem para estudos observacionais.

**Por que fica atrás do T1:** perde o eixo de segurança, e a variável dependente
(produtividade, manutenibilidade) é bem mais difícil de medir com rigor do que
"vulnerabilidade detectada".

**Leitura:**
- [Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability (EMSE 2026)](https://link.springer.com/article/10.1007/s10664-026-10889-1)
- [Examining the Use and Impact of an AI Code Assistant on Developer Productivity](https://arxiv.org/pdf/2412.06603)
- [Self-Admitted GenAI Usage in Open-Source Software](https://arxiv.org/pdf/2507.10422)
- [Usage, Effects and Requirements for AI Coding Assistants in the Enterprise](https://arxiv.org/pdf/2601.20112)

---

## Ranking final, depois da checagem

| Posição | Tema | Status | Observação decisiva |
|---|---|---|---|
| 1º | **T1 reformulado** — código gerado por LLM + validade do oráculo | 🟢 | Único que combina os dois tipos de brecha. Corpus você fabrica. Depende de hardware. |
| 2º | **A1 reformulado** — acessibilidade de serviços públicos BR | 🟢 | A grande surpresa. Corpus abundante, custo zero, impacto social, mesma força metodológica. Fora de cibersegurança. |
| 3º | **T3 reformulado** — LGPD e dados sensíveis (Art. 11) | 🟢 | Ferramental maduro, recorte jurídico afiado, risco baixo. |
| 4º | **T5 reformulado** — concordância entre scanners de IaC | 🟡 | O mais difícil de dar errado. Pouco vistoso. |
| 5º | **T6 reformulado** — phishing em português | 🟡 | Ótimo se houver corpus. Investigue antes. |
| 6º | **T2** — cadeia de suprimentos BR | 🟡 | Preso ao teste de corpus. |
| 7º | **T7** — injeção de prompt em agentes | 🟠 | Maior teto, exige pré-requisitos. |
| 8º | **A2** — IA e qualidade de código | 🟡 | Sobrepõe o T1 com menos força. |
| 9º | **T4** — IDS e concept drift | 🔴 | Pergunta respondida. Evitar. |

### Como usar isto na semana que vem

Leia **dois ou três artigos** de cada um dos três primeiros. Não leia para dominar o
assunto — leia para sentir se você aguenta conviver com aquilo até dezembro de 2027. O
sinal que importa não é "entendi tudo", é **"fiquei com vontade de ver o resultado"**.

Depois cruze com a lista de linhas de pesquisa dos orientadores, apresentada na aula de
**25/08**. Tema forte sem orientador disponível perde para tema bom com orientador
engajado, sempre.
