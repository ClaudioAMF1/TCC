# Top 3 — Versão Final

Decisão consolidada após checagem de literatura de todos os temas considerados, do
currículo do orientador e das regras metodológicas das Aulas 04 a 06.

**Este documento substitui os rankings dos arquivos anteriores.**

Critérios aplicados, nesta ordem de peso:

1. **Orientável pelo Prof. Izycki** — a Aula 05/06 diz que o tema deve ser compatível com
   os conhecimentos do orientador. É critério da disciplina, não preferência.
2. **Ineditismo verificado** — todos passaram por busca de literatura; nenhum repete o erro
   do T4, cuja pergunta já estava respondida.
3. **Suficientemente técnico** — computação de verdade, não só medição descritiva.
4. **Executável sozinho até dezembro de 2027**, com o hardware disponível e custo próximo
   de zero.
5. **Maturidade nível 3–4** na escala da Aula 04 — comparação com métrica objetiva.

---

## 🥇 1º — Rastreadores e soberania de dados em aplicativos móveis governamentais

**EN:** *Who Else Is in the App? Third-Party Tracking and Data Sovereignty in Brazilian
Government Mobile Applications*

**Objetivo.** **Medir** a prevalência de SDKs de rastreamento de terceiros e de falhas de
segurança em aplicativos móveis governamentais brasileiros, e **comparar** seu
comportamento com o de aplicativos comerciais pareados.

**Hipótese central.** Aplicativos governamentais embarcam rastreadores em proporção
**estatisticamente indistinguível** da de aplicativos comerciais equivalentes, apesar de
submetidos a regime jurídico distinto — e parte relevante desses SDKs não está declarada na
política de privacidade.

**Por que é o primeiro.** É o mais técnico entre os temas que este orientador consegue
orientar: análise estática, engenharia reversa leve, interceptação de tráfego, estatística.
Tem grupo de controle embutido, o que o coloca direto no nível 4 de maturidade. O método
está validado em muitos domínios (apps de terapia, saúde mental, fitness, controle
parental) e **nunca foi aplicado ao parque governamental brasileiro**. E carrega duas
camadas de relevância — LGPD e soberania de dados —, sendo a segunda exatamente o que o
orientador publica sobre poder cibernético e Sul Global.

**Pitch de 30 segundos.** *"Quero medir quantos rastreadores de terceiros existem dentro dos
aplicativos oficiais do governo brasileiro, inclusive os que lidam com dado de saúde e
previdência, e para onde esses dados vão. Comparo com aplicativos comerciais de porte
parecido para saber se o regime jurídico diferente produz comportamento diferente. A
hipótese é que não produz."*

**Risco decisivo.** *Certificate pinning* impede interceptação em parte dos apps. Isso
**limita** a análise dinâmica a uma subamostra — não inviabiliza o trabalho, porque a
análise estática cobre a hipótese principal. Reporte como limitação declarada.

**Teste de viabilidade desta semana.** Contar quantos aplicativos governamentais oficiais
existem de fato (federais, estaduais, municipais) e conseguir baixar os APKs de uma dúzia.
Se passar de ~60 apps, o tema está de pé.

---

## 🥈 2º — Superfície de ataque exposta da infraestrutura crítica brasileira

**EN:** *Exposed by Default: Measuring Internet-Facing Industrial Control Systems in
Brazilian Critical Infrastructure*

**Objetivo.** **Medir e caracterizar** a exposição de sistemas de controle industrial
atribuíveis à infraestrutura crítica brasileira, **comparando** a distribuição setorial com
as linhas de base publicadas para outros países.

**Hipótese central.** A exposição concentra-se desproporcionalmente em setores sob menor
supervisão regulatória (saneamento, automação predial) frente aos fortemente regulados
(energia elétrica, financeiro); e a proporção de dispositivos com vulnerabilidade conhecida
é significativamente maior que nas linhas de base europeias publicadas.

**Por que é o segundo.** **A maior afinidade com o orientador de toda a lista** — proteção
de infraestrutura crítica foi o trabalho dele por 15 anos no GSI/PR e é tema de publicações
dele na ECCWS 2019 e ICCWS 2021. Existem estudos nacionais publicados para Países Baixos,
Itália e Hong Kong, mais um paper no EuroS&P 2025, e **nenhum para o Brasil**: método
validado por pares, população inédita. É também o de resultado mais impactante numa defesa.

