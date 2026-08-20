# Novos Temas em Cibersegurança — Orientáveis pelo Prof. Izycki

Propostas construídas sob três restrições simultâneas:

1. **Compatibilidade com o orientador** — a Aula 05/06 afirma explicitamente que *"o tema
   da pesquisa tem que ser compatível com os conhecimentos do orientador"*. Não é
   conselho: é critério da disciplina.
2. **Regras de formulação da Aula 05/06** — objetivo expresso com verbo **verificável**
   (demonstrar, medir, comparar, avaliar). Os verbos *propor*, *estudar* e *apresentar*
   são explicitamente apontados como inadequados, por serem de verificação trivial. O
   problema de pesquisa tem três partes obrigatórias: enunciado preciso, demonstração por
   referência bibliográfica de que ainda não foi tratado, e discussão de por que importa.
3. **Maturidade (Aula 04)** — todos os temas abaixo são de **estilo empírico**, no qual,
   nas palavras do slide, *"os métodos estatísticos serão a grande ferramenta de trabalho"*.
   Nenhum é "apresentação de um produto", o nível que a aula desqualifica.

> Uma observação da Aula 04 que vale reter: o nível empírico mais maduro é descrito como
> **"a pesquisa mais fácil de executar, porém tem como principal dificuldade encontrar uma
> boa hipótese de trabalho"**. É exatamente por isso que estas propostas gastam mais
> espaço na hipótese do que no método.

---

## O perfil do orientador, traduzido em capacidade de orientação

Do currículo: proteção de infraestrutura crítica (15 anos no GSI/PR), estratégias nacionais
de segurança cibernética, capacidades cibernéticas de Estados-nação, inteligência de
ameaças, atribuição e hacktivismo, América Latina no ciberespaço, e formação jurídica
(Direito UFPR + Direito Eletrônico).

O padrão que funciona: **você executa a medição técnica; ele orienta o enquadramento, a
interpretação de domínio e a relevância**. É a divisão que o Art. 22, §2º do Regulamento
define — ao orientador cabe o marco teórico e a produção do texto.

---

## N1 — Superfície de ataque exposta da infraestrutura crítica brasileira

**Título provisório (EN):** *Exposed by Default: Measuring Internet-Facing Industrial
Control Systems in Brazilian Critical Infrastructure*

### Problema de pesquisa (nas três partes exigidas)

**Enunciado.** Qual a extensão, a composição setorial e o perfil de risco dos dispositivos
de controle industrial (ICS/SCADA) e interfaces de gerenciamento acessíveis pela internet
atribuíveis a operadores de infraestrutura crítica no espaço de endereçamento brasileiro?

**Lacuna na literatura.** A metodologia é estabelecida e há estudos nacionais publicados
para **Países Baixos**, **Itália** e **Hong Kong**, além de um trabalho no EuroS&P 2025.
**Não há estudo equivalente para o Brasil.** Isso é vantagem dupla: o método está validado
e revisado por pares, e a população é inédita.

**Por que importa.** O Brasil aprovou a Política Nacional de Cibersegurança sem que exista
uma linha de base pública da exposição real da sua infraestrutura crítica. Sem linha de
base não há como medir progresso.

### Objetivo geral

**Medir e caracterizar** a exposição de sistemas de controle industrial atribuíveis à
infraestrutura crítica brasileira, **comparando** a distribuição setorial com as linhas de
base publicadas para outros países.

### Hipótese

A exposição concentra-se desproporcionalmente em setores sob menor supervisão regulatória
(saneamento e gestão predial) em comparação com setores fortemente regulados (energia
elétrica e financeiro); e a proporção de dispositivos expostos que executam versões com
vulnerabilidade conhecida é significativamente maior no Brasil do que nas linhas de base
europeias publicadas.

### Método e dados

