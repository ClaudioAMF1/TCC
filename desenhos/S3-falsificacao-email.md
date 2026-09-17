# S3 — Falsificação de e-mail em domínios públicos brasileiros

**Estado:** 🟡 **finalista.** Viabilidade verificada em 17/09/2026. A hipótese que eu
havia proposto como eixo principal **não sobreviveu ao teste** — mas três achados
sobreviveram, e dois são fortes.

**Script:** `scripts/teste_viabilidade_s3.py` · **Custo:** 60 segundos, sem chave de API

---

## 1. A pergunta

> **Os domínios públicos brasileiros estão configurados para impedir que alguém
> falsifique e-mails em nome deles?**

E-mail funciona como carta com remetente escrito à mão: qualquer um pode escrever
"Receita Federal" no campo do remetente, e o protocolo original não verifica nada.
Três proteções precisam ser ligadas pelo dono do domínio:

| | O que faz | Se faltar |
|---|---|---|
| **SPF** | publica quais servidores podem enviar em nome do domínio | qualquer servidor pode alegar ser o `gov.br` |
| **DKIM** | assinatura criptográfica da mensagem | adulteração no caminho não é detectável |
| **DMARC** | instrui o destinatário sobre o que fazer quando a checagem falha | ninguém disse o que fazer, então a mensagem passa |

O DMARC é a variável dependente do trabalho, e é boa justamente por **não ser
binária**: tem três níveis ordenados — `none` (entrega e avisa) < `quarantine`
(manda para o spam) < `reject` (recusa).

---

## 2. O que o teste mediu

121 domínios: executivo federal (40), grandes municípios (40), os 27 estados mais o
DF (28), judiciário (10) e legislativo (3). Só consulta de DNS — nenhum e-mail
enviado, nenhuma falsificação tentada, nenhum servidor de terceiro tocado.

Todos os 121 resolveram.

---

## 3. Achado 1 — adotaram e pararam antes de proteger

```
Com SPF ..... 92,6%          Política DMARC:   24  p=reject
Com DMARC ... 81,8%                            49  p=quarantine
Com DKIM .... 66,9%                            26  p=none
                                               22  sem DMARC
```

Nível de proteção efetiva contra uma mensagem falsificada:

| | | |
|---|---|---|
| **22** | 18,2% | recusa a mensagem |
| **51** | 42,1% | entrega no spam (proteção parcial) |
| **48** | 39,7% | **nenhuma** — entrega na caixa de entrada |

**75 dos 99 domínios que têm DMARC escolheram uma política que não recusa nada.**

Esse é o achado. A pergunta de pesquisa que ele abre não é *"por que não adotam?"* —
é **"por que param antes de proteger?"**. E a segunda é muito melhor: ninguém pode
alegar desconhecimento ou falta de ferramenta. Eles conhecem o mecanismo,
configuraram, e deixaram em modo de observação.

> ⚠️ `quarantine` **protege parcialmente**: a mensagem chega, mas no spam. Dizer que
> tudo que não é `reject` é falsificável seria exagero — e foi um erro que o próprio
> script cometia na primeira versão.

---

## 4. Achado 2 — o contraste entre esferas é contraintuitivo

| esfera | n | SPF | DMARC | reject |
|---|---|---|---|---|
| federal | 40 | 97,5% | 92,5% | 25,0% |
| municipal\* | 40 | 97,5% | 85,0% | 17,5% |
| **estadual** | 28 | **75,0%** | **53,6%** | 17,9% |
| judiciário | 10 | 100% | **100%** | **10,0%** |
| legislativo | 3 | 100% | 100% | 33,3% |

**O estadual é o pior estrato**, não o municipal — o oposto do esperado. E o
judiciário é o caso mais puro do padrão "adotou e parou": todos têm DMARC, quase
nenhum recusa.

\* **Viés declarado:** a amostra municipal são capitais e cidades grandes. Não é o
estrato municipal, é o topo dele. As 5.570 prefeituras incluem milhares de cidades
pequenas que provavelmente não têm nada. **Ampliar esse estrato é obrigatório** se o
tema avançar.