**Pitch de 30 segundos.** *"Existem estudos medindo quantos sistemas de controle industrial
estão expostos na internet na Holanda, na Itália e em Hong Kong. Não existe nenhum para o
Brasil. Quero produzir essa linha de base, quebrada por setor, e comparar com os números
europeus — usando apenas bases de varredura de terceiros, sem tocar em nada."*

**Risco decisivo.** Depende de **acesso acadêmico ao Shodan ou Censys**. Sem isso, o tema
não existe.

**Limite ético inegociável.** Nenhuma varredura ativa, nenhuma conexão, nenhuma tentativa
de autenticação. Resultados agregados por setor, jamais identificando o operador. Achado
crítico e atribuível → notificar o CTIR Gov antes de publicar.

**Teste de viabilidade desta semana.** Solicitar o acesso acadêmico. É literalmente o que
decide se este tema entra ou sai.

---

## 🥉 3º — Postura técnica dos domínios governamentais versus a política nacional

**EN:** *Declaratory or Effective? Measuring the Technical Security Posture of Brazilian
Government Domains Against National Cyber Strategy Commitments*

**Objetivo.** **Medir** a postura técnica de segurança dos domínios governamentais
brasileiros (SPF/DKIM/DMARC, DNSSEC, TLS, RPKI) e **demonstrar** em que grau ela diverge
dos compromissos declarados nos instrumentos nacionais de política de segurança cibernética.

**Hipóteses.** Desigualdade federativa (federal ≫ estadual ≫ municipal); **adoção declarada
superestima proteção real**, porque a maioria dos domínios com DMARC permanece em `p=none`,
que não protege contra nada; e ausência de inflexão mensurável após a publicação dos
instrumentos de política — o que os caracterizaria como declaratórios.

**Por que é o terceiro.** É **a pergunta de pesquisa do orientador com um método empírico
que você traz** — estratégias nacionais de segurança cibernética são o núcleo da produção
dele, incluindo a tese em andamento. É o candidato mais provável a publicação conjunta, e o
de menor risco de execução da lista inteira: consulta DNS é rápida, gratuita e não invasiva.

Fica em terceiro por ser o menos impressionante tecnicamente, e por um risco invertido: **a
coleta é fácil demais.** Sem o eixo longitudinal e a análise federativa, vira relatório
técnico raso em vez de pesquisa.

**Pitch de 30 segundos.** *"O Brasil publicou instrumentos de política de segurança
cibernética com compromissos técnicos. Quero medir se isso apareceu na realidade: quantos
domínios do governo têm autenticação de e-mail funcionando de verdade, quantos só têm no
papel, e se houve alguma inflexão depois da publicação da política. A hipótese é que os
instrumentos são declaratórios."*

**Teste de viabilidade desta semana.** Nenhum — este tema não tem porta de entrada. Roda
sempre. É por isso que ele é a rede de segurança.

---

## Como usar isto em 25/08

Leve os três, **nesta ordem**, e diga que são três. Chegar com um leque checado contra a
literatura muda o tom da conversa: você deixa de ser alguém pedindo um tema e passa a ser
alguém escolhendo um.

Se ele demonstrar entusiasmo por um em particular, **vá com o dele** — engajamento do
orientador vale mais do que a diferença entre o 1º e o 3º desta lista.

Há um quarto tema que não entrou no ranking por risco alto demais, mas que vale mencionar
por último, como ideia: **operacionalizar computacionalmente o método de atribuição de
hacktivismo que ele mesmo publicou em 2025**, medindo a concordância entre a classificação
automatizada e a de especialista. É o de maior teto e o de maior engajamento possível — se
ele se empolgar, você descobre na hora, e ainda tem três alternativas sólidas na mesa.

## Ordem das ações nesta semana

| Prioridade | Ação | Decide |
|---|---|---|
| 1 | Solicitar acesso acadêmico ao Shodan/Censys | se o N1 existe |
| 2 | Contar os apps governamentais e baixar uma dúzia de APKs | se o N3 se sustenta |
| 3 | Rodar consulta DNS num punhado de domínios `.gov.br` | nada — só confirma que o N2 é trivial de começar |
| 4 | Ler 2–3 artigos de cada tema | qual deles te prende |

O critério de leitura não é "entendi tudo". É **"fiquei com vontade de ver o resultado"**.
