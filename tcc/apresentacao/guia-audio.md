# Áudio guia da apresentação

Texto do áudio, para ler junto. Feito a partir das notas do seu arquivo apresentacao_TCC1.pptx.

## Abertura do guia

Áudio guia da simulação de defesa do Capstone I.

Olá, Claudio. Este áudio acompanha a sua apresentação, slide por slide. Para cada slide, você vai ouvir o que aparece na tela, a fala que está nas suas notas e, depois, o que lembrar ou o que responder se perguntarem.

São dezessete slides. A sua fala completa dá entre onze e doze minutos, num ritmo calmo. Você tem quinze minutos para apresentar e dez para as perguntas.

Uma dica antes de começar: não decore palavra por palavra. Guarde a ideia de cada slide e os números, e fale do seu jeito. Vamos começar.

## Slide 1. Capa

Slide um. A capa.

Na tela: o título, Quem mais está dentro do aplicativo?, o subtítulo sobre rastreamento por terceiros e soberania de dados em aplicativos do governo, o seu nome e o nome do seu orientador.

A fala: Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu projeto se chama “Quem mais está dentro do aplicativo?”. Muitos aplicativos do governo trazem, dentro deles, código de outras empresas, que pode coletar dados de quem usa. Eu quero descobrir que código é esse e se o governo avisa o cidadão sobre isso.

Para lembrar: a ideia central do trabalho cabe numa frase. Os aplicativos do governo trazem código de outras empresas, e você quer saber se o governo avisa o cidadão sobre isso.

## Slide 2. Agenda

Slide dois. A agenda.

Na tela: os quatro blocos da apresentação, na mesma ordem do texto do TCC. Um, introdução. Dois, referencial teórico. Três, procedimentos metodológicos. Quatro, conclusão e referências.

A fala: Vou seguir a mesma ordem do texto do TCC. Primeiro, a introdução: por que o tema importa, a pergunta, os objetivos e as hipóteses. Depois, o referencial teórico: os estudos em que me baseio e o que ainda falta neles. Em seguida, os procedimentos metodológicos: como vou fazer a pesquisa e o que já testei. No fim, a conclusão e as referências.

Para lembrar: este slide é rápido. Diga os quatro blocos e siga em frente.

## Slide 3. Motivação

Slide três. Motivação.

Na tela: à esquerda, o texto sobre o Meu INSS e o Meu SUS Digital, com mais de 50 milhões de instalações cada. À direita, num quadrado azul, um fluxo em três caixas: o aplicativo do governo, o SDK de terceiro embutido e o servidor da empresa, para onde os dados podem ir. Embaixo, a pergunta central: o que está declarado é compatível com os SDKs?

A fala: Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada. Só que esses aplicativos não têm só o código do órgão: eles trazem pedaços prontos de outras empresas, os SDKs, para coisas como mapas, notificações e estatísticas de uso. Alguns desses SDKs podem coletar dados de quem usa. No governo isso pesa mais, porque o cidadão não tem como trocar de aplicativo. e um detalhe importante: o SDK estar dentro do aplicativo não prova que ele enviou dados.

Para lembrar: SDK é um pedaço de código pronto, feito por outra empresa, que roda dentro do aplicativo. E guarde a frase de proteção: o SDK estar dentro do aplicativo não prova que ele enviou dados.

## Slide 4. Pergunta e objetivos

Slide quatro. Pergunta e objetivos.

Na tela: a pergunta de pesquisa, o objetivo geral e cinco caixinhas com os objetivos específicos.

A fala: A minha pergunta é: em que medida os aplicativos oficiais do governo trazem SDKs de rastreamento e enviam dados a terceiros sem avisar isso na política de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo é medir essa proporção, à luz da LGPD. São cinco passos: conferir quais aplicativos são mesmo oficiais, detectar os SDKs, comparar com o que cada aplicativo declara, observar o tráfego numa parte deles e verificar se os detectores concordam.

Para lembrar: a pergunta começa com em que medida, porque a resposta é um número, uma proporção, e não um sim ou não. Foi um pedido do seu orientador. Os cinco objetivos específicos são: conferir o corpus, detectar os SDKs, comparar as declarações, observar os fluxos de rede e verificar os detectores.

## Slide 5. Hipóteses

Slide cinco. Hipóteses.

