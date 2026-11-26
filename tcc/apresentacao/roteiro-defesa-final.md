# Roteiro da defesa final (Capstone I)

Mesmo texto das notas do apresentador do arquivo `apresentacao-defesa-final.pptx`, slide a slide. Tempo estimado: cerca de 13 minutos, no ritmo do ensaio de 24/11 (limite da defesa: 15 minutos de apresentação e 15 de perguntas). As linhas marcadas com LEMBRETE e a cola das perguntas não são para ler em voz alta.

## Slide 1: Capa

Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu trabalho trata do rastreamento por terceiros nos aplicativos do governo brasileiro. Esses aplicativos trazem código de outras empresas, que pode coletar dados de quem usa. Quero descobrir que código é esse e se o governo avisa o cidadão sobre ele.

## Slide 2: Agenda

A apresentação segue a ordem do texto. Começo pela introdução, com o problema, os objetivos e a hipótese. Depois vem o referencial teórico, com os estudos de base e a lacuna. Em seguida, os procedimentos metodológicos. No fim, a conclusão.

## Slide 3: MOTIVAÇÃO

Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada um. Esses aplicativos não têm só o código do órgão: trazem componentes prontos de outras empresas, os SDKs, para mapas, notificações e estatísticas de uso. Alguns desses SDKs coletam dados de quem usa. No governo isso pesa mais, porque o cidadão muitas vezes não tem outro aplicativo para usar. Um cuidado importante: o SDK estar no código não prova que ele enviou dados.

## Slide 4: PROBLEMA E OBJETIVO GERAL

O problema da pesquisa é: em que medida os SDKs de rastreamento dos aplicativos oficiais do governo estão declarados ao cidadão, na política de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo geral é medir isso como uma proporção, à luz da LGPD. A unidade é o par aplicativo–SDK: cada SDK encontrado em cada aplicativo forma um par. Um aplicativo com três SDKs gera três pares, e cada par é classificado de acordo com as declarações.

## Slide 5: OBJETIVOS ESPECÍFICOS

São cinco objetivos específicos. Primeiro, revisar os 376 aplicativos oficiais e medir quanto a classificação automática errou. Segundo, baixar a versão atual de cada aplicativo e listar os SDKs com três detectores. Terceiro, ler as declarações e classificar cada par; é daí que sai a proporção que testa a hipótese. Quarto, executar uma parte dos aplicativos num emulador Android, no computador, e registrar para onde os dados vão. Quinto, medir se os detectores concordam, com o kappa de Fleiss.

## Slide 6: HIPÓTESE

A pesquisa tem uma hipótese só, construída a partir da literatura. Andow e colegas analisaram quase 14 mil aplicativos e viram que até 42,4% omitiam ou declaravam errado para onde iam dados sensíveis. Samarasinghe e colegas, em 1.166 aplicativos de governo, viram que 27% enviavam informações sensíveis a terceiros ou sem criptografia. Carlsson e colegas acharam divergências entre as políticas e o tráfego de aplicativos públicos da Finlândia. E Kollnig e colegas apontaram falta de transparência sobre rastreamento no Android e no iPhone. Daí a hipótese: pelo menos 10% dos pares aplicativo–SDK não terão declaração compatível. Ela se confirma se a proporção que eu encontrar for de 10% ou mais. O 10% fica bem abaixo dessas taxas de propósito: elas contam aplicativos, e eu conto pares, então escolhi um patamar conservador.

LEMBRETE (não precisa falar). Como analiso todos os aplicativos oficiais, e não uma amostra, a decisão usa a proporção encontrada. O intervalo de confiança de 95% só mostra a precisão; ele é calculado agrupando por aplicativo, porque os pares do mesmo aplicativo usam a mesma política. Se der menos de 10%, só dá para dizer que ficou abaixo do meu patamar, não que o governo é mais transparente que nos outros estudos. O 10% é um critério do estudo, não um limite da LGPD.

## Slide 7: ESTUDOS QUE ORIENTAM O PROJETO (1/2)

