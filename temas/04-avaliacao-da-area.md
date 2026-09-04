# Cibersegurança como área de TCC — avaliação honesta e temas de baixo custo de tempo

Documento escrito em resposta a três perguntas diretas: cibersegurança é difícil? é
arriscada? é interessante para TCC? E, se for, quais temas são fortes **sem** exigir
dedicação integral.

Incorpora o conteúdo das Aulas 07 e 08 (Revisão Bibliográfica), que muda duas coisas ditas
nos documentos anteriores.

---

## Parte 1 — As três perguntas

### "Cibersegurança é muito difícil?"

**A pergunta está mal formulada, e essa é a resposta mais útil que eu tenho.**
Cibersegurança não é uma área com um nível de dificuldade. São duas áreas muito diferentes
compartilhando um nome:

| Metade | O que é | Dificuldade real |
|---|---|---|
| **Ofensiva / sistemas** | desenvolvimento de exploits, fuzzing, engenharia reversa, criptanálise, segurança de kernel | **Genuinamente difícil.** Exige pré-requisitos profundos que levam anos. Alto risco de não terminar um TCC. |
| **Empírica / medição** | medir, minerar, caracterizar, comparar — é o que todos os temas propostos aqui fazem | **Não é difícil.** É engenharia de dados e estatística com enquadramento de segurança. |

A metade empírica é, honestamente, **um dos lugares mais fáceis de toda a computação para
fazer um TCC sólido**. O motivo é estrutural: os dados já existem, são públicos e
gratuitos; as métricas já estão definidas; as ferramentas são maduras e abertas. Você gasta
o tempo pensando, não construindo infraestrutura.

Se a sua imagem de "cibersegurança" era a primeira coluna, ela explica o receio — e o
receio está correto sobre aquela coluna. Só que não é lá que o seu TCC vai acontecer.

### "É arriscada?"

Aqui existe um risco **real e específico da área**, que outras áreas da computação não têm,
e seria desonesto minimizá-lo:

**Risco jurídico.** A Lei 12.737/2012 tipifica invasão de dispositivo informático. Qualquer
tema que envolva teste ativo contra sistema de terceiros sem autorização formal por escrito
é crime — não "é antiético", é crime. Isso elimina de saída toda uma família de temas
(pentest, varredura ativa, exploração de falha em alvo real).

**A mitigação é simples e é a que todos os temas aqui adotam:** ficar do lado
**observacional**. Consultar bases coletadas por terceiros, analisar artefatos públicos,
medir passivamente o que o próprio sistema entrega a qualquer visitante. Nenhum dos temas
propostos toca em sistema alheio.

Os outros riscos são menores e gerenciáveis:

- **Ritmo da literatura** — varia muito por subárea. Segurança de IA muda toda semana;
  medição de infraestrutura muda devagar. Escolher a segunda reduz o risco.
- **Acesso a dados** — alguns temas dependem de API ou base que você pode não conseguir.
  Resolve-se testando o acesso **antes** de fechar o tema, não depois.
- **Divulgação responsável** — se você achar algo grave e atribuível, há um procedimento a
  seguir. Não é obstáculo; é uma seção do texto.

**Comparado a outras áreas, o risco é baixo.** Um TCC de IHC precisa de comitê de ética e
recrutamento de pessoas. Um de aprendizado de máquina profundo precisa de GPU e semanas de
treino. Medição em segurança precisa de um notebook e disciplina.

### "É uma área interessante para TCC?"

Sim, e por razões concretas — não por ser um assunto que soa bem:

1. **Dados públicos em abundância.** NVD, EPSS, KEV, Certificate Transparency, Shodan
   acadêmico, OSV, PhishTank. Tudo gratuito, tudo estruturado.
2. **Métricas já estabelecidas.** Você não precisa inventar como medir — logo, consegue
   hipótese falsificável sem esforço criativo extra.
3. **Resultados legíveis.** Um achado de segurança é compreensível pela banca inteira em
   segundos. Isso vale muito no dia da defesa.
4. **Veículos ativos no Brasil.** SBSeg, SBRC, e a SBC publica minicursos gratuitos.