Na tela: quatro blocos. À esquerda, a H1, principal, e a H2, secundária. À direita, a referência comercial, que é só contexto, e os detectores, que são uma checagem do instrumento, e não uma hipótese.

A fala: Tenho duas hipóteses. A H1 é a principal: pelo menos 1 em cada 10 pares aplicativo–SDK não tem declaração compatível. Par aplicativo–SDK é cada SDK encontrado em cada aplicativo. E a declaração não precisa citar o nome do SDK: basta dizer que tipo de dado é coletado e para quê. Esse limite de 10% é um critério do estudo, não uma tolerância da LGPD. A H2 é secundária. Seria de esperar que os aplicativos com dados sensíveis, como os de saúde, tivessem menos SDKs; a minha hipótese é que não têm menos. Os aplicativos comerciais ficam só como contexto, e a concordância entre os detectores serve para checar a ferramenta; não é uma hipótese.

Se perguntarem como a H1 é testada: você calcula a proporção de pares sem declaração compatível, com intervalo de confiança de 95%, agrupando por aplicativo, porque os SDKs do mesmo aplicativo dependem da mesma política. A H1 é rejeitada se o limite superior do intervalo ficar abaixo de 10%. A H2 só é rejeitada se os dados mostrarem claramente que os aplicativos sensíveis têm menos SDKs.

Se perguntarem por que 10%: é um critério do estudo, e não da LGPD. Andow e colegas acharam até 42,4% de aplicativos com declaração incorreta ou omitida, mas em outra população e contando por aplicativo. Isso só mostra que o problema é comum.

Para lembrar a frase exata da H1: pelo menos um em cada dez pares aplicativo–SDK sem declaração compatível. É um limiar do estudo, não da lei.

## Slide 6. Literatura

Slide seis. O que a literatura já mostrou.

Na tela: três colunas, uma para cada estudo. Em cada uma, um número grande, como fizeram e o que acharam.

A fala: No referencial teórico, parto de três estudos. Binns e colegas baixaram cerca de 959 mil aplicativos e procuraram rastreadores no código, sem executar os apps: acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam cerca de um milhão de aplicativos de 2017 com um milhão de 2020, antes e depois do GDPR, o regulamento europeu de proteção de dados, e viram pouca mudança, o que sozinho não prova efeito da lei. Samarasinghe e colegas acharam 1.166 aplicativos de governo de 71 países pelos links nos sites oficiais e examinaram os SDKs e os dados enviados: 37% tinham rastreadores do Google, e 27% enviavam dados sensíveis, como identificadores, a terceiros ou sem criptografia. Ou seja, o problema existe também no governo, e vale olhar o caso brasileiro.

Para lembrar os números: Binns, 959 mil aplicativos. Kollnig, cerca de um milhão antes e um milhão depois do GDPR. Samarasinghe, 1.166 aplicativos de governo em 71 países, com 37% com rastreadores do Google e 27% enviando dados sensíveis.

## Slide 7. Lacuna e contribuição

Slide sete. Lacuna e contribuição.

Na tela: três abas, numeradas de um a três: corpus brasileiro, transparência e checagem do método.

A fala: O que falta nesses estudos, pelo menos na literatura que examinei até agora: nenhum mede os SDKs no conjunto dos aplicativos do governo brasileiro comparando com o que cada um declara. Essa é a lacuna. A contribuição tem três partes. Primeiro, estudar os aplicativos federais, estaduais e municipais, separando os que tratam dados sensíveis. Segundo, comparar o que os SDKs fazem com o que cada aplicativo declara e, numa parte deles, com o tráfego observado. Terceiro, medir o quanto o resultado muda conforme o detector. E uma divergência não é prova de infração à LGPD; é um indício que merece ser examinado.

Para lembrar: a lacuna vale para a literatura examinada até agora. E uma divergência é um indício, não uma prova de que a lei foi violada.

## Slide 8. Método

Slide oito. Método.

Na tela: seis caixas, numeradas de um a seis: corpus, caracterização, pacotes atuais, detectores, declarado versus detectado, e análise.