No referencial, separei seis estudos que orientam o projeto, com o que cada um buscava, o que fez, como fez e o que achou. Os três primeiros tratam de rastreamento e declarações. Binns e colegas examinaram 959 mil aplicativos procurando rastreadores no código e acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam aplicativos de antes e de depois do GDPR, o regulamento europeu, e viram pouca mudança. E Andow e colegas compararam o que os aplicativos enviam com o que as políticas dizem: até 42,4% omitiam ou declaravam errado. É dessa linha que vem o meu método.

## Slide 8: ESTUDOS QUE ORIENTAM O PROJETO (2/2)

Os outros três estudaram aplicativos de governo. Samarasinghe e colegas examinaram 1.166 aplicativos de 71 países: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis a terceiros ou sem criptografia, mas o Brasil não aparece separado. Carlsson e colegas compararam o tráfego de 32 aplicativos públicos da Finlândia com as políticas e acharam divergências, às vezes com dados indo para fora da Europa. É o estudo mais parecido com o meu. E Serrano e colegas acharam rastreadores em 402 de 595 aplicativos da COVID-19.

## Slide 9: LACUNA E CONTRIBUIÇÃO

Juntando esses estudos, aparecem três lacunas, e cada uma vira uma contribuição. Primeiro, o caso brasileiro: há estudos de um aplicativo por vez, mas ninguém mediu o conjunto; o trabalho analisa os 376 aplicativos classificados como oficiais, das três esferas. Segundo, o confronto entre o declarado e o encontrado já foi feito em outros contextos, mas não aqui; o trabalho classifica cada par e testa a hipótese. Terceiro, o instrumento: o trabalho mede quanto o resultado depende do detector. E uma divergência não prova infração à LGPD; é um indício a ser examinado.

## Slide 10: ETAPAS DO MÉTODO

O estudo é quantitativo e observacional, em seis etapas, e cada uma atende a um objetivo. Primeiro, a seleção dos aplicativos. Depois, o download da versão atual, com o hash, que é a impressão digital do arquivo. Em seguida, a detecção dos SDKs com três detectores e a classificação das declarações. A quinta etapa observa o tráfego de uma parte dos aplicativos num emulador Android, com o mitmproxy, que registra as conexões. Por fim, a análise estatística decide a hipótese.

## Slide 11: POR QUE SÓ ANDROID

Por que só Android? São três motivos. Primeiro, abrangência: segundo a StatCounter, o Android está em 73,76% dos celulares no Brasil. Segundo, acesso ao código: Kollnig e colegas explicam que, no iPhone, os aplicativos são criptografados, não há ferramenta pública para baixá-los em escala, e decriptar exige um aparelho físico e tem legalidade incerta. Terceiro, a hipótese usa a seção “Segurança dos dados”, que só existe na Google Play. Isso não quer dizer que o iPhone seja mais seguro: o mesmo estudo achou rastreamento nas duas plataformas. O iOS fica como trabalho futuro.

## Slide 12: APLICATIVOS SELECIONADOS

Para montar a lista, busquei 21 termos ligados a serviço público na Google Play e depois o catálogo de cada publicador oficial. Foram 396 candidatos. Pelo nome jurídico de quem publica, ficaram 376 oficiais: 85 federais, 199 estaduais e 92 municipais. Saíram 20, de empresas privadas ou de contas de pessoa física. A lista é preliminar e será revista antes da coleta.

## Slide 13: FONTE DOS PACOTES

Na hora de buscar os pacotes, apareceu um problema. O AndroZoo, um acervo acadêmico, tinha só 92 dos 396 aplicativos do governo, 23,2%, contra 84,2% dos comerciais. Dependendo só dele, a maioria ficaria de fora. Por isso, a fonte principal será a versão atual da Google Play, que é a que o cidadão instala, baixada com o apkeep, uma ferramenta aberta, com uma conta criada só para a pesquisa. Registro o hash, a versão, a data e o motivo de cada falha. O AndroZoo fica para a reprodutibilidade.

LEMBRETE (não precisa falar). Quando o aplicativo vem dividido em vários pacotes, guardo o APK base, que tem o código. O apkeep é da Electronic Frontier Foundation (EFF). Não redistribuo os pacotes.

