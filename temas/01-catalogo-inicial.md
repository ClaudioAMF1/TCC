# Propostas de Tema — Projeto Capstone I (TCC 1) — 2026.2

Documento de apoio para a escolha do tema. Elaborado a partir do **Plano de Ensino
de Projeto Capstone I (2026.2)**, do **Regulamento de TCC do curso de Ciência da
Computação do IDP (v. 2026-05)** e das Aulas 01 e 02.

---

## 1. O que as regras já decidem por você

Antes de pensar em tema, vale fixar as restrições que saem direto dos documentos —
elas eliminam boa parte das ideias ruins sozinhas.

| Restrição | Origem | Consequência prática na escolha do tema |
|---|---|---|
| Trabalho **individual** | Reg., Art. 6º | O escopo tem que caber em uma pessoa. Nada de "plataforma completa com backend, app e dashboard". |
| **Dois semestres**: Capstone I = projeto de pesquisa + referencial teórico; Capstone II = execução e defesa | Reg., Art. 9º, §1º e §2º | Em 2026.2 você **não precisa** ter resultados. Precisa ter um projeto defensável. Mas escolha um tema cuja execução em 2027.1 seja realista. |
| O projeto de pesquisa **deve conter toda a fundamentação e revisão bibliográfica** do Capstone | Reg., Art. 25, §3º | O tema precisa ter literatura acessível e organizável. Tema sem literatura = revisão bibliográfica impossível. |
| **Qualificação perante banca de 3 docentes** no fim do Capstone I | Reg., Art. 11 | O projeto será arguido. Ele precisa sobreviver à pergunta "e como você vai avaliar isso?". |
| O texto final deve ser **em inglês** | Reg., Art. 32, §3º | Escreva o projeto já pensando em inglês, e prefira temas cuja literatura seja majoritariamente em inglês (é quase toda). |
| Modalidade **artigo científico** exige aceite em conferência (Capstone I) e em periódico **Qualis ≥ B2** (Capstone II) | Reg., Art. 25, §4º e Art. 29, §1º | **Alto risco.** Aceite em periódico B2 não depende de você, depende de revisores e de prazos de 6–12 meses. Recomendação: **monografia** (ou relatório técnico-científico), e transformar em artigo depois, como o Art. 29, §2º sugere. |
| Orientador escolhido no 1º bimestre, com termo de aceite | Reg., Art. 10 e Art. 15 | Os orientadores e linhas de pesquisa são apresentados na **aula de 25/08**. O tema tem que ter alguém no corpo docente disposto e capaz de orientar. |
| 5 encontros obrigatórios com o orientador no 2º bimestre, com ficha assinada | Reg., Art. 19, II e Art. 24 | Burocracia que reprova. Coloque no calendário desde o começo. |
| Uso indevido de IA = reprovação definitiva + sindicância | Reg., Art. 49 | Cuidado com a distinção: **IA como objeto de pesquisa** é ótimo; **IA escrevendo o TCC por você** é infração. Se o método usar LLM, isso vai declarado e documentado no capítulo de metodologia — o que aliás fortalece o trabalho. |

### Critérios de avaliação da banca (Reg., Art. 31)

O primeiro critério é literal: **"presença do quadrante metodológico:
tema–problema–hipótese–marco teórico"**. Ou seja, o tema só está pronto quando você
consegue preencher as quatro caixas:

- **Tema**: a área delimitada.
- **Problema**: uma pergunta de pesquisa específica e respondível.
- **Hipótese**: uma afirmação que pode ser **refutada** por evidência (é exatamente o
  ponto da Aula 02, sobre refutação/Popper).
- **Marco teórico**: o corpo de literatura sobre o qual você se apoia.

Se um tema não permite escrever uma hipótese falsificável, ele não passa na
qualificação — não importa quão legal seja.

---

## 2. O filtro que mais elimina ideias: maturidade em pesquisa

