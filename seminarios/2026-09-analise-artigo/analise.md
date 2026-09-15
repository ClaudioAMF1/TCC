# Análise do artigo científico

**Aluno:** Claudio Meireles. **Disciplina:** Projeto Capstone I, IDP, 2026.2.

## 1. Escolha do recorte e do artigo

A área de interesse é cibersegurança, mas o tema do TCC ainda não foi definido. Para esta atividade, adota-se **priorização de vulnerabilidades** como recorte provisório. Ele já aparece como possibilidade no documento `temas/04-avaliacao-da-area.md` e permite investigar uma decisão concreta: como selecionar correções quando a capacidade de trabalho é limitada.

Essa decisão não significa aceitar o tema L1 como definitivo nem descartar o candidato N3. Também não implica assumir que as hipóteses ou afirmações de originalidade dos documentos antigos estejam demonstradas. A finalidade aqui é selecionar uma pesquisa relevante e aprender com seu desenho, seus resultados e suas limitações.

O artigo escolhido é:

> KOSCINSKI, Viktoria; NELSON, Mark; OKUTAN, Ahmet; FALSO, Robert; MIRAKHORLI, Mehdi. Conflicting Scores, Confusing Signals: An Empirical Study of Vulnerability Scoring Systems. In: Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security. New York: ACM, 2025. p. 1904–1918. DOI: [10.1145/3719027.3765210](https://doi.org/10.1145/3719027.3765210).

A publicação nos anais foi verificada pelo registro do DOI e pela [programação oficial da CCS 2025](https://www.sigsac.org/ccs/CCS2025/schedule/). A leitura integral utilizou a [versão aberta dos autores, arXiv:2508.13644v1](https://arxiv.org/abs/2508.13644), de 19 de agosto de 2025. A versão aberta tem 15 páginas e conserva campos editoriais provisórios. O DOI válido é o da ACM acima, não o campo de exemplo que aparece nesse PDF. As seções e páginas citadas nesta análise referem-se ao arXiv v1; não foi feita comparação integral com o texto diagramado final da editora.

### Por que é um artigo original

Os autores apresentam uma análise empírica própria, com unidades de análise definidas, comparação de sistemas e resultados obtidos a partir dos dados. Usar fontes públicas não transforma a pesquisa em revisão bibliográfica. A contribuição está no desenho e na análise realizada. O trabalho também possui uma seção de trabalhos relacionados, mas sua atividade principal é empírica.

A expressão dos autores de que seria a primeira comparação desse tipo é uma **alegação de posicionamento na literatura**. Para demonstrar independentemente que nenhum trabalho anterior realizou comparação equivalente, seria necessária uma revisão mais abrangente. Não é necessário repetir essa alegação como fato absoluto para justificar que o artigo relata pesquisa original.

### Critérios de relevância

| Critério | Evidência do artigo | Relevância para um possível TCC |
|---|---|---|
| Aderência à área | Gestão e priorização de vulnerabilidades | Trata de uma decisão defensiva em cibersegurança |
| Questão mensurável | Comparação das saídas de quatro sistemas | Permite avaliar concordância e diferenças na seleção |
| Base empírica | 600 CVEs no estudo principal | Fornece referência de população e unidades de análise |
| Transparência | [Dados, scripts e figuras públicos](https://github.com/SoftwareDesignLab/Vulnerability-Scoring-Systems-Comparison) | Permite inspeção e uma replicação parcial, a planejar |
| Atualidade | Publicação de 2025, dados principais de 2024 | Referência recente, sem confundir data do artigo com data dos dados |
| Potencial de aprofundamento | Limitações de contexto, limiar e temporalidade | Orienta perguntas de pesquisa, cuja novidade ainda precisa ser verificada |

O prestígio do veículo é um critério complementar. Não garante a validade de cada conclusão nem substitui a leitura crítica. Não foi adotado número de citações do artigo, porque essa contagem não foi conferida em uma base com data e cobertura definidas.

### Procedimento de busca

O arquivo [protocolo-busca.md](protocolo-busca.md) apresenta o procedimento proposto para a seleção via CAFe e distingue o que foi efetivamente feito nesta sessão. A pesquisa pública, a leitura integral e a inspeção do repositório dos autores foram realizadas. A busca autenticada ainda não foi executada, portanto não há um fluxo de seleção com quantidades inventadas.

## 2. Métricas e classificação

O artigo foi publicado em **conferência**. Segue-se o ramo correspondente do enunciado. JIF Percentile e Highest Percentile do Scopus pertencem à alternativa destinada a periódicos e não são exigidos simultaneamente para esta escolha.

| Item | Resultado | Base, período e ressalva |
|---|---|---|
| Rank CORE | **A*** | Portal CORE, fonte **ICORE2026**, consultado em 15/09/2026 |
| Classificação oficial documentada | **A1** | Qualis **Eventos**, área Computação, lista **2017–2020**, p. 9 |
| Correspondência por h5 | **A1 para h5 ≥ 35** | Relatório 2017–2020, p. 2; critério mantido no relatório 2021–2024, página impressa 11 |
| h5 histórico | **77** | Lista **provisória de 2019** disponível em página acadêmica da PUC-Rio; não é uma consulta atual |
| h5 atual no Google Scholar Metrics | **Não verificado** | Consulta bloqueada por detecção de tráfego automatizado. Requer confirmação e registro da janela de anos |

Fontes: [CORE](https://portal.core.edu.au/conf-ranks/?by=all&search=security), [CAPES 2017–2020](https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/avaliacao/09012022_RELATORIOQUALISEVENTOS20172020COMPUTACAO.PDF/@@display-file/file), [CAPES 2021–2024](https://www.gov.br/capes/pt-br/acesso-a-informacao/acoes-e-programas/avaliacao/sobre-a-avaliacao/areas-avaliacao/sobre-as-areas-de-avaliacao/colegio-de-ciencias-exatas-tecnologicas-e-multidisciplinar/ciencias-exatas-e-da-terra/Computao.pdf/@@display-file/file), [registro histórico de 2019](https://www-di.inf.puc-rio.br/~endler/qualis/QualisEventosComputa%C3%A7%C3%A3o-2019Provis.pdf).

O h5 é o maior número h para o qual pelo menos h trabalhos publicados na janela de cinco anos considerada receberam pelo menos h citações cada. Trata-se do veículo e da janela usados no cálculo. Não é a quantidade de citações deste artigo e não é uma porcentagem. A edição e os anos da janela precisam acompanhar o valor.

### Correspondência dos estratos para eventos

| Faixa de h5 | Estrato de referência pelo critério da área |
|---|---|
| h5 ≥ 35 | A1 |
| 25 ≤ h5 < 35 | A2 |
| 20 ≤ h5 < 25 | A3 |
| 15 ≤ h5 < 20 | A4 |
| 12 ≤ h5 < 15 | B1 |
| 9 ≤ h5 < 12 | B2 |
| 6 ≤ h5 < 9 | B3 |
| 0 < h5 < 6 | B4 |

Essa tabela reproduz o critério quantitativo dos ciclos citados. A classificação final da CAPES pode incorporar ajustes qualitativos e indução. Para a CCS, há também a confirmação direta de A1 na lista oficial 2017–2020. Não se apresenta essa lista histórica como decisão oficial sobre um artigo de 2025.

### Terminologia do enunciado e Documento Técnico

O enunciado utiliza “Qualis Periódicos” também na alternativa para conferências. A designação técnica pertinente à CCS é **Qualis Eventos**. O estrato solicitado é apresentado com essa identificação para não confundir os dois procedimentos.

A [versão pública do Documento Técnico do Qualis Periódicos, janeiro de 2023](https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/avaliacao/avaliacao-quadrienal-2017/DocumentotcnicoQualisPeridicosfinal.pdf/@@display-file/file) traz, na página 13 do PDF (página impressa 10), a figura de correspondência para **percentis de periódicos**: A1 a partir de 87,5; A2 a partir de 75; A3 a partir de 62,5; A4 a partir de 50; B1 a partir de 37,5; B2 a partir de 25; B3 a partir de 12,5; B4 abaixo de 12,5. Cada faixa termina no início da seguinte.

**Não se compara h5 = 77 com percentil = 77.** São medidas diferentes. O documento descreve procedimentos de imputação para periódicos sem certos indicadores; não autoriza converter diretamente o número h5 em percentil. Também não se presume que as regras históricas sejam idênticas às do ciclo 2025–2028. A atividade deve usar o documento indicado pela professora, cuja cópia anexada ainda precisa ser conferida.

## 3. Análise da estrutura

### Título, autoria e identificação

O título combina uma formulação do problema com a identificação do objeto e da abordagem empírica. Sua segunda parte permite ao leitor reconhecer o escopo antes de abrir o texto. Autores e afiliações estabelecem responsabilidade acadêmica e identificação institucional. Os conceitos ACM e as palavras-chave favorecem recuperação em bases bibliográficas. Na apresentação, esses elementos devem ser explicados pela função que cumprem, sem transformar autoria ou instituição em garantia de correção.

### Resumo

O resumo reúne contexto, propósito, método e contribuição. Minha avaliação é que a indicação da amostra torna o desenho mais concreto, enquanto a formulação dos resultados poderia ser mais precisa com um efeito numérico central. Essa leitura dialoga com as Aulas 13 e 14: o resumo deve permitir reconhecer o conhecimento produzido, e não apenas o assunto estudado.

### Introdução — seção 1

A introdução estabelece o problema prático e apresenta a lacuna defendida pelos autores. As quatro perguntas de pesquisa organizam o restante do artigo: concordância entre sistemas, suporte à triagem, relação com exploração conhecida e comportamento por classes CWE. A função da seção é justificar por que a investigação deve ser realizada e tornar seus objetivos verificáveis.

Minha leitura crítica é que as perguntas sobre diferenças de pontuação e sobre utilidade operacional precisam ser distinguidas. Demonstrar diferença entre instrumentos não basta para demonstrar falha de todos eles, especialmente quando seus objetivos são diferentes.

### Fundamentos — seção 2

Esta seção explica os quatro sistemas usados. Ela fornece as definições necessárias para compreender o método e interpretar os resultados. CVSS, EPSS e SSVC expressam, respectivamente, severidade, probabilidade de exploração e orientação de ação conforme contexto. O Exploitability Index do estudo é o modelo de Okutan e Mirakhorli, que deve ser distinguido do produto homônimo da Microsoft.

A normalização das saídas para uma mesma faixa numérica facilita cálculos, mas não torna os conceitos equivalentes. A [documentação do EPSS](https://www.first.org/epss/faq) esclarece que o modelo estima exploração em 30 dias e não incorpora sozinho impacto e contexto organizacional.

### Metodologia — seção 3

O desenho é um estudo de caso incorporado, com vulnerabilidades como unidades de análise dentro do contexto Patch Tuesday. Metodologicamente, a comparação é observacional: os autores não distribuem organizações aleatoriamente entre sistemas nem medem diretamente um experimento de correções em empresas.

Um ponto importante para a apresentação é a existência de **populações analíticas diferentes**. O artigo descreve 600 casos no estudo principal, 458 com EPSS disponível no retrato utilizado e um conjunto adicional de 1.226 CVEs na análise temporal. Esses números não devem aparecer como se fossem etapas de exclusão de uma mesma amostra.

A seção informa coleta, atribuição de escores e instrumentos de análise. Minha avaliação considera positivos o detalhamento dos procedimentos e o pacote público. A reprodutibilidade, porém, depende de conferir datas, versões, dados ausentes e regras operacionais. A existência do repositório não prova que todos os resultados já tenham sido reproduzidos nesta atividade.

### Resultados — seção 4

Os resultados seguem as perguntas de pesquisa. Esse paralelismo facilita verificar se os objetivos apresentados na introdução foram respondidos. Figuras e tabelas sustentam as afirmações, e o texto apresenta sínteses dos achados.

Para a exposição oral, foram selecionados resultados que permitem explicar a pesquisa sem sobrecarregar os slides: baixa concordância categórica, listas ampliadas por empates e a proporção de CVEs com EPSS elevado antes da inclusão no KEV. A escolha desses resultados não substitui a leitura das demais análises.

O gráfico do seminário transforma os dados da Tabela 6 e do texto adjacente em três categorias exclusivas: 244 com máximo mensal anterior ≥ 0,5; 275 sem escore anterior; e 707 com registros anteriores abaixo desse limiar. O último valor é a diferença **1.226 − 244 − 275**. Essa derivação é identificada no slide. O denominador é o conjunto analisado no artigo, e **19,9% não é acurácia**.

### Ameaças à validade — seção 5

A seção delimita o que pode ser concluído a partir do desenho. A validade de construto pergunta se as medidas representam os conceitos de interesse. A validade interna considera a sustentação das inferências pelos dados e procedimentos. A validade externa trata da generalização para outras populações e contextos.

Na leitura crítica, merecem atenção a concentração em um fornecedor, a ausência de escores, o uso de retratos mensais e a interpretação de dados de exploração conhecida. Essas limitações não anulam automaticamente o trabalho; orientam a extensão das conclusões.

### Discussão — seção 6

A discussão interpreta os achados e apresenta implicações para prática e pesquisa. Sua função é explicar o significado dos resultados, ligando-os às perguntas e ao problema inicial.

Minha avaliação separa a evidência apresentada da força das recomendações. A baixa concordância entre instrumentos com finalidades diferentes pode ser esperada. A escolha de um limiar de 0,5 para um evento raro precisa de justificativa. Além disso, amostrar um dia por mês pode perder variações, e a data de inclusão no KEV não identifica necessariamente o início da exploração. Seria necessário um desenho adicional para concluir qual estratégia gera melhores decisões sob o mesmo orçamento de correções.

### Trabalhos relacionados — seção 7

Esta seção aparece depois da discussão. Ela posiciona o artigo em relação a estudos sobre pontuação, inconsistência, predição e contexto organizacional. Sua função é mostrar o que já se conhece e em que a contribuição se diferencia. A localização tardia é uma escolha de organização, não ausência de revisão da literatura.

Para o TCC, a lição é não fundamentar novidade apenas em “não encontrei outro estudo”. Aulas 07 e 08 e Aula 12 exigem uma comparação concreta com trabalhos anteriores e uma justificativa do problema.

### Conclusões — seção 8

As conclusões retomam a contribuição e suas implicações. A avaliação deve verificar se cada conclusão decorre dos resultados e respeita as limitações. Na fala, o encerramento enfatiza a necessidade de interpretar os escores dentro de suas finalidades, evitando declarar um vencedor universal.

### Referências, apêndices e artefato

As referências identificam o suporte teórico e empírico das afirmações. Os apêndices A e B acrescentam análises de correlação e de sobreposição entre rankings. O pacote de reprodução oferece dados, scripts e figuras. Juntos, esses elementos permitem rastrear e conferir o trabalho. Não equivalem a uma reprodução realizada pelo aluno.

## 4. Possível aproveitamento no TCC

**Pergunta exploratória:** com o mesmo limite de correções, como critérios baseados em CVSS, EPSS e evidência de exploração conhecida alteram a seleção de CVEs?

Um desenho inicial poderia delimitar fornecedores e período, conservar os dados disponíveis em cada instante e comparar regras sob um orçamento comum. Deveria prever tratamento explícito de ausências, versões dos modelos, empates e datas dos registros. Se o desfecho for futura inclusão no KEV, é preciso nomeá-lo dessa forma, sem descrevê-lo como toda exploração real. Informações que só ficaram disponíveis depois da decisão não podem ser usadas retroativamente como se já fossem conhecidas.

A contribuição, o conjunto de dados e o escopo ainda dependeriam de revisão atualizada e piloto. Não se afirma que essa extensão seja inédita. Também não se afirma que o artigo selecionado resolva a escolha do orientador.

## 5. Limites desta preparação

O material considera o enunciado fornecido, o repositório e as novas aulas. Os cinco anexos específicos da atividade não foram localizados: dois tutoriais da Biblioteca do IDP, o Documento Técnico fornecido pela professora e dois exemplos de análise. Foi consultada a versão pública do Documento Técnico da CAPES. Ainda faltam a seleção autenticada via CAFe e a confirmação direta do h5 atual. Esses pontos estão destacados no roteiro e nos slides, para que não sejam confundidos com etapas concluídas.
