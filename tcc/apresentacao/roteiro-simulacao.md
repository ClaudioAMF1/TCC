# Roteiro da simulação de defesa

Versão revisada em 21/11/2026, com foco nas declarações de privacidade dos aplicativos governamentais e nos indícios técnicos obtidos na análise dos pacotes. Os aplicativos comerciais ficam só como contexto. São 15 minutos de apresentação e 10 de perguntas. As falas abaixo somam cerca de 12 minutos, o que deixa folga para pausas. O mesmo texto está nas notas de cada slide. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra: leia algumas vezes e fale com as suas palavras, mantendo os números exatos.

## Slide 1. Abertura (30 s)

Bom dia. Meu nome é Claudio, e meu projeto se chama "Quem mais está dentro do aplicativo?". Meu trabalho investiga quais componentes de terceiros estão presentes em aplicativos do governo e se as informações publicadas sobre coleta e compartilhamento de dados são compatíveis com esses componentes. A presença de um SDK, sozinha, não prova envio de dados. Neste semestre, a entrega é o projeto: o problema, o método e os testes que mostram que ele é viável. A coleta principal fica para o Capstone II.

## Slide 2. Por que este tema (50 s)

Hoje muito serviço público passa pelo celular: o Meu INSS e o Meu SUS Digital têm mais de 50 milhões de instalações cada um. Quase nenhum aplicativo é escrito do zero. Como mostra o esquema, além do código do próprio órgão, ele incorpora SDKs, que são bibliotecas prontas de outras empresas, para medir o uso, enviar notificações ou mostrar mapas. O código do órgão conversa com o servidor do órgão; já os SDKs podem enviar identificadores do aparelho e dados de uso para os servidores das empresas que os fornecem. Num aplicativo comercial, o usuário pode trocar de serviço. No do INSS, não: quem paga o benefício é o INSS. Por isso vale perguntar quem mais recebe os dados desses aplicativos.

## Slide 3. O que a literatura já sabe (60 s)

Binns e colegas analisaram cerca de 959 mil aplicativos da Google Play e mostraram que a maioria tem rastreadores de terceiros, concentrados em poucas empresas, como Google e Facebook. Kollnig e colegas compararam aplicativos de antes e de depois do regulamento europeu de proteção de dados: o rastreamento quase não mudou, e o consentimento raramente é pedido. O estudo mais próximo do meu é o de Samarasinghe e colegas, de 2022: 1.166 aplicativos de governo de 71 países, dos quais 269, ou 23,1%, enviaram dados do aparelho a rastreadores conhecidos.

## Slide 4. O que este trabalho acrescenta (50 s)

São três coisas. Primeiro, o caso brasileiro: no estudo internacional, o Brasil aparece só em exemplos, sem separar esfera de governo nem os aplicativos que tratam dados sensíveis. Segundo, o confronto entre as declarações de privacidade e o que pode ser identificado tecnicamente. Vou verificar a função dos SDKs e as categorias e finalidades declaradas. Onde houver observação de tráfego, também vou comparar os destinatários efetivos. Uma divergência é um indício a investigar, não prova isolada de ilegalidade. Terceiro, o instrumento: vou rodar mais de um detector sobre os mesmos pacotes e medir quanto eles concordam, porque a taxa publicada depende da ferramenta usada.

## Slide 5. Pergunta e objetivos (50 s)

A pergunta de pesquisa é: em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado nas políticas de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo geral é medir a proporção de SDKs e de envios de dados sem declaração compatível. A presença de código é examinada na análise estática; os envios só podem ser confirmados pela análise dinâmica de uma subamostra. Os objetivos específicos são: confirmar quais aplicativos são de fato oficiais; detectar os SDKs por esfera de governo e por tratamento de dado sensível; confrontar o que for encontrado com a política de privacidade e com a seção "Segurança dos dados" da loja; observar numa subamostra para onde os dados vão, inclusive se saem do país; e medir a concordância entre os detectores.

## Slide 6. Hipóteses (70 s)

Tenho uma hipótese central e uma secundária. A H1 propõe que ao menos 10% dos pares aplicativo–SDK identificados não tenham declaração compatível na política de privacidade e na seção “Segurança dos dados”. A declaração por categoria de dados e finalidade pode ser suficiente: não se exige que a política liste nominalmente todos os SDKs. O patamar de 10% significa que, se pelo menos um em cada dez pares avaliáveis não tiver declaração compatível, o resultado merece ser quantificado e discutido. É uma escolha do estudo, não uma tolerância prevista na LGPD. Andow e colegas encontraram até 42,4% de inconsistências em outra população e com outro método, portanto não é uma taxa diretamente comparável. A H2 considera que aplicativos com dados sensíveis não apresentam uma prevalência menor de SDKs do que os demais aplicativos governamentais. Essa é uma comparação dentro do próprio corpus. A comparação comercial permanece apenas como contexto. A concordância dos detectores é uma checagem do instrumento, sem numeração como hipótese.

## Slide 7. Método (60 s)

