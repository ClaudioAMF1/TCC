# Roteiro da simulação de defesa

Versão de 22/11/2026, igual às notas da apresentação `TCC1_apresentacao_revisao_redacional_20261121.pptx`. São 15 minutos de apresentação e 10 de perguntas. As falas somam cerca de 9 minutos, num ritmo calmo, o que deixa folga para pausas. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra: leia algumas vezes e fale com as suas palavras, mantendo os números exatos.

## Slide 1. Abertura (40 s)

Bom dia. Esta é a apresentação do meu projeto de Capstone I, intitulado “Quem mais está dentro do aplicativo?”. A pesquisa se concentra nos aplicativos Android oficiais do governo brasileiro e na transparência sobre os SDKs de terceiros. Quero entender quais desses componentes estão presentes e se o que é informado ao cidadão sobre a coleta e o compartilhamento de dados é compatível com a evidência técnica. O objetivo deste semestre é apresentar um problema bem definido, o método e um piloto de viabilidade. A coleta principal e os testes das hipóteses serão realizados no Capstone II.

## Slide 2. Por que investigar as declarações dos apps públicos? (40 s)

Boa parte dos serviços públicos passou para o celular. Aplicativos como Meu INSS e Meu SUS Digital são usados por milhões de pessoas e frequentemente constituem a principal porta de entrada para esses serviços. Um aplicativo Android não contém apenas código desenvolvido pelo órgão responsável: ele pode integrar SDKs de mapas, notificações, análise de uso e outros serviços. Alguns componentes podem coletar identificadores ou informações de utilização. Essa possibilidade exige transparência, especialmente no setor público, onde a escolha de prestador pelo cidadão costuma ser limitada. Ressalto que encontrar uma biblioteca instalada não equivale a observar transmissão de dados.

## Slide 3. O que a literatura já demonstrou (40 s)

A literatura oferece três pontos de partida. Binns e colaboradores examinaram aproximadamente 959 mil aplicativos e encontraram referências a rastreadores distribuídas de maneira concentrada em poucas empresas; a medição é principalmente estática. Kollnig e outros autores discutiram o cenário anterior e posterior ao GDPR e os desafios de consentimento, sem que uma comparação temporal prove, isoladamente, o efeito de uma lei. Samarasinghe e colaboradores analisaram 1.166 aplicativos de governo de 71 países e observaram 269 que transmitiam dados do dispositivo a rastreadores conhecidos. Esses resultados justificam investigar o contexto brasileiro com atenção às declarações de privacidade.

## Slide 4. Lacuna e contribuição proposta (40 s)

A contribuição esperada tem três partes. Primeiro, estudar sistematicamente aplicativos federais, estaduais e municipais brasileiros, distinguindo serviços que podem tratar dados sensíveis. Segundo, confrontar a presença e a função dos SDKs com as categorias de dados e finalidades declaradas na política de privacidade e na seção Segurança dos dados da Google Play. Para uma subamostra, o confronto será ampliado aos fluxos efetivamente observados. Terceiro, verificar as diferenças entre detectores, porque a prevalência reportada pode variar conforme o instrumento. Uma divergência não é prova automática de infração à LGPD; é uma evidência para exame adicional.

## Slide 5. Pergunta e objetivos (45 s)

No texto do TCC, a pergunta foi formulada assim: “Em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado em suas políticas de privacidade e na seção Segurança dos dados da Google Play?”. O objetivo geral é medir a proporção de SDKs e de envios sem declaração compatível nos aplicativos governamentais brasileiros, à luz da LGPD. Para isso vou confirmar o corpus, detectar os componentes, comparar as declarações, observar uma subamostra dinamicamente e conferir a concordância dos detectores. A evidência estática e a de tráfego serão apresentadas separadamente.

## Slide 6. Hipóteses e verificação do instrumento (60 s)

A H1 é a principal: ao menos 10% dos pares aplicativo–SDK identificados não teriam declaração compatível, considerando categorias de dados e finalidades, e não apenas o nome comercial da biblioteca. O critério utiliza um intervalo de confiança de 95%. O limiar de 10% corresponde a ao menos um par sem declaração compatível em cada dez pares que possam ser avaliados. É uma escolha operacional para o teste, e não uma margem permitida pela LGPD. Andow relatou até 42,4% de inconsistências, mas em outro método e outra população, de modo que não posso comparar diretamente as duas taxas. A H2 é secundária: procura verificar se aplicativos governamentais que tratam dados sensíveis têm prevalência de SDKs menor do que os demais. A hipótese considera que essa prevalência não é menor. Os comerciais ficam como contexto; concordância entre detectores é checagem do instrumento sem hipótese própria.

## Slide 7. Procedimentos metodológicos (40 s)

O método é quantitativo e observacional. Primeiro, delimitar e conferir os aplicativos oficiais encontrados na Google Play. Segundo, caracterizá-los por esfera e tipo de serviço. Terceiro, obter a versão atual na Google Play quando possível, com data, versão e SHA-256. O AndroZoo será fonte complementar para reprodutibilidade e para medir defasagem entre a versão arquivada e a que o usuário instala. Quarto, aplicar os detectores e examinar suas divergências. Quinto, comparar resultados técnicos com políticas de privacidade e declarações na loja. Sexto, calcular proporções e intervalos e, para uma subamostra, observar fluxos de rede em cenários documentados.

