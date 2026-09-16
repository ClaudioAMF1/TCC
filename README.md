# TCC — Projeto Capstone I (IDP, 2026.2)

Repositório de trabalho do meu Trabalho de Conclusão de Curso em Ciência da Computação
no IDP. Reúne o material da disciplina, a busca pelo tema, os testes de viabilidade que
foram feitos e os scripts que os produziram.

**Estado atual:** **tema definido — N3, rastreamento em aplicativos móveis governamentais
brasileiros.** Quatro candidatos foram testados empiricamente; três caíram com evidência e
um sobreviveu. A proposta formal para o orientador está em
`desenhos/N3-proposta-formal.md`. Ver a Seção 3.

---

## 1. Como o repositório está organizado

```
disciplina/     Plano de ensino, regulamento do TCC, slides das aulas e listas
seminario/      Seminário de análise de artigo (29/09 e 01/10) e material fornecido
temas/          A busca pelo tema: catálogo, estado da arte, avaliação da área
desenhos/       Desenhos experimentais completos dos candidatos que avançaram
descartados/    Temas testados e rejeitados, com a evidência que os derrubou
scripts/        Ferramentas escritas para testar a viabilidade de cada tema
dados/          Saída bruta das coletas (não versionado — ver .gitignore)
```

### `disciplina/`
| Arquivo | Para quê |
|---|---|
| `Plano de Ensino - Projeto Capstone I.pdf` | Cronograma, avaliação, prazos |
| `Regulamento TCC CIC v.2026-05 -- VIGENTE.pdf` | Regras formais: modalidades, orientação, banca |
| `aulas/` | Slides 01 a 14 — metodologia, maturidade em pesquisa, questões de pesquisa, análise crítica de propostas, escrita da monografia |
| `listas/` | Listas de exercícios da disciplina e guias de estudo correspondentes |

### `seminario/`
| Arquivo | Conteúdo |
|---|---|
| `plano-do-seminario.md` | Estratégia, artigo recomendado, planilha de levantamento de métricas, roteiro dos 15 min e formato da análise de estrutura |
| `qualis-faixas-de-percentil.png` | Figura 6 do Documento Técnico: percentil → estrato |
| `material-fornecido/` | PDFs disponibilizados pela professora |

### `temas/`
| Arquivo | Conteúdo |
|---|---|
| `01-catalogo-inicial.md` | Primeiro leque de 9 temas, com as restrições que o regulamento impõe |
| `02-estado-da-arte.md` | Checagem de literatura de cada tema: o que já foi feito, onde há espaço, veredito |
| `03-temas-cyber.md` | Temas em cibersegurança compatíveis com o orientador pretendido |
| `04-avaliacao-da-area.md` | Avaliação honesta da área como escolha de TCC + temas de menor custo de tempo |
| `05-teste-genealogia-malware.md` | Teste de viabilidade da genealogia do malware bancário brasileiro e por que ele ficou inconclusivo |

### `desenhos/`
Desenhos experimentais completos — problema de pesquisa nas três partes exigidas pela
disciplina, hipóteses falsificáveis, corpus, instrumentos, plano estatístico, ética,
ameaças à validade e divisão entre Capstone I e II.

| Arquivo | Tema | Situação |
|---|---|---|
| `N3-proposta-formal.md` | **Proposta que vai ao orientador** — quadrante, hipóteses, método, ética, pendências formais | ⭐ **tema escolhido** |
| `N3-apps-governamentais.md` | Desenho experimental detalhado do mesmo tema | ✅ corpus verificado (396 apps) |
| `T1-seguranca-codigo-llm.md` | Segurança do código gerado por LLM + validade do oráculo | ⏸️ forte, mas sem encaixe com o orientador |
| `T3-lgpd-sites-saude.md` | LGPD Art. 11 e rastreamento em sites de saúde | ⏸️ viável, pouco técnico |

### `descartados/`
| Arquivo | Por que caiu |
|---|---|
| `N1-infraestrutura-critica.md` | A variável independente (o setor do operador) é inobservável nos dados |

---

## 2. Restrições que o regulamento impõe

Extraídas do `disciplina/Regulamento TCC CIC v.2026-05`:

- Trabalho **individual** (Art. 6º).
- **Texto final em inglês** (Art. 32, §3º).
- Modalidade *artigo científico* exige **aceite em periódico Qualis ≥ B2** para aprovar em
  Capstone II (Art. 29, §1º) — risco alto, fora do controle do aluno.
- Orientador precisa de **titulação stricto sensu em tecnologia ou engenharias** (Art. 13, §1º)
  e pode ter no máximo **3 orientandos novos por semestre** (Art. 13, §6º).
- **5 encontros obrigatórios** com o orientador no 2º bimestre, com ficha assinada
  (Art. 19, II e Art. 24) — requisito de aprovação, reprova por si só.
- Primeiro critério da banca: **quadrante tema–problema–hipótese–marco teórico** (Art. 31, I).

E das aulas 04 a 08:
- O objetivo deve usar verbo **verificável** — *medir*, *comparar*, *demonstrar*. Os verbos
  *propor*, *estudar* e *apresentar* são apontados como inadequados.
- **"Evite o fundamento vazio"**: justificar um tema apenas pela ausência de estudo anterior
  não basta. É preciso mostrar o que outros fizeram e no que o seu difere.
- Tema interdisciplinar custa **três revisões bibliográficas**, não uma.

---

## 3. O que já foi testado

Cada tema candidato passou por um teste de viabilidade **antes** de virar desenho
experimental. Os resultados:

| Tema | Teste | Resultado |
|---|---|---|
| **N1** — ICS exposta no Brasil | Contagem e facetas no Shodan | ❌ **Descartado.** Os mesmos hosts respondem em Modbus, IEC-104 e EtherNet/IP ao mesmo tempo — comportamento de honeypot e de nuvem, não de equipamento industrial. O conjunto confirmado está atrás de provedores de acesso, ocultando o operador. |
| **CT** — abuso de marca em Certificate Transparency | 20 mil entradas de log, casamento por token | ❌ **Descartado.** Zero imitações reais. Phishing moderno raramente põe a marca no domínio, o que impõe teto de recall por construção. |
| **N3** — apps móveis governamentais | Busca e expansão por catálogo na Play Store | ✅ **Confirmado.** 396 aplicativos de 71 publicadores públicos distintos, três esferas representadas, publicador identificado na origem. |
| **Genealogia do malware bancário BR** | imphash de 1.764 amostras brasileiras × 2.104 de controle, no MalwareBazaar | ⚠️ **Inconclusivo.** O rótulo de família marca a campanha, não o payload: 85% do acervo brasileiro são containers (zip/iso/lnk/msi), onde imphash não existe. Testar de verdade exigiria desempacotar malware vivo em VM isolada. Detalhes em `temas/05-teste-genealogia-malware.md`. |

Os dois descartes são material de TCC, não tempo perdido: sustentam a seção de metodologia
e demonstram a postura que as aulas 04 a 08 cobram — hipótese falsificável, verificação
empírica, disposição de abandonar o que não se sustenta.

---

## 4. Scripts

Todos são de leitura passiva de fontes públicas. Nenhum acessa sistema de terceiros,
nenhum explora falha, nenhum baixa conteúdo de área autenticada.

| Script | O que faz |
|---|---|
| `teste_viabilidade_n1.py` | Consulta o Shodan (contagens e facetas) para dimensionar a exposição de ICS no Brasil |
| `ct_direto.py` | Lê os logs de Certificate Transparency direto pela API padrão (RFC 6962) e procura imitação de marca brasileira |
| `teste_viabilidade_ct.py` | Versão anterior, via crt.sh — mantida como registro; o crt.sh se mostrou instável |
| `teste_viabilidade_n3.py` | Enumera aplicativos governamentais na Play Store por termo e por catálogo de publicador |
| `teste_viabilidade_n3_robusto.py` | Mede a **porta de cada hipótese** antes de baixar APK: pareamento (H1), política de privacidade acessível (H2), povoamento das células (H3), potência estatística, e um sinal preliminar da variável dependente |
| `teste_viabilidade_malware.py` | Consulta metadados de famílias de malware bancário no MalwareBazaar e mede compartilhamento de imphash entre famílias, com grupo de controle não brasileiro |
| `gera_deck_seminario.js` | Gera o deck do seminário de análise de artigo |

### Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install google-play-scraper cryptography

python3 scripts/teste_viabilidade_n3.py --expandir
python3 scripts/ct_direto.py --entradas 20000 --logs 1
```

O teste robusto do N3 reaproveita a saída do anterior. Ele tem autoteste offline:

```bash
python3 scripts/teste_viabilidade_n3_robusto.py --autoteste       # valida a lógica, sem rede
python3 scripts/teste_viabilidade_n3_robusto.py --limite 40        # rodada curta (~5 min)
python3 scripts/teste_viabilidade_n3_robusto.py                    # completo (~40 min)
```

O teste de malware exige uma chave gratuita do MalwareBazaar (auth.abuse.ch):

```bash
export MALWAREBAZAAR_API_KEY="..."
python3 scripts/teste_viabilidade_malware.py
```

> Esse script lê **apenas metadados** — hashes, tipo de arquivo, data e assinatura.
> Nenhuma amostra de malware é baixada.

O script do Shodan exige uma chave em variável de ambiente:

```bash
export SHODAN_API_KEY="..."
python3 scripts/teste_viabilidade_n1.py --apenas-contagem
```

> A chave **nunca** vai para o repositório. O `.gitignore` cobre `.env`, `*.key` e o
> diretório `dados/`.

---

## 5. Calendário

| Data | Marco |
|---|---|
| 10/09 | Entrega da **Lista de Exercícios 01** (impressa) — enunciado e guia de estudo em `disciplina/listas/` |
| **29/09 e 01/10** | **Seminário de análise de artigo científico** (4 dos 6 pontos da AV1) — plano em `seminario/` |
| Out–Nov | 5 encontros de orientação, com ficha assinada e entregue mensalmente |
| 24/11 a 01/12 | Simulação de defesa |
| **03/12** | **Entrega da redação do TCC I no Canvas** — prazo duro |
| 08 a 15/12 | Defesa final / qualificação perante banca |

---

## 6. O que falta

- ~~**Tema definitivo.**~~ Definido: **N3**. Proposta formal em `desenhos/N3-proposta-formal.md`.
- **Rodar o teste robusto** (`scripts/teste_viabilidade_n3_robusto.py`) e levar os números
  das seis portas junto da proposta.
- **Orientador.** A apresentação das linhas de pesquisa já ocorreu; o termo de aceite
  precisa ser formalizado (Art. 10 e Art. 15), e é preciso confirmar a elegibilidade do
  professor pretendido junto à Coordenação (Art. 13, §1º e §6º).
- **Acesso ao AndroZoo** (`androzoo.uni.lu`) — é o gargalo de prazo, o pedido leva dias.
- **Modalidade.** Monografia é o caminho de menor risco. Artigo científico depende de
  aceite em periódico Qualis B2, o que não está sob controle do aluno.
