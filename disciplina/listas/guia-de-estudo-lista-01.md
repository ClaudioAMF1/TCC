# Guia de estudo — Lista de Exercícios 01

Mapa de onde cada questão é respondida nos slides, com o conteúdo da aula organizado
em notas. **Serve para você escrever as respostas com suas palavras, não para copiar.**

Entrega: **10/09/2026, impressa, individual**. Peso: 2 pontos dos 6 da AV1
(a lista vale 2 e o seminário 4, conforme o Plano de Ensino).

Fonte de tudo: WAZLAWICK, *Metodologia de Pesquisa para Ciência da Computação*, 3ª ed. —
bibliografia básica da disciplina e base declarada de todas as aulas.

---

## Questão 1 — Classificações das ciências [1,2]

📁 **Aula 01** (`disciplina/aulas/Aula 01.pdf`)

São cinco pares. Cada um é um **critério diferente** de classificar — não são níveis nem
hierarquia. Ao responder, deixe claro qual é o critério de cada par.

| Par | Critério de divisão | Notas da aula |
|---|---|---|
| **a)** Formais × empíricas | O objeto existe no mundo ou é construção abstrata | Formais: lógica, matemática — validade por coerência interna, sem experimento. Empíricas: dependem de observação da realidade |
| **b)** Puras × aplicadas | Finalidade | Puras: conhecimento por si. Aplicadas: resolver problema prático |
| **c)** Exatas × inexatas | Precisão da medição e previsão | |
| **d)** Hard × soft | Grau de consenso metodológico e de formalização | |
| **e)** Nomotéticas × idiográficas | Buscam **leis gerais** × descrevem o **caso particular** | |

> Reveja os slides para preencher as células vazias com a definição exata da professora —
> ela cobra os termos dela. E pense onde a Computação se encaixa em cada par: é uma boa
> frase de fechamento e mostra que você entendeu, não decorou.

---

## Questão 2 — Método científico e sua importância [0,5]

📁 **Aula 02**

Vale meio ponto, então é resposta curta. Cubra duas coisas:

1. **O que é**: procedimento sistemático para produzir e validar conhecimento.
2. **Por que importa**: é o que separa afirmação fundamentada de opinião.

A aula abre com dois exemplos que valem citar, porque são dela:
- O aluno que aplicou questionário a **cinco pessoas**, teve 3 sim e 2 não, e concluiu que
  "havia tendência para o sim (60%)". A aula pergunta: *que valor tem essa conclusão?*
- O grupo que usou software educacional × o que não usou.

Ambos ilustram o mesmo ponto: **sem método, o dado não sustenta a conclusão.**

---

## Questão 3 — Positivismo, reducionismo e um caso onde o reducionismo falha [1,0]

📁 **Aula 02**

Duas definições e **um exemplo autoral em Computação**. O exemplo é o que vale a nota —
não copie exemplo pronto.

- **Positivismo**: conhecimento válido é o que deriva da observação empírica.
- **Reducionismo**: explicar o todo decompondo-o em partes.

Para o exemplo de onde o reducionismo **não** se aplica, pense em fenômenos de Computação
que **emergem da interação** e desaparecem quando você olha as partes isoladas. Direções
possíveis (escolha uma e desenvolva com suas palavras):

- desempenho de sistema distribuído — analisar cada nó isolado não prevê o comportamento do conjunto
- deadlock — não existe em nenhum processo isolado, só na relação entre eles
- usabilidade — testar cada tela separadamente não diz se o fluxo funciona
- segurança — cada componente pode estar correto e a composição ser vulnerável

Escolha o que você conseguir defender numa arguição, porque isso pode voltar na banca.

---

## Questão 4 — Tipos de pesquisa [1,2]

📁 **Aula 03** — a aula é literalmente estruturada nesses três eixos.

**a) Quanto à natureza**
- **Primária**: gera conhecimento novo por experimento, entrevista, observação
- **Secundária**: só a partir de trabalhos já publicados. Duas formas: mapeamento sistemático e revisão sistemática
- **Terciária**: revisão sistemática **sobre** revisões sistemáticas

**b) Quanto aos objetivos**
- **Exploratória**: sem hipótese definida; examina fenômenos buscando anomalias que virem base para estudo posterior
- **Descritiva**: obtém dados consistentes sobre uma realidade, sem interferência do pesquisador e sem tentar explicar — apenas descreve ou categoriza
- **Explicativa**: "a pesquisa científica por excelência" — além de analisar os dados, busca causas e fatores determinantes
- **De design/projeto**: tentativa de determinar **como as coisas poderiam ser**

**c) Quanto aos procedimentos técnicos**
- **Bibliográfica** — artigos, teses, livros indexados
- **Documental** — documentos ainda não sistematizados: relatórios de empresa, arquivos de órgãos públicos, bancos de dados
- **Experimental** — o pesquisador **manipula** um aspecto da realidade
- **Não experimental / observacional** — estuda sem intervir. Inclui o **quase-experimento**, quando o controle é relaxado (amostra por conveniência, ex.: alunos voluntários)
- **De levantamento** — questionários a um grupo
- **Pesquisa-ação** — o pesquisador interage e se envolve; foca design; exige um **dono do problema**
- **Etnográfica** — o pesquisador mergulha no grupo social. Caso especial: participação observacional
- **Estudo de caso** — em duas variedades: **exploratório** (estudar em profundidade para levantar hipóteses) e **confirmatório** (mostrar que a teoria se confirma na prática)
- **Triangulação** — abordagem mista, evidências por técnicas diferentes

