# Roteiro do encontro de orientação

Versão de 13/11/2026. Tempo sugerido: 30 minutos.

Data: ____/____/2026. Ficha de orientação nº ____. Levar para assinatura.

Levar o projeto em `tcc/latex/main.pdf`, os slides, a matriz de critérios da LGPD e as planilhas de F1, F2 e reteste.

## 1. Apresentação do trabalho

A pesquisa mede a presença de SDKs de rastreamento em aplicativos Android do governo brasileiro e propõe compará-la com a de aplicativos comerciais de categoria e porte semelhantes. A LGPD e a soberania de dados orientam a interpretação. O projeto inclui comparação entre detectores, confronto com políticas de privacidade e análise dinâmica de uma subamostra.

No Capstone I, a entrega é o projeto com fundamentação, procedimentos, recursos e cronograma. A coleta principal e os testes das hipóteses continuam previstos para o Capstone II.

## 2. O que já existe

| Etapa | Evidência ou método | Estado em 13/11 |
|---|---|---|
| Corpus | Google Play, `google-play-scraper`, buscas e catálogo de publicadores | 396 candidatos; a classificação registrada mantém 376. Validação pessoal pendente |
| Controle | Categoria e faixa de instalações | 190 inicialmente, ampliados para 252 |
| Classificação sensível | Nome jurídico e funcionalidade descrita | 100 de 376 marcados como saúde ou biometria; conferir pessoalmente |
| Fonte dos APKs | Consulta histórica ao AndroZoo | 92/396 candidatos governamentais e 160/190 controles. Teste de coleta direta pendente |
| Piloto | 20 APKs, assinaturas de código e domínios no pacote | Taxas de detecção de 75%, 95% e 80%; κ original 0,52 e após adjudicação 0,69 |
| Revisão sistemática | 17 buscas em Scopus, IEEE Xplore, BDTD e SOL | 1.531 registros; 1.249 sem duplicatas; 357 candidatos à F2 |
| Leitura completa | Planilha F2 | 79 propostas: 71 I e 8 E, pendentes de validação pessoal. 278 decisões em aberto; ainda não há total final |
| Reteste | Sorteio cego, semente 20261116 | Planilha com 125 registros pronta, ainda sem respostas ou κ |
| Recursos e LGPD | Seções 3.13 e 3.14 e matriz complementar | Propostas escritas para validação na orientação |
| Documento e apresentação | Modelo do IDP | Texto e 14 slides revistos; completar informações da banca e ensaiar |

## 3. Resultados que podem ser apresentados

A declaração de anúncios foi zero entre os 376 aplicativos mantidos e 63/190 (33,2%) no controle original. Isso descreve anúncios declarados, não a presença de SDKs nem o envio de dados.

No piloto, a detecção variou conforme a técnica. A adjudicação classificou 88 das 123 detecções de B como falsas (71,5%). Essa revisão usa a evidência dos próprios detectores, não uma verdade de referência independente. B e C analisam domínios em textos do APK; não houve captura de tráfego no piloto.

A consulta histórica ao AndroZoo encontrou cobertura menor entre candidatos governamentais. É preciso testar a fonte complementar antes de prometer cobertura completa ou atualizar esses percentuais para o corpus revisto.

Samarasinghe et al. (2022) já estudaram 1.166 apps de governo de 71 países com análise estática e dinâmica. A contribuição proposta deve ser defendida pelo recorte brasileiro, pela comparação pareada e pela avaliação explícita da concordância, sem alegar que o estudo anterior usou uma única ferramenta.

## 4. Decisões para o encontro

### 4.1 Escopo da validação pessoal

Proposta: conferir as classificações de artigos e aplicativos, registrar alterações e preservar uma primeira versão pessoal datada. O reteste só ocorrerá pelo menos sete dias depois dessa avaliação. Definir se será necessária validação integral ou algum procedimento amostral justificado.

Decisão e justificativa: ___________________________________________________

### 4.2 Volume e suficiência da revisão bibliográfica