## Slide 14: PILOTO DOS DETECTORES

No piloto, testei três detectores em 20 pacotes. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet dentro do pacote. O C faz o mesmo que o B, com a lista da Disconnect. As taxas foram diferentes: 75%, 95% e 80% dos pacotes com rastreador. Revisando as detecções uma a uma, 88 das 123 do B pareciam falsos positivos, quase todas por endereços genéricos do Google ou do Facebook. Ou seja, a ferramenta muda o resultado, e por isso a comparação entre detectores faz parte do método.

LEMBRETE (não precisa falar). A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método). B não é tráfego, é texto dentro do pacote: um link para maps.google.com bastou para apontar Google Ads. C usa só as categorias publicidade, análise de uso e impressão digital. Exodus Privacy: base aberta de rastreadores, com assinaturas de código e de rede. Disconnect: lista de domínios que coletam dados, separados por categoria.

## Slide 15: COMO LER O κ DE FLEISS

Para medir essa concordância, uso o kappa de Fleiss. Ele mede se vários avaliadores concordam, descontando o acordo que aconteceria por acaso; aqui, os avaliadores são os três detectores, e cada um diz se o aplicativo tem ou não rastreador. P o é a concordância observada: em cada aplicativo, a fração dos pares de detectores que concordam; se os três concordam, dá 1; se um discorda, dá um terço. P e é a concordância esperada só por acaso. Descontar o acaso importa porque, se quase todo aplicativo tem rastreador, concordar é fácil. Pela escala de Landis e Koch, o piloto deu 0,52, moderada, e 0,69, substancial, sem os falsos positivos. Meu limiar é 0,6.

LEMBRETE (não precisa falar). Fórmula por aplicativo: P i = soma de n ij vezes (n ij − 1), dividida por n vezes (n − 1), com n = 3 detectores e n ij = quantos deram a resposta j. P e = soma de p j ao quadrado, com p j = proporção de todas as respostas na categoria j. Junto do κ, reporto o IC95% e as concordâncias positiva e negativa, porque o κ fica instável quando quase todos os aplicativos estão na mesma categoria. Na revisão, a reclassificação às cegas da triagem usa o κ de Cohen, a versão para dois avaliadores, com a mesma escala.

## Slide 16: CLASSIFICAÇÃO DAS DECLARAÇÕES

Esta é a parte central do teste. Para cada par, leio a política de privacidade e a seção “Segurança dos dados” e escolho uma de cinco situações: o SDK é citado pelo nome; o tipo de dado e a finalidade estão declarados, mesmo sem o nome; não há declaração compatível; a informação é genérica demais; ou a política não está disponível. A proporção é a terceira situação dividida pelas três primeiras; se der 10% ou mais, a hipótese se confirma. As duas últimas ficam à parte, para não inflar nem esconder o problema. Não citar o nome do SDK, sozinho, não conta como omissão.

## Slide 17: Revisão sistemática

Para a literatura, fiz uma revisão sistemática: uma busca planejada e documentada, para que a escolha dos artigos não dependa de preferência pessoal. Segui o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as palavras de busca e os critérios. O resultado segue o PRISMA 2020, um fluxograma do que entrou e saiu em cada etapa. Foram 15 buscas em quatro bases, de 2018 a 2026, exigindo um termo do tema no título. Para testar as buscas, separei estudos que tinham de aparecer: dos nove dentro do escopo, elas acharam os oito que estão no Scopus. Foram 396 resultados, 312 sem repetidos, e 148 seguiram para a leitura completa, que está em andamento.

Guia de Kitchenham: divide a revisão em planejamento (questões e protocolo), condução (busca, seleção, avaliação de qualidade e extração dos dados) e relatório (síntese dos resultados).

PRISMA 2020: padroniza o relato da revisão num fluxograma, da identificação dos registros e remoção de duplicatas até a triagem, a leitura completa e os estudos incluídos.

## Slide 18: LIMITAÇÕES

