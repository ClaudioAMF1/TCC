# Roteiro da simulação de defesa

Versão de 23/11/2026, igual às notas da apresentação `apresentacao_TCC1_final.pptx` (no repositório, `simulacao-defesa-rascunho.pptx`), com 16 slides no padrão do template do IDP. São 15 minutos de apresentação e 10 de perguntas. As falas somam cerca de 12 minutos, num ritmo calmo, o que deixa folga para pausas. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra: leia algumas vezes e fale com as suas palavras, mantendo os números exatos.

## Slide 1. Abertura (40 s)

Bom dia. Esta é a apresentação do meu projeto de Capstone I, intitulado “Quem mais está dentro do aplicativo?”. A pesquisa se concentra nos aplicativos Android oficiais do governo brasileiro e na transparência sobre os SDKs de terceiros. Quero entender quais desses componentes estão presentes e se o que é informado ao cidadão sobre a coleta e o compartilhamento de dados é compatível com a evidência técnica. O objetivo deste semestre é apresentar um problema bem definido, o método e um piloto de viabilidade. A coleta principal e os testes das hipóteses serão realizados no Capstone II.

## Slide 2. Agenda (30 s)

Vou apresentar em duas partes. Primeiro, o problema: por que olhar os aplicativos públicos, o que a literatura já mostrou, a lacuna e a pergunta, com os objetivos e as hipóteses. Depois, o método e o que já foi feito: as etapas, os resultados preparatórios do corpus e do piloto, como a revisão bibliográfica foi conduzida e, por fim, as limitações e os próximos passos.

## Slide 3. Motivação (40 s)

Boa parte dos serviços públicos passou para o celular. Aplicativos como Meu INSS e Meu SUS Digital são usados por milhões de pessoas e frequentemente constituem a principal porta de entrada para esses serviços. Um aplicativo Android não contém apenas código desenvolvido pelo órgão responsável: ele pode integrar SDKs de mapas, notificações, análise de uso e outros serviços. Alguns componentes podem coletar identificadores ou informações de utilização. Essa possibilidade exige transparência, especialmente no setor público, onde a escolha de prestador pelo cidadão costuma ser limitada. Ressalto que encontrar uma biblioteca instalada não equivale a observar transmissão de dados.

## Slide 4. O que a literatura já demonstrou (55 s)

A literatura oferece três pontos de partida. Binns e colaboradores baixaram cerca de 959 mil aplicativos e procuraram, no código, referências a rastreadores, sem executar os apps; acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam cerca de um milhão de aplicativos de 2017 com um milhão de 2020, antes e depois do GDPR, e viram pouca mudança, sem que essa comparação prove, sozinha, o efeito da lei. Samarasinghe e colaboradores acharam 1.166 aplicativos de governo de 71 países pelos links da Google Play nos sites oficiais e examinaram os SDKs e os dados enviados: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis, como identificadores, a terceiros ou sem criptografia. Esses resultados justificam investigar o contexto brasileiro com atenção às declarações de privacidade.

## Slide 5. Lacuna e contribuição (40 s)

A contribuição esperada tem três partes. Primeiro, estudar sistematicamente aplicativos federais, estaduais e municipais brasileiros, distinguindo serviços que podem tratar dados sensíveis. Segundo, confrontar a presença e a função dos SDKs com as categorias de dados e finalidades declaradas na política de privacidade e na seção Segurança dos dados da Google Play. Para uma subamostra, o confronto será ampliado aos fluxos efetivamente observados. Terceiro, verificar as diferenças entre detectores, porque a prevalência reportada pode variar conforme o instrumento. Uma divergência não é prova automática de infração à LGPD; é uma evidência para exame adicional.

## Slide 6. Pergunta e objetivos (45 s)

