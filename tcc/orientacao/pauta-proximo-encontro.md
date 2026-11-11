# Roteiro do encontro de orientação (novembro de 2026)

Data: ____/11/2026        Ficha de orientação nº ____ (levar para assinar)

Tempo sugerido: 30 minutos.

| Parte | Tempo |
|---|---|
| 1. O trabalho em um minuto | 1 min |
| 2. O que foi feito | 7 min |
| 3. Resultados até agora | 5 min |
| 4. Perguntas | 15 min |
| 5. Avisos rápidos e próximos passos | 2 min |

Levar aberto: o texto no Overleaf (36 páginas), com a Seção 2.14 à mão.

---

## 1. O trabalho em um minuto

> "A pergunta é se os aplicativos do governo brasileiro na Google Play trazem
> SDKs de rastreamento de empresas terceiras e se fazem isso mais ou menos que
> aplicativos comerciais da mesma categoria e do mesmo porte. São quatro
> hipóteses:
>
> - **H1:** o governo rastreia tanto quanto o mercado;
> - **H2:** parte dos SDKs não aparece na política de privacidade;
> - **H3:** os aplicativos com dado de saúde ou biometria não rastreiam menos;
> - **H4:** a taxa medida depende da ferramenta de detecção.
>
> Neste semestre, o objetivo é mostrar que dá para medir tudo isso e montar os
> dados. A coleta completa e a análise ficam para o Capstone II."

---

## 2. O que foi feito, como e com quê

| Etapa | O que foi feito | Como, e com que ferramentas | Resultado |
|---|---|---|---|
| Escolha do tema | Quatro temas testados com dados antes de escolher | Shodan, Certificate Transparency, *imphash* de malware e Google Play | Três descartados porque a variável principal não era observável |
| Corpus do governo | Busca de aplicativos de órgãos públicos | Python com a biblioteca `google-play-scraper`; 21 termos de busca e depois o catálogo de cada publicador | 396 candidatos de 71 publicadores (set/2026) |
| Grupo de controle | Aplicativos comerciais da mesma categoria e faixa de instalações | Mesmo coletor, por categoria e faixa | 190, depois ampliado para 252 (04/11) |
| Viabilidade | Cada hipótese conferida antes de baixar qualquer pacote | Critérios escritos antes; intervalo de Wilson; cálculo de poder estatístico | As quatro hipóteses têm instrumento |
| Fonte dos pacotes (APKs) | Pedido de acesso ao AndroZoo, acervo acadêmico de APKs | Acesso concedido em 17/09; download pelo hash SHA-256, que garante a mesma versão | Só 23% dos aplicativos do governo estão no acervo, contra 84% do controle; o resto será baixado da loja com o `apkeep`, ferramenta da EFF |
| Detectores | Leitura do código das ferramentas previstas | MobSF 4.5.3, Exodus Privacy e Androguard | O MobSF usa a mesma base do Exodus, então não é independente. Três detectores novos: **A** (Exodus, código), **B** (Exodus, domínios), **C** (lista Disconnect, domínios) |
| Piloto | 20 APKs passados pelos três detectores | Script `piloto_androzoo.py` (Python e Androguard); conferência das 223 detecções pela evidência | κ de Fleiss de 0,52, que sobe para 0,69 depois da conferência; 72% das detecções do B eram falsas |
| Classificação do corpus | Para cada aplicativo: quem publica, esfera e dado sensível | Nome jurídico em "Sobre o desenvolvedor" na Google Play; amostra de 32 em 04/11; os 396 em 10/11, com apoio de IA (pergunta 1) | 376 oficiais; 100 com dado de saúde ou biometria |
| Revisão sistemática | Protocolo, buscas e triagem | Kitchenham e Charters (2007); PRISMA 2020; Scopus via CAPES, IEEE Xplore, BDTD e SBC OpenLib; 11 estudos de controle para validar as buscas; triagem com apoio de IA (pergunta 1) | 1.531 registros, 1.249 sem repetição, 357 para leitura completa |
| Texto e reprodutibilidade | Redação no modelo ABNT | LaTeX (abnTeX2) no Overleaf; scripts e dados num repositório Git; texto e scripts feitos com apoio de IA (pergunta 1) | 36 páginas |

