# Roteiro da simulação de defesa

Versão de 24/11/2026, igual às notas do seu arquivo `apresentacao_TCC1.pptx`, editado no Google Slides (no repositório, `simulacao-defesa-rascunho.pptx`), com 17 slides no padrão do template do IDP, na mesma ordem do texto do TCC (introdução, referencial teórico, procedimentos metodológicos, conclusão e referências). São 15 minutos de apresentação e 10 de perguntas. As falas somam cerca de 12 minutos, num ritmo calmo, o que deixa folga para pausas. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra. A fala de cada slide vem primeiro; os lembretes e as explicações para consulta vêm em destaque logo abaixo. Fale com as suas palavras e mantenha os números exatos.

## Slide 1. Abertura (25 s)

Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu projeto se chama “Quem mais está dentro do aplicativo?”. Muitos aplicativos do governo trazem, dentro deles, código de outras empresas, que pode coletar dados de quem usa. Eu quero descobrir que código é esse e se o governo avisa o cidadão sobre isso.

## Slide 2. Agenda (25 s)

Vou seguir a mesma ordem do texto do TCC. Primeiro, a introdução: por que o tema importa, a pergunta, os objetivos e as hipóteses. Depois, o referencial teórico: os estudos em que me baseio e o que ainda falta neles. Em seguida, os procedimentos metodológicos: como vou fazer a pesquisa e o que já testei. No fim, a conclusão e as referências.

## Slide 3. Motivação (40 s)

Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada. Só que esses aplicativos não têm só o código do órgão: eles trazem pedaços prontos de outras empresas, os SDKs, para coisas como mapas, notificações e estatísticas de uso. Alguns desses SDKs podem coletar dados de quem usa. No governo isso pesa mais, porque o cidadão não tem como trocar de aplicativo. e um detalhe importante: o SDK estar dentro do aplicativo não prova que ele enviou dados.

## Slide 4. Pergunta e objetivos (35 s)

A minha pergunta é: em que medida os aplicativos oficiais do governo trazem SDKs de rastreamento e enviam dados a terceiros sem avisar isso na política de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo é medir essa proporção, à luz da LGPD. São cinco passos: conferir quais aplicativos são mesmo oficiais, detectar os SDKs, comparar com o que cada aplicativo declara, observar o tráfego numa parte deles e verificar se os detectores concordam.

## Slide 5. Hipóteses (75 s)

Tenho duas hipóteses. A H1 é a principal. Dentro de cada aplicativo, eu olho cada SDK encontrado; cada combinação de um aplicativo com um SDK é um par. Para cada par, verifico se o aplicativo avisa o que aquele SDK faz, na política de privacidade ou na seção “Segurança dos dados”. Não precisa citar o nome do SDK: basta dizer que tipo de dado é coletado e para quê. Por exemplo: se um aplicativo tem um SDK de estatísticas de uso e não avisa em lugar nenhum que coleta dados de uso, esse par fica sem declaração. A H1 diz que isso acontece em pelo menos 1 de cada 10 pares. Esse 10% é um critério que eu defini para o estudo, não um limite da LGPD. A H2 é secundária. Seria de esperar que os aplicativos com dados sensíveis, como os de saúde, tivessem menos SDKs; a minha hipótese é que não têm menos. Os aplicativos comerciais ficam só como contexto, e a concordância entre os detectores serve para checar a ferramenta; não é uma hipótese.

> **Lembrete, não precisa falar.** Como a H1 é testada: calculo a porcentagem de pares sem declaração, com intervalo de confiança de 95%. Os pares do mesmo aplicativo usam a mesma política, então o intervalo é calculado agrupando por aplicativo. A H1 só é rejeitada se até o limite de cima do intervalo ficar abaixo de 10%. A H2 só é rejeitada se os dados mostrarem claramente que os aplicativos sensíveis têm menos SDKs. Por que 10%: Andow et al. (2020) acharam até 42,4% de apps com declaração errada ou omitida, em outra população e contando por app; isso mostra que o problema é comum, e 10% é um patamar modesto.

## Slide 6. O que a literatura já mostrou (55 s)

