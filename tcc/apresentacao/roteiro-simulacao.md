# Roteiro da simulação de defesa

Versão de 16/11/2026. São 15 minutos de apresentação e 10 de perguntas. As falas abaixo somam cerca de 12 minutos, o que deixa folga para pausas. O mesmo texto está nas notas de cada slide. Ensaie com cronômetro pelo menos três vezes e grave uma delas.

Não é para decorar palavra por palavra: leia algumas vezes e fale com as suas palavras, mantendo os números exatos.

## Slide 1. Abertura (30 s)

Bom dia. Meu nome é Claudio, e meu projeto se chama "Quem mais está dentro do aplicativo?". Eu investigo se os aplicativos oficiais do governo brasileiro carregam bibliotecas de rastreamento de outras empresas, e se isso acontece mais ou menos do que em aplicativos comerciais parecidos. Neste semestre, a entrega é o projeto: o problema, o método e os testes que mostram que ele é viável. A coleta principal fica para o Capstone II.

## Slide 2. Por que este tema (50 s)

Hoje muito serviço público passa pelo celular: o Meu INSS e o Meu SUS Digital têm mais de 50 milhões de instalações cada um. Quase nenhum aplicativo é escrito do zero. Como mostra o esquema, além do código do próprio órgão, ele incorpora SDKs, que são bibliotecas prontas de outras empresas, para medir o uso, enviar notificações ou mostrar mapas. O código do órgão conversa com o servidor do órgão; já os SDKs podem enviar identificadores do aparelho e dados de uso para os servidores das empresas que os fornecem. Num aplicativo comercial, o usuário pode trocar de serviço. No do INSS, não: quem paga o benefício é o INSS. Por isso vale perguntar quem mais recebe os dados desses aplicativos.

## Slide 3. O que a literatura já sabe (60 s)

Binns e colegas analisaram cerca de 959 mil aplicativos da Google Play e mostraram que a maioria tem rastreadores de terceiros, concentrados em poucas empresas, como Google e Facebook. Kollnig e colegas compararam aplicativos de antes e de depois do regulamento europeu de proteção de dados: o rastreamento quase não mudou, e o consentimento raramente é pedido. O estudo mais próximo do meu é o de Samarasinghe e colegas, de 2022: 1.166 aplicativos de governo de 71 países, dos quais 269, ou 23,1%, enviaram dados do aparelho a rastreadores conhecidos.

## Slide 4. O que este trabalho acrescenta (50 s)

São três coisas. Primeiro, o caso brasileiro: no estudo internacional, o Brasil aparece só em exemplos, sem separar esfera de governo nem os aplicativos que tratam dados sensíveis. Segundo, uma linha de base: vou comparar os aplicativos do governo com aplicativos comerciais da mesma categoria e faixa de instalações, para saber se o governo rastreia mais, menos ou igual ao mercado. Terceiro, o instrumento: vou rodar mais de um detector sobre os mesmos pacotes e medir quanto eles concordam, porque a taxa publicada depende da ferramenta usada.

## Slide 5. Pergunta e objetivos (50 s)

A pergunta de pesquisa é: os aplicativos oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros, e em que medida isso difere de aplicativos comerciais de mesma categoria e porte? O objetivo geral é medir essa prevalência e compará-la. Os objetivos específicos são: confirmar quais aplicativos são de fato oficiais; contar os SDKs por esfera de governo e por tratamento de dado sensível; confrontar o que for encontrado com a política de privacidade; observar para onde os dados vão numa subamostra; e medir a concordância entre os detectores.

## Slide 6. Hipóteses (75 s)

São quatro hipóteses, cada uma com um critério de rejeição definido antes da coleta. H1 é a hipótese nula de que a prevalência é igual nos dois grupos. Eu a rejeito se o intervalo de confiança da razão de prevalências, ajustada por categoria e porte, não incluir 1. Não rejeitar H1 não prova que os grupos são iguais. H2 diz que pelo menos 10% dos pares aplicativo–SDK não aparecem declarados na política; rejeito se o limite superior do intervalo ficar abaixo de 10%. H3 diz que os aplicativos que tratam dado de saúde ou biométrico não rastreiam menos que os outros do governo. E H4 diz que a concordância entre detectores é baixa, com κ de Fleiss abaixo de 0,6. Esses critérios serão congelados com o orientador antes da análise principal.

