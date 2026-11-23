# Auditoria ampliada F2 — 357 registros (21/11/2026)

## Escopo e resultado

**Status: a conferência de integridade e rastreabilidade do universo F2 foi concluída; a validação científica integral por texto completo NÃO foi concluída.** A informação é indispensável para não apresentar propostas ou análises preliminares como decisões finais da revisão.

Fontes: `dados/revisao/leitura_F2_registro_20261113.csv` (histórica), `dados/revisao/leitura_F2_registro_20261121_validacao_parcial.csv` (com concordância do autor em 18 pareceres), o protocolo `tcc/revisao/protocolo-revisao-sistematica.md` versão 1.7, e fontes acadêmicas externas indicadas por ID.

**Entregável principal:** `dados/revisao/F2_matriz_rastreabilidade_357_20261121.csv`. São 357 linhas, IDs únicos, com as colunas históricas preservadas e campos de:
- tipo de evidência adicional e URL;
- sugestão **não decisória** de I/E/R, quando fundamentada;
- prioridade para obter/ler o texto;
- QR candidata;
- QA1–QA8 e total (sem valores inventados) e status da documentação QA.

### Reconciliação dos registros

| Natureza do registro | n |
|---|---:|
| Propostas I/E cujo autor informou ter concluído leitura e QA1–QA8, mas sem notas numéricas no repositório | 18 |
| Outras propostas I/E, com evidência anterior, ainda não verificadas integralmente nesta auditoria | 61 |
| Sem decisão F2, com fonte adicional pesquisada nesta rodada | 16 |
| Sem decisão F2 e ainda sem texto integral confirmado após esta rodada | 121 |
| F1=T sem decisão F2, triadas apenas por título/metadados nesta rodada | 141 |
| **TOTAL** | **357** |

Os 16 com novas fontes estavam antes entre os 278 sem decisão (2 com divergência de versão, 2 com dúvida de escopo, 2 F1=T e 10 no conjunto de 131 sem texto). A fonte adicional de alguns deles é **somente resumo ou metadado**, não texto integral. Portanto, eles também **permanecem sem decisão F2 validada**.

| Decisão já registrada na F2 | n |
|---|---:|
| I (proposta) | 71 |
| E (proposta) | 8 |
| Sem decisão | 278 |
| **TOTAL** | **357** |

Apenas 18 das 79 propostas têm concordância do autor expressa no registro. O número de **71 propostas de inclusão não pode ser convertido em 71 estudos definitivamente incluídos**.

## Estudos com nova fonte pesquisada — 16 casos

| ID | Tipo de evidência | Indicação **não decisória** | Fundamentação e fonte |
|---|---|---|---|
| R0026 | PDF de dez páginas acessível | I condicional (QR1) | CRiOS identifica bibliotecas e endpoints em 43.404 apps **iOS**; <https://megele.io/crios-spsm2016.pdf> |
| R0031 | Resumo editorial, texto condicionado a acesso | I condicional (QR1) | SecureComm 2022; Libmonitor avalia TPLs e riscos de vazamento; <https://eudl.eu/doi/10.1007/978-3-031-25538-0_30> |
| R0038 | Resumo do periódico | I condicional (QR1) | Análise Xposed de riscos de bibliotecas de terceiros em 150 apps; <https://www.sciencedirect.com/science/article/pii/S2214212618304356> |
| R0117 | Registro de publicação | I condicional (QR2) | AppChk, comunicação com terceiros em apps iOS; <https://extern.fis.uni-bamberg.de/en/entities/publication/a7abe7ae-4497-40f8-bf66-25c767db5782/> |
| R0119 | Fonte de texto identificada, acesso restringido na conferência | I condicional (QR2) | The Price to Play, estudo de jogos Android pagos e gratuitos, WWW 2022; <https://hal.science/hal-03559973v1/document> |
| R0134 | PDF completo de oito páginas | I condicional (QR2, QR3) | ARES 2023, 200 apps Android e 200 iOS, trackers e consentimento; <https://research.tue.nl/files/345462655/3600160.3605079.pdf> |
| R0200 | Artigo completo em HTML | R para bola de neve | Revisão sistemática dos apps COVID e políticas; o protocolo não admite revisão como estudo primário; <https://mhealth.jmir.org/2022/7/e35195> |
| R0254 | PDF publicado | I condicional (QR2, QR3) | FAccT 2022, 1.759 apps iOS e impacto do App Tracking Transparency; <https://cris.maastrichtuniversity.nl/files/139816360/Kollnig_2022_Goodbye_Tracking_Impact_of_iOS.pdf> |
| R0299 | PDF do artigo completo | I condicional (QR2, QR3) | BMJ 2021, estudo de 20.991 apps de saúde, práticas estáticas/dinâmicas e políticas; <https://www.bmj.com/content/bmj/373/bmj.n1248.full.pdf> |
| R0356 | Artigo de seis páginas | I condicional (QR2) | WiSec 2015: rastreamento em apps pagos. A palavra Short no título **não** significa que o artigo tenha até quatro páginas (EC6); <https://research.csiro.au/isp/wp-content/uploads/sites/106/2015/06/wisec2015.pdf> |
| R0429 | PDF completo | I condicional (QR3) | IEEE 2024, estudo de 30 apps Android de crédito e políticas de privacidade; <https://amoralesflor01.github.io/files/A_License_to_Prey_Investigating_the_Impact_of_Digital_Loan_App_Regulations_on_Permission_Requests_and_Privacy_Policies_in_the_Kenyan_Market.pdf> |
| R0513 | Pré-publicação PDF e publicação IEEE verificadas | I condicional (QR3) | *Do as You Say*, mini-apps WeChat; versão publicada IEEE TSE 50(12):3225–3248 (2024), DOI 10.1109/TSE.2024.3479288. Comparar versões; <https://arxiv.org/pdf/2302.13860> |
| R0556 | PDF integral de 19 páginas | E/IC1 proposto | Estudo jurídico e entrevistas sobre SuperApp JAKI na Indonésia, sem mensuração de SDKs/terceiros nem LGPD brasileira; <https://repository.uin-malang.ac.id/21021/2/21021.pdf> |
| R0638 | PDF integral de 33 páginas | E/IC1 ou EC3 proposto | Análise jurídica de apps de geolocalização COVID na República Tcheca/Áustria, sem medição de bibliotecas de terceiros; limite de QR4 requer decisão explícita; <https://cjir.iir.cz/index.php/cjir/article/download/62/46> |
| R0701 | Publicação de periódico verificada | I condicional (QR5) | LGPDCheck publicado em *Empirical Software Engineering* 2025; texto final ainda não cotejado com arXiv 2308.14874; <https://dblp.org/rec/journals/ese/CerqueiraMCT25> |
| R1214 | PDF integral e publicação verificados | I condicional (QR2) | *Your Doctor is Spying on You*, estudo em 272 apps Android mHealth, BuildSEC 2025; <https://arxiv.org/pdf/2510.06015> |