Consulta a **bases de varredura de terceiros** (Shodan e Censys, ambos com acesso
acadêmico gratuito) — **sem varredura ativa realizada por você**. Atribuição
IP → organização → setor via ASN, whois e heurísticas validadas manualmente em amostra.
Filtragem de *honeypots*, que a literatura mostra serem numerosos (um estudo identificou
1.174 entre 100.766 dispositivos) — **fazer essa filtragem é, sozinho, um refinamento
metodológico defensável**.

### Ética — limite não negociável

Medição **passiva**, sobre dados já coletados e publicados por terceiros. Nenhuma conexão
ativa, nenhuma tentativa de autenticação, nenhuma exploração. Resultados reportados de
forma **agregada por setor** — nunca identificando o operador específico. Se algo crítico
e atribuível for encontrado, o caminho é notificar o CTIR Gov antes de publicar. Essa
seção vai escrita no projeto desde o Capstone I.

### Encaixe com o orientador

**O mais direto de todos.** Proteção de infraestrutura crítica foi literalmente o trabalho
dele por 15 anos no GSI/PR, e é o tema de várias das publicações dele (*Protection of
Critical Infrastructure in National Cyber Security Strategies*, ECCWS 2019; *Critical
Infrastructure: A Battlefield for Cyber Warfare?*, ICCWS 2021).

### Riscos

Acesso acadêmico ao Shodan/Censys (solicite **nesta semana** — é o teste de viabilidade
deste tema). Atribuição IP→setor é imprecisa e exige validação manual documentada.

### Maturidade

Nível 3–4 — caracterização com eixo comparativo internacional e métrica objetiva.

