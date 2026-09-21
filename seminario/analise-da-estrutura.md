# Análise da estrutura — PREENCHIDA

**Artigo:** NGUYEN, Trung Tin; BACKES, Michael; STOCK, Ben. *Freely Given Consent?
Studying Consent Notice of Third-Party Tracking and Its Violations of GDPR in
Android Apps.* In: CCS '22 — Proceedings of the 2022 ACM SIGSAC Conference on
Computer and Communications Security. Los Angeles, 7–11 nov. 2022, p. 2369–2383.
DOI 10.1145/3548606.3560564. **15 páginas.**

Vale 5 dos 15 minutos e é o que mais rende nota. O enunciado pede: *"analise a
estrutura do trabalho (introdução, metodologia, resultados, discussão, conclusão,
etc.)"* e *"descreva e explique as principais características de cada elemento"*.

> ⚠️ **Confira contra o PDF antes de apresentar.** Tudo abaixo saiu do texto, mas eu
> já errei número quatro vezes nesta preparação. Abra o artigo e valide.

---

## Bloco 1 — Estrutura geral

| Seção | Páginas | Função |
|---|---|---|
| **1 Introduction** | 1–3 | Contextualiza, posiciona na literatura, declara as 3 questões de pesquisa e lista as contribuições |
| **2 Legal Background of GDPR Consent** | 3–4 | **Marco jurídico** — define os 4 tipos de violação que o trabalho vai medir |
| 2.1 Legal Background · 2.2 Legal Analysis (2.2.1 a 2.2.4) | | |
| **3 Methodology** | 4–6 | Procedimento: como identificar avisos de consentimento |
| 3.1 Collecting Privacy-Related UI · 3.2 Identifying Consent Notices (3.2.1 a 3.2.4) | | |
| **4 Large-Scale Analysis** | 6–11 | Aplicação do método em escala + resultados |
| 4.1 App Dataset Construction · 4.2 Identifying In The Wild · 4.3 Automating Violations · 4.4 Observed Violations (4.4.1 a 4.4.6) | | |
| **5 Developer Notification** | 11–12 | Notificação dos desenvolvedores e respostas obtidas |
| **6 Discussion** | 12–13 | Interpreta e generaliza |
| **7 Related Work** | 13 | Revisão da literatura |
| **8 Conclusion** | 13 | Retoma e fecha |

### As quatro observações estruturais que rendem mais que descrição

**1. A revisão de literatura é a Seção 7, depois da discussão.** A convenção mais
comum põe *Related Work* como Seção 2. Aqui o posicionamento na literatura é feito
**dentro da introdução** — é lá que eles dizem que Nguyen et al. [43] fez a primeira
medição em larga escala por análise de tráfego, mas que *"no study has
systematically analyzed the current practices of implemented consent notices"*. A
Seção 7 fica para o cotejo detalhado. **É escolha, não descuido**, e mostra que a
introdução carrega o peso de justificar a lacuna.

**2. Metodologia e aplicação são seções separadas.** A Seção 3 desenvolve o
*método*; a Seção 4 o *aplica em escala*. Trabalho que só usa ferramenta pronta não
precisa dessa divisão — quem constrói instrumento próprio, precisa.

**3. Juntas, as Seções 3 e 4 ocupam cerca de 7,5 das 15 páginas — metade do
artigo.** Compare com o exemplo que a professora forneceu, em que o avaliador teve
de **reconstruir** o método porque não havia seção explícita. Estudo de 239 mil
aplicativos não pode se dar a esse luxo: **a metodologia detalhada é consequência da
escala, não escolha de estilo.**

**4. Não existe seção de Limitações nem de Ética.** As limitações aparecem como
parágrafo solto na página 7, dentro da Seção 4, começando com *"Limitations. We
naturally suffer from certain limitations from OCR and dynamic analysis..."*. A
ética aparece em duas frases na página 11, dentro da 5.1: *"our institution's ethics
guidelines do not mandate approval for such a study"*.

> **Apontar isso é análise de estrutura, e é exatamente o movimento que o avaliador
> faz no segundo exemplo fornecido.** Em conferência de segurança isso é comum, mas
> a ausência de seção autônoma dificulta localizar a informação — e é uma decisão
> estrutural que eu **não** vou repetir na minha monografia, onde ética e ameaças à
> validade terão seções próprias.