No texto do TCC, a pergunta foi formulada assim: “Em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado em suas políticas de privacidade e na seção Segurança dos dados da Google Play?”. O objetivo geral é medir a proporção de SDKs e de envios sem declaração compatível nos aplicativos governamentais brasileiros, à luz da LGPD. Para isso vou confirmar o corpus, detectar os componentes, comparar as declarações, observar uma subamostra dinamicamente e conferir a concordância dos detectores. A evidência estática e a de tráfego serão apresentadas separadamente.

## Slide 7. Hipóteses (50 s)

A H1 é a principal: ao menos 10% dos pares aplicativo–SDK identificados não teriam declaração compatível, considerando categorias de dados e finalidades, e não apenas o nome comercial da biblioteca. O critério utiliza um intervalo de confiança de 95%. O limiar de 10% corresponde a ao menos um par sem declaração compatível em cada dez pares que possam ser avaliados. É uma escolha operacional para o teste, e não uma margem permitida pela LGPD. A H2 é secundária: procura verificar se aplicativos governamentais que tratam dados sensíveis têm prevalência de SDKs menor do que os demais. A hipótese considera que essa prevalência não é menor. Os comerciais ficam como contexto; concordância entre detectores é checagem do instrumento sem hipótese própria.

## Slide 8. Método (40 s)

O método é quantitativo e observacional. Primeiro, delimitar e conferir os aplicativos oficiais encontrados na Google Play. Segundo, caracterizá-los por esfera e tipo de serviço. Terceiro, obter a versão atual na Google Play quando possível, com data, versão e SHA-256. O AndroZoo será fonte complementar para reprodutibilidade e para medir defasagem entre a versão arquivada e a que o usuário instala. Quarto, aplicar os detectores e examinar suas divergências. Quinto, comparar resultados técnicos com políticas de privacidade e declarações na loja. Sexto, calcular proporções e intervalos e, para uma subamostra, observar fluxos de rede em cenários documentados.

## Slide 9. Corpus (35 s)

A busca inicial produziu 396 aplicativos candidatos. Pela classificação preliminar de seus publicadores, 376 foram mantidos como oficiais: 85 federais, 199 estaduais e 92 municipais. Entre eles, 100 foram classificados preliminarmente como relacionados a serviços que podem tratar dados sensíveis, como saúde ou biometria. Vinte candidatos foram excluídos nesta etapa por divergências de titularidade. Esses números descrevem o corpus preparatório; a classificação ainda será conferida antes da coleta principal. Os círculos mostram a distribuição por esfera, e não uma medida de rastreadores encontrados.

## Slide 10. Anúncios (40 s)

Um dado descritivo da Google Play é a declaração de anúncios. Entre os 376 aplicativos governamentais classificados preliminarmente como oficiais, nenhum declarou exibir anúncios. Na primeira referência comercial, a informação aparece em 63 dos 190 aplicativos, ou 33,2%. Os intervalos de confiança mostrados dizem respeito apenas a essa declaração feita pelos publicadores. Não significam que os aplicativos do governo não incorporem SDKs de análise de uso ou de rastreamento. Também não uso a referência comercial como grupo de controle, pois sua coleta não foi planejada para um teste inferencial equivalente.

## Slide 11. Piloto dos detectores (55 s)

No piloto, utilizei 20 pacotes arquivados no AndroZoo e três detectores. O detector A buscou assinaturas de código na base do Exodus; B procurou assinaturas de rede em textos do pacote usando a mesma base; C utilizou assinaturas da Disconnect sobre os mesmos textos. As proporções de pacotes com detecção foram 75%, 95% e 80%, respectivamente. O kappa de Fleiss foi 0,52. Conferi as detecções uma a uma, olhando a classe ou o domínio que gerou cada uma, e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por domínios genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas isso é só uma análise de sensibilidade: não existe uma referência independente que diga a resposta certa.