## Slide 7. Método (65 s)

O método é quantitativo, observacional e comparativo, em seis passos. Primeiro, o corpus: busquei aplicativos na Google Play com 21 termos ligados a serviço público e depois expandi pelo catálogo de cada órgão encontrado. Segundo, o controle comercial, por categoria e porte. Terceiro, os pacotes: o AndroZoo, que é um acervo acadêmico, quando o aplicativo está lá, e a própria loja nos demais casos, sempre com o hash registrado. Quarto, a detecção, com mais de um detector. Quinto, o confronto com a política de privacidade e com a seção "Segurança dos dados" da loja. Sexto, a estatística, com o plano congelado antes. O corpus, o controle e um piloto com 20 pacotes já foram feitos.

## Slide 8. Corpus (50 s)

A busca encontrou 396 candidatos. Conferindo o nome jurídico de cada publicador, que a loja mostra em "Sobre o desenvolvedor", 376 ficaram como oficiais. No gráfico, são 85 federais, 199 estaduais e 92 municipais; a parte escura de cada barra mostra os que tratam dado de saúde ou biometria, 100 no total. Saíram 20: 13 eram empresas privadas usando nome de serviço público e 7 eram contas de pessoa física. O controle comercial tem 252 aplicativos. Essa classificação ainda é preliminar e será conferida antes da coleta principal.

## Slide 9. Anúncios declarados (45 s)

Um primeiro dado, tirado dos metadados da loja: nenhum dos 376 aplicativos do governo declara exibir anúncios, contra 63 dos 190 aplicativos do controle original, ou 33,2%. No gráfico, as linhas mostram o intervalo de confiança de 95%: no governo, de 0 a 1%; no controle, de 27% a 40%. Mas isso fala só de anúncio, e quem declara é o próprio publicador. Um aplicativo sem anúncio pode ter um SDK de análise de uso, por exemplo. Quem vai dizer quais SDKs existem é a análise dos pacotes.

## Slide 10. Piloto dos detectores (60 s)

O piloto testou o instrumento em 20 pacotes do AndroZoo, com três detectores. O A procura o código do SDK, com a base do Exodus. O B procura domínios dentro do pacote, também com a base do Exodus. O C procura domínios com a lista da Disconnect. O A achou rastreador em 75% dos aplicativos, o B em 95% e o C em 80%: mesma amostra, taxas diferentes. O κ de Fleiss foi 0,52. Na adjudicação das 223 detecções, 88 das 123 do B (71,5%) foram classificadas como falsos positivos potenciais, sobretudo por referências a domínios genéricos. Desconsiderando essas detecções numa análise de sensibilidade, o κ passa de 0,52 para 0,69. Essa classificação não equivale a uma validação independente por verdade de referência. Por isso proponho usar o A como medida principal, o que ainda vou confirmar com o orientador.

## Slide 11. Onde estão os pacotes (40 s)

Outro achado: o AndroZoo tinha só 92 dos 396 candidatos do governo, 23,2%, contra 84,2% do controle. Mesmo comparando aplicativos da mesma faixa de instalações, a chance de um aplicativo do governo estar no acervo é bem menor. Então a maior parte do corpus vai ser baixada direto da loja, com o hash de cada pacote registrado.

## Slide 12. Revisão sistemática (55 s)

A fundamentação vem de uma revisão sistemática, seguindo Kitchenham e o PRISMA 2020, com cinco questões de pesquisa. Fiz 17 buscas no Scopus, IEEE Xplore, BDTD e SBC OpenLib, que retornaram 1.531 registros, ou 1.249 sem duplicatas. Para validar as buscas, usei 11 estudos que tinham de aparecer; os 10 que o Scopus indexa foram encontrados. Na triagem por título e resumo, 357 registros foram encaminhados à fase de texto completo. Dos 214 inicialmente priorizados para obtenção, foram recuperados 80 textos correspondentes: 71 receberam proposta de inclusão, 7 de exclusão e 2 ficaram com dúvida de escopo. Houve ainda uma exclusão por evidência de versão ampliada. A Seção 2.7 apresenta uma síntese provisória dos 71; a validação das decisões e a leitura do restante continuam pendentes.

