# N1 — Resultado do teste de viabilidade: tema rejeitado

**Data da coleta:** 31/08/2026
**Custo:** zero créditos (apenas endpoints de contagem e faceta)
**Decisão:** **rejeitar o tema N1** conforme desenhado.

Este documento registra um resultado negativo. Ele é material útil: um tema descartado
**com evidência** sustenta o capítulo de metodologia e demonstra rigor na qualificação.

---

## 1. O que se pretendia testar

O N1 propunha medir a exposição de sistemas de controle industrial brasileiros na internet,
com a hipótese de que **a exposição se concentra em setores sob menor supervisão
regulatória** (saneamento, automação predial) frente aos fortemente regulados (energia,
financeiro).

Isso exige que a variável independente — **o setor do operador** — seja observável a partir
dos dados. O teste verificou exatamente isso.

---

## 2. Contagens obtidas

| Consulta | Total |
|---|---|
| `country:BR tag:ics` (confirmado pela Shodan) | **557** |
| `country:BR port:502` (Modbus) | 1.888 |
| `country:BR port:102` (S7comm) | 2.373 |
| `country:BR port:20000` (DNP3) | 6.736 |
| `country:BR port:47808` (BACnet) | 121 |
| `country:BR port:44818` (EtherNet/IP) | 1.866 |
| `country:BR port:2404` (IEC 60870-5-104) | 2.878 |
| `country:BR port:1911,4911` (Niagara Fox) | 4.050 |
| `country:BR port:10001` (ATG) | 11.156 |
| `country:BR port:34962-34964` (PROFINET) | 6 |
| **Soma bruta** | **31.631** |

A discrepância de 57× entre a soma bruta e o conjunto confirmado (557) já indicava
contaminação. As facetas explicaram a causa.

---

## 3. A evidência que derrubou o tema

### 3.1 Os mesmos hosts respondem em protocolos mutuamente exclusivos

Distribuição por organização, três protocolos distintos:

| Organização | Modbus | IEC-104 | EtherNet/IP |
|---|---|---|---|
| ACEVILLE PTE.LTD. | 433 | 540 | 434 |
| Agencia Estado Ltda | 223 | 255 | 220 |
| Amazon Data Services Brazil | 180 | 217 | 237 |
| Fly.io, Inc. | 180 | 201 | 187 |
| Alibaba Cloud LLC | 30 | 47 | 36 |

**Equipamento industrial real não fala os três protocolos simultaneamente.** Um CLP fala
Modbus; um IED de subestação fala IEC-104; um controlador Allen-Bradley fala EtherNet/IP.
A coincidência quase perfeita das contagens entre protocolos indica que **são os mesmos
hosts respondendo em todas as portas**.

As explicações compatíveis com esse padrão são: **honeypots** (o Conpot e similares simulam
múltiplos protocolos ICS ao mesmo tempo), hosts de nuvem com todas as portas abertas, e
tarpits de varredura. A literatura já alertava para isso — um estudo identificou 1.174
honeypots entre 100.766 dispositivos —, mas aqui o ruído não é contaminante minoritário: é
o **sinal dominante**.

### 3.2 Nenhum operador industrial aparece

Entre as maiores organizações das três consultas de protocolo não há **uma única**
concessionária de energia, companhia de saneamento, indústria ou órgão público. Há
provedores de nuvem (Amazon, Fly.io, Alibaba), CDN/WAF (Incapsula) e entidades
estrangeiras.

Sinais adicionais de que a consulta não está medindo infraestrutura brasileira:

- **ACEVILLE PTE.LTD.**, entidade de **Singapura**, é a maior "operadora de ICS brasileira".
- **APNIC**, o registro regional do **Ásia-Pacífico**, aparece em consulta `country:BR`,
  evidenciando erro de geolocalização.

### 3.3 O conjunto confirmado está atrás de provedores de acesso

Os 557 hosts com `tag:ics` — os únicos com fingerprint de protocolo confirmado — se
distribuem assim: Telefônica (69), COPREL Telecom (37), FAZZY Internet (36), Claro (26),
Algar (10), Telespazio (10), V.tal (8), Unifique (7).

**São provedores de acesso.** Os dispositivos estão atrás de banda larga empresarial, e o
ASN pertence à operadora, não ao operador do equipamento. A fábrica ou a estação de
tratamento permanece invisível.

---

## 4. Por que isso encerra o tema

A hipótese exigia observar o **setor** do operador. Os dados não o expõem:

- No conjunto grande, a organização é um provedor de nuvem ou um honeypot — não há
  operador real por trás.
- No conjunto confirmado, a organização é a operadora de telecomunicações — o operador real
  está oculto por construção.

**Não é limitação de esforço.** Nenhuma quantidade de trabalho manual extrai setor de
"TELEFÔNICA BRASIL S.A". A variável independente da hipótese é inobservável nesta fonte de
dados.

Restaria tentar atribuição por DNS reverso, conteúdo de banner ou certificado — o que
recuperaria uma fração pequena dos 557, com custo manual alto e retorno incerto. Sob
restrição de tempo, não se justifica.

---

## 5. O que sobra de aproveitável

O achado da Seção 3.1 — **a maior parte do que se reporta como ICS exposta no Brasil não é
ICS real** — tem valor metodológico e serve como crítica à literatura que conta porta
aberta e chama de dispositivo industrial. Mas é fino para sustentar um TCC inteiro, e a
detecção de honeypots em dados da Shodan já tem literatura própria.

**Registrado como achado, não como tema.**

---

## 6. Decisão

- **N1: rejeitado.** Hipótese não testável com a fonte de dados disponível.
- **Novo primeiro lugar: L1** — caracterização das falhas de predição de exploração de
  vulnerabilidades (NVD + EPSS + KEV). Já era o mais adequado sob restrição de tempo, e sua
  variável independente é observável por construção, que é exatamente o que faltou aqui.
- **Segunda opção: N2** — postura técnica de domínios governamentais. A variável
  independente (esfera federativa) é trivialmente observável a partir do próprio domínio.

---

## 7. Uso deste resultado no TCC e na orientação

Leve esta tabela para a conversa de 25/08. Chegar tendo **testado e rejeitado** um tema com
evidência quantitativa vale mais que chegar com três ideias não testadas — e demonstra
exatamente a postura que as Aulas 04 a 08 cobram: hipótese falsificável, verificação
empírica, e disposição de abandonar o que não se sustenta.

Os dados brutos estão em `dados/contagens_20260831.json` e `dados/facetas_20260831.json`
(não versionados, por decisão do `.gitignore` — guarde-os localmente).
