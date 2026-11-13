# Roteiro da simulação de defesa

Versão de 13/11/2026. Confirmar a data da apresentação com a disciplina.

## Slide 1

Tempo sugerido: 30 s.
Meu projeto investiga quais SDKs de rastreamento aparecem em aplicativos oficiais do governo brasileiro e como essa presença se compara à de aplicativos comerciais de categoria e porte semelhantes. Neste semestre, a entrega é o projeto de pesquisa, com o método, a fundamentação e os testes de viabilidade. A coleta principal e os testes das hipóteses ficam para o Capstone II.
Fonte: tcc/latex/main.tex, Seções 1 e 3.

## Slide 2

Tempo sugerido: 50 s.
Aplicativos públicos concentram serviços como saúde e previdência. SDK é um kit ou biblioteca que outro fornecedor desenvolveu e que o aplicativo incorpora. Ele pode servir para análise de uso, notificações ou publicidade. A presença de um SDK não demonstra, sozinha, que dados foram enviados. A motivação está na dependência do cidadão em relação ao órgão responsável: podem existir canais alternativos, mas o prestador do benefício não é livremente substituível. O estudo mede componentes e confronta os achados com as declarações de privacidade.
Fontes: Binns et al. (2018), DOI 10.1145/3201064.3201089; Pohle e Thiel (2020), DOI 10.14763/2020.4.1532.

## Slide 3

Tempo sugerido: 65 s.
A literatura já mostra que rastreamento por terceiros é frequente em apps comerciais e se concentra em poucos fornecedores. Binns e colaboradores examinaram cerca de 959 mil aplicativos. Kollnig e colaboradores observaram persistência do rastreamento em comparações anteriores e posteriores ao GDPR, além de problemas de consentimento. Isso não permite atribuir causalidade à lei. O estudo mais próximo é o de Samarasinghe e colaboradores: 1.166 apps de governo de 71 países. Na análise dinâmica, 269 (23,1%) enviaram dados do dispositivo a rastreadores conhecidos. A Seção 5 usa 37,1% para ocorrências de SDKs atribuídas ao Google, por isso esse percentual não será apresentado como proporção de apps. O referencial também incorpora PoliCheck, para relacionar destinatários e declarações, e avaliações de detectores.
Fontes: Binns et al. (2018), DOI 10.1145/3201064.3201089; Kollnig et al. (2021a), DOI 10.14763/2021.4.1611; Kollnig et al. (2021b), https://www.usenix.org/conference/soups2021/presentation/kollnig; Samarasinghe et al. (2022), DOI 10.1145/3485447.3512223; Andow et al. (2020), https://www.usenix.org/conference/usenixsecurity20/presentation/andow.

## Slide 4

Tempo sugerido: 50 s.
A contribuição proposta combina o recorte brasileiro, controles comerciais pareados por categoria e faixa de instalações e a comparação de detectores sobre as mesmas versões dos APKs. O estudo internacional já usou análise estática e dinâmica, com MobSF, LiteRadar e verificação de Firebase. Portanto, a contribuição não é simplesmente usar mais de uma ferramenta. É medir concordância com unidades harmonizadas e registrar a evidência das divergências. A ausência de um estudo equivalente ainda precisa ser confirmada ou corrigida pela leitura completa e pela bola de neve.
Fontes: Samarasinghe et al. (2022), https://users.encs.concordia.ca/~mmannan/publications/govt-privacy-WWW2022.pdf; Zhan et al. (2022), DOI 10.1109/TSE.2021.3115506.

## Slide 5

Tempo sugerido: 55 s.
A pergunta é se os aplicativos oficiais brasileiros embarcam SDKs de rastreamento e em que medida isso difere de aplicativos comerciais comparáveis. Os objetivos desdobram essa pergunta: validar quem publica, medir a presença dos SDKs, confrontar com políticas e rótulos de privacidade, observar destinos em uma subamostra e medir a concordância entre detectores. País do servidor, país do fornecedor e localização de tratamento não são equivalentes. A análise dinâmica ajuda a observar destinos, mas caracterizar transferência internacional também exige identificar agentes e operação.
Fontes: projeto, Seção 1.2; LGPD, Arts. 5º, 7º, 11 e 33; Resolução CD/ANPD nº 19/2024, Arts. 3º a 6º e 9º.

## Slide 6

Tempo sugerido: 80 s.
H1 testa igualdade da prevalência entre governo e controle. Não rejeitar essa hipótese não prova equivalência. H2 usa pares aplicativo–SDK com detecção confirmada e política recuperada; documentos indisponíveis ficam fora do numerador de ausência de declaração e são informados separadamente. H3 compara a prevalência entre apps governamentais classificados como sensíveis e não sensíveis, com ajustes que os dados permitirem. H4 operacionaliza concordância baixa como κ abaixo de 0,6. Os limiares são escolhas do protocolo, ainda sujeitos à orientação antes da análise principal. O piloto não é um teste confirmatório dessas hipóteses.
Fontes: projeto, Seções 1.4 e 3.12; Cohen (1960), DOI 10.1177/001316446002000104; Fleiss (1971), DOI 10.1037/h0031619; Zou (2004), DOI 10.1093/aje/kwh090.

## Slide 7