---

## Bloco 2 — Resumo

| Trecho | Função |
|---|---|
| *"Adopted in May 2018, the European Union's GDPR requires the consent for processing users' personal data to be freely given, specific, informed, and unambiguous."* | **Contextualiza** — estabelece a norma |
| *"While prior work has shown that this often is not given through automated network traffic analysis, no research has systematically studied how consent notices are currently implemented and whether they conform to GDPR in mobile apps."* | **Declara a lacuna** — o que já se sabe e o que falta |
| *"To close this research gap, we perform the first large-scale study into consent notices for third-party tracking in Android apps..."* | **Objetivo** |
| *"...we propose a mostly automated and scalable approach to identify the currently implemented consent notices and apply it to a set of 239,381 Android apps."* | **Método empregado** |
| *"...we recognize four widely implemented mechanisms... from 13,082 apps... we find 30,160 apps do not even attempt to implement consent notices... out of 13,082 apps implemented consent notices, we identify 2,688 (20.54%) apps violate at least one of the GDPR consent requirements..."* | **Resultados** |
| *"Our study shows the urgent need for more transparent processing of personal data and supporting developers in this endeavor to comply with legislation..."* | **Implicação** |

**Palavras-chave:** Android Security; Consent; GDPR; User Privacy

**CCS Concepts:** General and reference → Measurement · Security and privacy →
Privacy protections; Usability in security and privacy

> **Comentário que rende:** o resumo segue exatamente a sequência
> contexto → lacuna → objetivo → método → resultado → implicação, e **cada elemento
> cabe em uma ou duas frases**. As palavras-chave mostram como os autores querem ser
> encontrados: *Consent* e *GDPR* aparecem, mas *tracking* e *third-party* não —
> mesmo estando no título. Vale comparar com os termos que eu usei na minha busca.

---

## Bloco 3 — Introdução

| Movimento | Conteúdo |
|---|---|
| **Contextualiza** | *"Every time we load a page on a commercial website or use a mobile app, information about us and about what we are doing online will be broadcast to large numbers of companies, most notably for advertising purposes."* Abre pelo fenômeno cotidiano, não pela técnica |
| **Problemática** | Órgãos reguladores responderam com legislação; o GDPR exige consentimento livre, específico, informado e inequívoco |
| **Posiciona na literatura** | Cita Nguyen et al. [43] como a primeira medição em larga escala por análise de tráfego, e delimita o que ainda não foi feito |
| **Questões de pesquisa** | Três, declaradas em lista |
| **Antecipa método e resultado** | Resume o que fizeram e o que encontraram |
| **Contribuições** | Lista com marcadores, ao final |

### As três questões de pesquisa, literais

> • *Do mobile apps implement any form of consent notices? What are the common
>   properties of such consent notices?*
> • *Can these implemented consent notices be legally justified under GDPR?*
> • *Are developers aware of the GDPR consent requirements and the violations of
>   their implementation?*

> **Isto é o que a Aula 05/06 chama de problema de pesquisa bem formulado.** São
> perguntas **respondíveis por medição**, não temas. E repare que a terceira exige um
> método completamente diferente das duas primeiras — é o que justifica a existência
> da Seção 5.

### A nota de rodapé 1 — o detalhe mais fino do artigo

> *"We note that we refer to the violations as **potential** because we carefully
> worded not to make legally conclusive statements since this could amount to legal
> consulting strictly regulated by our national law. Therefore, only a judicial
> ruling can provide legal certainty."*

**Eles medem violação e se recusam a chamar de violação.** Chamam de *potencial*, e
explicam por quê numa nota de rodapé. É precisão de linguagem com consequência
jurídica — e é exatamente o cuidado que eu vou precisar ter ao falar de LGPD, porque
eu também não posso emitir juízo legal.

---

## Bloco 4 — Método

