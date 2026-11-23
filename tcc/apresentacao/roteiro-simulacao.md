# Roteiro da simulação de defesa

Versão revisada em 21/11/2026, com foco nas declarações de privacidade dos aplicativos governamentais e nos indícios técnicos obtidos na análise dos pacotes. Os aplicativos comerciais ficam só como contexto. São 15 minutos de apresentação e 10 de perguntas. As falas abaixo somam cerca de 12 minutos, o que deixa folga para pausas. O mesmo texto está nas notas de cada slide. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra: leia algumas vezes e fale com as suas palavras, mantendo os números exatos.

## Slide 1. Abertura (40 s)

Bom dia. Meu nome é Claudio, e meu projeto se chama "Quem mais está dentro do aplicativo?". Meu trabalho investiga quais componentes de terceiros estão presentes em aplicativos do governo e se as informações publicadas sobre coleta e compartilhamento de dados são compatíveis com esses componentes. A presença de um SDK, sozinha, não prova envio de dados. Neste semestre, a entrega é o projeto: o problema, o método e os testes que mostram que ele é viável. A coleta principal fica para o Capstone II.

## Slide 2. Agenda (35 s)

Vou seguir a mesma ordem do texto do TCC. Na introdução, a motivação, a pergunta, os objetivos e as hipóteses. No referencial teórico, os estudos que servem de base e a lacuna que eles deixam. Nos procedimentos metodológicos, o método, o corpus, os dados preparatórios sobre anúncios, fonte dos pacotes e piloto dos detectores, a revisão sistemática e as limitações com os próximos passos. Fecho com a conclusão e as referências.

## Slide 3. Motivação (40 s)

Boa parte dos serviços públicos passou para o celular. Aplicativos como Meu INSS e Meu SUS Digital passam de 50 milhões de instalações cada e frequentemente constituem a principal porta de entrada para esses serviços. Um aplicativo Android não contém apenas código desenvolvido pelo órgão responsável: ele pode integrar SDKs de mapas, notificações, análise de uso e outros serviços. Alguns componentes podem coletar identificadores ou informações de utilização. Essa possibilidade exige transparência, especialmente no setor público, onde a escolha de prestador pelo cidadão costuma ser limitada. Ressalto que encontrar uma biblioteca instalada não equivale a observar transmissão de dados.

## Slide 4. Pergunta e objetivos (45 s)

São três coisas. Primeiro, o caso brasileiro: no estudo internacional, o Brasil aparece só em exemplos, sem separar esfera de governo nem os aplicativos que tratam dados sensíveis. Segundo, o confronto entre as declarações de privacidade e o que pode ser identificado tecnicamente. Vou verificar a função dos SDKs e as categorias e finalidades declaradas. Onde houver observação de tráfego, também vou comparar os destinatários efetivos. Uma divergência é um indício a investigar, não prova isolada de ilegalidade. Terceiro, o instrumento: vou rodar mais de um detector sobre os mesmos pacotes e medir quanto eles concordam, porque a taxa publicada depende da ferramenta usada.

## Slide 5. Hipóteses (50 s)

A pergunta de pesquisa é: em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado nas políticas de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo geral é medir a proporção de SDKs e de envios de dados sem declaração compatível. A presença de código é examinada na análise estática; os envios só podem ser confirmados pela análise dinâmica de uma subamostra. Os objetivos específicos são: confirmar quais aplicativos são de fato oficiais; detectar os SDKs por esfera de governo e por tratamento de dado sensível; confrontar o que for encontrado com a política de privacidade e com a seção "Segurança dos dados" da loja; observar numa subamostra para onde os dados vão, inclusive se saem do país; e medir a concordância entre os detectores.

> **Lembrete, não precisa falar.** Par aplicativo–SDK: cada SDK encontrado em cada app; para cada par, verifico se o que o SDK faz aparece nas declarações do app, pelo nome ou pela categoria e finalidade do dado. IC95% agrupado por app: os SDKs do mesmo app dependem da mesma política, então não são independentes, e o intervalo é calculado agrupando por app. A H1 é rejeitada se o limite superior do intervalo ficar abaixo de 10%. Por que 10%: critério operacional do estudo; Andow et al. (2020) acharam até 42,4% de apps com declaração incorreta ou omitida, mas em outra população e por app, então serve só para mostrar que o problema é comum.