A aula de 13/08 é "Maturidade em Pesquisa", e o Wazlawick (bibliografia básica) organiza
os trabalhos em uma escala. Simplificando:

1. **Apresentação de um produto** — "eu construí um sistema X". *Nível mais fraco.*
2. **Apresentação de algo diferente** — "meu X é diferente do que existe".
3. **Apresentação de algo presumivelmente melhor** — "meu X deve ser melhor, porque...".
4. **Apresentação de algo reconhecidamente melhor** — "meu X é melhor, e aqui está a
   medição comparativa que sustenta isso". *Nível forte.*
5. **Apresentação de uma prova** — demonstração formal.

**Praticamente todo TCC ruim mora no nível 1.** "Desenvolvi um firewall", "criei um
sistema de detecção de phishing" — sem baseline, sem métrica, sem comparação.

Isso muda a forma de escolher tema: em vez de perguntar *"o que eu quero construir?"*,
pergunte *"o que eu quero medir, e contra o que eu vou comparar?"*. Todos os temas
abaixo foram desenhados para nascer no nível 3–4.

Existe um atalho honesto e muito bem aceito em banca: **estudos empíricos de
medição/caracterização** (medir um fenômeno em escala e descrever o que se encontra) e
**replicações em nova população** (aplicar uma metodologia já validada na literatura a
um contexto ainda não estudado — por exemplo, o contexto brasileiro). Esses formatos
têm contribuição clara, risco baixo e não dependem de você inventar um algoritmo novo.

---

## 3. Sobre a sua dúvida: cibersegurança é uma boa aposta?

Resposta curta: **sim, é uma das melhores áreas para TCC**, por três razões concretas:

1. **Dados públicos e gratuitos em abundância** (OSV, GitHub, PhishTank, CIC-IDS, CVE/NVD).
   Você não depende de coletar dados com pessoas, não precisa de comitê de ética, não
   precisa de laboratório nem de orçamento.
2. **Métricas objetivas já estabelecidas** (taxa de vulnerabilidade, precisão/recall,
   tempo até correção). Métrica pronta = hipótese falsificável = banca satisfeita.
3. **Ferramental maduro e aberto** (Semgrep, CodeQL, Trivy, Checkov, scikit-learn,
   Playwright). Você gasta o tempo na pesquisa, não em encanamento.

Mas note uma coisa importante: **"cibersegurança" não é um tema, é um continente.**
Os temas abaixo são de subáreas bem diferentes entre si — segurança de código,
segurança de cadeia de suprimentos, privacidade/medição web, ML aplicado a segurança,
segurança de IA. Você pode gostar de uma e detestar a outra. Vale ler as sete e
perceber qual tipo de *trabalho diário* te atrai: escrever scripts de mineração de
dados? treinar modelos? montar experimentos com LLMs? auditar configuração?

E, para testar se o insight é real, incluí na Seção 5 duas alternativas **fora** de
cibersegurança que usam exatamente a mesma metodologia — se elas te animarem mais, o
que te atrai talvez seja o método empírico, não a segurança.

---

## 4. Sete temas em cibersegurança

Cada tema traz o quadrante metodológico já esboçado, os dados/ferramentas, o que
entra no Capstone I versus no Capstone II, e os riscos honestos.

---

### T1 — Segurança do código gerado por LLMs

> *Título provisório (EN): "Security of LLM-Generated Code: A Comparative Evaluation of
> Models and Prompting Strategies Against CWE Classes"*

**Problema.** Assistentes de código (Copilot, Cursor, Claude Code) já escrevem uma
fração relevante do código em produção. Qual a taxa de vulnerabilidades desse código, e
dá para reduzi-la só mudando o prompt — sem trocar de modelo?

**Hipótese.** Estratégias de prompting com contexto de segurança (instrução explícita de
CWE, auto-revisão em duas etapas, RAG sobre catálogo de vulnerabilidades) reduzem
significativamente a taxa de código vulnerável gerado, **sem perda relevante de
corretude funcional**.

