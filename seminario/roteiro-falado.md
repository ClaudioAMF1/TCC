# Roteiro falado — 15 minutos

O que dizer, slide a slide. Os trechos entre aspas são **texto para falar**, não
para ler no slide. `[COLCHETES]` marcam o que só você pode preencher, porque
depende de consultar a fonte.

**Orçamento de tempo.** Os 5 minutos da análise da estrutura são inegociáveis — é
o que mais rende nota. Se atrasar, corte do slide 6, não do 9–14.

---

## Slide 1 — Capa · sem tempo

Título do artigo, seu nome, Projeto Capstone I, IDP, 29/09/2026.

---

## Slide 2 — Contexto do TCC · 1 min

> "Meu TCC mede rastreamento por terceiros em aplicativos móveis do governo
> brasileiro. A pergunta é simples: quando um cidadão usa o Meu SUS Digital ou o
> Meu INSS, quais empresas além do governo recebem dados dele?
>
> Aplicativo nenhum é escrito do zero. O desenvolvedor usa bibliotecas prontas de
> terceiros — uma que conta quantas pessoas abriram o app, outra que reporta
> travamentos. Cada uma dessas peças é código de outra empresa rodando dentro do
> app do governo, e cada uma manda dados para o servidor dessa empresa.
>
> Duas coisas tornam isso diferente de um app comercial. A primeira é jurídica: o
> Artigo 11 da LGPD impõe regime mais estrito ao dado sensível, e 152 dos
> aplicativos do meu corpus tratam saúde, biometria ou previdência. A segunda é que
> não existe alternativa — você troca de banco, não troca de INSS."

**No slide:** a pergunta em uma linha, e os três números — 396 apps, 71
publicadores, 152 com dado do Art. 11.

---

## Slide 3 — Como cheguei aqui · 1 min

> "Cheguei nesse tema testando e descartando outros três, com dados.
>
> Primeiro tentei infraestrutura industrial exposta no Brasil. Descartei porque os
> mesmos endereços respondiam em Modbus, IEC‑104 e EtherNet/IP ao mesmo tempo — isso
> é honeypot e nuvem, não equipamento industrial. A variável que eu precisava
> observar, o setor do operador, não era observável.
>
> Depois tentei abuso de marca em Certificate Transparency. Li vinte mil entradas de
> log e não encontrei uma imitação real sequer. O phishing moderno raramente põe a
> marca no domínio, então o método tinha um teto de recall por construção.
>
> Depois tentei medir o parentesco entre famílias de malware bancário brasileiro. Aí
> o erro foi meu: o repositório rotula a campanha, não o payload, e 85% das amostras
> brasileiras eram containers, onde a métrica que eu estava usando nem existe.
>
> Os três descartes não são tempo perdido. São a seção de metodologia do meu TCC."

**No slide:** três linhas, uma por tema, com o número que derrubou cada um.

> Esse slide é o que te separa de uma apresentação comum. Não corra nele.

---

## Slide 4 — Passo a passo da seleção · 2 min

Este é o slide que a atividade pede explicitamente e que quase todo mundo esquece.
Os valores saem de `protocolo-de-busca.md`, preenchido **enquanto** você busca — é
impossível reconstruir depois.

> "A busca foi feita em `[BASES]`, em `[DATA]`. A string foi `[STRING]`.
>
> Apliquei estes filtros: `[FILTROS]`. Os critérios de inclusão foram: artigo
> original e não revisão, com medição empírica em escala, sobre rastreamento por
> terceiros em Android, publicado em veículo indexado.
>
> Isso devolveu `[N]` resultados. Li o título e o resumo de todos, passei `[M]` para
> leitura completa, e escolhi um."

**No slide:** funil visual — `[N]` encontrados → `[M]` lidos → 1 escolhido.

---

## Slide 5 — O artigo · 1 min

> "O artigo é `[CITAÇÃO COMPLETA — conferir no PDF, não copiar de terceiros]`,
> publicado na CCS de 2022.
>
> É um artigo **original**, não uma revisão: os autores construíram um corpus
> próprio, executaram uma medição e reportaram resultados primários. Isso importa
> porque a atividade pede análise de artigo original."

**No slide:** a citação em formato ABNT e o DOI.

> ⚠️ Confira autores, título e paginação no PDF baixado. Nunca copie referência de
> segunda mão — é o tipo de erro que a banca pega.

---

## Slide 6 — Relevância quantitativa · 1,5 min

> "Nas três bases, em `[DATA]`: `[X]` citações no Google Scholar, `[Y]` no Scopus,
> `[Z]` na ACM Digital Library. Os números diferem porque as bases indexam conjuntos
> distintos, e isso por si só é um dado sobre como o campo se mede.
>
> A escala do estudo é um critério quantitativo de relevância: `[N]` aplicativos
> analisados — duas ordens de grandeza acima das alternativas que considerei."

