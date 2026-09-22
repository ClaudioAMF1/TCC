# Roteiro da apresentação

O que falar em cada slide da versão final (`apresentacao/seminario-analise-de-artigo.pptx`).

**Como usar**

- O texto é para **falar com as suas palavras**, não para decorar. Leia duas vezes e
  depois ensaie olhando só os slides.
- **Não leia os trechos em inglês.** Aponte para eles e diga o que significam.
- **Relógio:** é o tempo acumulado ao terminar o slide. Se no fim do slide 12 você
  estiver passando de 8 min, acelere nos slides 9, 10 e 14.
- **Total: 14 min 35 s.** Sobram 25 s de margem.

---

## Item 1 — Seleção do artigo

### Slide 1 · Capa · 20 s · relógio 0:20

> Bom dia. Eu sou o Claudio e vou apresentar a análise do artigo *Freely Given
> Consent?*, de Nguyen, Backes e Stock, publicado na ACM CCS de 2022. Vou seguir a
> ordem do enunciado: como selecionei o artigo, as métricas do veículo e a análise
> da estrutura.

### Slide 2 · Seleção no Scopus · 45 s · relógio 1:05

**Aponte** para cada imagem quando falar o número dela.

> Fiz a busca no Scopus, pelo portal da CAPES, entrando pela CAFe com o login do IDP,
> no dia 21 de setembro. Busquei a expressão exata "third-party tracking" em título,
> resumo e palavras-chave: **131** resultados. Filtrei por ano, de 2018 a 2026, área
> de Computação e tipo de documento: ficaram **70**. Com as palavras-chave Third
> Parties e Third-party Tracking, **39**. O último corte foi uma decisão de método:
> como o meu TCC é sobre consentimento, acrescentei o termo *consent* e fiquei com
> **5** finalistas. Li título e resumo dos cinco e escolhi **um**. Os finalistas estão
> no slide de apoio.

### Slide 3 · Originalidade e relevância · 35 s · relógio 1:40

> É um artigo original: os autores montaram um corpus próprio de **239 mil
> aplicativos** e construíram uma ferramenta de análise de tráfego. A própria ACM
> classifica o trabalho como *research article*.
>
> Relevância quantitativa: **42** citações na ACM, **52** no Scopus e **99** no Google
> Acadêmico. Os números diferem porque cada base cobre um conjunto diferente.
>
> Relevância qualitativa: o meu TCC estuda rastreamento por terceiros em aplicativos
> do governo brasileiro, e este artigo me dá o método: comparar o que a tela promete
> com o que o aplicativo realmente envia.

---

## Item 2 — Métricas do veículo

### Slide 4 · Métricas da ACM CCS · 40 s · relógio 2:20

**Aponte** para cada caixa, da esquerda para a direita.

> O artigo saiu numa conferência, então as métricas são as do ramo de conferência.
> O índice **h5** no Google Scholar é **90**: quinta posição em Computer Security and
> Cryptography, e terceira entre as conferências da lista. No **CORE**, a CCS é
> **A estrela**, a classificação máxima.
>
> E o **Qualis**: procurei a CCS no Qualis Periódicos, nos quadriênios 2017–2020 e
> 2021–2024, e ela não aparece, porque essa lista é só de revistas. A classificação
> da CAPES para conferências de Computação é o Qualis Eventos, e nele a CCS é **A1**.

---

## Item 3 — Análise da estrutura

### Slide 5 · Como o artigo se organiza · 35 s · relógio 2:55

> Agora a estrutura. O artigo tem oito seções. Resumo e introdução trazem contexto,
> lacuna e objetivo. A seção 2 define os critérios jurídicos. A 3 constrói o método, e
> a 4 aplica esse método em larga escala e traz os resultados. A 5, notificação dos
> desenvolvedores, existe porque responde a uma das perguntas de pesquisa. Depois vêm
> discussão, trabalhos relacionados e conclusão. Um detalhe: os trabalhos relacionados
> ficam depois da discussão, e não no começo.

### Slide 6 · Resumo, parte 1 · 40 s · relógio 3:35

> No resumo, marquei a função de cada trecho, como no exemplo da professora. Primeiro
> o **contexto**: o GDPR exige consentimento livre, específico, informado e inequívoco.
> Depois a **lacuna**: ninguém tinha estudado de forma sistemática como os avisos de
> consentimento são implementados. E o **objetivo**: fazer o primeiro estudo em larga
> escala desses avisos em aplicativos Android. Essa afirmação de ser o primeiro é dos
> próprios autores.