---

## Questão 5 — Os cinco tipos por maturidade [1,2]

📁 **Aula 04** (é a aula inteira)

A escala é **crescente em maturidade**. Deixe isso explícito na resposta.

1. **Apresentação de um produto** — "fiz algo novo, eis meu produto". Aceitável em áreas emergentes, onde a pesquisa é exploratória e comparar é difícil. A aula é dura aqui: *"se uma ferramenta construída justificasse o título de mestre, as universidades distribuiriam diplomas a todos os analistas e programadores"*. Artigos tipo "manual da ferramenta" devem ser evitados.

2. **Apresentação de algo diferente** — outra forma de resolver um problema. Comparação simples entre técnicas, sem rigor estatístico, com um ou dois estudos de caso confirmatórios. Aceito se a argumentação convencer. Dica da aula: estruturar como **tabela comparativa** de artefatos × características, com os artefatos escolhidos por mapeamento sistemático e critério objetivo.

3. **Apresentação de algo presumivelmente melhor** — propõe-se algo melhor, com argumentação. Aqui entra a **métrica**: afirmar que "X é mais fácil de usar que Y" não tem fundamento sem definir o que significa "fácil de usar".

4. **Apresentação de algo reconhecidamente melhor** — resultados demonstrados por **testes padronizados e internacionalmente aceitos**. Típico de boas teses de doutorado. A aula observa algo contraintuitivo: é *"a pesquisa mais fácil de executar"*, e a dificuldade está em **achar uma boa hipótese**.

5. **Apresentação de uma prova** — demonstração formal pelas regras da lógica. Exigida em áreas como métodos formais e compiladores.

Fechamento útil: a aula também separa **três estilos** — pesquisa formal (ferramenta: lógica), empírica (ferramenta: estatística) e exploratória (ferramenta: argumentação).

---

## Questão 6 — Formulação do objetivo [0,7]

📁 **Aulas 05 e 06**, seção "Formulação do Objetivo"

Os aspectos que a aula lista:

- O objetivo deve ser **diretamente verificável ao final do trabalho**
- Expresso como **condição não trivial** cujo sucesso possa ser verificado
- **Verbos adequados**: demonstrar, provar, melhorar
- **Verbos inadequados**: propor, estudar, apresentar — porque a verificação é trivial (só são aceitáveis se o objeto for original)
- **Extensão compatível com o tempo do curso** — nem trivial demais, nem complexo demais
- Não confundir o **objetivo** com os **meios** de atingi-lo (o exemplo da aula: quem quer eficiência em compressão de texto e define como objetivo "definir um novo modelo de redes neurais" trocou o fim pelo meio)
- Não confundir objetivo com **tema**

Vale citar as quatro perguntas que a aula diz que o avaliador se faz ao ler a monografia:
qual é a questão de pesquisa; é uma boa questão; ela foi respondida adequadamente; houve
contribuição ao conhecimento.

---

## Questão 7 — Objetivo geral × específicos, com exemplo [1,0]

📁 **Aulas 05 e 06**

A distinção que a aula faz, e que é a resposta:

- Específicos seguem a **mesma regra** do geral: não triviais e verificáveis ao final
- ⚠️ **Objetivos específicos NÃO são etapas do trabalho — são subprodutos.** Este é o ponto que a professora destaca e provavelmente o que ela quer ver
- Cada específico deve indicar contribuição ao conhecimento: hipótese a demonstrar, teoria a refinar ou refutar
- São **detalhamentos** do geral. Se o geral é provar uma hipótese, os específicos estabelecem a prova de condições associadas a ela