Tempo sugerido: 75 s.
O desenho é quantitativo, observacional e comparativo. O corpus parte da Google Play e o controle busca categoria e porte semelhantes. Cada pacote terá origem, versão e hash registrados. No piloto, A usa assinaturas de código do Exodus; B aplica assinaturas de domínio do Exodus a textos do APK; C aplica a lista Disconnect aos mesmos textos. B e C não representam captura de tráfego. A e B compartilham a base, e B e C compartilham extração. Depois vêm o confronto documental e a análise dinâmica. O plano principal será congelado após os ajustes do piloto, com data e versão.
Fontes: scripts e Seções 3.2–3.8 do projeto; https://reports.exodus-privacy.eu.org/en/trackers/; https://github.com/disconnectme/disconnect-tracking-protection.

## Slide 8

Tempo sugerido: 55 s.
Foram encontrados 396 candidatos. A classificação registrada manteve 376 como oficiais e excluiu 20 com publicador privado ou pessoa física. Ela identifica 100 apps que tratam saúde ou biometria do usuário. Esses números ainda dependem da minha validação pessoal, cujo escopo será combinado com o orientador. A regra inicial por palavras-chave e a classificação registrada divergem em 108 dos 376 casos de sensibilidade. Isso não é, por si, uma taxa de erro validada por referência independente. O controle começou com 190 apps e foi ampliado para 252.
Fontes: dados/classificacao_396_para_conferir.xlsx; projeto, Seções 3.3, 3.5 e 3.8.

## Slide 9

Tempo sugerido: 45 s.
Nenhum dos 376 apps mantidos na classificação declara anúncios na Google Play. No controle original, são 63 de 190, ou 33,2%. Os intervalos são de Wilson. É uma descrição dos metadados coletados e dos respectivos denominadores históricos. Anúncios declarados não medem rastreamento: um aplicativo sem anúncios pode incorporar analytics ou outro SDK. A prevalência de rastreadores no corpus completo ainda será medida nos APKs.
Fontes: projeto, Seção 3.8; Wilson (1927), DOI 10.1080/01621459.1927.10502953.

## Slide 10

Tempo sugerido: 60 s.
O piloto teve 20 APKs. A encontrou ao menos uma detecção em 15, B em 19 e C em 16. A concordância de Fleiss foi 0,52. A adjudicação das 223 detecções classificou 88 das 123 detecções de B como falsas, cerca de 72%, porque referências genéricas a domínios podem ser confundidas com um SDK. Depois dessa adjudicação, κ foi 0,69. Essa revisão usa a evidência dos próprios detectores, não uma verdade de referência independente, e a amostra não permite generalizar as taxas para o corpus. A escolha de A como medida principal ainda será discutida com o orientador.
Fontes: scripts/piloto_androzoo.py e registros do piloto; projeto, Seções 3.7 e 3.8.

## Slide 11

Tempo sugerido: 45 s.
Esta consulta foi feita antes da redução do corpus e da ampliação do controle: 92 de 396 candidatos governamentais estavam no AndroZoo, contra 160 de 190 controles. Não devemos misturar esses denominadores com os 376 e 252 atuais. Mesmo controlando a faixa de instalações, a cobertura histórica difere entre os grupos. A próxima tarefa é testar a obtenção direta de cinco apps. O hash identifica a versão, mas não garante que outra pessoa conseguirá baixá-la no futuro. Pacotes não serão redistribuídos.
Fontes: projeto, Seções 3.6 e 3.8; Allix et al. (2016), DOI 10.1145/2901739.2903508.

## Slide 12

Tempo sugerido: 55 s.
As 17 buscas de 6 de novembro recuperaram 1.531 registros. A deduplicação removeu 282, deixando 1.249. A F1 registra 886 exclusões, seis revisões reservadas para bola de neve e 357 candidatos à leitura completa, sendo 214 inclui e 143 talvez. A rodada de 13 de novembro registrou 71 propostas de inclusão e oito de exclusão, ainda sujeitas à minha validação pessoal. Restam 278 decisões em aberto, incluindo os 143 talvez que aguardam definição do orientador. Portanto, não há um número final de estudos incluídos. A amostra cega do reteste tem 125 registros e já está pronta para preenchimento, pelo menos sete dias após minha primeira avaliação pessoal. A conferência de 20 registros pelo orientador é opcional.
Fontes: dados/revisao/triagem_20261106.csv; dados/revisao/leitura_F2_para_preencher.xlsx; protocolo, Seções 7 e 12; Kitchenham e Charters (2007); Page et al. (2021), DOI 10.1136/bmj.n71.

## Slide 13

Tempo sugerido: 75 s.
As limitações principais são a diferença entre código e execução, o recorte Android/Google Play, a seleção do controle e as dependências entre detectores. Ainda preciso validar as classificações, fazer o reteste e ampliar o referencial com as decisões da F2. A matriz com dez critérios da LGPD e o planejamento de recursos estão preparados para revisão com o orientador. O uso de recursos próprios é uma premissa a confirmar; não há compra aprovada. Antes da coleta principal, serão definidos detector, regras de correspondência das políticas e plano estatístico. Também preciso confirmar a data da simulação, ensaiar em até 15 minutos e completar os dados da banca. A entrega do documento está prevista para 3 de dezembro.
Fontes: projeto, Seções 3.10–3.17; tcc/metodologia/criterios-lgpd.md; Plano de Ensino do Projeto Capstone I.

## Slide 14

Tempo sugerido: 10 s.
Encerro com a pergunta central: quanto o resultado depende da população de aplicativos e quanto depende do instrumento usado para medir? Obrigado.
Tempo total planejado: aproximadamente 14 minutos e 10 segundos. O ensaio com cronômetro definirá os ajustes finais.