| Etapa | Como o artigo descreve |
|---|---|
| **Fonte do corpus** | Lista de nomes de aplicativos do **AndroZoo** (5,8 milhões), com coleta na Play Store de país do EEE entre out/2021 e mar/2022 |
| **Critérios de inclusão** | Três, explícitos: (a) ao menos 10.000 downloads; (b) solicita permissão sensível, como localização ou contatos; (c) última atualização posterior a maio de 2018 |
| **Exclusão declarada** | Só aplicativos gratuitos — *"we cannot generalize our findings to paid apps"* |
| **Instrumento 1** | Processamento de imagem (OCR) e PLN para identificar avisos de consentimento nas telas |
| **Pipeline de PLN** | Pré-processamento de texto → bag-of-words → **clustering hierárquico aglomerativo** → verificação manual |
| **Instrumento 2** | Ferramenta própria que detecta dado pessoal enviado à internet sob diferentes condições de consentimento, por análise dinâmica de tráfego |
| **Ambiente controlado** | Testes executados **em país do EEE**, com a loja configurada para a variante local — porque o GDPR só se aplica lá |

### O funil amostral

```
5.800.000  nomes de aplicativos na lista do AndroZoo
     ↓     filtros: ≥10k downloads · permissão sensível · atualizado após maio/2018
  250.972  aplicativos obtidos
     ↓     análise dinâmica bem-sucedida em 95,38%
  239.381  aplicativos efetivamente analisados
     ↓
   13.082  com aviso de consentimento identificado
           (4 mecanismos de interação reconhecidos)
     ↓
    2.688  (20,54% de 13.082) violam ao menos um requisito do GDPR
           ├─ 2.181  (16,67%) enviaram dado ANTES do consentimento explícito
           ├─ 1.084  ( 8,28%) sem forma de recusar
           └─   134  enviaram dado DEPOIS do opt-out

   30.160  não tentam sequer implementar aviso de consentimento
   32.341  enviaram dado pessoal sem aviso de consentimento
    1.127  desenvolvedores notificados por e-mail
```

### Três observações sobre o funil

**1. O denominador muda no meio.** Os 20,54% são sobre os **13.082** que *têm*
mecanismo — não sobre os 239.381. Percentual sobre subconjunto precisa ser lido com
atenção.

**2. Os 30.160 são categoria separada.** Não violam o mecanismo: **não têm mecanismo
nenhum.** É outro tipo de problema, e o artigo o trata em separado.

**3. Eles reportam a taxa de sucesso da análise, não só o número final.** 239.381 de
250.972 é **95,38%**, e eles dizem isso. Reportar quanto do corpus a ferramenta
*não* conseguiu processar é honestidade metodológica que muita gente omite.

> **A conexão direta com o meu TCC:** o corpus deles nasce da lista do **AndroZoo**,
> que é a mesma fonte que eu vou usar. E cada corte do funil é uma decisão que
> precisou de justificativa — exatamente a decisão que eu vou tomar nos meus 396
> aplicativos governamentais.

---

## Bloco 5 — Resultados

| Resultado | Como foi validado |
|---|---|
| Quatro mecanismos de interação com avisos de consentimento, a partir de 13.082 apps | Clustering hierárquico mais **verificação manual** da classificação |
| 30.160 apps sem qualquer aviso, compartilhando dado com terceiros | Análise dinâmica de tráfego — *"This allows us to ensure the potential violations indeed took place"* |
| 2.688 (20,54%) violando ao menos um requisito, decompostos em 2.181 / 1.084 / 134 | Cada tipo de violação mapeado a um requisito jurídico definido na Seção 2 |
| Cerca de 99% das violações envolvem o **Android Advertising ID (AAID)** | Identificação do dado no tráfego capturado |

### As quatro verificações

- ☑ **Medida de incerteza?** **Não.** Só contagens e percentuais, sem intervalo de
  confiança. É censo do corpus, não amostra — mas os critérios de inclusão são
  restritivos, então generalizar para "apps Android" exigiria ressalva.
- ☑ **Tamanho de efeito?** Não se aplica: não há comparação entre grupos.
- ☑ **Grupo de controle?** **Não existe.** Não há população de comparação — e
  **essa é a lacuna que o meu trabalho preenche.**
- ☑ **Artefato disponível?** Sim. O artigo aponta para `github.com/cispa/gdpr-consent`
  (template do e-mail de notificação). *Confirmar o repositório completo.*

