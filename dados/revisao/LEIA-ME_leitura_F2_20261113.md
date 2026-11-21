# Leitura F2: rodada de 13/11/2026

> **Atualização de 21/11/2026:** após examinar e concordar com os 18 pareceres da auditoria documental, o autor confirmou essas 18 decisões (12 I, 6 E; cinco com ressalvas). O registro atualizado está em `dados/revisao/leitura_F2_registro_20261121_validacao_parcial.csv`. Os 339 restantes seguem pendentes. **Complemento informado pelo autor em 21/11:** a leitura integral e a avaliação QA1–QA8 também foram concluídas para esses 18 registros, conforme declaração registrada no CSV atualizado; as notas individuais não foram anexadas. O arquivo datado de 13/11 foi preservado como histórico.

A planilha contém **71 propostas de inclusão e 8 de exclusão**, com páginas e justificativas. A validação pessoal permanece pendente. Os 357 registros continuam sendo o conjunto encaminhado pela F1; 71 não é o número final da revisão.

| Situação da decisão | Registros |
|---|---:|
| Proposta I | 71 |
| Proposta E | 8 |
| Sem decisão: acesso ainda pendente | 131 |
| Sem decisão: PDF de versão diferente | 2 |
| Sem decisão: dúvida de escopo | 2 |
| F1=T, aguardando definição do orientador | 143 |
| Total | 357 |

## O que foi examinado

A busca de textos nesta rodada abrangeu os **214 registros I da F1**. Foram tentados os links da planilha, páginas das editoras e cópias públicas em repositórios institucionais ou páginas de autores. Um segundo passe seguiu links de PDF das páginas, pois uma resposta HTML não significa ausência do texto. Falhas de acesso nesta sessão não demonstram indisponibilidade definitiva.

Foram obtidos 80 textos correspondentes aos registros. O exame usou resumo, método e resultados pertinentes aos critérios, com as páginas indicadas no CSV. Não se afirma leitura integral de cada página, extração completa ou conclusão da avaliação de qualidade QA1–QA8. Desses 80 textos, 78 receberam proposta I/E e dois ficaram com dúvida de escopo. Há mais uma exclusão EC1 sustentada pela declaração explícita de ampliação no artigo posterior, mesmo sem acesso ao texto anterior.

Também foram encontradas duas cópias de versões materialmente diferentes, mantidas pendentes. Assim, **134 registros estão sem o texto correspondente**, incluindo R0375, cuja duplicidade já está documentada. Essa contagem de acesso se sobrepõe à contagem de decisões e não deve ser somada a ela.

Os 143 registros T da F1 não receberam preenchimento. As colunas A:M e R da aba Leitura foram preservadas, assim como os links originais. As propostas estão em N:Q. O cinza da formatação condicional indica preenchimento da decisão, não validação pessoal concluída.

## Exclusões propostas

| ID | Critério | Evidência |
|---|---|---|
| R0020 | EC1 | Versão anterior de R0007, que amplia a avaliação de ferramentas |
| R0067 | EC1 | Versão anterior de R0064, que amplia o estudo LibD |
| R0375 | EC1 | R0192, páginas 2–3 e 20, declara a versão ampliada e identifica o DOI 10.1145/3615366.3615426 |
| R0036 | EC6 | DroidNative: quatro páginas no PDF do artigo |
| R0074 | EC6 | LibRadar: quatro páginas no PDF do artigo |
| R1239 | EC6 | Conecte SUS: quatro páginas no PDF do artigo |
| R0102 | EC4 | Bibliotecas usadas como filtro em análise de comportamento/malware; não avalia detecção de bibliotecas ou rastreamento |
| R0565 | IC1 | Texto declara ser revisão, sem estudo primário pertinente ao IC1; pode apoiar fundamentação e bola de neve |

EC6 segue a regra de até quatro páginas do protocolo atual. Não foi aplicado apenas pelo metadado de páginas da planilha, que contém imprecisões. **Nenhuma exclusão EC7 foi aplicada e nenhum pedido foi enviado aos autores.** EC7 exige a tentativa de contato e sete dias sem resposta. *Atualização de 15/11/2026: o EC7 saiu do protocolo (versão 1.6). Texto não obtido, inclusive pela CAPES, conta como não recuperado no PRISMA, sem e-mail ao autor. Na aba "Como ler" da planilha, ignore as linhas sobre EC7.*

## Quatro casos para resolver

- **R0513:** a cópia de 2023 usa 2.998 políticas; a publicação de 2024 informa MiniDetector, 3.369 políticas e avaliação ampliada. Obter a versão correspondente antes de decidir.
- **R0701:** a cópia LGPDCheck de 2023 é um plano de estudo; a publicação de 2025 apresenta avaliação concluída e autoria ampliada. Não atribuir ao artigo de 2025 a ausência de resultados da cópia anterior.
- **R1214:** confirmar se a análise vai além de permissões e vulnerabilidades gerais e atende à delimitação do IC1.
- **R0556:** estudo jurídico e entrevistas sobre JAKI. Alinhar com o orientador a abrangência da QR4 em relação ao IC1, pois não há análise técnica de bibliotecas ou fluxos.

## Cuidados para a síntese

As observações do registro distinguem presença estática, tráfego observado e informações declaradas em políticas. Essas medidas não são intercambiáveis. Amostras compartilhadas entre publicações e versões anteriores não devem ser contadas como populações independentes.

Em R0229, a Seção 5 informa 611/1.647 (37,1%) ocorrências de SDKs atribuídas ao Google; a discussão usa uma redação diferente, referindo-se a apps. O texto do TCC e os slides passam a usar o resultado inequívoco de tráfego: 269/1.166 apps (23,1%) enviaram dados do dispositivo a rastreadores conhecidos. Em R0662, há divergência entre o tamanho declarado da amostra e denominadores da tabela; conferir antes de transcrever porcentagens.

## Arquivos e continuação

- `leitura_F2_para_preencher.xlsx`: planilha editável com propostas e pendências.
- `leitura_F2_registro_20261113.csv`: todos os 357 IDs, estados, evidências, páginas, fontes e hashes disponíveis.
- `leitura_F2_decisoes_20261113.json`: decisões documentais e dúvidas com observações completas.
- `leitura_F2_acesso_20261113.json`: tentativas de obtenção, URLs, falhas e identificação das cópias.
- `leitura_F2_manifesto_20261113.json`: escopo, contagens e hashes da planilha.

O próximo passo é conferir as propostas, resolver os quatro casos e tentar os textos restantes pela CAPES/CAFe ou por cópias autorizadas. Depois, preencher a extração e a avaliação de qualidade dos incluídos e ampliar a síntese bibliográfica. PDFs e textos integrais não são redistribuídos nestes arquivos. A conferência cega da F1 (antigo reteste) continua separada e sem respostas preenchidas.