**E agora a parte que ninguém diz.** Cibersegurança é uma área **saturada de TCC ruim** —
"desenvolvi um IDS", "criei um sistema de detecção de phishing", sem baseline e sem
métrica. Isso tem uma consequência de mão dupla: a barra para *parecer* bom é baixa, mas a
barra para *ser* bom exige exatamente a disciplina de estado da arte que fizemos nos
documentos anteriores. Sem ela, você vira mais um.

**Veredito:** sim, vá para cibersegurança — mas o que decide a qualidade do seu TCC não é a
área, é a subárea e o desenho. Medição empírica em segurança é uma escolha acertada para
quem tem tempo limitado.

---

## Parte 2 — Duas correções vindas das Aulas 07 e 08

### Correção 1: "não existe estudo disso no Brasil" não basta como justificativa

A Aula 07 é explícita: **"Evite o fundamento vazio! Não se deve fundamentar todo um
trabalho de pesquisa em uma negação. Deve-se mostrar o que outros fizeram e depois mostrar
que o trabalho feito é diferente ou melhor."**

Vários temas dos documentos anteriores foram apresentados apoiados justamente numa negação
("ninguém mediu isso para o Brasil"). **Isso é insuficiente como justificativa central.**
Cada tema precisa de um argumento positivo: o que o resultado permite concluir, decidir ou
mudar — independentemente de ser inédito.

Onde isso aparece nos temas abaixo, o argumento positivo está escrito explicitamente.

### Correção 2: tema interdisciplinar custa três revisões, não uma

Também da Aula 07: quando se aplica uma técnica de Computação a outra área, é preciso
revisar **a técnica em si, a área de aplicação, e as aplicações já tentadas**.

Isso é um custo de tempo direto, e é decisivo para quem está ocupado. Temas
interdisciplinares — direito e tecnologia, infraestrutura crítica, saúde — exigem
literalmente o triplo de leitura. Temas monodisciplinares são muito mais baratos.

**Isso reordena tudo, e por um motivo legítimo: você me deu uma restrição nova.**

---

## Parte 3 — Os temas reordenados por custo de tempo

| Tema | Coleta de dados | Trabalho manual | Revisão | **Custo total** |
|---|---|---|---|---|
| **L1 — Falhas da priorização de vulnerabilidades** | download direto | nenhum | mono | 🟢 **muito baixo** |
| **N2 — Postura técnica de domínios gov** | consulta DNS | nenhum | inter (política) | 🟢 baixo |
| **L2 — Abuso de marca via Certificate Transparency** | consulta a CT | rotulagem pequena | mono | 🟢 baixo |
| N1 — ICS exposta | Shodan | atribuição IP→setor | inter (infra crítica) | 🟡 médio-alto |
| N3 — Apps móveis gov | coleta de APKs | política × SDK | inter (LGPD) | 🟡 médio-alto |
| T3 — LGPD e saúde | crawler | classificação semântica | inter (direito) | 🔴 alto |

O N1 continua sendo excelente e o acesso ao Shodan já está aprovado. Mas a atribuição
IP→organização→setor é trabalho manual repetitivo, e o tema exige aprender infraestrutura
crítica além de segurança. **Para quem está ocupado, ele não é a melhor escolha** — e isso
é uma reavaliação honesta, não uma mudança de opinião sobre a qualidade do tema.

---

## L1 — Onde a priorização de vulnerabilidades falha 🟢

**EN:** *When Prioritization Fails: Characterizing the Vulnerabilities That Exploit
Prediction Misses at the Moment They Become Known-Exploited*

### O problema

Toda equipe de segurança enfrenta o mesmo dilema: milhares de vulnerabilidades, capacidade
de corrigir dezenas. A indústria hoje usa três sinais em camadas — **CVSS** (gravidade),
**EPSS** (probabilidade de exploração nos próximos 30 dias) e **KEV** (catálogo da CISA de
vulnerabilidades comprovadamente exploradas).

Está estabelecido que o EPSS supera o CVSS na priorização. Mas há um achado incômodo na
literatura: **os escores de EPSS são frequentemente baixos ou inexistentes justamente
quando a vulnerabilidade entra no KEV** — ou seja, o melhor preditor disponível falha
exatamente no momento em que acertar mais importa.

### A pergunta (e o argumento positivo, não a negação)

Ninguém caracterizou **a população de falhas**. Para quais classes de software, fornecedores,
tipos de CWE ou faixas de idade o EPSS erra sistematicamente? Se existir padrão, ele é
**acionável**: uma equipe de segurança pode saber em que categorias não confiar no escore e
aplicar julgamento humano.