**Leitura:**
- [Uncovering Exposed Industrial Control Systems (EuroS&P 2025)](https://gsmaragd.github.io/publications/EuroSP2025-ICS/EuroSP2025-ICS.pdf)
- [Online Discoverability and Vulnerabilities of ICS/SCADA Devices in the Netherlands](https://arxiv.org/pdf/2011.02019)
- [Investigation of risks for Critical Infrastructures due to exposure of SCADA on Shodan](https://library.imaging.org/ei/articles/32/3/art00006)
- [Vulnerability assessment of industrial systems using Shodan (Cluster Computing)](https://link.springer.com/article/10.1007/s10586-021-03330-3)

---

## N2 — Estratégia nacional versus realidade mensurável

**Título provisório (EN):** *Declaratory or Effective? Measuring the Technical Security
Posture of Brazilian Government Domains Against National Cyber Strategy Commitments*

### Problema de pesquisa

**Enunciado.** Os compromissos técnicos assumidos nos instrumentos brasileiros de política
de segurança cibernética se traduzem em melhoria mensurável na postura técnica dos
domínios governamentais — autenticação de e-mail, DNSSEC, TLS, RPKI?

**Lacuna.** A medição global desses indicadores é abundante, e ela revela um achado que
funciona como ponto de partida: em 2026, **30,4% dos domínios adotam DMARC, mas apenas
12,8% aplicam política que efetivamente protege contra falsificação** — mais da metade
está em `p=none`, que oferece proteção nula. **Adoção não é proteção.** Ninguém aplicou
esse recorte ao governo brasileiro, nem cruzou os números com os compromissos de política
pública.

**Por que importa.** Golpes que falsificam remetentes governamentais (Receita Federal,
gov.br, INSS) são um dos vetores de fraude mais comuns no Brasil. DMARC em `p=none` num
domínio da Receita significa que qualquer pessoa pode enviar e-mail em nome dela.

### Objetivo geral

**Medir** a postura técnica de segurança dos domínios governamentais brasileiros e
**demonstrar** em que grau ela diverge dos compromissos declarados nos instrumentos
nacionais de política de segurança cibernética.

### Hipóteses

- **H1** — A adoção de autenticação de e-mail nos domínios federais é substancialmente
  superior à dos domínios estaduais e municipais, revelando desigualdade federativa na
  capacidade de defesa.
- **H2** — Entre os domínios que adotam DMARC, a maioria permanece em política sem
  enforcement (`p=none`), de modo que **a adoção declarada superestima a proteção real**.
- **H3** — Não há inflexão mensurável nos indicadores após a publicação dos instrumentos
  de política, sustentando a caracterização desses instrumentos como declaratórios.

### Método e dados

Consulta DNS em massa aos domínios `.gov.br` (federais, estaduais e municipais) para
SPF/DKIM/DMARC, DNSSEC, CAA, MTA-STS; verificação de TLS/HSTS; RPKI via bases do RIPE/NIST.
Para a série temporal de H3, dados históricos de projetos de medição longitudinal e
arquivos web. Análise: comparação de proporções entre esferas, com controles por porte.

### Encaixe com o orientador

**Excelente.** Estratégias nacionais de segurança cibernética são o núcleo da produção dele
(*Estratégias nacionais de segurança cibernética na América Latina*, RISTI 2018; *National
Cyber Strategies*; a tese de doutorado em andamento). Este tema é a pergunta dele com um
método empírico que você traz — o tipo de combinação que vira publicação conjunta.

### Riscos

**Baixíssimos.** Consulta DNS é rápida, gratuita e não invasiva. O risco real é o oposto:
a coleta é tão fácil que o trabalho pode ficar raso. **A profundidade tem que vir do eixo
longitudinal (H3) e da análise federativa (H1)** — sem eles, isto vira relatório técnico.

### Maturidade

Nível 3 — comparação com métrica objetiva e eixo temporal.

**Leitura:**
- [The Evolution of DNS-based Email Authentication: Measuring Adoption and Finding Flaws (ACM)](https://dl.acm.org/doi/fullHtml/10.1145/3471621.3471842)
- [Lazy Gatekeepers: A Large-Scale Study on SPF Configuration in the Wild](https://arxiv.org/pdf/2502.08240)
- [Spoofed Emails: Issues Hindering a Larger Deployment of DMARC](https://link.springer.com/chapter/10.1007/978-3-031-56249-5_10)
- [Revisiting Email Spoofing Attacks](https://arxiv.org/pdf/1801.00853)

---

## N3 — Aplicativos móveis governamentais: rastreadores, dado sensível e soberania

**Título provisório (EN):** *Who Else Is in the App? Third-Party Tracking and Data
Sovereignty in Brazilian Government Mobile Applications*

### Problema de pesquisa

**Enunciado.** Aplicativos móveis oficiais do governo brasileiro — inclusive os que tratam
dado pessoal sensível, como saúde, benefícios previdenciários e situação fiscal — embarcam
SDKs de rastreamento de terceiros que transmitem identificadores a servidores estrangeiros?

**Lacuna.** A metodologia é madura e replicada em muitos domínios — apps de terapia, saúde
mental, fitness, controle parental, rastreamento de contato —, com achados recorrentes de
SDKs não declarados nas políticas de privacidade. **Não há estudo do parque de aplicativos
governamentais brasileiros.**

**Por que importa.** Duas camadas de consequência, e é a segunda que torna o tema
distintivo: a violação de LGPD (Art. 11, se houver dado sensível) e a **questão de
soberania de dados** — identificadores de cidadãos brasileiros interagindo com serviços
públicos fluindo para infraestrutura sob jurisdição estrangeira.

### Objetivo geral

**Medir** a prevalência de SDKs de rastreamento de terceiros e de falhas de segurança em
aplicativos móveis governamentais brasileiros, e **comparar** o comportamento desses
aplicativos com o de aplicativos comerciais de porte equivalente.

### Hipóteses

- **H1** — Aplicativos governamentais embarcam SDKs de rastreamento em proporção
  **estatisticamente indistinguível** da de aplicativos comerciais pareados, apesar do
  regime jurídico distinto a que estão submetidos.
- **H2** — Uma fração relevante dos SDKs identificados **não é declarada** na política de
  privacidade do aplicativo.
- **H3** — Aplicativos que tratam dado sensível não apresentam postura de proteção superior
  à dos demais aplicativos governamentais.

### Método e dados

Coleta dos APKs públicos (aplicativos oficiais de órgãos federais, estaduais e municipais).
Análise estática com **MobSF** e Androguard: permissões perigosas, segredos embutidos,
criptografia fraca, configuração de rede, SDKs de terceiros identificados por assinatura
(Exodus Privacy como referência). Análise dinâmica de tráfego em subamostra, com
interceptação TLS em dispositivo/emulador próprio. Grupo de controle pareado de apps
comerciais. Confronto automatizado entre SDKs detectados e política de privacidade
declarada.

### Ética

Analisa-se **o aplicativo**, não pessoas. Interceptação apenas em dispositivo próprio, com
conta própria. Nenhum dado de terceiros é coletado. Divulgação responsável antes da
publicação, se houver achado grave atribuível.

### Encaixe com o orientador

**Bom, por duas vias.** A camada jurídica (LGPD, dado sensível, política de privacidade) é
o terreno da formação em Direito e Direito Eletrônico. A camada de **soberania de dados e
dependência de infraestrutura estrangeira** é literalmente o tema das publicações dele
sobre poder cibernético e Sul Global.

### Riscos

Interceptação TLS falha em apps com *certificate pinning* — isso limita a análise dinâmica
a uma subamostra, e **deve ser reportado como limitação, não escondido**. Coleta de APKs de
apps estaduais/municipais pode ser trabalhosa.

### Maturidade

Nível 3–4 — comparação com grupo de controle e métrica objetiva.

**Leitura:**
- [Speak Freely & Never Mind the Pesky Trackers: Privacy Analysis of Popular Therapy Apps (2026)](https://arxiv.org/html/2605.02016v2)
- [Security Analysis of Top-Ranked mHealth Fitness Apps: An Empirical Study](https://arxiv.org/pdf/2409.18528)
- [Third Party Tracking in the Mobile Ecosystem](https://arxiv.org/html/1804.03603v1)
- [Betrayed by the Guardian: Security and Privacy Risks of Parental Control Solutions](https://arxiv.org/pdf/2012.06502)

---

## N4 — Automatizar o método de atribuição de hacktivismo do próprio orientador

**Título provisório (EN):** *From Framework to Pipeline: Operationalizing and Validating a
Method to Distinguish False-Flag Operations from Genuine Hacktivism*

### Problema de pesquisa

**Enunciado.** É possível operacionalizar computacionalmente o método analítico de
distinção entre operações de bandeira falsa e hacktivismo genuíno, e qual a concordância
entre a classificação automatizada e a classificação manual de especialista?

**Lacuna.** O método existe como **framework analítico manual** — publicado pelo próprio
orientador na *Revista Brasileira de Estudos de Defesa* em 2025 (*Is There Real Hacktivism?
A Method To Distinguish False-Flag Operations From Genuine Hacktivists*). Transformá-lo em
pipeline reprodutível e medir sua confiabilidade é trabalho inédito.

**Por que importa.** Atribuição é o problema mais difícil e mais consequente da segurança
cibernética internacional. Um método manual não escala; um método automatizado e validado,
sim.

### Objetivo geral

**Demonstrar** a viabilidade de operacionalizar computacionalmente o método de distinção
entre bandeira falsa e hacktivismo genuíno, e **medir** a concordância entre a
classificação automatizada e a de especialista humano sobre um corpus de operações
reivindicadas.

### Hipótese

A operacionalização automatizada alcança concordância substancial com a classificação
manual (κ > 0,6) nos indicadores de natureza estrutural — cadência temporal, reuso de
infraestrutura, padrão linguístico —, mas concordância baixa nos indicadores que dependem
de contexto geopolítico, delimitando com precisão **quais partes do método podem ser
automatizadas e quais exigem analista humano**.

### Método e dados

Corpus de reivindicações públicas de operações (canais públicos, agregadores de incidentes,
rastreadores abertos). Extração de indicadores: temporais, linguísticos (NLP), de
infraestrutura. Classificação. Comparação com rotulagem manual — **e aqui há uma vantagem
rara: o especialista de referência é o seu próprio orientador**.

### Ética

Trabalha-se com **metadados de reivindicação** — quem reivindicou, quando, contra quem.
**Nunca** com o conteúdo de dados vazados de vítimas. Esse limite é absoluto e vai escrito.

### Encaixe com o orientador

**O máximo possível: é a extensão direta do trabalho dele.** Orientadores costumam se
engajar muito mais quando o TCC avança a própria agenda de pesquisa — e aqui existe
caminho natural para publicação conjunta.

### Riscos

**O mais alto desta lista.** Coleta de dados em fontes de hacktivismo é ruidosa e exige
cuidado ético e jurídico. Rotulagem de referência limitada. Se a concordância der baixa em
tudo, o resultado ainda é publicável (delimita os limites da automação), mas é preciso
aceitar essa possibilidade desde o início.

### Maturidade

Nível 3–4, com componente exploratório.

---

## N5 — Ransomware no Brasil (com ressalva)

Caracterização de vítimas brasileiras a partir de dados públicos de *leak sites*.

**A ressalva, e ela é séria:** um trabalho de 2026 já fez a caracterização com **27.000
posts de 325 grupos**, cobrindo concentração do ecossistema, rotinas temporais e
regularidades de seleção de alvo **por geografia e por setor**. O eixo de alinhamento
Estado–cibercrime também já foi publicado. A contribuição marginal de um recorte brasileiro
ficou fina.

Só vale se houver um ângulo que a literatura não cobre — por exemplo, cruzar as vítimas
brasileiras com dados de porte e setor da Receita/IBGE para testar se a seleção de alvo
segue capacidade de pagamento. **Não é minha recomendação**, mas fica registrado.

**Leitura:**
- [Analyzing Concentration, Temporal Routines and Targeting in Public Ransomware Leak Site Data (2026)](https://arxiv.org/abs/2605.24559)
- [Informal allies: State–cybercriminal alignment in the ransomware ecosystem (Journal of Cybersecurity)](https://academic.oup.com/cybersecurity/article/11/1/tyaf037/8340911)

---

## Comparação com os temas anteriores

| Tema | Técnico? | Risco de execução | Encaixe com o orientador | Ineditismo |
|---|---|---|---|---|
| **N1** — ICS exposta | alto | médio (depende de acesso Shodan) | **máximo** | alto |
| **N2** — Postura de domínios gov | médio | **muito baixo** | **máximo** | alto |
| **N3** — Apps móveis gov | **alto** | baixo | bom | alto |
| **N4** — Atribuição de hacktivismo | alto | **alto** | **máximo** | alto |
| N5 — Ransomware BR | médio | baixo | bom | **baixo** |
| T3 — LGPD e saúde | baixo | muito baixo | ótimo | alto |
| T1 — Código de LLM | alto | médio | **ruim** | alto |

### Recomendação

**N3 é o melhor equilíbrio.** É o mais **técnico** dos temas que este orientador consegue
orientar — análise estática, engenharia reversa leve, interceptação de tráfego, estatística
—, tem grupo de controle embutido, risco de execução baixo e duas camadas de relevância
(LGPD e soberania de dados). Se a sua insatisfação com o T3 era ele ser "pouco computação",
o N3 resolve isso mantendo o mesmo orientador.

**N1 é o de maior afinidade com o orientador** e o mais alinhado com a experiência
profissional dele. Faça o pedido de acesso acadêmico ao Shodan **esta semana** — é o teste
de viabilidade que decide.

**N2 é o mais seguro** e o que tem maior chance de virar publicação conjunta, por ser
literalmente a pergunta de pesquisa dele com método empírico. Cuidado com a rasura: a
coleta é fácil demais, e a profundidade precisa vir do eixo longitudinal.

**N4 é o mais empolgante e o mais arriscado.** Se você conversar com ele e houver entusiasmo
mútuo, é o que tem maior teto — mas leve o N1 ou o N3 como alternativa na mesma conversa.
