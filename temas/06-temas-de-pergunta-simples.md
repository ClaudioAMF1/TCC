# Temas de pergunta simples — cibersegurança

Critério de seleção destes quatro: **a pergunta de pesquisa cabe numa frase que
alguém de fora da computação entende**, e a medição é contagem e proporção, sem
maquinaria estatística.

Todos são compatíveis com o orientador pretendido (soberania, postura de
segurança do Estado), todos usam **dado público lido passivamente**, e todos têm
literatura anterior em outros países — o que satisfaz o "evite o fundamento
vazio" da Aula 07/08: existe o que citar, e existe o que diferenciar.

---

## S1 — Onde o governo brasileiro está hospedado?

> **A pergunta:** quando você acessa um serviço público brasileiro, em qual
> empresa e em qual país está o servidor que responde?

**O que se mede.** Para cada domínio `.gov.br`: resolve o DNS, pega o IP, e do IP
extrai o **número de sistema autônomo (ASN)** e a organização que o opera. O
mesmo para três dependências que quase ninguém olha:

- **Quem hospeda o site** (ASN do endereço final)
- **Quem serve o DNS** (registros NS — se o DNS do Ministério da Saúde está numa
  empresa estrangeira, é ela que decide se o domínio resolve)
- **Quem recebe o e-mail** (registros MX — quantos órgãos públicos brasileiros
  entregam correio institucional ao Google ou à Microsoft?)

**Por que não é óbvio.** A resposta esperada é "está na nuvem, todo mundo sabe".
O trabalho não é a manchete, é a **estrutura**: quanto da dependência se
concentra em quantos fornecedores, se difere por esfera, e se os serviços que
tratam dado sensível são os mesmos que dependem mais de fora. Concentração é
mensurável (índice de Herfindahl) e é argumento de risco sistêmico, não de
opinião.

**Custo.** Baixo. `dnspython` e uma base pública de ASN. Roda em horas.

**A armadilha, e o tratamento.** Geolocalizar IP é impreciso, e CDN *anycast*
torna "onde" ambíguo por construção. **Solução: medir quem opera, não onde o
pacote cai.** O ASN e a organização são fatos de registro; a latitude não é. Isso
vira uma seção de validade, não um problema.

**Encaixe com o orientador.** Direto. É soberania de dados na camada de
infraestrutura.

---

## S2 — Quem mais está na página do governo?

> **A pergunta:** quando você abre o site de um serviço público, para quantos
> terceiros o seu navegador manda uma requisição sem você saber?

**O que se mede.** Carrega a página num navegador controlado e registra **todo
domínio de terceiro contactado**: scripts, fontes, pixels, analytics, mapas.
Classifica cada um por finalidade e por jurisdição do operador. Compara portais
de serviço com um grupo de controle comercial.

**Por que é o mais fácil dos quatro, tecnicamente.** É a pergunta do tema N3, na
web em vez do Android. Sem APK, sem descompilação, sem MobSF, sem AndroZoo. Um
navegador headless e a lista de requisições que ele faz — que o próprio navegador
já entrega pronta.

**O que já está feito e transfere.** A revisão de literatura de rastreamento por
terceiros, o enquadramento jurídico (LGPD Arts. 7º e 11) e o argumento de
soberania são os mesmos do N3. E o achado de que **aplicativo de governo não
exibe anúncio** (0 de 396) tem um paralelo direto a testar aqui: se o site também
não monetiza, o rastreamento encontrado é de infraestrutura, não de publicidade —
e isso fecha o argumento nas duas plataformas.

**A armadilha.** Coletar só o HTML estático subconta muito, porque metade das
requisições nasce de JavaScript. Precisa de navegador de verdade (Playwright,
que já está instalado aqui), não de `requests`.

---

## S3 — Dá para mandar e-mail fingindo ser o governo?

> **A pergunta:** os domínios públicos brasileiros estão configurados para
> impedir que alguém falsifique e-mails em nome deles?

**O que se mede.** Três registros de DNS, por domínio:

| Registro | O que significa se faltar |
|---|---|
| **SPF** | Qualquer servidor pode alegar enviar por aquele domínio |
| **DKIM** | A mensagem não é assinada; adulteração não é detectável |
| **DMARC** | Ninguém instruiu o destinatário sobre o que fazer com falsificação |

O **DMARC** é a melhor variável dependente que existe para um TCC de graduação:
tem três níveis ordenados — `none` (só observa), `quarantine` (manda para spam),
`reject` (recusa). Ou seja, não é sim/não, é uma escala de rigor, e dá para
perguntar *quanto* de rigor por esfera, por porte de município, por setor.

**Por que importa de verdade.** Golpe com "Receita Federal" e "INSS" no remetente
é o vetor de fraude mais comum contra cidadão brasileiro. Um domínio sem DMARC em
`reject` é tecnicamente falsificável.

**Custo.** O menor dos quatro. São consultas de DNS: roda em minutos.

**A ressalva honesta.** Esse levantamento já foi feito para governos de vários
países, então a contribuição **não** pode ser "medimos no Brasil". Tem que ser a
estratificação: as três esferas, e a correlação com quem presta o serviço de TI —
municípios que terceirizam para a mesma empresa estadual têm a mesma postura? Aí
sim há pergunta nova.

---

## S4 — O governo desliga o que abandona?

> **A pergunta:** quantos serviços digitais públicos continuam no ar sem
> manutenção — certificado vencido, app sem atualização há anos, domínio
> expirado?

**O que se mede.** Validade e cadeia dos certificados TLS, data da última
atualização dos aplicativos, domínios que não resolvem mais mas continuam
linkados em portais oficiais.

**Por que é interessante.** Serviço abandonado no ar não é só desleixo: é
superfície de ataque sem dono. Domínio público que **expira** pode ser registrado
por qualquer um — e passa a receber o tráfego e o e-mail de quem confia na marca.
Isso é concreto, visual e ninguém precisa de formação em segurança para entender
por que é grave.

**Ressalva.** É o mais fino dos quatro em teoria. Funciona bem como **eixo
secundário** dentro do S1 ou do S3, e mal como tema sozinho.

---

## Comparação

| | Pergunta clara | Custo | Teoria disponível | Encaixe com o orientador |
|---|---|---|---|---|
| **S1** infraestrutura | ✅✅ | baixo | boa | ✅✅ direto |
| **S2** terceiros na web | ✅✅ | baixo | **ótima — já levantada** | ✅ |
| **S3** falsificação de e-mail | ✅✅✅ | mínimo | boa, mas já replicada | ✅ |
| **S4** abandono | ✅✅ | baixo | fraca | ✅ |

**Recomendação.** **S1 + S2 como um tema só**, sob o título de *dependências
externas do governo digital brasileiro*: a infraestrutura que serve (S1) e os
terceiros que a página carrega (S2). Não é interdisciplinar — é a **mesma
literatura** (medição da web) e a **mesma ferramenta**, em duas camadas. A Aula
07/08 penaliza tema que exige três revisões bibliográficas; este exige uma.

E aproveita o que já foi feito: o enquadramento jurídico, a revisão de
rastreamento por terceiros e o achado do anúncio zero migram inteiros do N3.

**Se o critério for só velocidade, S3.** Roda numa tarde e você tem resultado
para levar à primeira orientação.

---

## O que fazer antes de decidir

O mesmo de sempre, e é o que salvou três decisões neste repositório: **teste de
viabilidade antes de desenho experimental.** Para estes temas o teste é barato:

- **S1** — resolver 200 domínios `.gov.br` e ver se o ASN identifica o operador
  de forma útil, ou se tudo cai em três nuvens e a variável perde variação.
- **S2** — carregar 50 portais em navegador headless e contar terceiros. Se a
  mediana for zero, não há o que medir.
- **S3** — consultar SPF/DMARC de 200 domínios e ver se há **variação** entre
  esferas. Se 95% não tiver DMARC, não há contraste: vira estatística
  descritiva, não pesquisa.

Cada um desses é uma tarde. Nenhum exige chave de API paga.