O Art. 25, §3º exige a fundamentação e a revisão bibliográfica no projeto. O texto já tem uma síntese de estudos e conceitos, mas a seleção sistemática em texto completo está pendente. Proposta: começar pelos 214 candidatos I, sem tratar essa prioridade como inclusão final nem excluir automaticamente os 143 T. Confirmar o que precisa estar concluído para 03/12 e como registrar o que permanecer pendente.

Decisão e justificativa: ___________________________________________________

### 4.3 Detector principal e evidência de validade

Proposta: A como medida principal, C como comparação com outra base e B como avaliação do efeito do método. A e B compartilham o Exodus; B e C compartilham extração. Discutir uma conferência de evidências que reduza a dependência da adjudicação em relação ao próprio detector. O resultado do piloto não prova precisão de 100% de A.

Decisão e justificativa: ___________________________________________________

### 4.4 Hipóteses e plano de análise

H1 e H3 usam prevalência de apps com ao menos um SDK, com razões de prevalências e variância robusta. Contagens serão secundárias. H2 usa pares app–SDK e distingue política indisponível, menção nominal e declaração genérica. H4 usa κ com intervalo, com τ complementar. Confirmar limiares, ajustes, dependência entre observações e multiplicidade antes de congelar o plano. Não rejeitar H1 não prova igualdade.

Decisão e justificativa: ___________________________________________________

### 4.5 Critérios da LGPD e eixo da discussão

A matriz tem dez critérios e separa componente, fluxo observado e documentação. Proposta: discutir a LGPD a partir das evidências e a soberania a partir das dependências técnicas e da governança. Nacionalidade do fornecedor ou país inferido de um IP não provam transferência internacional. Confirmar o tratamento das bases legais dos Arts. 7º e 11 e dos mecanismos do Art. 33.

Decisão e justificativa: ___________________________________________________

### 4.6 Recursos, coleta direta e análise dinâmica

Confirmar computador, armazenamento, dispositivo Android e conta de pesquisa disponíveis. A reserva inicial de 100 GB é uma estimativa de planejamento, sujeita ao teste de cinco apps; não é compra aprovada. Verificar acesso institucional às fontes e condições de obtenção dos APKs. Manter análise dinâmica no Capstone II, com cenários e limites documentados.

Decisão e justificativa: ___________________________________________________

### 4.7 Questões administrativas

Confirmar data da simulação (24/11, 26/11 ou 01/12), titulação do orientador, terceiro membro e IDs Lattes/ORCID. Confirmar a aplicação da regra de idioma ao projeto e a documentação necessária para português. Conferir termo de aceite e cinco encontros, com fichas assinadas e entregues nos prazos.

Decisão e justificativa: ___________________________________________________

## 5. Pedidos e próximos passos

Se houver disponibilidade, solicitar a classificação cega dos 20 artigos em `dados/revisao/conferencia_orientador_20261110.xlsx`. É uma conferência prevista no protocolo, não uma exigência expressa da disciplina. Registrar se o orientador aceitar e a data combinada.

| Atividade pendente | Prazo proposto |
|---|---|
| Validação pessoal e definição do plano | Combinar neste encontro |
| Reteste dos 125 artigos | 16/11 ou depois, respeitando sete dias da primeira avaliação pessoal |
| Teste da coleta direta em cinco apps | Até 16/11, sujeito a acesso e condições de uso |
| Leitura completa e ampliação do referencial | Até 23/11, com continuidade até 02/12 conforme escopo definido |
| Validação dos recursos e critérios; congelamento do protocolo | Até 23/11 |
| Revisão e ensaio de 15 minutos | Antes da data confirmada da simulação |
| Incorporação das sugestões e entrega no Canvas | Até 03/12 |

Esses prazos são propostas; registrar a data efetiva e o que ficou pendente. Não preencher resultados de etapas ainda não realizadas.

## Anotações e compromissos

Responsável, decisão, prazo e evidência de conclusão:

________________________________________________________________________

________________________________________________________________________