## Slide 13. Limitações e próximos passos (65 s)

As limitações: achar o código de um SDK no pacote não prova que ele roda nem que envia dados, e por isso há a análise dinâmica numa subamostra. O estudo cobre só Android e Google Play. O controle não é uma amostra aleatória do mercado. E os detectores compartilham bases ou métodos de extração. Até a entrega de 3 de dezembro, reviso a síntese dos estudos no referencial e passo o projeto pelo orientador. No Capstone II, termino a revisão, confiro as classificações e defino com o orientador o detector principal e o plano de análise. Depois vêm a coleta, a detecção, o confronto com as políticas e a análise dinâmica.

## Slide 14. Encerramento (10 s)

A pergunta que fica é: quanto do resultado depende dos aplicativos, e quanto depende da ferramenta usada para medir? Obrigado.

---

## Perguntas prováveis

**Como você decide que um aplicativo é oficial? Por que 20 saíram?**
Pelo nome jurídico do publicador, que a loja mostra em "Sobre o desenvolvedor". Treze eram empresas privadas com nome de serviço público e sete eram contas de pessoa física. A classificação será conferida antes da coleta principal.

**O que há de novo em relação a Samarasinghe et al.?**
O caso brasileiro separado por esfera e por dado sensível, a comparação com controles comerciais pareados e a medida de concordância entre detectores sobre as mesmas versões dos pacotes.

**Ter o SDK no pacote prova que dados são enviados?**
Não. A análise estática mostra presença de código. O envio só é observado na análise dinâmica da subamostra. O texto separa presença, transmissão observada e declaração.

**Se o detector B errou 71,5%, por que mantê-lo?**
Ele não é a medida principal proposta. Como A e B usam a mesma base com métodos diferentes, a diferença ilustra o efeito do método, que a H4 pretende medir. Os 88 casos foram considerados falsos positivos potenciais na adjudicação interna, não confirmados por um padrão de referência externo.

**Como você vai obter os pacotes que o AndroZoo não tem? Isso é permitido?**
Baixando da Google Play com conta própria, registrando o hash e sem redistribuir os pacotes. O procedimento será testado em cinco aplicativos no início do Capstone II.

**O que "soberania de dados" quer dizer no seu trabalho?**
A capacidade do Estado de saber e decidir para onde vão os dados gerados nos seus serviços. Mede-se pela dependência de SDKs de terceiros e, na subamostra, pelos destinos observados. A nacionalidade do fornecedor ou o país de um IP não provam, sozinhos, uma transferência internacional.

**Quantos artigos a revisão incluiu?**
Até 13/11, há 71 propostas de inclusão, não 71 inclusões definitivamente validadas. A Seção 2.7 traz a síntese provisória. Faltam 278 registros em aberto e a conferência pessoal das propostas registradas.

**Por que o controle não é aleatório?**
A busca da loja ordena por relevância e quase não devolve aplicativos comerciais pequenos. O pareamento por categoria e faixa reduz esse problema, a H1 fica restrita às células com controle e a limitação é declarada.

**Por que κ e não só a porcentagem de acordo?**
O κ desconta o acordo esperado ao acaso. Como prevalência muito alta deixa o κ instável, ele será reportado junto com os acordos positivo e negativo.

**Como as classificações foram feitas e conferidas?**
Responda como de fato aconteceu, incluindo as ferramentas usadas e o que o orientador avaliou. As duas classificações serão conferidas no início do Capstone II.

## Fontes de cada slide

| Slide | Onde está no projeto |
|---|---|
| 2 a 4 | Seções 1 e 2; Binns et al. (2018b); Kollnig et al. (2021a, 2021b); Samarasinghe et al. (2022) |
| 5 e 6 | Seções 1.1 a 1.4 e 3.10 |
| 7 | Seções 3.1 a 3.5 |
| 8 a 11 | Seção 3.6 |
| 12 | Seções 2.7 e 3.7 e Figura 1 |
| 13 | Seções 3.9, 3.12 e 3.13 |