> **Lembrete, não precisa falar.** A, Exodus por código: usa a base do Exodus Privacy e procura, nos nomes das classes do código do app (o arquivo DEX), o pacote de cada SDK conhecido, como com.google.firebase.analytics. Se acha, o código do SDK está dentro do APK. B, Exodus por domínio: mesma base do Exodus, mas procura os endereços de internet dos rastreadores, como google-analytics.com, escritos nos textos do APK. Não é tráfego, é texto dentro do pacote; por isso um link para maps.google.com bastou para apontar Google Ads. C, Disconnect por domínio: mesmo método do B, com outra lista, a da Disconnect, que classifica domínios por finalidade; uso só publicidade, análise de uso e impressão digital. A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método).

## Slide 12. Fonte dos APKs (70 s)

Uma limitação prática apareceu na busca por pacotes. O AndroZoo possuía apenas 92 dos 396 candidatos governamentais da consulta histórica, ou 23,2%; na primeira referência comercial eram 160 de 190, ou 84,2%. Isso indica que depender apenas do acervo acadêmico poderia deixar muitos aplicativos oficiais de fora. Por isso o plano prevê coletar as versões atuais disponibilizadas na Google Play, com registro de hash, data e eventuais falhas. O AndroZoo continua relevante para recuperar versões específicas, medir defasagem e possibilitar reprodutibilidade onde os arquivos estiverem disponíveis. Na prática, a coleta usa o apkeep, uma ferramenta aberta da EFF, com uma conta Google criada só para a pesquisa e acesso a partir do Brasil. Para cada aplicativo, registro o hash SHA-256 do arquivo, a versão, a data e, se o download falhar, o motivo; a falha também vira dado. Quando o app vem em pacotes divididos, guardo o APK base, que é onde está o código. Antes do corpus inteiro, testo a coleta em cinco aplicativos.

## Slide 13. Revisão sistemática (85 s)

A revisão sistemática seguiu o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as strings e os critérios de seleção. O fluxo é relatado no modelo PRISMA 2020, que mostra quantos registros entraram e saíram em cada etapa. Fiz 17 buscas em 6 de novembro, em quatro bases: o Scopus, que é a principal, o IEEE Xplore e, para a produção nacional, a SBC OpenLib e a BDTD, com trabalhos de 2015 a 2026, em inglês e português. Cada string tem três blocos: um de aplicativo móvel, um do fenômeno, como rastreador, SDK de terceiros ou política de privacidade, e, quando preciso, um de contexto, como governo, COVID-19 ou Brasil. O bloco de contexto evita ruído: a palavra tracker sozinha traz até rastreador de atividade física. Para validar as strings, usei onze estudos conhecidos como controle, e as buscas recuperaram os dez que o Scopus indexa. Os 1.531 registros viraram 1.249 sem duplicatas; a triagem por título e resumo levou 357 à leitura completa, e há 71 propostas de inclusão. Os 278 registros em aberto e a bola de neve ficam para o Capstone II, como combinado com o orientador.

## Slide 14. Limitações e próximos passos (50 s)

Entre as limitações, destaco que uma assinatura de código não prova execução nem transmissão, e que as políticas de privacidade podem declarar categorias de dados e finalidades sem nomear todos os SDKs. Há ainda limitações na seleção da revisão, na classificação do corpus, na disponibilidade de versões e na independência dos detectores. Até a entrega do Capstone I, a prioridade é incorporar o retorno do orientador e da simulação. No Capstone II serão concluídas a leitura e as decisões dos artigos pendentes, além da conferência das classificações do corpus, seguida da coleta das versões atuais, do confronto documental, da análise dinâmica de subamostra, da avaliação estatística e da discussão jurídica fundamentada.

## Slide 15. Conclusão (35 s)

Para concluir, o Capstone I apresenta um problema delimitado, um desenho metodológico e dados preparatórios suficientes para demonstrar viabilidade. O foco não é comparar o governo ao mercado, mas verificar se aquilo que os aplicativos públicos declaram sobre tratamento de dados é compatível com os componentes identificados e, onde houver observação dinâmica, com os fluxos realmente transmitidos. Essa distinção é fundamental para produzir resultados defensáveis sobre privacidade, transparência e dependência de fornecedores. Obrigado. Estou à disposição para as perguntas.

