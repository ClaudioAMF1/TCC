# Prompt para finalizar a apresentação

Para colar em outro modelo, junto com os anexos listados logo abaixo. Escrito em
22/09/2026, depois da conferência dos prints e das citações contra o PDF.

**Anexe estes arquivos:**

| Anexo | Onde está |
|---|---|
| A apresentação | `seminario/apresentacao/seminario-analise-de-artigo.pptx` |
| O artigo | baixe pelo DOI 10.1145/3548606.3560564 (acesso livre na ACM) |
| O exemplo da professora | `seminario/material-fornecido/Exemplo de Analise da Estrutura de Artigo.pdf` |
| Os quatro degraus do funil | `seminario/pesquisa/recortes-para-slide/funil-1-131.jpg`, `funil-2-70.jpg`, `funil-3-39.jpg`, `funil-4-5.jpg` |
| O Qualis da CAPES | `seminario/pesquisa/metricas/07-qualis-eventos-computacao-2017-2020-ccs-a1.png` |

---

```text
Você vai finalizar uma apresentação de seminário acadêmico. O arquivo .pptx está
anexado. Seu trabalho é aplicar correções específicas e dar acabamento, SEM mudar
o conteúdo que já foi verificado. Leia tudo antes de começar.

## Contexto

Seminário de análise de artigo científico, disciplina Projeto Capstone I, curso de
Ciência da Computação do IDP. Apresentação individual de no máximo 15 minutos.
Vale 4 dos 6 pontos do bimestre. O enunciado exige, nesta ordem:

1. Seleção do artigo: o passo a passo da busca numa base acessada via CAFe, a
   justificativa de que é artigo original e a relevância para o TCC do aluno, com
   critérios quantitativos e/ou qualitativos.
2. Métricas do veículo. Como o artigo saiu em conferência: índice h5 no Google
   Scholar, o Qualis correspondente e o rank no CORE Conference Portal.
3. Análise da estrutura do artigo (introdução, método, resultados, discussão,
   conclusão), descrevendo e explicando cada elemento.

Artigo: NGUYEN, T. T.; BACKES, M.; STOCK, B. "Freely Given Consent? Studying
Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android
Apps". ACM CCS 2022, p. 2369–2383. DOI 10.1145/3548606.3560564. O PDF está
anexado.

O deck tem 23 slides numerados e 2 de apoio. Os slides 5 a 22 seguem o formato do
exemplo da professora (PDF anexado): trecho literal do artigo em inglês, tradução
em português e a análise da função daquele trecho. Esse formato é exigência e
deve ser mantido.

## Parte 1 — Correções obrigatórias

Aplique exatamente estas. Todas foram conferidas contra fonte primária.

1. SLIDE 4, caixa do Qualis. Hoje diz "Não determinável com os dados
   disponíveis" e explica que A1 exige percentil ≥ 87,5. Substitua por:
   - Título da caixa: "QUALIS CAPES"
   - Valor em destaque: "A1"
   - Texto: "Qualis Eventos da Computação, quadriênio 2017–2020, p. 9. A sigla
     CCS amarra o registro ao veículo do artigo. O h5 é coerente: a posição 5 da
     subárea atinge o limiar de 87,5 do A1 a partir de um universo de 40
     veículos."
   Se couber, use a imagem anexada do relatório da CAPES como miniatura.

2. SLIDE 4, caixa do h5. Hoje diz "Valores registrados no material fornecido.
   Sem nova confirmação no Google Scholar." Substitua por: "Google Scholar
   Metrics, Computer Security & Cryptography: posição 5. Entre as conferências da
   lista, é a 3ª. Consulta: 17/09/2026." Mantenha "90" e "mediana h5: 146".

3. SLIDE 4, linha de fonte no topo. Substitua por: "Fontes: Google Scholar
   Metrics e ICORE, consulta em 17/09/2026; CAPES, Qualis Eventos Computação
   2017–2020."

4. SLIDE 2, o funil. Hoje tem 3 degraus (131, 70, 5) e atribui o 5 a
   "palavras-chave específicas". O correto tem 4 degraus. Troque as 3 imagens
   pelas 4 anexadas (funil-1 a funil-4), lado a lado, mesma altura, na ordem:
   - 131 | "expressão exata, sem filtros"
   - 70 | "2018–2026, Computação, artigos e conferências"
   - 39 | "palavras-chave Third Parties e Third-party Tracking"
   - 5 | "+ termo consent na busca, período 2018–2025"
   Mantenha a caixa "1 artigo selecionado" e a linha "Busca: "third-party
   tracking"". O degrau de 39 para 5 é o mais importante: foi uma decisão de
   método (consentimento é o recorte do TCC), não um filtro de interface.

5. SLIDE 3. Acrescente, sem tirar nada, uma linha de relevância quantitativa:
   "Citações em 17/09/2026: 42 na ACM Digital Library · 52 no Scopus · 99 no
   Google Acadêmico". Se precisar de espaço, reduza a caixa do "239.381".

6. SLIDE 8, pergunta 02. O texto em inglês está errado. Substitua por:
   "Can these implemented consent notices be legally justified under GDPR?"
   e REMOVA do rodapé a frase "A redação original da segunda pergunta foi
   preservada." A tradução em português pode ficar como está.

7. SLIDE 24, tabela de finalistas.
   - A linha "WhisperTest | CCS / 2025 | 0 | Recorte iOS" está errada. Substitua
     por: "An Empirical Measurement of Cookie Banners Potential Legal Violations
     in EU vs US Websites | LNCS / 2025 | 0 | Recorte web". Abrevie o título se
     não couber.
   - Na linha "A fait accompli?", troque "Menor prioridade na seleção" por
     "Veículo CORE B".

8. SLIDE 25, fontes.
   - Acrescente: "CAPES. Relatório Qualis Eventos, Computação, quadriênio
     2017–2020, p. 9."
   - Troque "h5 e mediana: valores do material original, sem nova confirmação na
     fonte." por "Google Scholar Metrics, Computer Security & Cryptography.
     Consulta: 17/09/2026."

## Parte 2 — Acabamento

Depois das correções, revise o deck inteiro com estes critérios:

- Nenhum texto transbordando da caixa ou sobreposto a outro elemento.
- Corpo de texto legível projetado. Nada abaixo de 12 pt, exceto as linhas de
  fonte no topo dos slides.
- Alinhamentos, margens e espaçamentos consistentes entre slides do mesmo tipo.
- Português claro e direto, frases curtas, sem jargão sem explicação.
- Sem travessão (—) usado como recurso de estilo no meio de frases. Use ponto,
  vírgula ou dois-pontos. Travessão em intervalo de páginas ("p. 2–3") e em
  célula vazia de tabela pode ficar.
- Numeração "NN / 23" correta em todos os slides numerados.

## O que você NÃO pode fazer

- Não altere nenhum número além dos da Parte 1. Todos estes foram conferidos no
  PDF do artigo e devem continuar exatamente assim: 239.381 · 13.082 · 2.688
  (20,54%) · 30.160 · 32.341 (93,26%) · 5.740 / 3.949 / 2.871 / 522 ·
  2.181 (16,67%) · 1.084 (8,28%) · 134 · 929 / 609 / 466 / 177 · 48 / 28 / 58 ·
  14.420 (47,81%) · 29.952 (99,31%) · 1.127 desenvolvedores · 1.859 apps ·
  43 respostas · 9/14 · 9/13 · 6/7 · 147 / 63 / 84 · 11.591 · 1.996 ·
  45 domínios · 150 s.
- Não mexa no texto dentro de aspas em inglês, exceto o do slide 8. Os outros
  16 recortes foram conferidos palavra por palavra contra o PDF.
- Não resuma nem parafraseie os recortes dos slides 5 a 22. O formato "trecho
  literal + tradução + análise" é o que a professora pediu.
- Não acrescente slides, não mude a ordem e não invente dado, fonte, data ou
  citação. Se algo não couber ou você achar que está errado, não conserte por
  conta própria: aponte no relatório final.
- Não troque fonte, paleta de cores nem o estilo visual geral. É acabamento, não
  redesenho.

## Tempo

São 15 minutos para 23 slides. Se você achar que o deck não cabe, não corte por
conta própria. Diga no relatório, sabendo que os únicos pares que podem ser
fundidos são 9+10 (Figura 1) e 6+7 (resumo). Os slides 5, 12, 13, 19, 21 e 22
não podem ser cortados nem fundidos.

## O que entregar

1. O .pptx corrigido. Se você consegue executar código, edite o arquivo com
   python-pptx, preservando o layout existente. Se não consegue gerar arquivo,
   entregue as instruções de edição slide a slide, com o texto final exato de
   cada caixa alterada.
2. Um relatório curto, em lista, com:
   - cada mudança feita, por slide, com o texto antes e depois;
   - tudo o que você achou estranho e NÃO mudou, com o motivo;
   - a confirmação de que conferiu, um por um, os 8 itens da Parte 1.
```