A fala: Nos procedimentos metodológicos, o estudo é quantitativo e observacional, em seis etapas. primeira: conferir quais aplicativos são oficiais. segunda: separar por esfera de governo e tipo de serviço. terceira: baixar a versão atual de cada aplicativo na Google Play, registrando o hash, que é a impressão digital do arquivo. quarta: rodar os detectores e comparar o que cada um encontra. quinta: comparar o que foi detectado com a política de privacidade e com a declaração na loja. sexta: calcular as proporções com intervalo de confiança e, numa parte dos aplicativos, observar o tráfego de rede.

Para lembrar: o hash é como a impressão digital do arquivo. Ele garante que todo mundo está falando exatamente da mesma versão do aplicativo.

## Slide 9. Corpus

Slide nove. Corpus.

Na tela: um círculo grande com 376 aplicativos oficiais e três círculos menores: 85 federais, 199 estaduais e 92 municipais. À esquerda, o texto sobre como a oficialidade foi conferida.

A fala: Na busca, encontrei 396 aplicativos candidatos. Conferindo o nome jurídico de quem publica, 376 ficaram como oficiais: 85 federais, 199 estaduais e 92 municipais. Vinte saíram: 13 eram de empresas privadas usando nome de serviço público e 7 estavam em contas de pessoa física. Cem dos 376 podem tratar dados sensíveis, como saúde ou biometria. essa é uma classificação preliminar e ainda vai ser conferida antes da coleta.

Se perguntarem como você sabe que um aplicativo é oficial: pelo nome jurídico de quem publica, que a Google Play mostra em Sobre o desenvolvedor. E a classificação ainda vai ser conferida antes da coleta.

## Slide 10. Anúncios

Slide dez. Anúncios.

Na tela: duas caixas. Zero de 376 aplicativos do governo declaram anúncios. E 63 de 190 aplicativos comerciais, ou 33,2%.

A fala: Um dado que a própria Google Play mostra é se o aplicativo declara exibir anúncios. Nenhum dos 376 aplicativos do governo declara. Entre os comerciais da referência, foram 63 de 190, ou 33,2%. isso é o que o publicador declara, e não diz nada sobre os SDKs de análise ou de rastreamento que estão dentro do aplicativo. E os comerciais servem só de contexto, não de grupo de controle.

Se perguntarem sobre os intervalos de confiança: com zero em 376, a proporção real de aplicativos do governo que declaram anúncios fica, com 95% de confiança, entre zero e um por cento. Nos comerciais, entre 26,9% e 40,1%. Isso vale só para a declaração de anúncios, e não diz nada sobre os SDKs.

## Slide 11. Fonte dos APKs

Slide onze. Fonte dos APKs.

Na tela: dois números grandes, 23,2% e 84,2%, que são a cobertura do AndroZoo. À direita, a fonte principal: a versão atual na Google Play. Embaixo, os quatro passos da coleta: conta da pesquisa, download com o apkeep, registro e teste primeiro.

A fala: Um problema prático apareceu na hora de buscar os pacotes. O AndroZoo, um acervo acadêmico de aplicativos, tinha só 92 dos 396 do governo, ou 23,2%; dos comerciais, tinha 160 de 190, ou 84,2%. Dependendo só dele, muitos aplicativos do governo ficariam de fora. Por isso a fonte principal vai ser a versão atual da Google Play, que é a que o cidadão instala. O download vai ser feito com o apkeep, uma ferramenta aberta, com uma conta Google criada só para a pesquisa, a partir do Brasil. Para cada aplicativo, registro o hash, a versão, a data e, se falhar, o motivo; a falha também vira dado. O AndroZoo continua útil para reproduzir a análise. Antes do corpus inteiro, testo em cinco aplicativos.

Se perguntarem: quando o aplicativo vem dividido em vários pacotes, você guarda o APK base, que é onde está o código. O apkeep é uma ferramenta aberta, de uma organização sem fins lucrativos. E você não redistribui os pacotes.

## Slide 12. Piloto dos detectores

Slide doze. Piloto dos detectores.

Na tela: três barras, uma para cada detector. A, 75%. B, 95%. C, 80%. À direita, no quadro azul, o kappa de Fleiss: 0,52, ou 0,69 na análise de sensibilidade.