No referencial teórico, parto de três estudos. Binns e colegas baixaram cerca de 959 mil aplicativos e procuraram rastreadores no código, sem executar os apps: acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam cerca de um milhão de aplicativos de 2017 com um milhão de 2020, antes e depois do GDPR, o regulamento europeu de proteção de dados, e viram pouca mudança, o que sozinho não prova efeito da lei. Samarasinghe e colegas acharam 1.166 aplicativos de governo de 71 países pelos links nos sites oficiais e examinaram os SDKs e os dados enviados: 37% tinham rastreadores do Google, e 27% enviavam dados sensíveis, como identificadores, a terceiros ou sem criptografia. Ou seja, o problema existe também no governo, e vale olhar o caso brasileiro.

## Slide 7. Lacuna e contribuição (45 s)

O que falta nesses estudos, pelo menos na literatura que examinei até agora: nenhum mede os SDKs no conjunto dos aplicativos do governo brasileiro comparando com o que cada um declara. Essa é a lacuna. A contribuição tem três partes. Primeiro, estudar os aplicativos federais, estaduais e municipais, separando os que tratam dados sensíveis. Segundo, comparar o que os SDKs fazem com o que cada aplicativo declara e, numa parte deles, com o tráfego observado. Terceiro, medir o quanto o resultado muda conforme o detector. E uma divergência não é prova de infração à LGPD; é um indício que merece ser examinado.

## Slide 8. Método (40 s)

Nos procedimentos metodológicos, o estudo é quantitativo e observacional, em seis etapas. primeira: conferir quais aplicativos são oficiais. segunda: separar por esfera de governo e tipo de serviço. terceira: baixar a versão atual de cada aplicativo na Google Play, registrando o hash, que é a impressão digital do arquivo. quarta: rodar os detectores e comparar o que cada um encontra. quinta: comparar o que foi detectado com a política de privacidade e com a declaração na loja. sexta: calcular as proporções com intervalo de confiança e, numa parte dos aplicativos, observar o tráfego de rede.

## Slide 9. Corpus (30 s)

Na busca, encontrei 396 aplicativos candidatos. Conferindo o nome jurídico de quem publica, 376 ficaram como oficiais: 85 federais, 199 estaduais e 92 municipais. Vinte saíram: 13 eram de empresas privadas usando nome de serviço público e 7 estavam em contas de pessoa física. Cem dos 376 podem tratar dados sensíveis, como saúde ou biometria. essa é uma classificação preliminar e ainda vai ser conferida antes da coleta.

## Slide 10. Anúncios (30 s)

Um dado que a própria Google Play mostra é se o aplicativo declara exibir anúncios. Nenhum dos 376 aplicativos do governo declara. Entre os comerciais da referência, foram 63 de 190, ou 33,2%. isso é o que o publicador declara, e não diz nada sobre os SDKs de análise ou de rastreamento que estão dentro do aplicativo. E os comerciais servem só de contexto, não de grupo de controle.

> **Lembrete, não precisa falar.** Os intervalos no slide: com 0 em 376, a proporção real de apps do governo que declaram anúncios fica, com 95% de confiança, entre 0% e 1,0%; nos comerciais, entre 26,9% e 40,1%. Valem só para essa declaração, não para os SDKs.

## Slide 11. Fonte dos APKs (55 s)

Um problema prático apareceu na hora de buscar os pacotes. O AndroZoo, um acervo acadêmico de aplicativos, tinha só 92 dos 396 do governo, ou 23,2%; dos comerciais, tinha 160 de 190, ou 84,2%. Dependendo só dele, muitos aplicativos do governo ficariam de fora. Por isso a fonte principal vai ser a versão atual da Google Play, que é a que o cidadão instala. O download vai ser feito com o apkeep, uma ferramenta aberta, com uma conta Google criada só para a pesquisa, a partir do Brasil. Para cada aplicativo, registro o hash, a versão, a data e, se falhar, o motivo; a falha também vira dado. O AndroZoo continua útil para reproduzir a análise. Antes do corpus inteiro, testo em cinco aplicativos.

> **Lembrete, não precisa falar.** Quando o app vem dividido em vários pacotes, guardo o APK base, que tem o código. O apkeep é da Electronic Frontier Foundation (EFF). Não redistribuo os pacotes.

## Slide 12. Piloto dos detectores (65 s)

