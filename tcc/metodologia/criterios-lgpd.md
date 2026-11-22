# Critérios de análise da LGPD

Versão 0.1, de 13/11/2026. Proposta para revisão com o orientador antes da coleta principal. A aplicação aos aplicativos ainda não foi realizada.

## Objetivo e unidade de análise

Registrar, de forma verificável, a relação entre o comportamento observado de um aplicativo, sua política de privacidade e os fundamentos declarados para o tratamento de dados. A unidade é **aplicativo × versão × destinatário × categoria de dado × finalidade × cenário de execução**. Uma versão diferente, uma nova política ou outro cenário exige novo registro.

A análise separa três perguntas: há um componente no pacote? Há transmissão observada? Há documentação correspondente? A presença de um SDK, sozinha, não responde às duas últimas.

## Evidência e resultado de cada critério

Guarde o `appId`, versão, SHA-256 do pacote, data da observação, ferramenta e versão da base de assinaturas. Para documentos, registre URL, data de acesso, versão ou hash e trecho/localização que sustenta a classificação. Para tráfego, registre cenário, destino e categoria do dado, preservando apenas evidência sanitizada. Credenciais, tokens e dados pessoais não devem ir para o repositório público.

Use estes quatro resultados, sem transformá-los em uma nota geral de legalidade:

| Resultado | Quando usar |
|---|---|
| Documentado | A evidência consultada responde ao item. Descrever exatamente o que foi encontrado |
| Indício de inconsistência | Uma evidência concreta diverge de uma declaração aplicável à mesma versão e finalidade |
| Não verificável | A informação ou o acesso necessário não está disponível, ou o teste não permite concluir |
| Não aplicável | O critério não incide no caso observado. Registrar o motivo |

“Documentado” não equivale a conformidade jurídica integral. “Não verificável” não equivale à inexistência de base legal ou de contrato.

## Matriz de critérios

| Código | Fundamento | O que registrar | Regra de interpretação |
|---|---|---|---|
| L01 | LGPD, Arts. 5º e 7º | Categoria de dado, finalidade específica, destinatário e hipótese legal indicada para essa operação | Uma referência genérica à LGPD não identifica a base de cada finalidade. Se a política não discriminar a operação, registrar a lacuna documental |
| L02 | LGPD, Arts. 7º, 8º e 9º | Quando a base declarada for consentimento: aviso, ação de aceitar/recusar, revogação e tráfego nos cenários autorizados | Não exigir consentimento para toda operação. Se houver outra base indicada, examiná-la no item L01 |
| L03 | LGPD, Arts. 5º, II, e 11 | Se o dado efetivamente observado é sensível e qual hipótese do Art. 11 é indicada | Um app de saúde não torna todo dado de rede um dado de saúde. Legítimo interesse não é uma hipótese do Art. 11 |
| L04 | LGPD, Arts. 6º e 23; guia da ANPD | Finalidade pública declarada, competência do órgão e relação entre serviço e coleta pelo terceiro | Avaliar separadamente a operação necessária ao serviço e funções adicionais. Não presumir que o caráter oficial autoriza qualquer coleta |
| L05 | LGPD, Arts. 26 e 27; guia da ANPD | Se há compartilhamento com terceiro privado, quem recebe, para quê e qual fundamento/instrumento público foi localizado | A ausência de documento público é limitação da observação. Não afirmar inexistência de contrato sem evidência |
| L06 | LGPD, Art. 33; Resolução CD/ANPD nº 19/2024, Arts. 3º a 6º | Exportador, importador, localização relevante e operação que os conecta, quando identificáveis | Separar transferência internacional, coleta internacional direta e situação indeterminada. Nacionalidade do fornecedor ou geolocalização do IP não bastam |
| L07 | LGPD, Arts. 7º, 11 e 33; Resolução nº 19/2024, Art. 9º | Base legal do tratamento e mecanismo de transferência declarado: adequação, garantia contratual ou outra hipótese aplicável | São dois registros diferentes. O mecanismo internacional não substitui a base legal do tratamento |
| L08 | Resolução nº 19/2024, Arts. 17 e 32; guia da ANPD | Destino, finalidade, agentes envolvidos e informações públicas sobre a transferência | Verificar o texto vigente na data da coleta. Registrar qual documento sustenta a alegação, sem presumir cobertura global de uma cláusula genérica |
| L09 | Protocolo empírico da H1 | Correspondência entre destinatário detectado, nome comercial/jurídico, categoria de terceiro, finalidade e categorias de dados declaradas | Classificar separadamente menção nominal, menção por categoria, ausência de menção e documento indisponível. Evitar confundir categorias genéricas com menção nominal |
| L10 | Protocolo empírico do objetivo 4 | Cenário executado, autenticação, duração, ações realizadas, limitação por TLS/pinning e cobertura do teste | Falha de observação não é ausência de transmissão. Só atribuir um dado ao destino quando a evidência permitir essa ligação |

