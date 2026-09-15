# Roteiro de apresentação

**Claudio Meireles · Projeto Capstone I · IDP · 2026.2**

Artigo: *Conflicting Scores, Confusing Signals: An Empirical Study of Vulnerability Scoring Systems*, Koscinski et al., ACM CCS 2025. DOI: [10.1145/3719027.3765210](https://doi.org/10.1145/3719027.3765210).

**Situação:** material preparado para ensaio. A busca na ACM pelo acesso CAFe do IDP foi concluída e documentada: 44 resultados. Faltam a conferência do h5 atual no Google Scholar e a comparação com os cinco anexos específicos da atividade, que não estavam acessíveis. O slide 3 descreve o procedimento realizado; o slide 6 distingue métricas verificadas de confirmação pendente.

**Duração planejada:** 13min05s, com 1min55s de margem até o limite de 15 minutos. Os tempos são metas de ensaio, não uma medição da sua fala. As referências nas notas não fazem parte da leitura oral.

**Uso:** ensaie com suas próprias palavras, evitando ler as referências. O recorte é provisório e não define o tema final do TCC. Os dias informados pela atividade são 29/09/2026 e 01/10/2026. A data individual não foi presumida pela ordem alfabética.

## Slide 1 — Priorização de vulnerabilidades

Tempo sugerido: 25s. Acumulado: 00:25.

O artigo que escolhi analisa como diferentes sistemas orientam a priorização de vulnerabilidades. Minha área de interesse é cibersegurança e o tema do TCC ainda está em definição. Por isso, uso gestão de vulnerabilidades como um recorte provisório para este seminário. Vou explicar a seleção, a classificação do veículo e a estrutura da pesquisa.

## Slide 2 — Recorte provisório do TCC

Tempo sugerido: 45s. Acumulado: 01:10.

O problema que orienta a escolha é simples: uma equipe encontra muitas vulnerabilidades, mas não consegue corrigir todas ao mesmo tempo. Ela precisa decidir quais tratar primeiro. No meu repositório, essa linha já aparece entre as possibilidades de TCC. O artigo ajuda a transformar uma área ampla em uma pergunta que pode ser investigada com dados: como a escolha do critério muda a lista de prioridades? Ainda será necessário delimitar população, período e contribuição com o orientador. O seminário serve para fundamentar essa decisão.

## Slide 3 — Seleção: busca e triagem

Tempo sugerido: 65s. Acumulado: 02:15.

A seleção começou pela delimitação provisória do problema e pela busca pública. Depois, executei a consulta na ACM pelo Portal CAPES via CAFe, com a instituição IDP reconhecida. A expressão foi vulnerability prioritization entre aspas, combinada com CVSS, EPSS ou SSVC. A busca em todos os campos recuperou 44 resultados na coleção de textos completos da ACM. Os filtros da interface apareciam como recurso Premium; por isso, período de 2021 a 2026 e pesquisa original foram critérios de triagem manual. O artigo escolhido apareceu na primeira página. Comparei a pertinência de entradas sobre EPSS e priorização adaptativa, mas escolhi a comparação de quatro sistemas por sua relação direta com o problema, método explícito e dados públicos. A análise integral usa a versão aberta dos autores. O protocolo e as capturas registram a consulta, sem apresentar a busca exploratória como revisão exaustiva.

## Slide 4 — Artigo selecionado

Tempo sugerido: 55s. Acumulado: 03:10.

O título é Conflicting Scores, Confusing Signals: An Empirical Study of Vulnerability Scoring Systems. Viktoria Koscinski e outros quatro autores publicaram o trabalho nos anais da ACM CCS de 2025. A contribuição original está na comparação empírica de quatro sistemas sobre um mesmo conjunto de vulnerabilidades, acompanhada de uma análise temporal do EPSS. Não se trata apenas de reunir opiniões da literatura. Os autores coletam dados, aplicam procedimentos de análise e apresentam resultados próprios. Para a leitura detalhada, usei a versão aberta dos autores, identificada como arXiv versão 1, e confirmei a publicação na página da ACM, acessada a partir dos resultados da busca via CAFe, além do DOI e dos registros da conferência.

## Slide 5 — Relevância para o meu TCC

Tempo sugerido: 45s. Acumulado: 03:55.

A relevância não depende só do prestígio da conferência. O assunto corresponde a uma decisão concreta de defesa: priorizar correções. O trabalho reúne 600 vulnerabilidades no estudo principal, compara quatro sistemas e disponibiliza um pacote de reprodução. Isso permite conhecer o desenho metodológico antes de assumir um escopo de TCC. A publicação é de 2025, mas os dados principais são de 2024, uma distinção importante. A análise é pertinente e tecnicamente aproveitável, embora a viabilidade de uma extensão ainda precise de piloto e revisão bibliográfica.

## Slide 6 — Métricas da conferência

Tempo sugerido: 65s. Acumulado: 05:00.

Como o artigo é de conferência, o caminho correspondente no enunciado é h5, classificação Qualis e rank CORE. Confirmei A estrela no portal CORE, na edição ICORE 2026. A lista oficial de eventos da CAPES para 2017 a 2020 classifica a CCS como A1. O corte por h5 para A1 é 35, critério também mantido no relatório do ciclo 2021 a 2024. Existe um registro histórico de h5 igual a 77 na lista provisória de 2019, mas ele não é a métrica atual. O Google Scholar bloqueou a consulta nesta sessão, então o h5 atual permanece pendente. Também é preciso distinguir Qualis Eventos de Qualis Periódicos: a tabela de percentis de revistas não deve ser aplicada diretamente ao h5 de conferências.

## Slide 7 — Mapa da estrutura do artigo

Tempo sugerido: 45s. Acumulado: 05:45.

O artigo tem uma organização própria. Começa pelos elementos de identificação e pelo resumo. Depois apresenta introdução, fundamentos e configuração do estudo de caso. Os resultados estão organizados pelas quatro perguntas de pesquisa. Ameaças à validade e discussão aparecem em seções separadas. Os trabalhos relacionados vêm depois da discussão, antes das conclusões. Por fim, há referências e dois apêndices. Essa ordem mostra por que analisar a estrutura vai além de procurar uma sequência rígida de introdução, método, resultado e conclusão. O importante é identificar a função que cada seção cumpre.

## Slide 8 — Título, resumo e indexação

Tempo sugerido: 40s. Acumulado: 06:25.

O título tem duas partes. A primeira destaca o problema dos sinais divergentes, e a segunda informa o objeto e o tipo de estudo. A autoria e as afiliações permitem identificar os responsáveis pela pesquisa. O resumo apresenta o problema, a comparação empírica e a dimensão da amostra, mas descreve os resultados de modo mais geral. Minha avaliação é que ele poderia indicar um efeito numérico para tornar a contribuição mais precisa. As palavras-chave e os conceitos de classificação da ACM ajudam a indexar e recuperar o trabalho nas bases.

## Slide 9 — Introdução e fundamentos

Tempo sugerido: 60s. Acumulado: 07:25.

A introdução contextualiza a limitação de recursos para corrigir vulnerabilidades e apresenta a lacuna que os autores pretendem enfrentar: comparar sistemas diferentes sobre os mesmos casos. Ela termina com quatro perguntas, sobre concordância, esforço de triagem, exploração conhecida e tipos de fraqueza. A seção de fundamentos explica os sistemas. CVSS expressa severidade técnica. EPSS estima probabilidade de exploração nos próximos trinta dias. SSVC orienta uma decisão considerando o contexto. Já o Exploitability Index usado no estudo combina um modelo e informações do produto. Ele é o modelo de Okutan e Mirakhorli, não o índice homônimo da Microsoft. Essa distinção conceitual é essencial para interpretar a comparação.

## Slide 10 — Metodologia e unidades de análise

Tempo sugerido: 75s. Acumulado: 08:40.

A metodologia descreve um estudo de caso incorporado: o caso é o Patch Tuesday da Microsoft e cada vulnerabilidade é uma unidade de análise. O conjunto principal contém 600 CVEs divulgados entre abril e julho de 2024. Os autores usam dados da Microsoft e do NVD, calculam ou coletam os diferentes escores e comparam suas saídas. O retrato do EPSS é de 9 de julho de 2024. Somente 458 CVEs tinham esse escore, por isso certas análises usam 458, não 600. Há ainda uma análise separada com 1.226 CVEs do KEV e observações mensais de EPSS. Concordância, correlação, agrupamentos por pontuação e sobreposição entre listas são os principais instrumentos. Essas escolhas precisam ser explicitadas para que outra pessoa consiga avaliar ou repetir o procedimento.

## Slide 11 — Resultados organizados pelas perguntas

Tempo sugerido: 65s. Acumulado: 09:45.

A seção de resultados responde às perguntas da introdução. Na primeira, as medidas apontam baixa concordância entre os sistemas. Na segunda, os autores mostram que empates ampliam listas que deveriam conter poucos casos prioritários. Um exemplo é o top vinte de CVSS, que inclui 198 vulnerabilidades quando os empates são preservados. Nas listas de maior prioridade, somente cinco CVEs são comuns aos quatro sistemas na comparação reportada. A terceira pergunta examina a relação com exploração conhecida. A quarta considera as classes de fraqueza, mas muitos grupos têm poucos casos. A função desta seção é apresentar a evidência e o procedimento de leitura dos números. A interpretação mais ampla deve considerar as limitações que vêm depois.

## Slide 12 — EPSS antes da inclusão no KEV

Tempo sugerido: 65s. Acumulado: 10:50.

Este gráfico reorganiza a tabela seis e o texto da seção quatro ponto três ponto dois em três grupos exclusivos. Entre 1.226 CVEs do catálogo analisado, 244 tiveram ao menos um retrato mensal com EPSS maior ou igual a meio antes da inclusão no KEV. Outros 275 não tinham escore anterior. O restante, 707, tinha observações, mas nenhuma atingiu esse limiar. Os 19,9 por cento são uma proporção nesse conjunto de CVEs conhecidos, não a acurácia do EPSS. A data de entrada no catálogo também não identifica necessariamente a primeira exploração. Minha leitura crítica é que avaliar utilidade preditiva exige justificar o limiar, a janela temporal e o conjunto de comparação.

## Slide 13 — Discussão, limites e conclusão

Tempo sugerido: 70s. Acumulado: 12:00.

Na discussão, os autores interpretam as divergências e defendem que os escores sejam considerados junto ao contexto da organização. A seção de ameaças à validade reconhece restrições de amostra e de medição. Na minha análise, há cuidados adicionais: normalizar escalas não faz os sistemas medirem o mesmo conceito, fotografias mensais podem perder variações diárias e entrada no KEV é um registro público, não o instante exato do ataque. Por isso, os resultados não demonstram sozinhos que um sistema seja universalmente melhor ou que o EPSS seja inútil. Os trabalhos relacionados posicionam a contribuição diante das pesquisas anteriores. As conclusões retomam as perguntas e as implicações, enquanto referências e apêndices permitem verificar as bases e os detalhes da análise.

## Slide 14 — Aproveitamento possível no TCC

Tempo sugerido: 45s. Acumulado: 12:45.

O artigo é útil porque oferece tanto um método quanto pontos que merecem investigação. Um possível TCC poderia comparar critérios de priorização mantendo o mesmo orçamento de correções, com registros históricos coletados antes do evento de interesse. A pergunta inicial seria quanto a lista selecionada muda entre CVSS, EPSS e uma regra que considere exploração conhecida. Para isso, seria preciso definir fornecedores, período, orçamento e medida de resultado, além de tratar dados ausentes e versões dos modelos. Isso é uma proposta exploratória. Ainda não afirmo que seja inédita nem que substitua as outras opções de tema registradas no repositório.

## Slide 15 — Referências principais

Tempo sugerido: 20s. Acumulado: 13:05.

As referências completas e o registro das fontes estão no material de apoio. A contribuição deste seminário é analisar criticamente uma pesquisa original que pode orientar a delimitação do meu TCC em cibersegurança. A escolha do artigo fundamenta um caminho possível, mantendo a decisão do tema em aberto.

## Perguntas que podem aparecer

**Você já definiu seu tema?** Ainda não. A área é cibersegurança. A priorização de vulnerabilidades é um recorte provisório, sustentado por literatura e por uma possibilidade já registrada no repositório.

**Por que esse artigo é original?** Ele apresenta coleta, análise e resultados próprios de uma comparação empírica. Usar dados públicos não retira a originalidade de uma análise. A alegação dos autores de serem os primeiros deve ser tratada como posicionamento do artigo, não como prova independente de que nenhum estudo anterior existe.

**O artigo comprova que EPSS não funciona?** Não. Os resultados dependem da população, dos retratos mensais, do limiar e do evento de referência. Eles motivam uma avaliação mais cuidadosa, mas não medem, sozinhos, acurácia ou superioridade geral.

**Por que aparecem 600, 458 e 1.226?** São conjuntos distintos: estudo principal, subconjunto com EPSS disponível e análise temporal adicional do catálogo KEV.

**Qual é a diferença entre CVE e CWE?** CVE identifica uma vulnerabilidade específica. CWE classifica tipos de fraqueza, como erros de validação ou de controle de acesso. Muitos CVEs podem estar associados a uma mesma CWE.

**h5 e rank CORE são métricas do artigo?** Não. São informações sobre o veículo. Não substituem a avaliação do método e das conclusões do artigo individual.

**Por que não há JIF ou Highest Percentile?** O trabalho foi publicado em conferência. O enunciado prevê um caminho distinto para esse tipo de publicação. A tabela de percentis de periódicos não é aplicada diretamente ao h5 de eventos.

**Por que Qualis Eventos se o enunciado diz Qualis Periódicos?** A formulação do enunciado usa esse termo também para conferências. A nomenclatura técnica da CAPES é Qualis Eventos. No seminário, apresento o estrato solicitado e identifico corretamente a origem, o ciclo e o critério. O anexo da professora deve ser conferido antes da entrega.

**O h5 é 77 atualmente?** Não foi possível verificar o valor atual. O 77 é um registro histórico em lista provisória de 2019. Ele não deve ser apresentado como consulta atual do Google Scholar.

**A proposta de TCC é inédita?** Isso ainda não foi demonstrado. A extensão precisa de revisão atualizada e de um piloto antes de definir sua contribuição.

## Ajustes antes da apresentação

1. Revisar o registro da busca já realizada via CAFe e suas três capturas na pasta `evidencias/`. A consulta retornou 44 resultados; o recorte temporal foi critério manual, pois os filtros da interface eram Premium.
2. Confirmar o h5 no Google Scholar Metrics, registrando nome da conferência, janela de anos e edição. Atualizar slide 6 e sua fala.
3. Conferir os tutoriais e os dois exemplos de análise da professora. A versão do Documento Técnico obtida publicamente é a da CAPES, de janeiro de 2023.
4. Reensaiar após essas atualizações. Cortar repetições se o tempo passar de 14 minutos.
