# Auditoria parcial de consistência — 16/11/2026

**Escopo.** Conferência computacional dos arquivos versionados e revisão pontual das afirmações do projeto. Não equivale a segunda avaliação cega, a aprovação do orientador ou a verificação independente de todos os aplicativos e PDFs. Nenhum campo `validacao_pessoal` foi alterado.

## Corpus Android

Fonte: `dados/n3_corpus_20260917.csv` (396 registros; nenhum `appId` duplicado).
 
| Verificação | Valor conferido |
|---|---:|
| Total de candidatos | 396 |
| OFICIAL_S_N = S | 376 |
| OFICIAL_S_N = N | 20 |
| Oficiais federais / estaduais / municipais | 85 / 199 / 92 |
| SENSIVEL_REVISADO = sim entre oficiais | 100 |
| Divergências sensibilidade automática × revisada entre oficiais | 108 |
| Automática sim → revisada não | 75 |
| Automática não → revisada sim | 33 |
| Oficiais com tem_anuncio=True | 0 |
| Oficiais classificados como sensíveis sem justificativa textual em OBS | 69 |

**Interpretação.** As contagens reproduzem o texto e os slides. São apenas consistências **internas**; a decisão de oficialidade e o tratamento de dados sensíveis ainda exigem reexame das fontes primárias.

**Pontos de atenção.** Sete exclusões relacionadas à PRODESP registram divergência entre o nome exibido do desenvolvedor e o titular jurídico da conta em uma coleta específica. Antes de consolidar esses casos, preservar evidência verificável da página “Sobre o desenvolvedor”, com data, versão e URL, e aplicar o critério de publicação de modo consistente. Em 69 das 100 classificações de sensibilidade não há comentário `OBS`; a ausência do comentário não prova erro, mas recomenda confirmar a evidência por aplicativo. Não inferir automaticamente tratamento de dado sensível apenas pela categoria da loja ou por mencionar consultas.

## Revisão sistemática F2

Fonte: `dados/revisao/leitura_F2_registro_20261113.csv` (357 registros).

| Status | Registros |
|---|---:|
| Propostas de inclusão (I) | 71 |
| Propostas de exclusão (E) | 8 |
| Sem texto correspondente, acesso pendente | 131 |
| Cópia obtida com versão divergente | 2 |
| Dúvida de escopo | 2 |
| F1=T, aguardando orientação | 143 |
| Total | 357 |

Todos os 357 registros apresentam `validacao_pessoal=pendente`. Das 214 buscas de texto correspondentes aos I da F1, há 80 textos correspondentes obtidos; destes, 71 propostas I, sete propostas E e duas dúvidas. A oitava proposta E foi inferida da informação publicada por versão ampliada, sem o PDF correspondente da versão anterior. Logo, **80 textos obtidos ≠ 79 propostas de decisão** e o fluxograma deve discriminar essas unidades.

Os 71 são **propostas preliminares**. Não há, nesses arquivos, avaliação QA1–QA8 concluída, nem dupla revisão independente finalizada. A amostra de 125 registros de F1 foi preparada, não avaliada; não há κ de Cohen a reportar até o preenchimento.

## Piloto e taxas

Os totais nominais do piloto foram confrontados com o texto: 20 APKs; 75%, 95% e 80% com detecção conforme A/B/C; 88/123 = 71,5% dos registros B classificados na adjudicação como falsos positivos potenciais. **Não se reproduziu κ = 0,52 ou κ = 0,69 de forma independente**, porque não foram obtidas as matrizes de decisões por APK/rastreador e a referência de adjudicação independente. A adjudicação foi baseada nas evidências dos próprios detectores; a estimativa corrigida é análise de sensibilidade, não verdade-terreno independente.

As contagens aritméticas de contexto se conciliam: 1.531 - 282 = 1.249; 1.249 - 886 - 6 = 357; 357 - 71 - 8 = 278; e 131 + 2 + 2 + 143 = 278. Isso não valida a correção das decisões artigo a artigo.

## Arquivos de texto ajustados

- `tcc/latex/main.tex`: resumo, abstract, síntese F2, descrição da adjudicação e rótulos do fluxo da revisão;
- `tcc/apresentacao/roteiro-simulacao.md`: fala da revisão, interpretação do piloto e respostas da banca.

**Atenção:** esses ajustes são em fontes textuais. Os PDFs e PPTX versionados precisam ser recompilados/reexportados e conferidos visualmente antes da entrega.

## Validação adicional necessária

1. Conferir as decisões de F2 contra seus PDFs, confirmando páginas, método, critérios e qualidade QA1–QA8.
2. Reavaliar os 125 registros da amostra cega sem consultar a primeira decisão e calcular κ de Cohen a partir dessas respostas.
3. Verificar fontes oficiais e titularidade jurídica dos 20 candidatos excluídos, com atenção aos sete casos PRODESP.
4. Conferir a evidência de dado sensível aplicativo a aplicativo, especialmente os 69 com `OBS` sem justificativa.
5. Reproduzir κ do piloto a partir dos resultados por APK e obter uma referência externa se se pretender afirmar uma taxa de falsos positivos.
6. Obter a revisão do orientador e confirmar a conformidade literal com plano de ensino e regulamento.

Este registro documenta **o que foi efetivamente auditado**, sem afirmar conclusão das etapas pendentes.