## Slide 16. Encerramento

Slide institucional do template, sem fala. Deixe na tela durante as perguntas.

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
Ele não é a medida principal proposta. Como A e B usam a mesma base com métodos diferentes, a diferença ilustra o efeito do método, que a checagem do instrumento mede. Os 88 casos foram marcados como possíveis falsos positivos na minha conferência, detecção por detecção, sem uma referência externa que confirme.

**Como você vai obter os pacotes? Isso é permitido?**
Todos na versão atual da Google Play, que é a que o cidadão instala. Quem baixa é o apkeep, ferramenta aberta da EFF, com uma conta Google criada só para a pesquisa, a partir do Brasil. Registro o SHA-256, a versão, a data e o motivo de cada falha, e não redistribuo os pacotes. Em app publicado em pacotes divididos, guardo o APK base, que tem o código. O AndroZoo serve para outra pessoa reproduzir a análise e para medir a defasagem. A coleta será testada em cinco apps no início do Capstone II.

**Por que o limiar de 10% na H1?**
O valor representa pelo menos um par sem declaração compatível em cada dez pares avaliáveis. É um critério de interesse definido para a pesquisa, não um valor previsto em lei. O estudo de Andow encontrou até 42,4% dos aplicativos com declarações incorretas ou omissas, com outra unidade de análise e outro método; serve de contexto, não de comparação direta, nem de parâmetro legal.

**O que "soberania de dados" quer dizer no seu trabalho?**
A capacidade do Estado de saber e decidir para onde vão os dados gerados nos seus serviços. Mede-se pela dependência de SDKs de terceiros e, na subamostra, pelos destinos observados. A presença de SDK de empresa estrangeira já mostra dependência de fornecedores estrangeiros; dizer que dados foram para o exterior exige a análise dinâmica. A nacionalidade do fornecedor ou o país de um IP não provam, sozinhos, uma transferência internacional.

**A ANPD não é uma autoridade?**
A ANPD tornou-se autarquia especial em 2022. Em 2026, a Lei 15.352 a transformou em agência reguladora, com a denominação Agência Nacional de Proteção de Dados. Os documentos anteriores preservam o nome institucional vigente à época.

**O que é seguir Kitchenham e relatar pelo PRISMA 2020?**
Kitchenham é o guia de revisão sistemática da engenharia de software: antes de buscar, escrevo um protocolo com perguntas, bases, strings, critérios de inclusão e exclusão e avaliação de qualidade, e registro cada mudança. O PRISMA 2020 é o modelo de relato: o fluxograma mostra quantos registros foram encontrados, quantos saíram em cada etapa e por quê. Um diz como fazer; o outro, como mostrar o que foi feito.

**Como as strings de busca foram montadas e validadas?**
Cada string tem três blocos: aplicativo móvel, o fenômeno (rastreador, SDK de terceiros, política de privacidade) e, quando a palavra sozinha traz ruído, um bloco de contexto, como governo, COVID-19 ou Brasil. Por exemplo, tracker sozinho traz rastreador de atividade física. Para validar, usei onze estudos conhecidos como controle: as buscas acharam os dez que o Scopus indexa; o décimo primeiro não está no Scopus. A ACM saiu porque exportar os resultados exige uma assinatura que a instituição não tem, e os anais dela estão em grande parte no Scopus.

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
| 2 | Agenda: a ordem dos capítulos 1 a 3 |
| 3 a 5 | Seções 1 e 2; Binns et al. (2018); Kollnig et al. (2021a, 2021b); Samarasinghe et al. (2022) |
| 6 e 7 | Seções 1.1 a 1.4 (problema, objetivos e hipóteses) |
| 8 | Seções 3.1 a 3.4 |
| 9 a 12 | Seção 3.5 |
| 13 | Seção 3.6, Figura 1 e protocolo da revisão (strings) |
| 14 | Seções 3.8, 3.11 e 3.12 |
| 16 | Encerramento do template, sem conteúdo |