**No slide:** a planilha de métricas com a data de consulta visível.

> Se perguntarem por que não escolheu algo de 2025: recência e citações se excluem
> por construção. Um artigo de 2025 teve um ano para ser citado. E o item 2 avalia a
> classificação do **veículo**, que independe da idade do artigo.

---

## Slide 7 — Relevância qualitativa · 1,5 min

É aqui que o seu trabalho entra.

> "Três coisas ligam este artigo ao meu TCC.
>
> **O método eu reuso inteiro:** análise estática em escala, identificação de SDKs
> de terceiros, e confronto entre o que o app faz e o que ele declara. É exatamente
> o meu pipeline.
>
> **A lacuna é minha contribuição:** este artigo estuda aplicativos comerciais sob a
> GDPR. Nenhum trabalho dessa linha cobre o parque de aplicativos governamentais
> brasileiros, e nenhum adota grupo de controle pareado. Eu tenho os dois: 396 apps
> de 71 publicadores públicos, e controle comercial com 92,4% de suporte comum.
>
> **E eu já tenho um resultado preliminar que muda a pergunta.** Medindo os
> metadados dos 396 aplicativos, nenhum deles exibe anúncio. Nenhum, em 396. No meu
> grupo de controle comercial, 33%. Isso significa que se houver rastreador nos apps
> de governo — e a literatura sugere fortemente que há — ele não está lá para vender
> publicidade. Está lá por dependência técnica: analytics, relatório de travamento,
> infraestrutura. Isso descarta o enquadramento fácil de que o governo vende dados, e
> deixa uma questão mais difícil: dados de cidadão em serviço público essencial
> fluindo para infraestrutura estrangeira sem que ninguém tenha decidido isso."

**No slide:** os dois intervalos de confiança lado a lado — governo `[0,000; 0,010]`,
controle `[0,269; 0,401]` — e a frase "não se sobrepõem".

> Este é o momento mais forte da sua apresentação. Ensaie ele separado.

---

## Slide 8 — Métricas do veículo e Qualis · 2 min

> "A CCS é uma das quatro principais conferências de segurança do mundo. O índice h5
> é `[H5]`, consultado em `[DATA]`. No CORE, o rank é `[RANK]`.
>
> Pela tabela de faixas de percentil do Documento Técnico do Qualis — Figura 6 —,
> esse percentil corresponde ao estrato `[ESTRATO]`."

**No slide:** a figura `qualis-faixas-de-percentil.png` e a sua linha destacada.

> Leve o print de cada tela. A professora pode pedir.

---

## Slides 9 a 14 — Análise da estrutura · 5 min

O formulário está em `analise-da-estrutura.md`. Seis blocos, seguindo o exemplo que
a professora forneceu: estrutura, resumo, introdução, método, resultados, conclusão.

**A regra que muda a nota:** não é resumir o artigo. É reproduzir o texto real e
anotar ao lado a função retórica de cada trecho.

Dois comentários que rendem mais que descrição:

> "Repare que, com 239 mil aplicativos, este artigo precisa dedicar uma seção
> inteira a como o corpus foi montado e filtrado. No exemplo que a professora
> forneceu, o avaliador teve de **reconstruir** o método porque não havia seção
> explícita. Estudo de larga escala não pode se dar a esse luxo — a metodologia
> detalhada é uma consequência da escala, não uma escolha de estilo."

> "O funil amostral vai de `[N]` aplicativos a `[M]` com mecanismo de consentimento
> identificado. Cada corte desses é uma decisão que precisa ser justificada, e é
> exatamente o tipo de decisão que eu vou ter de tomar no meu corpus de 396."

---

## Slide 15 — Fechamento · 30 s

> "Este artigo me dá três coisas: o método validado, a lacuna que justifica o meu
> trabalho, e um padrão de escrita para a minha própria seção de metodologia.
>
> E me dá uma pergunta que eu não tinha antes: se o rastreamento no governo não é
> comercial, o que explica ele estar lá?"

---

## Antes do dia

| | |
|---|---|
| ☐ | Ler o artigo **inteiro**, não só o resumo |
| ☐ | Preencher `protocolo-de-busca.md` **durante** a busca |
| ☐ | Levantar as métricas com print e data de cada tela |
| ☐ | Preencher `analise-da-estrutura.md` com o texto real do artigo |
| ☐ | Ensaiar cronometrado, em voz alta, pelo menos duas vezes |
| ☐ | Conferir a citação completa no PDF |

**Pergunta provável da banca:** *"por que este artigo e não um mais recente?"* — a
resposta está no slide 6, e você deve tê-la na ponta da língua.

**Segunda pergunta provável:** *"o que você faria diferente do que eles fizeram?"* —
responda com o grupo de controle pareado e com o recorte governamental. São
exatamente as duas coisas que o artigo não tem.