A fala: Fiz um piloto com 20 pacotes do AndroZoo e três detectores. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet escritos dentro do pacote. O C faz o mesmo que o B, com outra lista, a da Disconnect. Cada um deu uma taxa diferente: 75%, 95% e 80% dos pacotes com pelo menos um rastreador. A concordância entre eles, medida pelo kappa de Fleiss, em que 1 é concordância total, foi 0,52. Conferi as detecções uma a uma e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por endereços genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas é só uma análise de sensibilidade, porque não há uma referência independente com a resposta certa. Conclusão: a ferramenta escolhida muda o resultado, e é por isso que comparar os detectores faz parte do método.

Para entender os nomes. O Exodus Privacy é uma plataforma sem fins lucrativos que analisa aplicativos Android para identificar rastreadores de anúncios, de telemetria e de análise, usando assinaturas de SDKs de terceiros. A Disconnect é uma lista que classifica milhares de domínios da internet que coletam dados, em categorias como publicidade, análise, redes sociais e impressão digital.

Para entender a comparação: A contra B mostra o efeito do método, porque os dois usam a mesma base. B contra C mostra o efeito da base, porque os dois usam o mesmo método. O detector B não olha o tráfego; ele olha o texto dentro do pacote. Por isso, um simples link para o Google Maps bastou para ele apontar o Google Ads.

Para lembrar: o kappa mede a concordância entre os detectores, e 1 é concordância total. 0,52 não é alto, e é exatamente por isso que comparar os detectores faz parte do método.

## Slide 13. Revisão sistemática

Slide treze. Revisão sistemática.

Na tela: no alto, três colunas: onde, como e validação. No meio, a faixa com o título. Embaixo, os números: 1.531 registros, 1.249 sem duplicatas e 357 à leitura completa.

A fala: Agora, como eu busquei a literatura. Fiz uma revisão sistemática, que é uma busca planejada e documentada, para que a escolha dos artigos não dependa de preferência pessoal. Para fazer a revisão, segui o guia de Kitchenham, que é um passo a passo muito usado em computação: antes de buscar, escrevi um protocolo dizendo quais perguntas quero responder, onde vou buscar, com quais palavras e quais estudos entram ou saem. Para mostrar o resultado, uso o PRISMA 2020, que é um padrão de prestação de contas: um fluxograma com quantos estudos entraram e saíram em cada etapa. Fiz 17 buscas, em quatro bases: Scopus, que é a principal, IEEE Xplore e, para trabalhos brasileiros, SBC OpenLib e BDTD. Cada busca combina três ideias: aplicativo de celular, o tema, como rastreador ou política de privacidade, e, quando precisa, o contexto, como governo ou Brasil. Para testar as buscas, separei antes onze estudos que tinham de aparecer: elas acharam os dez que estão no Scopus, e o décimo primeiro não está nessa base. No fim, os 1.531 resultados viraram 1.249 sem repetidos, e 357 passaram para a leitura completa.

Para entender o guia de Kitchenham: ele divide a revisão em três etapas. Planejamento, em que se definem as perguntas e o protocolo, com os critérios de inclusão e exclusão. Condução, em que os artigos são buscados nas bases, filtrados, avaliados e têm os dados extraídos. E relatório, em que os resultados são resumidos para responder às perguntas.

Para entender o PRISMA: ele padroniza como mostrar as etapas da revisão. Primeiro, os registros encontrados e a remoção dos repetidos. Depois, a triagem por título e resumo e a leitura do texto completo. Por fim, os estudos incluídos. No seu texto, isso é a Figura 1.

Se perguntarem a diferença: Kitchenham diz como fazer a revisão. O PRISMA diz como mostrar o que foi feito.

Se perguntarem sobre os onze estudos de controle: você escolheu antes de buscar, entre os estudos que já estavam no seu referencial e os de uma busca exploratória inicial. As buscas acharam os dez que estão no Scopus. O décimo primeiro, de Zimmeck e colegas, de 2019, não está nessa base, e entra pela busca nas referências dos estudos, a chamada bola de neve.

## Slide 14. Limitações e próximos passos

Slide catorze. Limitações e próximos passos.

Na tela: à esquerda, cinco limitações. À direita, quatro etapas com datas.