---

## 5. Achado 3 — o que caiu no colo: soberania do correio institucional

Do levantamento de quem recebe o e-mail de cada domínio:

| Provedor | Domínios |
|---|---|
| **Microsoft** | 40 |
| **Google** | 15 |

**55 de 121 — 45% da amostra do setor público brasileiro tem o correio
institucional em infraestrutura americana.** Ministérios, tribunais, governos
estaduais.

Isso não era o que o teste procurava. É soberania de dados, medida com uma consulta
de DNS, e é o achado que mais diretamente toca a linha do orientador pretendido.

---

## 6. A hipótese que NÃO sobreviveu

O eixo que eu havia proposto para elevar o tema:

> A postura de segurança de um município não é escolha dele — é **herdada** de quem
> presta o serviço de TI.

Medida pela concordância da política DMARC dentro de cada fornecedor, contra a
concordância do conjunto todo:

| | primeira versão | corrigido (todos) | **só quem contrata terceiro** |
|---|---|---|---|
| DNS | +32% | +27% | **+14%** (n=15) |
| E-mail | +16% | +12% | **+6%** (n=59) |

O critério era 15 pontos. **Não passou.**

### Por que os números iniciais estavam inflados

1. **Auto-hospedagem contada como fornecedor.** Sete domínios agrupados sob
   "próprio/outro (sp.gov.br)" eram domínios de São Paulo servidos por DNS dentro do
   próprio `sp.gov.br`. Dizer que `sp.gov.br` herdou a configuração de `sp.gov.br` é
   circular.
2. **O grupo `sem_mx` entrando na conta.** Domínios que não recebem e-mail concordam
   em 100% por definição.

### Por que a hipótese pode não ter sido testada de verdade

A herança fala de **prefeituras pequenas que terceirizam para a empresa estadual de
tecnologia**. O corpus é governo federal, estados e capitais — exatamente as
organizações que têm TI própria. **A hipótese foi testada na população onde ela não
se aplica.**

É a mesma classe de erro do teste de genealogia de malware (ver
`../temas/05-teste-genealogia-malware.md`), com uma diferença importante: lá o erro
só apareceu depois da coleta; aqui foi nomeado antes de custar tempo.

**Para testar de verdade** seria preciso um corpus de municípios pequenos — que é
onde o `scripts/ct_direto.py`, herdado do tema de Certificate Transparency que foi
descartado, enumera domínios `.gov.br` que emitiram certificado.

---

## 7. Se este tema for escolhido, o que muda

O eixo principal deixa de ser a herança e passa a ser o **abandono a meio caminho**:
por que organizações que adotaram DMARC param em `none` e `quarantine`? Hipóteses
testáveis com o mesmo dado:

- **H1.** A distância entre adoção e enforcement difere por esfera e por poder.
- **H2.** Domínios que terceirizam o correio a provedor estrangeiro têm postura
  diferente dos que operam o próprio.
- **H3.** A herança por fornecedor aparece **nos municípios pequenos**, ausente na
  amostra atual — o que exige ampliar o corpus antes de afirmar qualquer coisa.
- **H4 (soberania).** A concentração do correio institucional público em dois
  provedores estrangeiros, medida por índice de concentração.

**Trabalho necessário antes de virar desenho experimental:** ampliar o corpus
municipal para além das capitais, e refazer a análise de herança com a população
certa.

---

## 8. Comparação honesta com o N3

| | N3 | S3 |
|---|---|---|
| Pergunta cabe numa frase | com esforço | sim |
| Corpus verificado | 396 apps, 4 portas | 121 domínios, 4 portas |
| Dependência externa | AndroZoo — **já concedido** | nenhuma |
| Achado próprio já em mãos | 0/396 apps com anúncio | 3 achados |
| Hipótese principal | intacta | **caiu** — precisa ser reconstruída |
| Tempo até o primeiro resultado | horas (piloto) | 60 segundos |
| Tamanho da monografia | maior | menor, precisa de ampliação |
| Encaixe com o orientador | soberania de dados | postura do Estado + soberania do correio |