**Método.** Quase-experimento fatorial: *modelos* × *estratégias de prompting* × *tarefas
de programação*. Cada célula gera N amostras de código; cada amostra é analisada por
ferramentas de SAST e por inspeção manual em uma subamostra (para medir falso positivo).

**Dados e ferramentas.** Benchmarks prontos: SecurityEval, LLMSecEval, CyberSecEval
(Purple Llama), conjunto de prompts derivado do CWE Top 25. Análise: Semgrep, CodeQL,
Bandit. Corretude funcional: HumanEval/MBPP. Modelos: pesos abertos rodando local via
Ollama (Qwen-Coder, DeepSeek-Coder, CodeLlama) + um ou dois comerciais.

**Métricas.** Taxa de código vulnerável por CWE; pass@k (funcionalidade); concordância
entre ferramentas (kappa); tamanho de efeito das estratégias de prompting.

**Capstone I.** Revisão sistemática sobre segurança de código gerado por IA; definição
do protocolo experimental; piloto com 1 modelo e 1 estratégia para validar o pipeline.
**Capstone II.** Execução completa, análise estatística, discussão.

**Riscos.** Custo de API dos modelos comerciais (mitigável: priorizar pesos abertos
locais). Não-determinismo dos modelos (mitigável: fixar temperatura e reportar variância
entre execuções).

**Por que passa na banca.** Nível 4 de maturidade — comparação controlada com métrica
objetiva. Tema extremamente atual, e a banca entende o problema em 30 segundos.

---

### T2 — Vulnerabilidades na cadeia de suprimentos de software brasileira

> *Título provisório (EN): "Transitive Dependency Risk in Brazilian Public-Sector Open
> Source: An Empirical Study of Exposure and Patch Lag"*

**Problema.** Software público brasileiro (repositórios de órgãos no GitHub, projetos
gov.br) depende de centenas de pacotes de terceiros. Qual é a exposição real a
vulnerabilidades conhecidas via dependências **transitivas**, e quanto tempo esses
projetos levam para aplicar a correção depois que ela existe?

**Hipótese.** A maior parte da exposição vem de dependências transitivas (não declaradas
diretamente), e o *patch lag* mediano é significativamente maior do que o de projetos
open source de referência internacional.

**Método.** Estudo empírico de mineração de repositórios. Coleta de repositórios →
geração de SBOM → cruzamento com bases de vulnerabilidade → análise longitudinal do
histórico de commits para medir o tempo entre publicação da correção e adoção.

**Dados e ferramentas.** GitHub API; OSV.dev e deps.dev (APIs públicas, gratuitas);
GHSA/NVD; Syft/CycloneDX para SBOM; OSV-Scanner e Trivy para detecção; análise de
alcançabilidade (*reachability*) para separar vulnerabilidade "presente" de
vulnerabilidade "explorável".

**Métricas.** Vulnerabilidades por projeto (normalizadas); profundidade transitiva
mediana; *patch lag* (dias); proporção de vulnerabilidades alcançáveis; distribuição por
severidade CVSS.

**Capstone I.** Revisão sobre segurança de cadeia de suprimentos; definição do universo
amostral e dos critérios de inclusão; protocolo de coleta; piloto com ~30 repositórios.
**Capstone II.** Coleta completa, análise, e publicação do dataset como artefato.

**Riscos.** Rate limit das APIs (mitigável com token e cache local). Definir "software
público brasileiro" de forma defensável exige critério explícito — isso vira uma seção
de metodologia, não um problema.

**Por que passa na banca.** Contribuição inequívoca: **ninguém mediu isso nesse
recorte**. Gera dataset público. Custo zero. E tem apelo institucional óbvio.

---

### T3 — Conformidade com a LGPD medida em escala na web brasileira

> *Título provisório (EN): "Measuring LGPD Consent Compliance at Scale: Third-Party
> Tracking and Dark Patterns in Brazilian Websites"*