---

## 3. Resultados até agora

1. **Nenhum aplicativo do governo declara anúncios** (0 de 376), contra 33%
   do controle. A declaração é feita pelo próprio publicador e trata só de
   anúncios: ela não mostra quais SDKs existem nem para onde os dados vão.
   Isso depende da detecção nos APKs e da análise dinâmica, que ainda não foram
   feitas no corpus completo.
2. **A ferramenta muda o resultado.** No piloto, a mesma amostra deu de 75% a
   95% de aplicativos com rastreador, conforme o detector. Isso já indica que a
   H4 tem fundamento.
3. **O AndroZoo quase não tem aplicativos do governo**: 23%, contra 84% do
   controle. Mesmo comparando aplicativos do mesmo porte, a chance de um
   aplicativo do governo estar no acervo é bem menor: a razão de chances é
   0,13. Por isso a maior parte terá de ser baixada da loja.
4. **A classificação automática não basta.** Ela errava o dado sensível em 29%
   dos aplicativos e deixava passar empresas privadas com nome de prefeitura.
5. **A literatura já mediu apps de governo de outros países** (Samarasinghe et
   al., 2022: 71 países, Google em 37%), mas sem o Brasil por esfera, sem
   comparação com o mercado e com uma só ferramenta. A lacuna foi reescrita
   com esses três pontos.

---

## 4. Perguntas

A primeira é a mais importante. Nas outras, levo uma proposta, e ele só
precisa concordar ou corrigir.

### Pergunta 1. O que o senhor aceita no uso de IA que fiz, e como registro?

Contar o que aconteceu, sem diminuir nem aumentar:

> "Usei dois assistentes de IA, e está declarado na Seção 2.14.
>
> - **Claude:** redigiu e revisou o texto e o protocolo, escreveu os scripts
>   e fez a classificação inicial dos 1.249 artigos da triagem e dos 396
>   aplicativos, como sugestão numa coluna separada.
> - **ChatGPT:** participou da conferência dessas classificações e alterou
>   parte delas, revisou trechos do texto e fez um teste às cegas numa amostra,
>   que não entra nos resultados.
>
> Ainda não validei as classificações registro a registro."

Perguntas:

- **O que desse uso o senhor considera aceitável, e o que não?**
- **Como devo registrar no texto? A Seção 2.14 basta?**
- **Quais etapas precisam de conferência pessoal minha?** Por exemplo:
  - validar todas as classificações ou uma amostra;
  - reescrever o texto com as minhas palavras;
  - refazer alguma etapa.

Resposta: ______________________________________________

### Pergunta 2. Qual deve ser o eixo da discussão: LGPD ou soberania de dados?

> "A justificativa tem dois eixos: a LGPD, nos Arts. 11 (dado sensível) e 33
> (transferência internacional), e a soberania de dados, pela dependência de
> empresas estrangeiras. Por enquanto, não tenho evidência de transferência
> para o exterior: isso depende da detecção nos APKs e da análise dinâmica.
> **O senhor acha que o eixo deve ser um dos dois, ou os dois com o mesmo
> peso?**"

Minha proposta: medir como está no plano e discutir pelos dois. A LGPD dá os
critérios verificáveis; a soberania entra na medida em que a análise dinâmica
mostrar para onde os dados vão.

Resposta: ______________________________________________

### Pergunta 3. Quanto da revisão precisa estar no texto de 03/12?