Tenho uma hipótese central e uma secundária. A H1 propõe que ao menos 10% dos pares aplicativo–SDK identificados não tenham declaração compatível na política de privacidade e na seção “Segurança dos dados”. A declaração por categoria de dados e finalidade pode ser suficiente: não se exige que a política liste nominalmente todos os SDKs. O patamar de 10% significa que, se pelo menos um em cada dez pares avaliáveis não tiver declaração compatível, o resultado merece ser quantificado e discutido. É uma escolha do estudo, não uma tolerância prevista na LGPD. Andow e colegas encontraram até 42,4% de inconsistências em outra população e com outro método, portanto não é uma taxa diretamente comparável. A H2 considera que aplicativos com dados sensíveis não apresentam uma prevalência menor de SDKs do que os demais aplicativos governamentais. Essa é uma comparação dentro do próprio corpus. A comparação comercial permanece apenas como contexto. A concordância dos detectores é uma checagem do instrumento, sem numeração como hipótese.

No referencial teórico, a literatura oferece três pontos de partida. Binns e colaboradores baixaram cerca de 959 mil aplicativos e procuraram, no código, referências a rastreadores, sem executar os apps; acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam cerca de um milhão de aplicativos de 2017 com um milhão de 2020, antes e depois do GDPR, o regulamento europeu de proteção de dados, e viram pouca mudança, sem que essa comparação prove, sozinha, o efeito da lei. Samarasinghe e colaboradores acharam 1.166 aplicativos de governo de 71 países pelos links da Google Play nos sites oficiais e examinaram os SDKs e os dados enviados: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis, como identificadores, a terceiros ou sem criptografia. Esses resultados justificam investigar o contexto brasileiro com atenção às declarações de privacidade.

O método tem seis etapas. Primeiro, confirmar os aplicativos oficiais encontrados na Google Play. Segundo, caracterizar o corpus por esfera e tipo de serviço. Terceiro, obter a versão atual dos pacotes, quando tecnicamente disponível, registrando o hash; o AndroZoo será usado para reprodutibilidade e comparação de versões. Quarto, identificar os SDKs e verificar se os detectores concordam. Quinto, confrontar cada componente com as categorias de dados e finalidades informadas nas políticas e na seção "Segurança dos dados". Sexto, calcular as proporções de divergência. A observação dinâmica de uma subamostra complementará a análise. Os dados e o piloto já realizados demonstram viabilidade, não resultados finais.

Nenhum dos estudos da revisão mede os SDKs no conjunto dos aplicativos de governo brasileiros confrontando o que cada um declara; essa é a lacuna. A contribuição esperada tem três partes. Primeiro, estudar sistematicamente aplicativos federais, estaduais e municipais brasileiros, distinguindo serviços que podem tratar dados sensíveis. Segundo, confrontar a presença e a função dos SDKs com as categorias de dados e finalidades declaradas na política de privacidade e na seção Segurança dos dados da Google Play. Para uma subamostra, o confronto será ampliado aos fluxos efetivamente observados. Terceiro, verificar as diferenças entre detectores, porque a prevalência reportada pode variar conforme o instrumento. Uma divergência não é prova automática de infração à LGPD; é uma evidência para exame adicional.

## Slide 8. Método (40 s)

Nos procedimentos metodológicos, o estudo é quantitativo e observacional. Primeiro, delimitar e conferir os aplicativos oficiais encontrados na Google Play. Segundo, caracterizá-los por esfera e tipo de serviço. Terceiro, obter a versão atual na Google Play quando possível, com data, versão e SHA-256. O AndroZoo será fonte complementar para reprodutibilidade e para medir defasagem entre a versão arquivada e a que o usuário instala. Quarto, aplicar os detectores e examinar suas divergências. Quinto, comparar resultados técnicos com políticas de privacidade e declarações na loja. Sexto, calcular proporções e intervalos e, para uma subamostra, observar fluxos de rede em cenários documentados.

## Slide 9. Corpus (45 s)