**Problema.** A LGPD exige consentimento para tratamento de dados. Na prática, quantos
sites brasileiros já instalam cookies de rastreamento **antes** de qualquer consentimento,
e quantos oferecem recusa tão fácil quanto a aceitação?

**Hipótese.** A maioria dos sites brasileiros de alto tráfego viola o requisito de
consentimento prévio, e a assimetria entre "aceitar" e "recusar" nos banners
(*dark patterns*) é a norma, não a exceção.

**Método.** Medição web automatizada em escala. Crawler visita N sites (top brasileiros
por ranking público, ou recortes: .gov.br, saúde, educação), captura requisições de rede
e cookies em dois cenários — sem interação e após aceitar — e classifica o banner de
consentimento.

**Dados e ferramentas.** Playwright para automação; listas EasyList/EasyPrivacy e
DuckDuckGo Tracker Radar para identificar rastreadores; taxonomias de *dark patterns* já
publicadas (Nouwens et al., Matte et al., Trevisan et al. — a literatura europeia sobre
GDPR é o marco teórico pronto).

**Métricas.** % de sites com rastreadores pré-consentimento; nº mediano de terceiros por
site; % com opção de recusa em um clique; taxonomia de padrões escuros observados.

**Capstone I.** Revisão da literatura de medição de conformidade (GDPR) + análise
jurídico-técnica dos requisitos da LGPD; definição da amostra; crawler funcionando em
piloto de 50 sites.
**Capstone II.** Medição completa, análise por setor, e comparação com os números
europeus da literatura.

**Riscos.** Robustez do crawler (sites quebram, CAPTCHAs). Mitigável: amostra com folga e
registro explícito de falhas. Escopo ético: é medição passiva de páginas públicas, sem
exploração — vale uma seção declarando isso.

**Por que passa na banca.** É uma **replicação em nova população** — formato canônico,
baixo risco metodológico, contribuição clara. Interdisciplinar (direito + computação),
o que costuma agradar bastante em banca. E o IDP tem tradição forte na área jurídica,
o que aumenta a chance de encontrar coorientação interessada.

---

### T4 — Detecção de intrusão sob mudança de distribuição (concept drift)

> *Título provisório (EN): "Do Machine Learning Intrusion Detectors Generalize?
> A Cross-Dataset Evaluation Under Concept Drift"*

**Problema.** A literatura reporta rotineiramente 99% de acurácia em detecção de intrusão
com ML. Mas quase sempre treinando e testando no **mesmo** dataset. O que acontece quando
o modelo encontra tráfego de outra origem ou de outra época?

**Hipótese.** O desempenho de detectores treinados em um dataset degrada
substancialmente quando avaliados em outro (*cross-dataset*), e a degradação não é
explicada por diferença de classes, mas por deslocamento de distribuição das features.

**Método.** Avaliação cruzada sistemática: treinar em A, testar em B, para todos os pares
de datasets; quantificar o drift; avaliar estratégias de mitigação (retreino incremental,
seleção de features robustas, detecção de drift).