Fiz um piloto com 20 pacotes do AndroZoo e três detectores. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet escritos dentro do pacote. O C faz o mesmo que o B, com outra lista, a da Disconnect. Cada um deu uma taxa diferente: 75%, 95% e 80% dos pacotes com pelo menos um rastreador. A concordância entre eles, medida pelo kappa de Fleiss, em que 1 é concordância total, foi 0,52. Conferi as detecções uma a uma e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por endereços genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas é só uma análise de sensibilidade, porque não há uma referência independente com a resposta certa. Conclusão: a ferramenta escolhida muda o resultado, e é por isso que comparar os detectores faz parte do método.

> **Lembrete, não precisa falar.** A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método). B não é tráfego, é texto dentro do pacote: um link para maps.google.com bastou para apontar Google Ads. C usa só as categorias publicidade, análise de uso e impressão digital.Exodus Privacy (εxodus): É uma plataforma sem fins lucrativos que analisa aplicativos Android para identificar rastreadores (trackers de anúncios, telemetria e análise) e permissões perigosas embutidas no código, utilizando assinaturas de SDKs de terceiros. Disconnect: É um catálogo estruturado em formato JSON que classifica milhares de domínios da internet que coletam dados dos usuários, dividindo-os em categorias como Advertising (Publicidade), Analytics (Análise), Social (Redes Sociais), Fingerprinting e Cryptomining.

## Slide 13. Revisão sistemática (80 s)

Agora, como eu busquei a literatura. Fiz uma revisão sistemática, que é uma busca planejada e documentada, para que a escolha dos artigos não dependa de preferência pessoal. Para fazer a revisão, segui o guia de Kitchenham, que é um passo a passo muito usado em computação: antes de buscar, escrevi um protocolo dizendo quais perguntas quero responder, onde vou buscar, com quais palavras e quais estudos entram ou saem. Para mostrar o resultado, uso o PRISMA 2020, que é um padrão de prestação de contas: um fluxograma com quantos estudos entraram e saíram em cada etapa. Fiz 17 buscas, em quatro bases: Scopus, que é a principal, IEEE Xplore e, para trabalhos brasileiros, SBC OpenLib e BDTD. Cada busca combina três ideias: aplicativo de celular, o tema, como rastreador ou política de privacidade, e, quando precisa, o contexto, como governo ou Brasil. Para testar as buscas, separei antes onze estudos que tinham de aparecer: elas acharam os dez que estão no Scopus, e o décimo primeiro não está nessa base. No fim, os 1.531 resultados viraram 1.249 sem repetidos, e 357 passaram para a leitura completa.

> **Para consulta, não precisa falar.** Guia de Kitchenham: Ele divide a pesquisa em três etapas principais: Planejamento, onde se definem as questões de pesquisa e o protocolo com critérios de inclusão e exclusão; Condução, onde os artigos são buscados em bases científicas, filtrados, avaliados quanto à qualidade e têm seus dados extraídos; e Relatório, onde os resultados são sintetizados e apresentados para responder às perguntas iniciais.

> **Para consulta, não precisa falar.** Fluxo PRISMA: padroniza a visualização e o relato das etapas de identificação, triagem e inclusão de estudos em revisões sistemáticas. O processo divide-se no mapeamento inicial de registros e remoção de duplicatas, na avaliação por títulos, resumos e textos completos, e na consolidação final dos estudos incluídos.

## Slide 14. Limitações e próximos passos (50 s)

Sobre as limitações: achar o SDK no código não prova que ele envia dados; o estudo cobre só Android e a Google Play; as políticas costumam falar de tipos de dados, e não do nome de cada SDK; as versões podem mudar entre a coleta e a análise; e a revisão e as classificações ainda estão sendo conferidas. Os próximos passos: até 3 de dezembro, ajustar o texto com o retorno do orientador e desta simulação. Em fevereiro, terminar a revisão e conferir o corpus. Em março e abril, a coleta, a detecção e a comparação com as declarações. Em maio e junho, a análise, a discussão jurídica e a defesa.

## Slide 15. Conclusão (30 s)

Para concluir: o problema está definido, o método é viável, e os resultados ainda são preliminares. O foco não é comparar o governo com o mercado, mas verificar se o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles realmente enviam. É isso que permite falar com segurança sobre privacidade, transparência e dependência de fornecedores. Obrigado.