A busca inicial produziu 396 aplicativos candidatos. Pela classificação preliminar de seus publicadores, 376 foram mantidos como oficiais: 85 federais, 199 estaduais e 92 municipais. Entre eles, 100 foram classificados preliminarmente como relacionados a serviços que podem tratar dados sensíveis, como saúde ou biometria. Vinte candidatos saíram: 13 eram de empresas privadas que publicam com nome de serviço público e 7 estavam numa conta de pessoa física. Em 108 casos, a classificação de dado sensível feita por palavra-chave divergiu da conferência, nos dois sentidos. Esses números descrevem o corpus preparatório; a classificação ainda será conferida antes da coleta principal. Os círculos mostram a distribuição por esfera, e não uma medida de rastreadores encontrados.

## Slide 10. Anúncios (40 s)

Um dado descritivo da Google Play é a declaração de anúncios. Entre os 376 aplicativos governamentais classificados preliminarmente como oficiais, nenhum declarou exibir anúncios. Na primeira referência comercial, a informação aparece em 63 dos 190 aplicativos, ou 33,2%. Os intervalos de confiança mostrados dizem respeito apenas a essa declaração feita pelos publicadores. Não significam que os aplicativos do governo não incorporem SDKs de análise de uso ou de rastreamento. Também não uso a referência comercial como grupo de controle, pois sua coleta não foi planejada para um teste inferencial equivalente.

Na consulta histórica, encontrei no AndroZoo apenas 92 dos 396 candidatos governamentais, ou 23,2%. Isso mostra que depender exclusivamente desse acervo poderia deixar a maior parte do corpus de fora. Vou priorizar as versões disponíveis na Google Play e documentar as limitações de coleta. As versões arquivadas no AndroZoo permitem avaliar mudanças entre versões e tornar parte da análise reproduzível.

Uma limitação prática apareceu na busca por pacotes. O AndroZoo possuía apenas 92 dos 396 candidatos governamentais da consulta histórica, ou 23,2%; na primeira referência comercial eram 160 de 190, ou 84,2%. Isso indica que depender apenas do acervo acadêmico poderia deixar muitos aplicativos oficiais de fora. Por isso o plano prevê coletar as versões atuais disponibilizadas na Google Play, com registro de hash, data e eventuais falhas. O AndroZoo continua relevante para recuperar versões específicas, medir defasagem e possibilitar reprodutibilidade onde os arquivos estiverem disponíveis. Na prática, a coleta usa o apkeep, uma ferramenta aberta da EFF, com uma conta Google criada só para a pesquisa e acesso a partir do Brasil. Para cada aplicativo, registro o hash SHA-256 do arquivo, a versão, a data e, se o download falhar, o motivo; a falha também vira dado. Quando o app vem em pacotes divididos, guardo o APK base, que é onde está o código. Antes do corpus inteiro, testo a coleta em cinco aplicativos.

## Slide 12. Piloto dos detectores (55 s)

No piloto, utilizei 20 pacotes arquivados no AndroZoo e três detectores. O detector A buscou assinaturas de código na base do Exodus; B procurou assinaturas de rede em textos do pacote usando a mesma base; C utilizou assinaturas da Disconnect sobre os mesmos textos. As proporções de pacotes com detecção foram 75%, 95% e 80%, respectivamente. O kappa de Fleiss foi 0,52. Conferi as detecções uma a uma, olhando a classe ou o domínio que gerou cada uma, e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por domínios genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas isso é só uma análise de sensibilidade: não existe uma referência independente que diga a resposta certa.

As limitações: achar o código de um SDK no pacote não prova que ele roda nem que envia dados, e por isso há a análise dinâmica numa subamostra. O estudo cobre só Android e Google Play. As políticas costumam declarar categorias de dados, e não a lista de SDKs; por isso o confronto separa a menção ao SDK pelo nome, a declaração por categoria e a ausência de menção. A seleção da revisão tem um revisor, e os detectores compartilham bases ou métodos de extração. Até 3 de dezembro, incorporo os comentários do orientador e da simulação e faço a revisão final do texto. No Capstone II, concluo a leitura e a avaliação dos artigos que faltam, confiro as classificações dos aplicativos e defino com o orientador o detector principal e o plano de análise. Depois vêm a coleta, a detecção, o confronto com as políticas e a análise dinâmica.