Isso é o argumento positivo que a Aula 07 exige: o resultado **muda uma decisão
operacional**, seja ele inédito ou não.

### Objetivo

**Caracterizar** o subconjunto de vulnerabilidades em que a predição de exploração falha no
momento da inclusão no catálogo de exploração conhecida, e **demonstrar** se essas falhas
se concentram em classes identificáveis a priori.

### Hipótese

As falhas de predição não são aleatórias: concentram-se em vulnerabilidades de fornecedores
com baixa cobertura de inteligência pública, em classes de CWE sub-representadas nos dados
de treino do modelo, e em CVEs recém-publicados — de modo que **é possível prever onde o
preditor vai falhar**.

### Por que o custo de tempo é o menor de todos

- **Coleta:** baixar arquivos. Os feeds do NVD são JSON público; o EPSS publica CSV diário
  gratuito; o KEV é um JSON da CISA. **Zero crawling, zero API key, zero rate limit.**
- **Trabalho manual:** nenhum. Não há rotulagem.
- **Revisão bibliográfica:** monodisciplinar — só gestão de vulnerabilidades.
- **Ferramenta:** pandas e scikit-learn. Roda em minutos.

O trabalho todo é **pensar e analisar**, que é exatamente onde você quer gastar tempo
limitado.

### Encaixe com o orientador

Bom, sem ser exclusivo dele: **avaliação e priorização de risco foi literalmente a função
dele por 15 anos no GSI/PR** (análise de risco de infraestruturas críticas e de grandes
eventos). Ele entende o problema de priorização por dentro, na prática.

### Riscos

O tema é tão barato de executar que corre risco de ficar raso. **A profundidade tem que
vir da análise** — modelagem estatística séria das falhas, análise temporal, e não apenas
tabelas descritivas.