**A indicação de I/E/R na tabela NÃO é uma decisão F2 final.** Nos casos em que foram obtidos PDFs, a verificação principal foi de autoria, versão, escopo e método resumido. Não houve uma avaliação quantitativa QA1–QA8 integral e uniforme para os 16 registros, nem decisões endossadas pelo autor.

## Triagem orientativa dos 143 casos originalmente T

A matriz registra a classificação por título para os **141** sem fonte adicional pesquisada:
- **53** prioridade alta: título contém conceitos diretamente associados aos eixos rastreamento, bibliotecas, privacidade, políticas ou LGPD;
- **83** prioridade média: pertinência incerta;
- **5** prioridade baixa: título sugere tema periférico.

Além desses 141, **R0356 e R0429** foram pesquisados por fonte externa (total 143). Essas prioridades são *mecânicas* e **não alteram o status T da F1 nem produzem decisão F2**.

## Regras científicas que impedem encerrar artificialmente a F2

1. **IC1–IC4 e EC1–EC6** exigem inspeção do texto completo para a decisão F2; um título, resumo ou DOI não comprova elegibilidade.
2. A falta do PDF **não constitui exclusão** no protocolo versão 1.7. Sem texto após tentativas documentadas, registrar como **não recuperado (NR)**.
3. Revisões secundárias devem receber **R para bola de neve**, não ser contadas entre estudos primários incluídos.
4. **QA1–QA8** deve registrar respostas 0/0,5/1 por critério, com justificativa por artigo. Para os 18 registros em que o autor informou conclusão, as notas individuais **não foram disponibilizadas**. A matriz as deixa em branco, não atribui zero.
5. O segundo avaliador/κ da F1 é fluxo separado. Não usar dados dessa matriz para simular conferência cega.
6. Não recalcular a seleção ou os totais PRISMA com sugestões ainda não confirmadas.

## Pendências reais para a validação científica integral

- Validar e, quando necessário, corrigir as 61 propostas I/E não examinadas externamente nesta rodada;
- Concluir análise documental e decisão dos 16 casos com fontes adicionais, inclusive cotejo de versões;
- Obter fontes integrais para os 121 ainda sem acesso confirmado nesta rodada; CAPES/CAFe pode ser essencial;
- Examinar resumo e texto completo e decidir os 141 F1=T triados apenas por título;
- Registrar **QA1–QA8 com pontuação, evidência e justificativa por estudo empírico incluído**;
- Documentar verificação independente final, aprovar decisões e atualizar PRISMA, síntese teórica e TCC/slide apenas depois de fechado o estado real.

A presente auditoria é **exaustiva na enumeração e rastreabilidade dos 357 registros**, mas **não equivale à validação integral por leitura crítica de 357 publicações**. Nenhum dado foi preenchido artificialmente para dar a aparência de conclusão.

## Referências operacionais

- Entrada: `dados/revisao/leitura_F2_registro_20261121_validacao_parcial.csv`;
- Saída: `dados/revisao/F2_matriz_rastreabilidade_357_20261121.csv`;
- Protocolo: `tcc/revisao/protocolo-revisao-sistematica.md` (v1.7);
- Relatório anterior de 18 pareceres: `dados/revisao/RELATORIO_auditoria_documental_F2_20261121.md`.