> "O regulamento (Art. 25, §3º) diz que o projeto deve contemplar toda a
> fundamentação e a revisão bibliográfica, e o texto ainda não tem uma seção
> de revisão bibliográfica. A triagem deixou 357 artigos para a leitura
> completa, umas 30 horas. Minha proposta é ler até 23/11 os 214 que já
> pareciam incluídos, começando pelos 51 sobre aplicativos de governo, LGPD e
> Brasil, e escrever com eles essa seção. Os 143 marcados como 'talvez' e a
> bola de neve viriam depois, registrados no protocolo. **Isso atende ao
> Art. 25, §3º, do jeito que o senhor entende?**"

Resposta: ______________________________________________

### Pergunta 4. A escolha do detector principal é defensável?

> "Proponho usar o detector A (assinatura de código do Exodus) como medida
> principal, porque no piloto todas as detecções dele se confirmaram. O C
> (Disconnect, de outra organização) entraria como verificação independente, e
> o B só para medir o efeito do método, porque 72% das detecções dele estavam
> erradas. **Essa divisão é defensável diante da banca, ou o senhor prefere
> tratar os três como iguais?**"

Resposta: ______________________________________________

### Pergunta 5. Há alguma restrição para baixar os APKs direto da Google Play?

> "Cerca de três quartos dos aplicativos do governo não estão no AndroZoo e
> terão de ser baixados da loja com o `apkeep`, usando uma conta Google criada
> só para a pesquisa. Os pacotes não são redistribuídos; só os hashes são
> publicados. **Vê algum problema ético ou de termos de uso que eu deva tratar
> no texto, ou que precise de aval do IDP?**"

Resposta: ______________________________________________

### Pergunta 6. A lacuna, como ficou, aguenta a banca?

> "Depois do estudo de Samarasinghe et al. (2022), a originalidade ficou em
> três pontos: o Brasil, com esfera e dado sensível; a comparação com
> aplicativos comerciais pareados; e a concordância entre ferramentas. **O
> senhor vê risco de a banca achar o trabalho repetido?**"

Resposta: ______________________________________________

### Pergunta 7, se der tempo. A análise dinâmica fica no Capstone II?

> "O objetivo 4 prevê, numa subamostra, ver para quais servidores e países os
> dados realmente vão, com celular e conta próprios. É a única parte que mede
> a transferência para o exterior, mas é a mais trabalhosa. **Mantemos no
> Capstone II ou deixamos como trabalho futuro?**"

Resposta: ______________________________________________

---

## 5. Avisos rápidos (só informar; ele corrige se discordar)

- **ACM Digital Library fora das buscas:** a exportação é paga e o IDP não dá
  acesso. Os 6 estudos de controle da ACM foram achados no Scopus.
- **20 aplicativos saíram do corpus:**
  - 13 de empresas privadas que publicam com nome de prefeitura;
  - 7 da área de agricultura de São Paulo publicados numa conta registrada em
    nome de pessoa física.

  O critério é quem publica.
- **Opcional:** se ele tiver 15 minutos, agora ou por e-mail, pode decidir 20
  artigos sorteados da triagem (`dados/revisao/conferencia_orientador_20261110.xlsx`).
  Isso mede se outra pessoa chegaria às mesmas decisões.

### Próximos passos

| O quê | Quando |
|---|---|
| Validação pessoal das classificações (escopo conforme a pergunta 1) | até 23/11 |
| Teste da coleta direta da Google Play em cinco aplicativos | até 16/11 |
| Reteste da triagem (refazer 10% sem ver as decisões) | 16/11 |
| Leitura completa (começando pelos 51 centrais) e seção de revisão bibliográfica, conforme a pergunta 3 | até 23/11 |
| Critérios da LGPD (Arts. 7º, 11 e 33) e congelamento do protocolo | 17/11 a 23/11 |
| Slides da simulação de defesa | até 24/11 |
| Entrega da redação | 03/12 |

---

## Anotações do encontro

&nbsp;

&nbsp;

&nbsp;
