# T1 — Desenho Experimental

**Título provisório (EN):** *Does Security Prompting Actually Work? A Replication Study on
LLM-Generated Code Security and the Validity of Static-Analysis Oracles*

Documento de trabalho para levar ao orientador. Complementa `TEMAS-PROPOSTOS-TCC1.md` e
`ESTADO-DA-ARTE-TEMAS.md`.

---

## 1. Quadrante metodológico

**Tema.** Segurança de código gerado por modelos de linguagem, e a validade das medições
adotadas pela literatura da área.

**Problema.** Estratégias de prompting orientadas a segurança reduzem de fato a incidência
de vulnerabilidades em código gerado por LLMs — ou apenas redistribuem as classes de CWE?
E em que medida a resposta a essa pergunta depende do analisador estático adotado como
referência?

**Hipóteses.**

- **H1** — O efeito agregado das estratégias de prompting sobre a *densidade* de
  vulnerabilidades não é estatisticamente significativo, ainda que altere a *distribuição*
  entre categorias de CWE.
- **H2** — A concordância entre analisadores estáticos sobre o mesmo corpus gerado é baixa
  (κ < 0,4), e o **ordenamento** das estratégias por eficácia muda conforme a ferramenta
  adotada como oráculo.
- **H3** — O valor preditivo positivo dos alertas, estabelecido por rotulagem manual, varia
  substancialmente por classe de CWE — de modo que taxas agregadas de vulnerabilidade não
  são diretamente comparáveis entre estudos que usaram ferramentas diferentes.

**Marco teórico.** Duas literaturas que hoje quase não se conversam:

1. Segurança de código gerado por IA — SecurityEval, LLMSecEval, CyberSecEval, CWEval,
   SafeGenBench, SecCodePLT, e os estudos de prompting de 2025–2026.
2. Confiabilidade de análise estática — avaliações SATE do NIST, estudos de taxa de falso
   positivo e de concordância entre ferramentas.

Costurar as duas já é contribuição. É também a resposta pronta para a pergunta de banca
"o que há de novo aqui?".

---

## 2. Hardware disponível e o que ele permite

| Componente | Especificação | Implicação |
|---|---|---|
| GPU | RTX 5070 Ti Laptop, **12 GB VRAM** | Modelos de 7B–14B em 4 bits rodam **inteiramente na GPU**. É o fator determinante. |
| CPU | Intel Core Ultra 9 | Suficiente. Ajuda no CodeQL, que é mais sensível a CPU/RAM que a GPU. |
| RAM | 32 GB DDR5 | Confortável para construir bases do CodeQL em lote. |
| Armazenamento | 2 TB NVMe | Não é restrição. Pesos + corpus + bases ficam abaixo de ~100 GB. |

### O que cabe em 12 GB (quantização de 4 bits, Q4_K_M)

| Classe | VRAM aprox. | Cabe? |
|---|---|---|
| 6–8B | 4–5 GB | ✅ folgado, contexto longo disponível |
| 13–14B | 8–9 GB | ✅ cabe, com contexto moderado |
| 22B | ~13 GB | ❌ estoura; exigiria descarregar para CPU |
| 32B+ | ≥19 GB | ❌ inviável em velocidade utilizável |

**Conclusão:** a faixa de trabalho é **7B a 14B**. É mais do que suficiente para o desenho
abaixo — mas cria uma ameaça à validade externa tratada na Seção 6.

---

## 3. Desenho fatorial

Experimento fatorial completo: **modelos × estratégias × tarefas × repetições**.

### Fator 1 — Modelos (4 locais + 2 âncoras comerciais)

Locais, escolhidos para variar em três eixos ao mesmo tempo:

| Modelo | Papel no desenho |
|---|---|
| Qwen2.5-Coder-7B-Instruct | referência da faixa 7B |
| Qwen2.5-Coder-14B-Instruct | **mesma família, escala maior** → isola o efeito de tamanho |
| DeepSeek-Coder-6.7B-Instruct | fornecedor distinto, porte equivalente |
| Llama-3.1-8B-Instruct | **modelo generalista** → isola o efeito de especialização em código |

Duas âncoras comerciais via API, com amostragem reduzida, para ligar os resultados ao que
desenvolvedores de fato usam (ver Seção 6).