A fala: Sobre as limitações: achar o SDK no código não prova que ele envia dados; o estudo cobre só Android e a Google Play; as políticas costumam falar de tipos de dados, e não do nome de cada SDK; as versões podem mudar entre a coleta e a análise; e a revisão e as classificações ainda estão sendo conferidas. Os próximos passos: até 3 de dezembro, ajustar o texto com o retorno do orientador e desta simulação. Em fevereiro, terminar a revisão e conferir o corpus. Em março e abril, a coleta, a detecção e a comparação com as declarações. Em maio e junho, a análise, a discussão jurídica e a defesa.

Para lembrar as datas: até 3 de dezembro, os ajustes do orientador e da simulação. Em fevereiro, concluir a revisão e conferir o corpus. Em março e abril, a coleta. Em maio e junho, a análise e a defesa.

## Slide 15. Conclusão

Slide quinze. Conclusão.

Na tela, em letras grandes: problema definido, método viável, resultados ainda preliminares. E a pergunta: o que os aplicativos do governo declaram é compatível com os SDKs identificados e os fluxos observados?

A fala: Para concluir: o problema está definido, o método é viável, e os resultados ainda são preliminares. O foco não é comparar o governo com o mercado, mas verificar se o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles realmente enviam. É isso que permite falar com segurança sobre privacidade, transparência e dependência de fornecedores. Obrigado.

Para lembrar: fale a conclusão devagar, olhando para a professora. É a última impressão que fica.

## Slides 16 e 17. Referências e encerramento

Slide dezesseis. Referências.

Na tela, as onze obras citadas na apresentação, no padrão da ABNT. Não é para ler. Depois do obrigado, deixe este slide na tela por alguns segundos.

Slide dezessete. Encerramento. É o slide institucional do IDP, e pode ficar na tela durante as perguntas. Nas notas dos slides dezesseis e dezessete está a sua cola para as perguntas.

## Perguntas prováveis

Agora, as perguntas mais prováveis, com respostas curtas. Tente responder em voz alta antes de ouvir a resposta.

Pergunta: por que 10%?

Resposta: é um critério do estudo, e não da LGPD. Andow achou até 42,4% de aplicativos com declaração errada ou omitida, mas em outra população e contando por aplicativo.

Pergunta: o kappa de 0,52 não é baixo?

Resposta: é, e por isso a concordância entre os detectores virou uma checagem do instrumento, e não uma hipótese.

Pergunta: ter o SDK no aplicativo prova que dados foram enviados?

Resposta: não. O envio só é observado na análise de tráfego de uma parte dos aplicativos.

Pergunta: por que não comparar com aplicativos comerciais?

Resposta: a coleta deles não foi planejada para um teste justo. Eles ficam só como contexto.

Pergunta: por que só Android?

Resposta: porque dá para obter e examinar o pacote do aplicativo. A limitação está declarada no texto.

Pergunta: como você sabe que o aplicativo é oficial?

Resposta: pelo nome jurídico em Sobre o desenvolvedor. E a classificação ainda vai ser conferida antes da coleta.

Pergunta: você leu os 71 artigos?

Resposta: não todos. São propostas de uma primeira leitura, cada uma com a página de onde saiu a informação. Conferi 18 decisões lendo o texto inteiro, e confiro as outras em fevereiro, antes de qualquer resultado.

Pergunta: como você escolheu os onze estudos de controle?

Resposta: antes de buscar, entre os estudos que já estavam no meu referencial e os de uma busca exploratória inicial. São estudos que uma boa busca sobre o tema tem de trazer.

Pergunta: você usou inteligência artificial?

Resposta: sim. Usei o ChatGPT e o Claude como apoio nos scripts em Python, no levantamento bibliográfico inicial, na organização das referências e na revisão da redação. As decisões e a interpretação são minhas, e esse uso está declarado na metodologia do TCC.

Pergunta: e se eu não souber a resposta?

Resposta: diga, isso ainda não medi, está previsto para o Capstone II. Ou, é uma boa sugestão, vou registrar. Não invente.

## Fechamento

Para fechar, os marcos de tempo. Comece o slide seis por volta de três minutos. O slide nove, por volta de cinco minutos e meio. O slide treze, por volta de nove minutos. E termine entre onze e doze minutos.

Se estiver mais de um minuto atrasado em algum marco, no slide seguinte fale só o essencial.

Últimas dicas: chegue um pouco antes e teste a apresentação no computador da sala. Leve o PDF de reserva. Fale a primeira frase devagar. Você está bem preparado. Boa apresentação.