### Slide 7 · Resumo, parte 2 · 35 s · relógio 4:10

> Em seguida, o resumo apresenta o **método**, uma abordagem quase toda automatizada;
> o **resultado**, 2.688 aplicativos, 20,54% dos que têm aviso, com pelo menos uma
> violação; e a **implicação**, a necessidade de mais transparência e de apoio aos
> desenvolvedores. Um detalhe: aqui no resumo eles escrevem que os apps **violam**.
> Guardem isso, porque na conclusão a palavra muda.

### Slide 8 · Introdução: as perguntas de pesquisa · 45 s · relógio 4:55

> A introdução transforma o tema em três perguntas de pesquisa. **Primeira**: os
> aplicativos implementam avisos de consentimento, e como eles são? **Segunda**: esses
> avisos se sustentam juridicamente diante do GDPR? **Terceira**: os desenvolvedores
> conhecem os requisitos?
>
> Cada pergunta pede um método diferente. A primeira pede classificar telas. A segunda
> pede medir o tráfego. A terceira pede conversar com os desenvolvedores, e é isso que
> explica a existência da seção 5.

### Slide 9 · Figura 1, exemplos a, b e c · 35 s · relógio 5:30

> A figura 1, ainda na introdução, mostra exemplos reais. Estes três são avisos só de
> confirmação: o botão diz "OK" ou "Eu concordo", e não há ali opção de recusar. A
> figura serve para o leitor ver o problema antes do método. Mas a tela sozinha não
> prova que dados foram enviados. Para isso, o artigo precisa da análise de tráfego.

### Slide 10 · Figura 1, exemplos d, e e f · 30 s · relógio 6:00

> Os outros três exemplos oferecem alguma escolha. No **d**, a recusa vale só para
> anúncios personalizados. No **e**, há aceitar e recusar. No **f**, escolhas
> detalhadas por fornecedor. A pergunta que o artigo faz é se a escolha mostrada na
> tela é respeitada pelo aplicativo.

### Slide 11 · Fundamentação jurídica · 35 s · relógio 6:35

> A seção 2 é a fundamentação. Ela transforma a lei em quatro situações que dá para
> observar: não ter aviso, enviar dados antes do consentimento, não ter como recusar,
> e continuar enviando depois da recusa. E os autores deixam uma cautela explícita:
> só uma decisão judicial dá certeza jurídica. Por isso eles falam em **potencial**
> violação.

### Slide 12 · Método I: identificar os avisos · 55 s · relógio 7:30

**Aponte** para a Figura 2 e depois siga as caixas da esquerda para a direita.

> O método tem duas partes. A primeira identifica os avisos. Os autores partiram de
> 5,8 milhões de nomes de aplicativos no AndroZoo e filtraram: gratuitos, com pelo
> menos 10 mil downloads, com permissão sensível e atualizados depois de maio de 2018.
> Isso deu 250.972 aplicativos, e a captura funcionou em **239.381**.
>
> De cada um, tiraram um print da tela depois de 5 segundos, extraíram o texto com
> OCR, trataram esse texto e agruparam as telas parecidas em 44 grupos. Depois da
> inspeção manual, chegaram a **13.082 avisos de consentimento**. A coleta foi feita
> num país do Espaço Econômico Europeu, onde o GDPR vale.

### Slide 13 · Método II: o tráfego em três condições · 55 s · relógio 8:25

**Aponte** para as três colunas.

> A segunda parte mede o tráfego. Cada aplicativo roda em três condições separadas:
> **sem interagir**, **depois de aceitar** e **depois de recusar**. Entre uma condição e
> outra, o app é reinstalado, para o aviso aparecer de novo. Cada execução dura até
> 150 segundos.
>
> Eles interceptam o tráfego com o mitmproxy, contornam as proteções do app com o
> Objection e navegam automaticamente com o DroidBot. Depois procuram dados pessoais
> saindo para 45 domínios de empresas de publicidade. É a comparação entre as três
> condições que permite dizer se a escolha do usuário foi respeitada.

### Slide 14 · Resultados: os quatro mecanismos · 40 s · relógio 9:05

> Agora os resultados. Nos 13.082 avisos, os autores acharam quatro mecanismos. Quase
> **44%** só pedem confirmação. **30%** permitem recusar apenas os anúncios
> personalizados. **22%** dão aceitar ou recusar. E só **4%** oferecem escolhas
> detalhadas. O ponto importante: recusar anúncios personalizados não significa,
> necessariamente, parar o rastreamento.

### Slide 15 · Resultados: dois grupos · 40 s · relógio 9:45

