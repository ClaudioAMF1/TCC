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

> **Atualização de 20/08/2026 — o ranking mudou.** O acesso acadêmico ao Shodan foi
> aprovado. Esse era o único portão do tema de infraestrutura crítica, que passa a **1º
> lugar**. Os apps móveis governamentais caem para 2º. Justificativa na seção de cada tema.

## 🥇 1º — Superfície de ataque exposta da infraestrutura crítica brasileira

**EN:** *Exposed by Default: Measuring Internet-Facing Industrial Control Systems in
Brazilian Critical Infrastructure*

**Objetivo.** **Medir e caracterizar** a exposição de sistemas de controle industrial
atribuíveis à infraestrutura crítica brasileira, **comparando** a distribuição setorial com
as linhas de base publicadas para outros países.

**Hipótese central.** A exposição concentra-se desproporcionalmente em setores sob menor
supervisão regulatória (saneamento, automação predial) frente aos fortemente regulados
(energia elétrica, financeiro); e a proporção de dispositivos com vulnerabilidade conhecida
é significativamente maior que nas linhas de base europeias publicadas.

**Por que subiu para primeiro.** Estava em segundo unicamente pelo risco de acesso aos
dados. Com o acesso acadêmico aprovado, sobram só as vantagens:

- **Maior afinidade com o orientador de toda a lista.** Proteção de infraestrutura crítica
  foi o trabalho dele por 15 anos no GSI/PR e é tema de publicações dele na ECCWS 2019 e
  ICCWS 2021. A Aula 05/06 estabelece compatibilidade com o orientador como critério.
- **Menor risco científico.** Método revisado por pares e replicado em três países
  (Países Baixos, Itália, Hong Kong) mais o EuroS&P 2025, com o Brasil ainda não estudado.
  Você replica um desenho validado numa população inédita.
- **Resultado mais impactante numa defesa.** "Esta é a linha de base da infraestrutura
  crítica brasileira exposta na internet" é uma frase que a banca não esquece.
- **Tem substância técnica real**, ao contrário do que "só consultar uma base" sugere: o
  pipeline de atribuição IP→ASN→organização→setor e a **filtragem de honeypots** são
  problemas de classificação com literatura própria.

**Pitch de 30 segundos.** *"Existem estudos medindo quantos sistemas de controle industrial
estão expostos na internet na Holanda, na Itália e em Hong Kong. Não existe nenhum para o
Brasil. Quero produzir essa linha de base, quebrada por setor, e comparar com os números
europeus — usando apenas bases de varredura de terceiros, sem tocar em nada."*

**Limite ético inegociável.** Nenhuma varredura ativa, nenhuma conexão, nenhuma tentativa
de autenticação. Resultados agregados por setor, jamais identificando o operador. Achado
crítico e atribuível → notificar o CTIR Gov antes de publicar.

**Riscos que restam.** A atribuição IP→setor é imprecisa e exige validação manual
documentada — é o trabalho braçal deste tema, o análogo da rotulagem manual do T1. E os
créditos de consulta são finitos: veja a seção de coleta abaixo.

### Primeiros passos concretos com o acesso já aprovado

1. **Não gaste créditos contando.** O endpoint `/shodan/host/count` retorna o total de
   resultados **sem consumir crédito de consulta** — é feito exatamente para levantamento
   de viabilidade. Confirme na documentação e use-o para todo o dimensionamento inicial.
2. **Levante o N do corpus** com consultas de contagem por protocolo industrial:

   | Protocolo | Consulta |
   |---|---|
   | Genérico ICS | `country:BR tag:ics` |
   | Modbus | `country:BR port:502` |
   | S7comm (Siemens) | `country:BR port:102` |
   | DNP3 | `country:BR port:20000` |
   | BACnet (automação predial) | `country:BR port:47808` |
   | EtherNet/IP | `country:BR port:44818` |
   | IEC 60870-5-104 | `country:BR port:2404` |
   | Niagara Fox | `country:BR port:1911,4911` |

3. **Salve o JSON bruto de tudo, sempre.** Os resultados mudam com o tempo e os créditos não
   voltam. Consultou uma vez, guardou para sempre — e registre a data de cada coleta, que
   vira dado de reprodutibilidade.
4. **Verifique sua cota real** no Developer Dashboard antes de desenhar a coleta completa.
   O desenho amostral tem que caber na cota, não o contrário.
5. **Nunca versione a API key.** Ela vai em variável de ambiente ou arquivo local
   ignorado pelo git — jamais dentro do repositório do TCC.

---

## 🥈 2º — Rastreadores e soberania de dados em aplicativos móveis governamentais

**EN:** *Who Else Is in the App? Third-Party Tracking and Data Sovereignty in Brazilian
Government Mobile Applications*

**Objetivo.** **Medir** a prevalência de SDKs de rastreamento de terceiros e de falhas de
segurança em aplicativos móveis governamentais brasileiros, e **comparar** seu
comportamento com o de aplicativos comerciais pareados.

**Hipótese central.** Aplicativos governamentais embarcam rastreadores em proporção
**estatisticamente indistinguível** da de aplicativos comerciais equivalentes, apesar de
submetidos a regime jurídico distinto — e parte relevante desses SDKs não está declarada na
política de privacidade.

**Por que é o segundo.** Continua sendo **o mais técnico da lista** — análise estática,
engenharia reversa leve, interceptação de tráfego, estatística — e o único com grupo de
controle embutido, o que o coloca direto no nível 4 de maturidade. O método está validado
em muitos domínios (apps de terapia, saúde mental, fitness, controle parental) e **nunca foi
aplicado ao parque governamental brasileiro**. Carrega duas camadas de relevância — LGPD e
soberania de dados —, sendo a segunda exatamente o que o orientador publica sobre poder
cibernético e Sul Global.

Perdeu o primeiro lugar apenas porque a afinidade do 1º com a trajetória profissional do
orientador é maior, e porque o 1º replica um desenho já revisado por pares. Se o corpus de
aplicativos vier grande e o de ICS vier pequeno, os dois trocam de lugar de novo — decida
pelos números dos testes de viabilidade, não por esta ordem.

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
| ~~1~~ | ~~Solicitar acesso acadêmico ao Shodan~~ | ✅ **aprovado em 20/08/2026** |
| 1 | Rodar as consultas de contagem da tabela do 1º lugar e anotar o N por protocolo | o tamanho real do corpus de ICS |
| 2 | Verificar a cota de créditos no Developer Dashboard | se a coleta completa cabe |
| 3 | Contar os apps governamentais e baixar uma dúzia de APKs | se o 2º se sustenta |
| 4 | Ler 2–3 artigos de cada tema | qual deles te prende |

**O número que decide tudo:** se as consultas de contagem devolverem alguns milhares de
dispositivos, o 1º lugar está confirmado e você já tem material de conversa para 25/08.
Se devolverem algumas centenas, a análise setorial fica frágil e o 2º lugar reassume.

Leve o número, seja ele qual for, para a conversa com o orientador. Chegar dizendo *"rodei
as consultas, o Brasil tem N dispositivos industriais expostos, e não existe estudo disso"*
é uma abertura completamente diferente de chegar com uma ideia.

O critério de leitura não é "entendi tudo". É **"fiquei com vontade de ver o resultado"**.