## Slide 8. Corpus governamental preliminar (35 s)

A busca inicial produziu 396 aplicativos candidatos. Pela classificação preliminar de seus publicadores, 376 foram mantidos como oficiais: 85 federais, 199 estaduais e 92 municipais. Entre eles, 100 foram classificados preliminarmente como relacionados a serviços que podem tratar dados sensíveis, como saúde ou biometria. Vinte candidatos foram excluídos nesta etapa por divergências de titularidade. Esses números descrevem o corpus preparatório; a classificação ainda será conferida antes da coleta principal. O gráfico apresenta a distribuição por esfera, e não uma medida de rastreadores encontrados.

## Slide 9. O que significa declarar anúncios? (40 s)

Um dado descritivo da Google Play é a declaração de anúncios. Entre os 376 aplicativos governamentais classificados preliminarmente como oficiais, nenhum declarou exibir anúncios. Na primeira referência comercial, a informação aparece em 63 dos 190 aplicativos, ou 33,2%. Os intervalos de confiança mostrados dizem respeito apenas a essa declaração feita pelos publicadores. Não significam que os aplicativos do governo não incorporem SDKs de análise de uso ou de rastreamento. Também não uso a referência comercial como grupo de controle, pois sua coleta não foi planejada para um teste inferencial equivalente.

## Slide 10. Piloto: detectores não são equivalentes (40 s)

No piloto, utilizei 20 pacotes arquivados no AndroZoo e três detectores. O detector A buscou assinaturas de código na base do Exodus; B procurou assinaturas de rede em textos do pacote usando a mesma base; C utilizou assinaturas da Disconnect sobre os mesmos textos. As proporções de pacotes com detecção foram 75%, 95% e 80%, respectivamente. O kappa de Fleiss foi 0,52. Uma adjudicação interna considerou 88 de 123 detecções do B potenciais falsos positivos, principalmente por domínios genéricos. Retirá-las na análise de sensibilidade elevou o kappa a 0,69, mas isso não constitui validação independente por padrão de referência.

## Slide 11. Fonte dos APKs e reprodutibilidade (35 s)

Uma limitação prática apareceu na busca por pacotes. O AndroZoo possuía apenas 92 dos 396 candidatos governamentais da consulta histórica, ou 23,2%; na primeira referência comercial eram 160 de 190, ou 84,2%. Isso indica que depender apenas do acervo acadêmico poderia deixar muitos aplicativos oficiais de fora. Por isso o plano prevê coletar as versões atuais disponibilizadas na Google Play, com registro de hash, data e eventuais falhas. O AndroZoo continua relevante para recuperar versões específicas, medir defasagem e possibilitar reprodutibilidade onde os arquivos estiverem disponíveis.

## Slide 12. Revisão bibliográfica: situação atual (45 s)

A revisão sistemática seguiu um protocolo baseado em Kitchenham e no relato PRISMA 2020. As buscas retornaram 1.531 registros, reduzidos a 1.249 após deduplicação. A triagem encaminhou 357 registros para a leitura completa. Destes, há 71 propostas de inclusão e oito de exclusão, e 278 registros ainda sem decisão. Até 21 de novembro, eu conferi 18 das 79 decisões registradas, com leitura integral e avaliação de qualidade declarada. As notas individuais de QA1 a QA8 ainda não estão anexadas à planilha. Portanto, as 71 inclusões são propostas preliminares; o orientador concordou em deixar os 278 registros em aberto para o Capstone II, quando também confiro as outras 61 decisões.

## Slide 13. Limitações e próximos passos (45 s)

Entre as limitações, destaco que uma assinatura de código não prova execução nem transmissão, e que as políticas de privacidade podem declarar categorias de dados e finalidades sem nomear todos os SDKs. Há ainda limitações na seleção da revisão, na classificação do corpus, na disponibilidade de versões e na independência dos detectores. Até a entrega do Capstone I, a prioridade é incorporar o retorno do orientador e da simulação. No Capstone II serão concluídas a leitura e as decisões dos artigos pendentes, além da conferência das classificações do corpus, seguida da coleta das versões atuais, do confronto documental, da análise dinâmica de subamostra, da avaliação estatística e da discussão jurídica fundamentada.

## Slide 14. Conclusão (35 s)

Para concluir, o Capstone I apresenta um problema delimitado, um desenho metodológico e dados preparatórios suficientes para demonstrar viabilidade. O foco não é comparar o governo ao mercado, mas verificar se aquilo que os aplicativos públicos declaram sobre tratamento de dados é compatível com os componentes identificados e, onde houver observação dinâmica, com os fluxos realmente transmitidos. Essa distinção é fundamental para produzir resultados defensáveis sobre privacidade, transparência e dependência de fornecedores. Obrigado. Estou à disposição para as perguntas.

---

## Perguntas prováveis