Sobre as limitações: achar o SDK no código não prova envio de dados, e por isso registro o tráfego de uma subamostra no emulador. Alguns aplicativos podem não rodar no emulador; nesse caso, registro o motivo. O estudo cobre só Android, pelos motivos que mostrei. As políticas falam de tipos de dados, e não do nome do SDK, então não citar o nome não conta como omissão. Registro a versão de cada pacote, porque eles mudam. E uma divergência não prova infração à LGPD; é um indício.

## Slide 19: PRÓXIMOS PASSOS NO CAPSTONE II (2027.1)

Os próximos passos ficam no Capstone II. Em fevereiro, termino a revisão e reviso a lista de aplicativos, testando o download e o emulador. Em março, baixo os pacotes e rodo os detectores. Entre março e abril, classifico as declarações. Em abril, registro o tráfego da subamostra no emulador. Em maio, faço a análise e decido sobre a hipótese, avisando os órgãos se houver achado grave. Em junho, escrevo, publico os dados e defendo.

## Slide 20: Conclusão

Para concluir: o problema está definido, o método é viável, e a hipótese está pronta para ser testada no Capstone II. O foco é medir o quanto o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles enviam. Obrigado.

## Slide 21: REFERÊNCIAS (1/4)

Não é para ler. São todas as referências do texto do TCC, em ordem alfabética, no padrão ABNT. Pode passar direto para o slide de encerramento.

## Slide 25: Encerramento

Slide de encerramento do template. Pode ficar na tela durante as perguntas.

## Cola para as perguntas

- Números: 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · AndroZoo: 92 de 396 (23,2%) · piloto: 75%, 95% e 80% com rastreador; κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · políticas acessíveis: 323 de 396 (81,6%) · revisão: 396 resultados, 312 sem repetidos, 148 à leitura completa, 31 propostas de inclusão (8 já confirmadas).
- Por que 10%? Fica bem abaixo da literatura (Andow 42,4%; Samarasinghe 27%), que conta aplicativos; eu conto pares, então é um patamar conservador. Se ficar abaixo, não dá para dizer que o governo é mais transparente que nos outros estudos, só que ficou abaixo do meu patamar. Não é limite da LGPD.
- Por que decidir pela proporção, e não pelo intervalo de confiança? Porque analiso todos os aplicativos oficiais, e não uma amostra. O intervalo mostra a precisão e entra como ressalva se incluir os 10%.
- Onde a LGPD obriga o órgão a declarar? Transparência (Art. 6º, VI); informação sobre o uso compartilhado e a finalidade (Art. 9º, V); e, no poder público, informar a previsão legal, a finalidade e as práticas, em veículos de fácil acesso (Art. 23, I). A lei não exige o nome do SDK; exige informar o tratamento e o compartilhamento.
- Por que só Android? 73,76% dos celulares no Brasil (StatCounter, out. 2026); no iPhone os aplicativos são criptografados e não há ferramenta pública para baixá-los em escala (Kollnig et al., 2022); a seção “Segurança dos dados” é da Google Play. Não quer dizer que o iPhone seja mais seguro.
- Como vai observar o tráfego sem celular Android? No emulador do Android Studio, no computador, com o mitmproxy registrando as conexões. Abro cada aplicativo sem login, sem conta pessoal. Se um aplicativo não funcionar no emulador, registro o motivo e reporto quantos foram.
- Por que uma hipótese só? Para concentrar o trabalho no que dá para provar no Capstone II: as declarações. A comparação dos aplicativos com dados sensíveis saiu do projeto.
- O κ de 0,52 não é baixo? É moderado. Por isso a concordância entre detectores é uma checagem do instrumento, com limiar de 0,6, e não uma hipótese.
- Ter o SDK no aplicativo prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos aplicativos.
- Por que a revisão caiu de 1.531 para 396? Exigi um termo do tema no título, comecei em 2018, quando o GDPR passou a valer e a LGPD foi sancionada, e tirei a questão sobre detecção de bibliotecas, que ficou como fundo no referencial. Os estudos de controle dentro desse escopo continuaram sendo achados.
- Você leu todos os artigos? Não. A leitura completa está em andamento: já confirmei parte das decisões lendo o texto inteiro e termino o restante em fevereiro, antes de qualquer resultado.
- Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”