### Leitura
- [Exploit Prediction Scoring System (EPSS) — artigo original](https://arxiv.org/pdf/1908.04856)
- [Vulnerability Management Chaining: An Integrated Framework for Efficient Cybersecurity Risk Prioritization (2025)](https://arxiv.org/pdf/2506.01220)
- [Comparing CVSS, EPSS, KEV, SSVC, LEV and PXS](https://www.picussecurity.com/resource/blog/comparing-cvss-epss-kev-ssvc-lev-and-pxs-from-scores-to-security-proof)
- Documentação oficial do [EPSS (FIRST)](https://www.first.org/epss/) e do [catálogo KEV (CISA)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### Estudo recomendado
- **Especificação do CVSS v3.1 e v4.0** (FIRST, gratuito) — leitura de uma tarde, e é a
  base conceitual do tema inteiro.
- **Documentação e artigo do EPSS** (FIRST) — entender como o modelo é treinado é o que
  permite hipotetizar onde ele falha.
- **StatQuest** (YouTube, gratuito) — para calibração, ROC, precisão/revocação. É o mínimo
  estatístico que este tema exige e é explicado de forma acessível.
- **Kitchenham & Charters (2007)** — o protocolo de revisão sistemática que a Aula 07 cita
  diretamente. Você vai precisar dele de qualquer forma.

---

## L2 — Abuso de marca brasileira detectado por Certificate Transparency 🟢

**EN:** *The Detection Gap: Measuring the Window Between Certificate Issuance and Blocklist
Coverage for Phishing Domains Targeting Brazilian Brands*

### O problema

Todo certificado TLS emitido é registrado publicamente em logs de **Certificate
Transparency**. Quando alguém registra um domínio para se passar por um banco ou por um
serviço público e emite um certificado, isso vira **registro público em segundos** — muitas
vezes **antes** de o site de phishing entrar no ar.

A classificação de phishing a partir de CT já foi pesquisada. O que não foi medido é a
**lacuna de detecção**: quanto tempo passa entre o certificado aparecer no log e o domínio
ser efetivamente bloqueado pelas listas de proteção que os navegadores usam.

### O argumento positivo

Se a lacuna for de horas, o ecossistema de defesa funciona. Se for de dias, **existe uma
janela mensurável em que a vítima está desprotegida e o sinal já estava público** — e isso
é uma recomendação operacional concreta, não uma curiosidade.

### Objetivo

**Medir** o intervalo entre a emissão de certificado para domínios que imitam marcas
brasileiras e sua inclusão em listas de bloqueio, e **comparar** essa lacuna entre setores
(bancos, governo, comércio).

### Hipótese

A lacuna mediana de detecção excede 24 horas e é significativamente maior para marcas
governamentais do que para marcas bancárias, refletindo a assimetria de investimento em
monitoramento de marca entre os dois setores.

### Custo de tempo: baixo

Consulta a logs de CT (crt.sh e similares são gratuitos), geração de variantes por
distância de edição sobre uma lista de marcas-alvo, verificação periódica contra listas de
bloqueio públicas. Rotulagem manual pequena, apenas para validar a classificação de
"imitação de marca". Monodisciplinar.

### Riscos

Precisa de **coleta contínua ao longo de semanas** — não dá para fazer tudo numa tarde,
porque a variável dependente é temporal. Comece cedo, deixe rodando. Isso é compatível com
agenda ocupada (o script trabalha sozinho), mas exige começar já.

### Leitura
- [Finding Phish in a Haystack: A Pipeline for Phishing Classification on Certificate Transparency Logs](https://arxiv.org/pdf/2106.12343)
- Documentação do [Certificate Transparency](https://certificate.transparency.dev/)
- [Detecting Phishing Domains with Certificate Transparency](https://inventivehq.com/blog/detecting-phishing-domains-with-certificate-transparency)

### Estudo recomendado
- **RFC 6962** (Certificate Transparency) — a fonte primária, e não é longa.
- **Curso gratuito de PKI/TLS** — a série do Cloudflare Learning Center sobre TLS e
  certificados cobre o necessário em poucas horas.

---

## Plano de estudo transversal (serve para qualquer tema escolhido)

O que compensa estudar independentemente do tema, em ordem de retorno sobre tempo
investido:

| Prioridade | Recurso | Por quê |
|---|---|---|
| 1 | **Kitchenham & Charters (2007)**, *Guidelines for performing Systematic Literature Reviews in Software Engineering* | É o protocolo que a Aula 07 cita e que a disciplina vai cobrar. Gratuito. |
| 2 | **Wazlawick**, *Metodologia de Pesquisa para Ciência da Computação* | Bibliografia básica da disciplina; a base de todas as aulas 03–08. |
| 3 | **StatQuest** (YouTube) | Estatística aplicada explicada de forma acessível: testes de hipótese, regressão, ROC, calibração. É o que todos os temas exigem. |
| 4 | **MIT 6.858 — Computer Systems Security** (OCW, gratuito, aulas em vídeo) | Base conceitual sólida de segurança, útil na arguição da banca mesmo que não seja o seu tema. |
| 5 | **Minicursos do SBSeg** (SBC, gratuitos, em português) | Panorama do que se pesquisa em segurança no Brasil — e ajuda a identificar veículo de publicação. |
| 6 | **Zotero** + **Overleaf** | Ferramenta, não conteúdo. Começar a revisão sem gerenciador de referências é retrabalho garantido. |

Por tema específico:

- **L1** → especificação CVSS (FIRST), documentação EPSS, catálogo KEV
- **L2** → RFC 6962, fundamentos de TLS/PKI
- **N1** → documentação do Shodan, materiais gratuitos de segurança de ICS/OT
- **N2** → RFC 7489 (DMARC), boas práticas M3AAWG
- **N3** → **OWASP MASTG** (Mobile Application Security Testing Guide) — gratuito e excelente

---

## Recomendação final para quem tem tempo limitado

**L1 é a escolha.** Menor custo de tempo de toda a lista, monodisciplinar, dados que se
baixam em vez de se coletar, nenhuma rotulagem manual, ferramenta trivial, e uma pergunta
com consequência operacional real. O orientador conhece o problema por experiência
profissional direta.

**N2 é a segunda**, e continua sendo a mais provável de virar publicação conjunta.

**N1 fica como terceira** — tema excelente, acesso já aprovado, mas com custo de trabalho
manual que não combina com agenda apertada. Se em algum momento o tempo abrir, ele volta
para o topo.

Leve **L1, N2 e N1** para a conversa de 25/08, nessa ordem, e seja honesto com o orientador
sobre a sua disponibilidade. Orientador que sabe da sua restrição de tempo ajuda a calibrar
o escopo; orientador que não sabe cobra o escopo errado em novembro.