O método tem seis etapas. Primeiro, confirmar os aplicativos oficiais encontrados na Google Play. Segundo, caracterizar o corpus por esfera e tipo de serviço. Terceiro, obter a versão atual dos pacotes, quando tecnicamente disponível, registrando o hash; o AndroZoo será usado para reprodutibilidade e comparação de versões. Quarto, identificar os SDKs e verificar se os detectores concordam. Quinto, confrontar cada componente com as categorias de dados e finalidades informadas nas políticas e na seção "Segurança dos dados". Sexto, calcular as proporções de divergência. A observação dinâmica de uma subamostra complementará a análise. Os dados e o piloto já realizados demonstram viabilidade, não resultados finais.

## Slide 8. Corpus (50 s)

A busca encontrou 396 candidatos. Conferindo o nome jurídico de cada publicador, que a loja mostra em "Sobre o desenvolvedor", 376 ficaram como oficiais. No gráfico, são 85 federais, 199 estaduais e 92 municipais; a parte escura de cada barra mostra os que tratam dado de saúde ou biometria, 100 no total. Saíram 20: 13 eram empresas privadas usando nome de serviço público e 7 eram contas de pessoa física. Também separei 252 aplicativos comerciais, que servem só como referência. Essa classificação ainda é preliminar e será conferida antes da coleta principal.

## Slide 9. Anúncios declarados (45 s)

Um primeiro dado, tirado dos metadados da loja: nenhum dos 376 aplicativos do governo declara exibir anúncios, contra 63 dos 190 aplicativos comerciais da primeira referência, ou 33,2%. No gráfico, as linhas mostram o intervalo de confiança de 95%: no governo, de 0 a 1%; nos comerciais, de 27% a 40%. Mas isso fala só de anúncio, e quem declara é o próprio publicador. Um aplicativo sem anúncio pode ter um SDK de análise de uso, por exemplo. É exatamente esse o ponto do trabalho: a declaração vem do publicador, e só a análise dos pacotes mostra o que o aplicativo de fato carrega.

## Slide 10. Piloto dos detectores (60 s)

O piloto testou o instrumento em 20 pacotes do AndroZoo, com três detectores. O A procura o código do SDK, com a base do Exodus. O B procura domínios dentro do pacote, também com a base do Exodus. O C procura domínios com a lista da Disconnect. O A achou rastreador em 75% dos aplicativos, o B em 95% e o C em 80%: mesma amostra, taxas diferentes. O κ de Fleiss foi 0,52. Na adjudicação das 223 detecções, 88 das 123 do B (71,5%) foram classificadas como falsos positivos potenciais, sobretudo por referências a domínios genéricos. Desconsiderando essas detecções numa análise de sensibilidade, o κ passa de 0,52 para 0,69. Essa classificação não equivale a uma validação independente por verdade de referência. Por isso proponho usar o A como medida principal, o que ainda vou confirmar com o orientador.

## Slide 11. Onde estão os pacotes (40 s)

Na consulta histórica, encontrei no AndroZoo apenas 92 dos 396 candidatos governamentais, ou 23,2%. Isso mostra que depender exclusivamente desse acervo poderia deixar a maior parte do corpus de fora. Vou priorizar as versões disponíveis na Google Play e documentar as limitações de coleta. As versões arquivadas no AndroZoo permitem avaliar mudanças entre versões e tornar parte da análise reproduzível.

## Slide 12. Revisão sistemática (55 s)

A fundamentação vem de uma revisão sistemática, seguindo Kitchenham e o PRISMA 2020, com cinco questões de pesquisa. Fiz 17 buscas no Scopus, IEEE Xplore, BDTD e SBC OpenLib, que retornaram 1.531 registros, ou 1.249 sem duplicatas. Para validar as buscas, usei 11 estudos que tinham de aparecer; os 10 que o Scopus indexa foram encontrados. Na triagem por título e resumo, 357 registros foram encaminhados à fase de texto completo. Dos 214 inicialmente priorizados para obtenção, foram recuperados 80 textos correspondentes: 71 receberam proposta de inclusão, 7 de exclusão e 2 ficaram com dúvida de escopo. Houve ainda uma exclusão por evidência de versão ampliada. A Seção 2.7 apresenta uma síntese provisória dos 71. Em 21/11 conferi 18 das 79 decisões, com leitura integral e avaliação de qualidade; as outras 61 e a leitura do restante ficam para o Capstone II.

## Slide 13. Limitações e próximos passos (65 s)

As limitações: achar o código de um SDK no pacote não prova que ele roda nem que envia dados, e por isso há a análise dinâmica numa subamostra. O estudo cobre só Android e Google Play. As políticas costumam declarar categorias de dados, e não a lista de SDKs; por isso o confronto separa a menção ao SDK pelo nome, a declaração por categoria e a ausência de menção. A seleção da revisão tem um revisor, e os detectores compartilham bases ou métodos de extração. Até 3 de dezembro, incorporo os comentários do orientador e da simulação e faço a revisão final do texto. No Capstone II, concluo a leitura e a avaliação dos artigos que faltam, confiro as classificações dos aplicativos e defino com o orientador o detector principal e o plano de análise. Depois vêm a coleta, a detecção, o confronto com as políticas e a análise dinâmica.

## Slide 14. Encerramento (10 s)

A pergunta que orienta o trabalho é simples: as práticas associadas aos componentes de terceiros nos aplicativos do governo são compatíveis com o que é informado ao cidadão? Obrigado.

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