### Fator 2 — Estratégias de prompting (4 níveis)

| Nível | Descrição |
|---|---|
| S0 — baseline | pedido funcional puro, sem menção a segurança |
| S1 — prefixo de segurança | instrução genérica de escrever código seguro |
| S2 — consciente de CWE | contexto explícito das classes de CWE relevantes à tarefa |
| S3 — reparo pós-hoc | S0 seguido de uma segunda chamada pedindo revisão e correção |

Esses quatro níveis cobrem justamente as estratégias cujos efeitos reportados na literatura
vão de 56% de redução a nenhum efeito estatisticamente detectável.

### Fator 3 — Tarefas (~60 prompts, **em Python**)

Composição: prompts do SecurityEval e do CWE Top 25, mais um subconjunto **autoral** de
tarefas inéditas — este último existe para mitigar contaminação de treino (Seção 6).

> **Por que Python, e por que isso não é arbitrário.** A comparação entre três analisadores
> só é possível numa linguagem que os três suportem bem. O Bandit é exclusivo de Python.
> Logo, a escolha da linguagem é **imposta pelo desenho**, não por preferência — e isso vai
> escrito na metodologia, porque é um bom argumento.

### Fator 4 — Repetições

**10 gerações por célula**, temperatura fixa (0,2 e 0,8, para tratar o não-determinismo
como variável controlada e não como ruído ignorado).

### Volume total

```
60 tarefas × 4 estratégias × 4 modelos locais × 10 repetições  =  9.600 gerações
+ chamadas extras da estratégia S3 (segunda passada)           ≈ 2.400
                                                     TOTAL     ≈ 12.000 gerações locais
```

---

## 4. Orçamento de tempo — o ponto que decide a viabilidade

Código gerado é curto (~300 tokens por amostra). Estimativas conservadoras para esta GPU:

| Modelo | Throughput estimado | Tempo/amostra |
|---|---|---|
| 7B Q4 | 40–60 tok/s | ~6–8 s |
| 14B Q4 | 20–30 tok/s | ~12–15 s |

**Total: aproximadamente 25 a 35 horas de GPU.** Distribuído em execuções noturnas, são
cerca de **cinco a sete noites**. Não é gargalo.

Três cuidados práticos de notebook:

1. **Throttling térmico.** Carga sustentada de várias horas em laptop reduz clock. Rode em
   lotes, na tomada, com boa ventilação, e **registre o tempo real de execução** — vira
   dado de reprodutibilidade.
2. **Meça antes de planejar.** Na primeira semana, rode um benchmark de throughput real dos
   quatro modelos e recalibre os números acima. Não confie na minha estimativa.
3. **Blackwell é arquitetura recente.** Use builds atuais de driver, CUDA e do runtime de
   inferência (Ollama, llama.cpp ou vLLM). Verifique isso no primeiro dia — é o tipo de
   problema que consome uma semana se descoberto tarde.

---

## 5. Pipeline de análise

1. **Geração** — os ~12.000 trechos, com registro completo de prompt, seed, temperatura,
   modelo e timestamp.
2. **Análise estática tripla** — CodeQL, Semgrep e Bandit sobre **todo** o corpus, com os
   alertas de cada ferramenta **armazenados separadamente**. Essa separação é o coração de
   H2; não agregue nada nesta etapa.
3. **Corretude funcional** — execução dos testes de cada tarefa. Sem isso, "seguro" pode
   significar apenas "não faz nada".
4. **Rotulagem manual** — amostra estratificada de **300 a 400 alertas**, balanceada por
   ferramenta e por classe de CWE, com protocolo de codificação escrito antes de começar.
5. **Análise estatística.**

### Plano estatístico

| Hipótese | Método |
|---|---|
| H1 | Regressão logística de efeitos mistos — desfecho binário por amostra, interceptos aleatórios para tarefa e modelo. Reportar **tamanho de efeito e intervalo de confiança**, não só valor-p. Para a redistribuição de CWE, comparar as distribuições entre estratégias. |
| H2 | κ de Fleiss entre as três ferramentas; e o teste decisivo — τ de Kendall entre os *ordenamentos* de estratégias induzidos por cada ferramenta. Se τ for baixo, a conclusão do campo depende da ferramenta escolhida. |
| H3 | Valor preditivo positivo por classe de CWE, a partir dos rótulos manuais, com intervalos de confiança. |