## Aplicação às hipóteses e aos resultados

**H1.** Conte pares aplicativo–SDK com função documentada, detecção confirmada e política recuperada com informação suficiente para julgar categorias de dados e finalidades. Informe o numerador, o denominador e a quantidade de políticas indisponíveis. Publique separadamente a ausência de menção nominal, que não é omissão por si só, a declaração compatível por categoria e finalidade e as divergências materiais justificadas com evidência. Faça análise de sensibilidade para declarações genéricas. Não inclua política indisponível no numerador de “não declarado”. Uma divergência estática será descrita como divergência documental ou ponto a verificar; a expressão “fluxo não declarado” exige evidência do fluxo.

**H2.** A classificação do aplicativo como sensível usa a funcionalidade que trata saúde ou biometria do usuário. Para discutir um envio específico, reavalie a natureza do dado observado. O fato de o aplicativo agendar consultas não prova que o SDK receba o conteúdo da consulta.

**Objetivo 4.** Separe o país inferido para o ponto de rede, o país da entidade destinatária e eventual localização de tratamento/armazenamento documentada. Registre a fonte e a incerteza de cada campo. CDN, proxy e infraestrutura compartilhada impedem tratar esses campos como equivalentes.

**Síntese.** Apresente contagens por critério e por nível de evidência, com denominadores explícitos. Não some os dez critérios em um índice de “conformidade LGPD”, porque o estudo não acessa todos os contratos, processos internos ou operações do órgão.

## Ficha para preencher

| Campo | Registro |
|---|---|
| Identificação | appId, versão, SHA-256, data, avaliador |
| Observação técnica | componente ou fluxo, destinatário, categoria de dado, finalidade, cenário |
| Declaração | política/loja/documento, URL, data, trecho e localização |
| Classificação | código L01–L10, resultado, justificativa, informação faltante |
| Revisão | data da conferência, alteração e motivo |

## Fontes consultadas

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais. Texto atualizado disponibilizado pela Câmara dos Deputados. Disponível em: https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-normaatualizada-pl.html. Acesso em: 13 nov. 2026.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Tratamento de dados pessoais pelo Poder Público: guia orientativo**. Versão 2.0. Brasília, DF: ANPD, 2023. Seções sobre bases legais, princípios e compartilhamento. Disponível em: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-poder-publico-anpd-versao-final.pdf. Acesso em: 13 nov. 2026.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Resolução CD/ANPD nº 19, de 23 de agosto de 2024**. Regulamento de Transferência Internacional de Dados e cláusulas-padrão contratuais. Texto consolidado consultado, com indicação de retificação em 2025. Disponível em: https://www.gov.br/anpd/pt-br/acesso-a-informacao/institucional/atos-normativos/regulamentacoes_anpd/resolucao-cd-anpd-no-19-de-23-de-agosto-de-2024. Acesso em: 13 nov. 2026.
