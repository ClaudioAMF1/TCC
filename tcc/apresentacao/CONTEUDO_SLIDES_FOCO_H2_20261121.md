# Conteúdo atualizado dos slides — orientação de 21/11/2026

Este arquivo registra a versão textual de **14 slides** com o foco sugerido pelo orientador. O roteiro de fala alinhado é `roteiro-simulacao.md`. A apresentação editável e o PDF revisados foram gerados nesta conversa; os arquivos binários `simulacao-defesa-rascunho.pptx` e `simulacao-defesa-rascunho.pdf` **precisam ser substituídos/reexportados** para que a pasta do repositório reflita a versão de 21/11. Não usar a versão binária anterior na simulação sem conferir.

## 1. Abertura
**Quem mais está dentro do aplicativo?**

Rastreamento por terceiros e soberania de dados em aplicativos móveis governamentais brasileiros. Projeto Capstone I, Ciência da Computação, IDP, 2026.

## 2. Motivação
Serviços essenciais são acessados por aplicativos públicos que podem incorporar SDKs de terceiros. Esses componentes podem processar dados do usuário; **a presença do código no APK, isoladamente, não prova transmissão de dados**.

## 3. O que a literatura demonstrou
- Binns et al. (2018): rastreadores identificados em grande escala (aprox. 959 mil apps), principalmente por evidência estática.
- Kollnig et al. (2021): comparação antes/depois do GDPR, sem atribuição causal automática.
- Samarasinghe et al. (2022): 1.166 apps governamentais de 71 países; 269 com transmissão de dados do dispositivo a terceiros conhecidos.

## 4. Lacuna e contribuições
- **Caso brasileiro:** federal, estadual e municipal, com atenção à sensibilidade dos serviços.
- **Transparência:** categorias de dados/finalidades declaradas versus componentes detectados e, na subamostra, fluxos observados.
- **Instrumento:** conferir concordância e limitações dos detectores.

## 5. Problema e objetivos
**Problema:** em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado em suas políticas de privacidade e na seção “Segurança dos dados” da Google Play?

**Objetivo:** medir a proporção de SDKs de rastreamento de terceiros e de envios de dados sem declaração compatível nos aplicativos móveis governamentais brasileiros, à luz da LGPD. O envio real só pode ser avaliado por análise dinâmica. Confirmar o corpus, identificar SDKs, documentar funções, examinar políticas/rótulos e verificar detectores.

## 6. Hipóteses e verificações
- **H1 — principal:** proporção de pares app–SDK com divergência material documentada. Limiar operacional de 10%, com IC95%; não é limiar legal.
- **H2 — secundária:** prevalência de SDKs em aplicativos do governo que tratam dados sensíveis versus demais.
- **Comparação comercial:** referência descritiva, sem hipótese numerada ou teste obrigatório.
- **Checagem do instrumento:** concordância entre detectores (\(\kappa\) de Fleiss), sem numeração como hipótese.

Andow et al. (2020) relataram até 42,4% de inconsistências em **outro método e outra unidade de análise**. A estimativa não é diretamente comparável à H1.

## 7. Método
1. Corpus de aplicativos oficiais via Google Play e catálogos.
2. Caracterização por esfera, tipo de serviço e sensibilidade.
3. Pacotes atuais da loja, com data, versão e SHA-256; AndroZoo para defasagem/reprodutibilidade.
4. Detecção estática de SDKs; verificação cruzada dos detectores.
5. Comparação com política de privacidade e seção Segurança dos dados.
6. Proporções e IC95%, análise dinâmica exploratória da subamostra e sensibilidade.

## 8. Corpus preliminar
- 396 candidatos governamentais, 376 preliminarmente oficiais;
- 85 federais, 199 estaduais, 92 municipais;
- 100 classificados preliminarmente com serviços que envolvem dados sensíveis;
- conferência de oficialidade e sensibilidade **pendente para a coleta principal**.

## 9. Anúncios declarados
- Governo: 0 de 376 declararam exibir anúncios na Google Play.
- Referência comercial inicial: 63 de 190, apenas como **contexto descritivo**.
- Não inferir presença/ausência de SDKs, de transmissão nem regularidade pela declaração de anúncios.

## 10. Piloto do instrumento
20 APKs. A (Exodus/código): 75%; B (Exodus/domínios no pacote): 95%; C (Disconnect/domínios no pacote): 80%.

κ de Fleiss 0,52; 0,69 após análise de sensibilidade interna. 88 de 123 detecções B foram questionadas como potenciais falsos positivos, **sem verdade de referência independente**.

## 11. Origem dos pacotes
Consulta histórica: 92 de 396 governamentais presentes no AndroZoo (23,2%). A versão atual da Google Play é a fonte principal planejada; o AndroZoo complementa a rastreabilidade, a comparação de versões e a reprodutibilidade onde houver arquivo correspondente.

## 12. Revisão bibliográfica
1.531 registros de busca → 1.249 após deduplicação → 357 F2. Dessas, 71 são propostas de inclusão; 8 propostas de exclusão; 278 ainda sem decisão. O autor conferiu 18 das 79 decisões, com leitura integral e avaliação de qualidade. **As notas QA1–QA8 individuais ainda não constam da planilha**. A conclusão dos 278 fica para fevereiro de 2027, conforme aval do orientador.

## 13. Limitações e cronograma
Limites: código ≠ tráfego; políticas podem indicar categorias e não SDKs; classificação preliminar; versão e fonte; ferramentas não inteiramente independentes. Próximos passos: revisão com orientador e simulação até 03/12; F2/corpus em fevereiro; coleta e exame documental entre março e abril; análises e redação até junho de 2027.

## 14. Encerramento
**Problema definido. Método viável. Resultados ainda preliminares.**

A presença e a função dos SDKs são compatíveis com o que os aplicativos do governo declaram ao cidadão?

## Notas de autoria e metodologia
Reescreva o roteiro oral com linguagem que corresponda ao que foi efetivamente executado. Não atribua à pesquisa resultados de análise dinâmica que ainda não existem; não diga que todos os artigos foram validados. Cite corretamente as fontes e siga as regras institucionais para atribuição de ferramentas e apoio à redação. O histórico de autoria do GitHub não foi modificado.