> Os resultados se dividem em dois grupos, e cada um tem o seu denominador. Entre os
> 13.082 aplicativos **com aviso**, **2.688**, ou 20,54%, têm pelo menos uma potencial
> violação. E há **30.160** aplicativos que **nem mostram aviso** e enviam dados para
> empresas de publicidade. Eles são 93% dos 32.341 que enviaram dados para esses
> domínios.

### Slide 16 · Resultados: tipos de violação · 45 s · relógio 10:30

> Esta tabela detalha as potenciais violações entre os aplicativos com aviso.
> **2.181** enviaram dados antes de qualquer consentimento: 16,67% do total. **1.084**
> não oferecem forma de recusar, e todos são do tipo só confirmação. E **134**
> continuaram enviando dados depois que o usuário recusou.
>
> As categorias se sobrepõem: um mesmo app pode estar em mais de uma coluna. Por isso a
> soma não dá 2.688.

### Slide 17 · Resultados: para onde vão os dados · 30 s · relógio 11:00

> Nos aplicativos sem aviso, a figura mostra para onde os dados vão. O facebook.com
> recebeu dados de **14.420** apps, quase metade. E **29.952**, mais de 99%, enviaram o
> identificador de publicidade do Android, que permite reconhecer o mesmo usuário em
> aplicativos diferentes.

### Slide 18 · Seção 5: notificação dos desenvolvedores · 40 s · relógio 11:40

> A seção 5 responde à terceira pergunta. Os autores notificaram **1.127**
> desenvolvedores, responsáveis por **1.859** aplicativos, e **43** responderam. Nem
> todos responderam tudo, por isso as frações: 9 de 14 não sabiam que dados eram
> coletados, 9 de 13 disseram conhecer os requisitos, e 6 de 7 queriam uma ferramenta
> automática. Depois, 147 apps foram atualizados: 63 corrigiram o problema, e 84
> continuaram com potencial violação.

### Slide 19 · Seção 6: discussão · 35 s · relógio 12:15

> A seção 6 é a **discussão**. Ela interpreta os resultados em três frentes: o alcance
> das violações, a falta de transparência sobre quem recebe os dados, e o suporte aos
> desenvolvedores. A conclusão dos autores é que faltam documentação dos serviços de
> terceiros e ferramentas de verificação. E eles têm o cuidado de não atribuir uma
> causa única aos problemas.

### Slide 20 · Limites da evidência · 35 s · relógio 12:50

> O artigo não tem uma seção própria de limitações, então reuni as que aparecem ao
> longo do texto. Só aplicativos gratuitos. **11.591** apps não puderam ser
> analisados. **1.996** telas ficaram de fora por não estarem em inglês. E cada
> execução dura no máximo 150 segundos, olhando só 45 domínios. Então, se o
> experimento não viu uma falha, isso não prova que ela não existe.

### Slide 21 · Conclusão, parte 1 · 40 s · relógio 13:30

> A seção 8, a **conclusão**, retoma o objetivo e a escala: um estudo sistemático em
> 239.381 aplicativos. E recupera os dois números centrais: **30.160** apps sem aviso
> que enviaram dados, e **2.688** apps com aviso e pelo menos uma potencial violação.

### Slide 22 · Conclusão, parte 2 · 35 s · relógio 14:05

**Aponte** para as duas caixas de baixo, "violate" e "potentially violate".

> E fecha com a implicação: é urgente ter mais transparência no tratamento de dados e
> mais apoio aos desenvolvedores.
>
> Aqui está a observação que eu queria mostrar. No resumo, os autores escrevem que os
> apps **violam**. Na conclusão, escrevem que os apps **potencialmente violam**. A
> conclusão é mais cautelosa, coerente com a nota 1, sobre a decisão judicial.

### Slide 23 · Contribuições para o meu TCC · 30 s · relógio 14:35

> Para terminar, o que eu levo para o meu TCC. Do **método**: comparar o que o app
> mostra com o que ele realmente envia. Da **escrita**: informar perdas, limitações e
> denominadores, e separar indício técnico de conclusão jurídica. E o **recorte**, que
> é o que o artigo não tem: aplicativos do governo brasileiro, comparados com um grupo
> comercial. Obrigado.

---

## Slides de apoio

Não entram no tempo. Só abra se ela perguntar.

- **Slide 24, os cinco finalistas**: se perguntar por que este artigo e não outro.
- **Slide 25, as fontes**: se perguntar de onde vem algum número.

As respostas às perguntas prováveis estão em `plano-de-execucao.md`, seção 4.