## Slide 13. Revisão sistemática (85 s)

A pergunta que orienta o trabalho é simples: as práticas associadas aos componentes de terceiros nos aplicativos do governo são compatíveis com o que é informado ao cidadão? Obrigado.

---

## Perguntas prováveis

**Como você decide que um aplicativo é oficial? Por que 20 saíram?**
Pelo nome jurídico do publicador, que a loja mostra em "Sobre o desenvolvedor". Treze eram empresas privadas com nome de serviço público e sete eram contas de pessoa física. A classificação será conferida antes da coleta principal.

**Como Binns, Kollnig e Samarasinghe fizeram as pesquisas?**
Binns e colegas baixaram cerca de 959 mil APKs da Google Play dos EUA e do Reino Unido e procuraram referências a rastreadores no código, sem executar os apps. Kollnig e colegas compararam cerca de um milhão de apps de 2017 com um milhão de 2020, antes e depois do GDPR, procurando rastreadores no código. Samarasinghe e colegas acharam os apps de governo pelos links da Google Play nos sites oficiais e examinaram os SDKs e os dados enviados. Os dois primeiros mostram presença de código; o terceiro também olha o envio de dados. O meu trabalho mede a presença e a confronta com o que cada app declara.

**O que há de novo em relação a Samarasinghe et al.?**
O caso brasileiro separado por esfera e por dado sensível, o confronto entre o que cada aplicativo declara e o que ele embarca e envia, e a medida de concordância entre detectores sobre as mesmas versões dos pacotes.

**Ter o SDK no pacote prova que dados são enviados?**
Não. A análise estática mostra presença de código. O envio só é observado na análise dinâmica da subamostra. O texto separa presença, transmissão observada e declaração.

**Se o detector B teve 71,5% das detecções questionadas, por que mantê-lo?**
Ele não é a medida principal proposta. Como A e B usam a mesma base com métodos diferentes, a diferença ilustra o efeito do método, que a checagem do instrumento mede. Os 88 casos foram considerados falsos positivos potenciais na adjudicação interna, não confirmados por um padrão de referência externo.

**Como você vai obter os pacotes? Isso é permitido?**
Todos na versão atual da Google Play, que é a que o cidadão instala. Quem baixa é o apkeep, ferramenta aberta da EFF, com uma conta Google criada só para a pesquisa, a partir do Brasil. Registro o SHA-256, a versão, a data e o motivo de cada falha, e não redistribuo os pacotes. Em app publicado em pacotes divididos, guardo o APK base, que tem o código. O AndroZoo serve para outra pessoa reproduzir a análise e para medir a defasagem. A coleta será testada em cinco apps no início do Capstone II.

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
A classificação inicial foi organizada em planilhas e scripts, com critérios definidos no protocolo. Até agora, conferi 18 propostas de decisão da F2; as outras 61 propostas e os 278 registros sem decisão ainda precisam ser examinados. O corpus de aplicativos também passará por conferência antes da coleta principal. Não apresento essas etapas pendentes como concluídas.

**Você utilizou inteligência artificial no trabalho?**
Sim. Usei ChatGPT e Claude como apoio na elaboração e depuração dos scripts em Python, no levantamento bibliográfico inicial, na localização de referências metodológicas e na revisão de clareza da redação. As sugestões não substituem as publicações originais nem as verificações previstas no protocolo. As decisões metodológicas e a interpretação do trabalho continuam sob minha responsabilidade. Esse uso está declarado na seção de procedimentos metodológicos do TCC.

## Fontes de cada slide

| Slide | Onde está no projeto |
|---|---|
| 2 a 4 | Seções 1 e 2; Binns et al. (2018b); Kollnig et al. (2021a, 2021b); Samarasinghe et al. (2022) |
| 5 e 6 | Problema, objetivos, hipóteses e resultados esperados no texto-fonte atualizado |
| 7 | Seções 3.1 a 3.5 |
| 8 a 11 | Seção 3.6 |
| 12 | Seções 2.7 e 3.7 e Figura 1 |
| 13 | Seções 3.9, 3.12 e 3.13 |