O exemplo da aula (use como **modelo**, mas escreva um seu — a questão pede "cite um
exemplo", e um exemplo próprio vale mais):

> Geral: verificar se equipes autogerenciadas funcionam melhor que equipes com gerente.
> Específicos: destrinchar o que significa "melhor" — são mais produtivas? seus membros se
> sentem mais felizes? seus produtos são melhores, segundo alguma métrica definida?

O padrão a imitar: **o objetivo geral contém um termo vago; os específicos são as dimensões
que dão significado a esse termo.**

---

## Questão 8 — Procedimento metodológico [1,0]

📁 **Aulas 05 e 06**

Definição da aula: *"a sequência de passos necessários para demonstrar que o objetivo
proposto foi atingido"* — se os passos forem executados corretamente, os resultados devem
ser convincentes.

Por que é fundamental:
- É o que liga objetivo e hipótese à **evidência**; sem ele não há como comprovar ou refutar
- Deve indicar o que será feito: revisão sistemática, entrevistas, protótipos, modelos
  teóricos, experimentos, e **como os dados serão organizados e comparados**
- Em pesquisa empírica, precisa detalhar **como as amostras serão colhidas, analisadas e
  julgadas por testes estatísticos**
- A aula avisa: **não basta ser uma lista de passos**. Ter grupo com ferramenta e grupo de
  controle "até poderia ser parte de um procedimento, mas não é suficiente"
- *"O aspecto mais importante de uma monografia é o pensamento crítico, não apenas a coleta
  de informações"*

Se quiser um parágrafo a mais, a aula alerta que trabalhos restritos a questionário +
tabulação + gráficos **não têm validade se não trouxerem informação nova**.

---

## Questão 9 — Aplicação: reconhecimento facial em baixa iluminação [1,2]

📁 **Aulas 05 e 06** — mas aqui **não há resposta nos slides**. Você tem que produzir.

Esta é a questão que mede se você entendeu as outras. Vale mais que qualquer definição
decorada, e é a que mais se parece com o que você vai fazer no TCC.

O que cada item precisa entregar:

**a) Justificativa** — por que o problema importa. Pense em: onde reconhecimento facial é
usado em condição de baixa luz (segurança pública, controle de acesso noturno, veicular), e
qual o custo do erro nesse cenário. A aula diz que justificar o problema é *menos*
importante que justificar a hipótese — mas o item pede o problema.

**b) Objetivo geral** — aplique a Questão 6 em você mesmo. Verbo verificável. Não use
"propor" nem "estudar". Não confunda o objetivo com o meio (o meio aqui é o aprendizado
profundo; o objetivo é o ganho de precisão).

**c) Hipótese** — definição da aula: *"afirmação da qual não se sabe, a princípio, se é
verdadeira ou falsa"*. Os dois modelos que ela dá:

> "O uso de redes neurais convolucionais pode aumentar a precisão na identificação do
> *Aedes aegypti* em imagens capturadas por câmeras de baixo custo."

> "A aplicação de um modelo baseado em aprendizado profundo pode prever falhas em sistemas
> de ar-condicionado com uma taxa de acerto superior a 90%."

Repare na forma: **[técnica] aplicada a [problema] produz [efeito mensurável]**. A segunda
inclui um limiar numérico — vale considerar fazer o mesmo.

**d) Justificativa da hipótese** — a aula é enfática: *"mais importante do que justificar o
problema de pesquisa é justificar a escolha da hipótese"*. E diz o que serve como
evidência: **referências a trabalhos que mostraram resultado correlato**, ou **dados
preliminares colhidos pelo próprio autor**, ou **estudo de caso exploratório**.

Ou seja: aqui você precisa apontar por que apostar em aprendizado profundo é aposta
razoável para este problema — não só afirmar que é.

---

## Questão 10 — Revisão × mapeamento sistemático [1,0]

📁 **Aula 03** (a distinção) e **Aulas 07 e 08** (as vantagens)

**A diferença principal** — está nos dois exemplos da Aula 03, e a chave é o **tipo de
pergunta**:

| | Mapeamento sistemático | Revisão sistemática |
|---|---|---|
| Pergunta | "Quais são as principais tendências e aplicações de IA na medicina?" | "Redes neurais profundas têm maior precisão na detecção de câncer de mama que métodos tradicionais?" |
| Objetivo | **Panorama**: quantos artigos existem, como se classificam, quais algoritmos aparecem mais, como evoluiu ao longo dos anos | **Resposta**: comparar métricas de desempenho, ver se há consenso ou conflito, sintetizar criticamente |
| Resultado | Mapa da área, identificando tendências e **lacunas** | Resposta baseada em evidência acumulada |

Em uma frase: **o mapeamento pergunta "o que existe?"; a revisão pergunta "o que é
verdade?"**

**Vantagens da pesquisa bibliográfica sistemática** (Aulas 07/08, protocolo de Kitchenham &
Charters): reprodutibilidade, redução de viés na seleção, critérios explícitos de inclusão
e exclusão, cobertura verificável, avaliação de qualidade dos estudos.

A Aula 07 traz dois avisos que valem meio ponto de argumentação:
- **"Síndrome da interseção esquecida"** — quem não faz a busca direito reinventa a roda
- **"Evite o fundamento vazio"** — não fundamente um trabalho numa negação ("não encontrei
  nada parecido"). Mostre o que outros fizeram e depois em que o seu difere

---

## Antes de entregar

- [ ] Cada resposta está **com suas palavras**? A professora conhece os slides dela de cor
- [ ] Os exemplos das questões 3, 7 e 9 são **seus**, não os da aula?
- [ ] Peso e extensão batem? A Q2 vale 0,5 e a Q1 vale 1,2 — não escreva o mesmo tanto nas duas
- [ ] **Impressa**, conforme o Plano de Ensino
- [ ] Nome e data preenchidos

Uma observação prática: as questões 5, 6, 7, 8 e 9 são exatamente o vocabulário que a banca
vai usar na qualificação em dezembro, e o mesmo que você precisa para escrever o projeto.
Vale escrever essas com atenção — é estudo que você usa duas vezes.
