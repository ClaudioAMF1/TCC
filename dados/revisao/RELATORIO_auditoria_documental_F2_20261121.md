# Auditoria documental da F2 — 21/11/2026

## Escopo e integridade

Fonte preservada: `leitura_F2_registro_20261113.csv`, SHA GitHub `448cf4dfcca922c24b498b0773482071b36651f9`.

Foram conferidas **as 357 linhas** quanto à estrutura e à consistência de estados/decisões. Não foram encontrados IDs duplicados, títulos vazios, decisões E sem critério, propostas sem fonte/evidência ou incompatibilidade entre a decisão registrada e o status `proposta_registrada`.

| Situação | Quantidade |
|---|---:|
| Registros F2 totais | 357 |
| Propostas I | 71 |
| Propostas E | 8 |
| Sem decisão | 278 |
| Registros examinados adicionalmente com fonte externa nesta auditoria | 18 |
| Propostas ainda sem conferência externa nesta rodada | 61 |
| Sem decisão em F2 | 278 |
| Sem texto correspondente obtido | 131 |
| Dúvida por versão divergente | 2 |
| Dúvida de escopo | 2 |
| Casos T da F1 aguardando F2 | 143 |

## Resultado da conferência documental externa — 18 registros

### Inclusões com escopo corroborado (12)

- **R0007** — Zhan et al.: avaliação sistemática de detectores de bibliotecas Android; não equivale a identificar comunicação de rede.
- **R0105** — Backes et al.: detector LibScout, inclusive versões de bibliotecas.
- **R0376** — Binns et al.: medição estática em aproximadamente 959 mil aplicativos; evitar interpretar como tráfego observado.
- **R0178** — Kollnig et al.: comparação de 2017/2020 por referências a rastreadores; não isola efeito causal do GDPR.
- **R0442** — Andow et al.: PoliCheck confronta fluxos com políticas; a identidade do destinatário importa.
- **R0504** — Baalous et al.: pertence ao tema QR3, mas o resultado 67,7% deve trazer definição exata do denominador e limitação da análise estática.
- **R0229** — Samarasinghe et al.: estudo de aplicativos governamentais de múltiplos países, com análise de tráfego e SDKs.
- **R0662** — Carlsson et al.: **ressalva obrigatória**: artigo diz 32 aplicativos, mas 29/85,3% na Tabela 1 pressupõe aproximadamente 34. Não reproduzir percentuais sem a inconsistência.
- **R0693** — Reis et al.: corpus de políticas e LGPD, sem execução dos aplicativos.
- **R0071** — LibKit: detecção de bibliotecas **iOS**; IC1 admite aplicativos móveis, mas é evidência comparativa, não específica de Android.
- **R0760** — Rodrigues/Grindr: análise documental jurídica pertinente à QR5, não medição técnica.
- **R0192** — Serrano et al. 2024: estudo ampliado de rastreadores em apps relacionados à COVID-19.

### Exclusões documentais corroboradas ou plausíveis (6)

- **R0020** — EC1: versão ASE 2020 é declarada anterior à versão ampliada de Zhan et al. (2022).
- **R0067** — EC1: versão de evento de LibD é declarada preliminar na publicação ampliada.
- **R0036** — EC6: DroidNative tem quatro páginas, short paper.
- **R0074** — EC6: LibRadar é artigo curto do ICSE Companion com quatro páginas.
- **R0375** — EC1: artigo de Serrano et al. 2024 afirma ser versão ampliada e revista do trabalho de 2023.
- **R0565** — IC1 (ressalva): estudo jurídico de saúde pública na Arábia Saudita; não mede bibliotecas/fluxos e não trata especificamente de LGPD ou transferência internacional em QR5. A exclusão por escopo é defensável, mas cabe discussão caso QR4 seja ampliada para estudos jurídicos internacionais.

As fontes e observações **por ID** estão nas colunas adicionadas de `leitura_F2_registro_20261113_com_auditoria_20261121.csv`. Elas são verificações **documentais assistidas** de escopo e informações centrais; não representam extração integral de dados nem avaliação QA1–QA8 completa.

## Registros ainda sem validação científica concluída

Os **61** registros com proposta I/E não examinados nesta rodada e os **278** sem decisão continuam dependentes de conferência individual dos textos corretos ou definição dos critérios. O código `validacao_pessoal` segue **pendente nas 357 linhas**, pois significa a conferência assumida e registrada pelo autor, não uma execução automática. Não é correto transformá-lo em `validado` sem concluir a etapa correspondente.

A conferência cega de 125 registros F1 permanece uma etapa **diferente** da F2: não deve ser simulada a partir da classificação inicial ou de decisões já visíveis, sob pena de invalidar o caráter cego e o κ de Cohen.

## Arquivos criados

1. `dados/revisao/auditoria_documental_F2_20261121.csv`: tabela sintética com uma linha para cada um dos 357 IDs e parecer documental quando houve revisão de fonte.
2. `dados/revisao/leitura_F2_registro_20261113_com_auditoria_20261121.csv`: **cópia integral das 357 linhas e 18 colunas originais**, acrescida de quatro colunas (status, parecer, fonte e data de auditoria). Nenhuma decisão histórica nem a coluna `validacao_pessoal` foi modificada.
3. Este relatório.

## Recomendação para o Capstone I

Descrever **71 propostas preliminares de inclusão**, não 71 inclusões definitivamente conferidas. Explicitar as limitações acima e confirmar com o orientador se o término da F2 pode ocorrer no Capstone II. Antes da defesa, revisar o enquadramento de R0071 e R0565 e evitar porcentagens problemáticas do R0662.

---
**Limitação de escopo:** esta auditoria verifica dados, fontes e coerência de uma parte dos artigos; não substitui uma revisão F2 integral, a decisão acadêmica de inclusão pelo autor ou o aval do orientador.