**Congele o plano de análise antes de olhar os resultados** e diga isso no texto. Análise
pré-registrada é um sinal de rigor barato de dar e caro de ignorar — e diferencia o
trabalho dos que estão sendo replicados.

---

## 6. Ameaças à validade (e como tratar cada uma)

| Ameaça | Por que importa | Tratamento |
|---|---|---|
| **Validade externa: só modelos pequenos** | 12 GB limita a 7–14B. Desenvolvedores usam Copilot, Claude, GPT. A banca vai perguntar. | Escopo declarado explicitamente como "modelos de pesos abertos executáveis em hardware de consumo" — o que é população legítima e interessante por si — **mais** duas âncoras comerciais via API com amostragem reduzida (60 tarefas × 4 estratégias × 3 repetições × 2 modelos ≈ 1.440 chamadas; custo na casa de poucas dezenas de dólares). |
| **Contaminação de benchmark** | Os modelos podem ter visto SecurityEval no treino. | Subconjunto autoral de tarefas inéditas; comparar o desempenho nele contra o do benchmark público. Se houver diferença sistemática, ela **é um resultado**. |
| **Subjetividade da rotulagem** | O ponto mais frágil do trabalho. | Protocolo escrito com critérios explícitos; se possível, segundo rotulador em subamostra, com medida de confiabilidade entre avaliadores. |
| **Não-determinismo** | Uma única geração por célula não mede nada. | 10 repetições, duas temperaturas, variância reportada. |
| **Ritmo da área** | Sai trabalho novo toda semana. | Formato de replicação é imune — resultado conflitante novo **aumenta** o valor do trabalho. Ainda assim, atualize a busca até a véspera da defesa. |

---

## 7. Onde está o trabalho de verdade

O gargalo **não é computacional**. A GPU resolve tudo em cinco a sete noites.

O gargalo é a **rotulagem manual**: 300–400 alertas, a 3–5 minutos cada, dão **20 a 33
horas** de trabalho concentrado. Diluído ao longo do Capstone II, são cerca de duas a três
horas por semana.

É bom saber disso agora, e não em outubro de 2027. Essa etapa é também o que separa este
trabalho dos que ele replica — a maioria confia na saída da ferramenta sem verificar. Se
você fizer a validação manual com rigor, é exatamente aí que sua contribuição se sustenta.

---

## 8. Divisão entre Capstone I e Capstone II

### Capstone I — entrega em **03/12/2026**

1. Revisão sistemática das **duas** literaturas, com a tabela de efeitos conflitantes
   reportados (56% / 60% / 28% / 17% / nenhum efeito) — essa tabela é, sozinha, a
   justificativa do trabalho.
2. Protocolo experimental completo e congelado, incluindo o plano de análise estatística.
3. **Piloto funcionando**: 1–2 modelos × 2 estratégias × subconjunto de tarefas, com o
   pipeline de três analisadores rodando ponta a ponta.
4. Protocolo de rotulagem manual escrito.

O piloto é o que torna a qualificação forte: você não chega com uma promessa, chega com um
pipeline que já produziu números preliminares.

### Capstone II — 2027.1

Execução completa, rotulagem manual, análise estatística, discussão e publicação do corpus
gerado como artefato.

---

## 9. Primeiros passos concretos

| Quando | O quê |
|---|---|
| Esta semana | Instalar o runtime de inferência e **medir throughput real** dos quatro modelos. Recalibrar a Seção 4 com os números da sua máquina. |
| Esta semana | Rodar CodeQL, Semgrep e Bandit sobre uma dúzia de trechos manuais só para validar o encanamento. |
| Até 25/08 | Levar este documento ao orientador. O piloto de throughput já dá credibilidade à conversa. |
| Oficina de 01–03/09 | Usar a oficina de bases bibliográficas para montar a busca sistemática **destas duas** literaturas. |
| Seminário de 29/09 | Apresentar um dos artigos de prompting conflitantes — cumpre a atividade avaliativa e adianta a revisão. |