**Dados e ferramentas.** CIC-IDS2017, CSE-CIC-IDS2018, UNSW-NB15, TON_IoT — todos
públicos e gratuitos. **Atenção crítica:** o CIC-IDS2017 tem erros de rotulagem
documentados na literatura (Engelen et al., "Troubleshooting an Intrusion Detection
Dataset"); usar a versão corrigida e **discutir isso** já é, sozinho, uma contribuição de
rigor que impressiona banca. Ferramentas: scikit-learn, XGBoost, River (aprendizado
incremental).

**Métricas.** F1/AUC intra vs. inter dataset; queda percentual; métricas de drift; custo
de retreino.

**Capstone I.** Revisão sistemática (com foco em expor o viés metodológico da área);
protocolo de avaliação; piloto com um par de datasets.
**Capstone II.** Matriz completa de avaliação cruzada + mitigação.

**Riscos.** Volume de dados (dezenas de GB) exige máquina razoável — verifique seu
hardware antes de fechar este tema. Harmonizar features entre datasets diferentes dá
trabalho e precisa ser documentado com cuidado.

**Por que passa na banca.** É um trabalho que **critica a literatura com evidência** —
maturidade alta. Cuidado: só funciona se você resistir à tentação de virar "treinei 5
modelos e comparei acurácia", que é o TCC genérico que todo mundo faz.

---

### T5 — Más configurações de segurança em Infraestrutura como Código

> *Título provisório (EN): "Security Misconfigurations in Infrastructure as Code:
> Prevalence and Scanner Agreement in Public Repositories"*

**Problema.** Terraform, Kubernetes e Dockerfiles definem a segurança da infraestrutura
em arquivos de texto versionados. Quão comuns são as más configurações nesses arquivos
em repositórios públicos — e as ferramentas que deveriam detectá-las concordam entre si?

**Hipótese.** As ferramentas de análise de IaC apresentam **baixa concordância** entre si,
e uma parcela significativa dos alertas de cada uma é falso positivo — de modo que
confiar em uma única ferramenta subestima o risco real.

**Método.** Mineração de repositórios + comparação de ferramentas. Coletar N repositórios
com artefatos IaC, rodar múltiplos scanners sobre o mesmo corpus, medir concordância e
validar manualmente uma amostra estratificada para estimar precisão.

**Dados e ferramentas.** GitHub Code Search / GHArchive para o corpus; Checkov, KICS,
Trivy, Terrascan como scanners; validação manual com protocolo de codificação
(e, idealmente, um segundo codificador para medir confiabilidade).

**Métricas.** Densidade de más configurações por KLOC; distribuição por categoria;
concordância entre ferramentas (Fleiss' kappa); precisão estimada por amostragem.

**Capstone I.** Revisão sobre *IaC smells* e segurança de configuração; protocolo de
coleta e de codificação manual; piloto.
**Capstone II.** Estudo completo + guia de uso combinado de ferramentas.

**Riscos.** A validação manual é trabalhosa — dimensione a amostra com realismo (algo
como 300–400 alertas, não 5.000).

**Por que passa na banca.** Metodologia limpa, custo zero, resultado útil na prática. É
o tema de **menor risco de execução** desta lista.

---

### T6 — Detecção de phishing: LLMs vs. aprendizado de máquina clássico

> *Título provisório (EN): "LLMs vs. Classical Machine Learning for Phishing Detection:
> Accuracy, Cost, and Robustness Against AI-Generated Lures"*

**Problema.** LLMs detectam phishing melhor que um classificador clássico bem ajustado?
E o que acontece com ambos quando o phishing é escrito por um LLM — sem os erros de
português e os sinais grosseiros que os modelos aprenderam a usar?

**Hipótese.** LLMs superam modelos clássicos em generalização para campanhas novas, mas
a vantagem se reduz drasticamente quando o phishing é gerado por IA; e o custo por
inferência do LLM é ordens de grandeza maior — o que torna a escolha uma questão de
trade-off, não de superioridade.

**Método.** Comparação com baseline forte (TF-IDF + SVM/Gradient Boosting é
surpreendentemente competitivo — e usar um baseline forte é sinal de rigor) contra LLMs
em *zero-shot* e *few-shot*. Segunda etapa: avaliação de robustez sobre um conjunto
adversarial gerado em ambiente controlado.

**Dados e ferramentas.** PhishTank, OpenPhish, corpus Nazario de phishing, Enron e
SpamAssassin como *ham*, PhiUSIIL (UCI) para URLs. scikit-learn + LLMs de pesos abertos.

**Ética — importante e não negociável.** O conjunto adversarial é gerado **apenas** para
avaliação offline, nunca enviado a pessoas, e o trabalho declara isso explicitamente
numa seção de considerações éticas. O enquadramento é **defensivo**: medir a fragilidade
dos detectores para melhorá-los. Isso precisa estar escrito no projeto desde o Capstone I,
porque a banca **vai** perguntar.

**Métricas.** Precisão/recall/F1; desempenho em campanhas fora da distribuição de treino;
custo por 1.000 classificações; latência.

**Riscos.** A seção ética exige cuidado real na redação. Alinhe com o orientador antes.

**Por que passa na banca.** Baseline forte + eixo de robustez + eixo de custo = trabalho
maduro. Tema que a banca entende e acha relevante imediatamente.

---

### T7 — Segurança de agentes de IA: defesas contra injeção indireta de prompt

> *Título provisório (EN): "Evaluating Defenses Against Indirect Prompt Injection in
> Tool-Using LLM Agents"*

**Problema.** Agentes de IA leem conteúdo externo (páginas, e-mails, documentos) e
executam ferramentas. Conteúdo malicioso embutido nesses dados pode sequestrar o agente.
Quão eficazes são as defesas propostas até agora?

**Hipótese.** As defesas baseadas em prompt (delimitação, *spotlighting*, instruções
defensivas) reduzem mas não eliminam o ataque, e degradam a utilidade do agente; defesas
arquiteturais (isolamento de privilégio das ferramentas) oferecem melhor relação
segurança/utilidade.

**Método.** Avaliação comparativa sobre benchmarks de agentes, medindo simultaneamente
**taxa de sucesso do ataque** e **taxa de sucesso da tarefa legítima** — o ponto central é
que segurança sem medir utilidade não significa nada.

**Dados e ferramentas.** AgentDojo, InjecAgent, BIPIA (benchmarks públicos). Modelos de
pesos abertos + comerciais.

**Métricas.** Attack success rate; benign task success rate; fronteira de trade-off.

**Riscos.** É o tema **mais difícil de executar** da lista: montar o ambiente de agentes
dá trabalho, os benchmarks evoluem rápido e o custo de inferência é o mais alto. Também
é o mais difícil de encontrar orientador confortável com o assunto.

**Por que passa na banca.** Fronteira de pesquisa, altíssima relevância. Escolha este se
você já tem familiaridade com agentes/LLMs — caso contrário, o T1 entrega apelo parecido
com metade do risco.

---

## 5. Duas alternativas fora de cibersegurança (para testar o insight)

Mesma metodologia empírica, domínio diferente. Se alguma destas te empolgar mais que as
sete acima, o que te atrai é o **método**, e vale considerar.

### A1 — Acessibilidade digital em serviços públicos brasileiros
Medição automatizada de conformidade com WCAG/eMAG em portais de serviços públicos,
combinando análise automatizada (axe-core) com auditoria manual amostrada — porque a
literatura mostra que ferramentas automáticas capturam só uma fração dos problemas
reais, e **quantificar essa fração** é a contribuição. Mesmo ferramental do T3, impacto
social direto, banca gosta.

### A2 — Impacto de assistentes de IA na qualidade de código em projetos reais
Mineração de repositórios para comparar métricas de qualidade, taxa de defeitos e tempo
de revisão entre contribuições assistidas por IA e não assistidas. Engenharia de software
empírica pura, dados abertos, e conversa com o T1 se você quiser migrar depois.

---

## 6. Recomendação

Ordenando por **(relevância × viabilidade individual) ÷ risco**:

| # | Tema | Recomendação |
|---|---|---|
| 🥇 | **T2 — Cadeia de suprimentos brasileira** | Melhor equilíbrio geral. Custo zero, dados públicos, contribuição inegável ("ninguém mediu isso"), gera dataset. Execução é essencialmente scripts + análise — totalmente factível sozinho. Risco baixíssimo de "não dar certo". |
| 🥈 | **T1 — Segurança de código gerado por LLM** | Maior apelo e maior atualidade. Metodologia experimental limpa, nível 4 de maturidade. Risco moderado (custo/não-determinismo dos modelos), controlável com pesos abertos locais. |
| 🥉 | **T3 — Conformidade LGPD na web brasileira** | Formato de replicação, o mais seguro metodologicamente. Ângulo interdisciplinar (LGPD) casa bem com o perfil do IDP e amplia as opções de orientação. |

**T5** é o *plano B* ideal: menos vistoso, mas o mais difícil de dar errado.
**T4** é excelente se — e só se — você tiver hardware para os datasets e disciplina para
não cair no comparativo genérico de classificadores.
**T7** só se você já mexe com agentes.

Uma observação que vale mais que o ranking: **a escolha do orientador pesa tanto quanto
a escolha do tema.** Um tema mediano com orientador engajado termina; um tema brilhante
sem orientador que o entenda trava em novembro. Na aula de 25/08, quando as linhas de
pesquisa forem apresentadas, cruze esta lista com o que os docentes efetivamente
orientam — e esteja disposto a adaptar o tema para o interesse de quem vai te orientar.

---

## 7. Armadilhas a evitar

- **"Vou desenvolver um sistema de segurança X."** Nível 1 de maturidade. Sem baseline e
  sem métrica, a banca pergunta "e daí?" e não há resposta.
- **Pentest em sistema real de terceiros.** Sem autorização formal por escrito, é crime
  (Lei 12.737/2012 e correlatas). Se for por esse caminho, tem que ser em ambiente
  próprio ou em plataforma explicitamente autorizada.
- **Dataset que você planeja coletar com pessoas.** Questionário/entrevista puxa comitê de
  ética e prazos que não cabem em um semestre. Prefira dados já públicos.
- **Tema amplo demais.** "Segurança em IoT" não é tema, é disciplina. Delimite até caber
  em uma pergunta única.
- **Comparação de ferramentas sem validação manual.** Rodar 4 scanners e tabular a saída
  não é pesquisa; validar uma amostra e estimar precisão é.
- **Escolher só pelo que é moderno.** Você vai conviver com esse assunto por dois
  semestres. Escolha o que aguenta ser lido em dezembro sem enjoo.

---

## 8. Próximos passos, ancorados no cronograma da disciplina

| Prazo | O que fazer |
|---|---|
| Até ~11/08 | Escolher **2 finalistas** desta lista. Ler 3–4 artigos recentes de cada um (Google Scholar / IEEE Xplore / ACM DL / SBC OpenLib) só para sentir se o assunto te prende. |
| Até 25/08 | Chegar na aula de apresentação dos orientadores **com os 2 finalistas na mão** e uma frase de 30 segundos sobre cada. Quem chega com tema pronto escolhe orientador; quem chega vazio é escolhido pelo que sobrou. |
| Aulas 9 e 10 (01 e 03/09) — Oficina de bases | Usar a oficina para montar a busca sistemática do tema **já escolhido**. Não desperdice a oficina com um tema genérico. |
| Até 10/09 | Lista de Exercícios 01 entregue (impressa). |
| 29/09 e 01/10 | Seminário de análise de artigo: escolha um artigo que seja **base do seu TCC**. O plano de ensino exige justificar a relevância para o seu trabalho — dois coelhos com uma cajadada. |
| Out–Nov | Os 5 encontros obrigatórios com o orientador, **com ficha assinada e entregue mensalmente** (Reg., Art. 24, §2º). Isso reprova gente boa. |
| 24/11–01/12 | Simulação de defesa. |
| **03/12** | **Entrega da redação do TCC I no Canvas.** Prazo duro. |
| 08–15/12 | Defesa final / qualificação perante banca. |

Ferramentas que a disciplina vai cobrar e que compensa já adotar desde agora: **LaTeX**
(Overleaf — e o texto final é em inglês, então já comece nele) e um **gerenciador de
referências** (Zotero ou JabRef). Começar a revisão bibliográfica sem gerenciador é
retrabalho garantido em novembro.