> **A validação decisiva é a combinação estática mais dinâmica.** Identificar o aviso
> na tela prova que ele existe; capturar o tráfego prova que o dado foi enviado assim
> mesmo. Um sozinho não sustenta a afirmação. **É o mesmo par que eu vou precisar:
> presença de SDK não é transmissão.**

---

## Bloco 6 — Discussão

**Existe seção autônoma** — Seção 6, páginas 12–13, com três subseções:

| Subseção | Função |
|---|---|
| **6.1 Widespread Violation of GDPR Consent** | Interpreta a escala do achado: não é caso isolado, é prática difundida |
| **6.2 Transparency of Processing Users' Data** | Implicação normativa: o problema não é só ilegalidade, é opacidade |
| **6.3 Lack of Support for Developers** | Desloca a causa — desenvolvedores não têm ferramenta nem orientação para cumprir a lei |

> **O movimento mais interessante do artigo está na 6.3.** Depois de medir 2.688
> violações, eles **não concluem que os desenvolvedores agem de má-fé**. A Seção 5
> coletou respostas de desenvolvedores notificados, e a discussão usa isso para
> reenquadrar o achado: falta suporte, não sobra intenção.
>
> **É exatamente o movimento que o meu próprio resultado preliminar pede.** Nenhum
> dos 396 aplicativos de governo exibe anúncio, contra 33,2% do controle comercial.
> Se houver rastreador ali, não é monetização — é dependência técnica. A mesma
> estrutura de argumento: medir o problema e resistir à explicação fácil.

---

## Bloco 7 — Conclusão

| Trecho | Função |
|---|---|
| *"we performed a systematic study into consent notices of third-party tracking in 239,381 Android apps in the wild"* | Retoma objetivo e escala |
| *"we first recognized four widely implemented mechanisms... We found 30,160 apps do not even attempt... we identified 2,688 (20.54%) apps potentially violate..."* | **Infere a partir dos dados obtidos** |
| *"We sent notification emails to inform affected developers and gather insights from their responses."* | Retoma a terceira questão de pesquisa |
| *"Our study showed the urgent need for more transparent processing of personal data and supporting developers..."* | Implicação normativa |

### O teste de coerência resumo × conclusão

Comparando os dois textos lado a lado, **a conclusão repete o resumo quase palavra
por palavra**, com uma diferença única e reveladora:

| Resumo | Conclusão |
|---|---|
| *"2,688 (20.54%) apps **violate** at least one..."* | *"2,688 (20.54%) apps **potentially violate** at least one..."* |

**O resumo diz "violam"; a conclusão diz "potencialmente violam".** Dada a nota de
rodapé 1 — em que eles explicam ter escolhido a palavra *potencial* justamente para
não emitir juízo jurídico —, a conclusão é a versão correta e o resumo escorrega.

> **Essa é a observação mais forte que eu tenho para fazer.** Comparar o que o resumo
> promete com o que a conclusão entrega é análise crítica de verdade, e aqui ela
> encontra uma inconsistência real num artigo de conferência A\*. Não desqualifica o
> trabalho — mostra que precisão de linguagem é difícil de sustentar em todas as
> partes de um texto, que é justamente o que a Aula 09/10 cobra.

---

## Fechamento

> "A estrutura deste artigo **sustenta** as conclusões que ele tira, porque separa o
> desenvolvimento do método da sua aplicação, define juridicamente cada violação
> antes de medi-la, e valida cada afirmação com dois instrumentos independentes: a
> tela e o tráfego.
>
> O que eu levo dele para o meu trabalho é o pareamento estático-dinâmico, a
> disciplina de reportar a taxa de sucesso da ferramenta, e o cuidado de linguagem ao
> falar de conformidade legal.
>
> O que eu faria diferente é dar seção própria a limitações e a ética, que aqui ficam
> diluídas no corpo do texto — e acrescentar o que falta aqui: **grupo de controle
> pareado** e **recorte governamental**."

**As duas coisas que este artigo não tem e o meu TCC terá** são a resposta para a
pergunta mais provável da banca. Tenha na ponta da língua.