**Como você decide que um aplicativo é oficial? Por que 20 saíram?**
Pelo nome jurídico do publicador, que a loja mostra em "Sobre o desenvolvedor". Treze eram empresas privadas com nome de serviço público e sete eram contas de pessoa física. A classificação será conferida antes da coleta principal.

**O que há de novo em relação a Samarasinghe et al.?**
O caso brasileiro separado por esfera e por dado sensível, o confronto entre o que cada aplicativo declara e o que ele embarca e envia, e a medida de concordância entre detectores sobre as mesmas versões dos pacotes.

**Ter o SDK no pacote prova que dados são enviados?**
Não. A análise estática mostra presença de código. O envio só é observado na análise dinâmica da subamostra. O texto separa presença, transmissão observada e declaração.

**Se o detector B teve 71,5% das detecções questionadas, por que mantê-lo?**
Ele não é a medida principal proposta. Como A e B usam a mesma base com métodos diferentes, a diferença ilustra o efeito do método, que a checagem do instrumento mede. Os 88 casos foram considerados falsos positivos potenciais na adjudicação interna, não confirmados por um padrão de referência externo.

**Como você vai obter os pacotes? Isso é permitido?**
Todos na versão atual da Google Play, que é a que o cidadão instala, com conta própria, registrando o hash e sem redistribuir os pacotes. O AndroZoo serve para outra pessoa reproduzir a análise e para medir a defasagem entre a versão arquivada e a atual. A coleta será testada em cinco aplicativos no início do Capstone II.

**Por que o limiar de 10% na H1?**
O valor representa pelo menos um par sem declaração compatível em cada dez pares avaliáveis. É um critério de interesse definido para a pesquisa, não um valor previsto em lei. O estudo de Andow encontrou até 42,4% com outra unidade de análise e outro método; serve de contexto, não de comparação direta, nem de parâmetro legal.

**O que "soberania de dados" quer dizer no seu trabalho?**
A capacidade do Estado de saber e decidir para onde vão os dados gerados nos seus serviços. Mede-se pela dependência de SDKs de terceiros e, na subamostra, pelos destinos observados. A presença de SDK de empresa estrangeira já mostra dependência de fornecedores estrangeiros; dizer que dados foram para o exterior exige a análise dinâmica. A nacionalidade do fornecedor ou o país de um IP não provam, sozinhos, uma transferência internacional.

**A ANPD não é uma autoridade?**
A ANPD tornou-se autarquia especial em 2022. Em 2026, a Lei 15.352 a transformou em agência reguladora, com a denominação Agência Nacional de Proteção de Dados. Os documentos anteriores preservam o nome institucional vigente à época.

**Quantos artigos a revisão incluiu?**
Até 13/11, foram registradas 71 propostas de inclusão e 8 de exclusão. Em 21/11, conferi 18 das 79 decisões, com leitura integral e avaliação de qualidade (12 propostas de inclusão e seis de exclusão). As notas QA por critério ainda não estão anexadas. As outras 61 e os 278 registros em aberto ficam para o início do Capstone II. A Seção 2.7 traz a síntese provisória.

**Por que você não compara com aplicativos comerciais?**
O governo tem obrigações próprias: a LGPD e a política de privacidade que ele mesmo publica. Por isso a referência principal é essa, e não o mercado. Uma comparação justa com o mercado exigiria uma amostra comercial sem viés, que a busca da loja não oferece, porque ela ordena por relevância e quase não devolve aplicativos comerciais pequenos. Os 252 comerciais ficam como contexto, sem teste de hipótese.

**O que conta como declaração compatível?**
A política não precisa necessariamente listar cada SDK pelo nome. Primeiro, identifico a função de coleta ou compartilhamento atribuída ao componente. Depois, verifico se a política ou a seção "Segurança dos dados" descreve categorias de dados e finalidades compatíveis. Informação insuficiente e política indisponível são registradas à parte, sem serem automaticamente tratadas como omissão.

**Por que mudou o foco desde a proposta?**
Por sugestão do orientador. Comparar com o mercado exigiria montar uma amostra comercial sem viés, um trabalho grande que não responde à pergunta mais importante: se o governo faz o que diz. O confronto com a própria declaração e com a LGPD responde a isso diretamente.

**Por que κ e não só a porcentagem de acordo?**
O κ desconta o acordo esperado ao acaso. Como prevalência muito alta deixa o κ instável, ele será reportado junto com os acordos positivo e negativo.

**Como as classificações foram feitas e conferidas?**
Responda como de fato aconteceu, incluindo as ferramentas usadas e o que o orientador avaliou. As duas classificações serão conferidas no início do Capstone II.

## Fontes de cada slide

| Slide | Onde está no projeto |
|---|---|
| 2 a 4 | Seções 1 e 2; Binns et al. (2018b); Kollnig et al. (2021a, 2021b); Samarasinghe et al. (2022) |
| 5 e 6 | Problema, objetivos, hipóteses e resultados esperados no texto-fonte atualizado |
| 7 | Seções 3.1 a 3.5 |
| 8 a 11 | Seção 3.6 |
| 12 | Seções 2.7 e 3.7 e Figura 1 |
| 13 | Seções 3.9, 3.12 e 3.13 |