## Slide 16. Referências (10 s)

Não é para ler. Depois do obrigado, avance para este slide e deixe-o na tela por alguns segundos, ou no começo das perguntas.

**Cola para as perguntas** (fica nas notas deste slide; não é para ler em voz alta):

- Números: 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · 0 de 376 declaram anúncios, contra 63 de 190 comerciais · κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · AndroZoo: 92 de 396 (23,2%) · revisão: 1.531, 1.249, 357, 18 decisões conferidas.
- Por que 10%? É um critério do estudo, não da LGPD. O Andow achou até 42,4% de apps com declaração errada ou omitida, mas em outra população e contando por app.
- O κ de 0,52 não é baixo? É, e por isso a concordância entre detectores virou checagem do instrumento, e não hipótese.
- Ter o SDK no app prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos apps.
- Por que não comparar com apps comerciais? A coleta deles não foi planejada para um teste justo; ficam só como contexto.
- Por que só Android? Porque dá para obter e examinar o pacote; a limitação está declarada.
- Como sabe que o app é oficial? Pelo nome jurídico em “Sobre o desenvolvedor”; a classificação ainda vai ser conferida antes da coleta.
- Você leu os 71 artigos? Não todos. São propostas de uma primeira leitura, cada uma com a página da informação. Conferi 18 decisões lendo o texto inteiro e confiro as outras em fevereiro, antes de qualquer resultado.
- Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”

## Slide 17. Encerramento

Sem fala. Pode ficar na tela durante as perguntas.

**Cola para as perguntas** (fica nas notas deste slide; não é para ler em voz alta):

- Números: 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · 0 de 376 declaram anúncios, contra 63 de 190 comerciais · κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · AndroZoo: 92 de 396 (23,2%) · revisão: 1.531, 1.249, 357, 18 decisões conferidas.
- Por que 10%? É um critério do estudo, não da LGPD. O Andow achou até 42,4% de apps com declaração errada ou omitida, mas em outra população e contando por app.
- O κ de 0,52 não é baixo? É, e por isso a concordância entre detectores virou checagem do instrumento, e não hipótese.
- Ter o SDK no app prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos apps.
- Por que não comparar com apps comerciais? A coleta deles não foi planejada para um teste justo; ficam só como contexto.
- Por que só Android? Porque dá para obter e examinar o pacote; a limitação está declarada.
- Como sabe que o app é oficial? Pelo nome jurídico em “Sobre o desenvolvedor”; a classificação ainda vai ser conferida antes da coleta.
- Você leu os 71 artigos? Não todos. São propostas de uma primeira leitura, cada uma com a página da informação. Conferi 18 decisões lendo o texto inteiro e confiro as outras em fevereiro, antes de qualquer resultado.
- Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”

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

**Você leu os 71 artigos?**
Não todos. Os 71 são propostas registradas numa primeira leitura dos textos obtidos, cada uma com a página de onde saiu a informação. Eu conferi 18 decisões lendo o texto inteiro, 12 delas de inclusão, e confiro as outras em fevereiro, antes de qualquer resultado. Só se perguntarem quem fez essa primeira leitura: foi feita com apoio de ferramenta de IA, e por isso nenhuma decisão vale antes da minha conferência.

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
| 2 | Agenda: os capítulos 1 a 3, a conclusão e as referências, como no sumário |
| 3 a 5 | Capítulo 1, Introdução: abertura, 1.1 a 1.5 (problema, objetivos, hipóteses e justificativa) |
| 6 e 7 | Capítulo 2, Referencial teórico: Binns et al. (2018b), Kollnig et al. (2021a) e Samarasinghe et al. (2022); lacuna no fim da Seção 2.7 |
| 8 e 9 | Capítulo 3: abertura e Seções 3.1 a 3.4 |
| 10 a 12 | Seção 3.5 (anúncios declarados, fonte dos pacotes e piloto dos detectores) |
| 13 | Seção 3.6, Figura 1 e protocolo da revisão (strings) |
| 14 | Seções 3.8, 3.11 e 3.12 |
| 16 | Referências do texto: as 11 obras citadas nos slides e na fala |
| 17 | Encerramento do template, sem conteúdo |
