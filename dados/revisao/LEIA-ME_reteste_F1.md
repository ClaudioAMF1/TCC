# Conferência cega da triagem F1

Preparada em 13/11/2026 como reteste e usada, desde 15/11/2026, como conferência cega por amostra (protocolo, versão 1.7, Seção 7.2). Os arquivos mantêm o nome `reteste_F1_20261116` para não romper o manifesto.

## Para que serve

A classificação F1 registrada para os 1.249 registros não foi feita inteiramente por você. Esta conferência mede o quanto ela coincide com a sua avaliação, numa amostra de 10%, sem precisar conferir os 1.249 um por um.

## Como fazer

1. Abra **reteste_F1_20261116.xlsx**, aba **Como decidir**. Leia as regras e preencha a data em B6.
2. Na aba **Reteste**, leia os 125 registros em ordem e preencha só as células amarelas: decisão, critério e observação. Não consulte as decisões registradas em outras planilhas.
3. Decisões: **I** segue para o texto completo; **T** (dúvida) também segue; **E** exclui, com o código do critério; **R** é revisão da literatura, reservada para a bola de neve.
4. Salve com o mesmo nome. Não há intervalo mínimo. A conferência está prevista para o início do Capstone II e não é exigida para a entrega de 03/12.

## Depois de preencher

A comparação é feita por `id` com a classificação registrada:

```bash
python3 scripts/revisao_triagem.py concordancia dados/revisao/reteste_F1_20261116.xlsx
```

O resultado traz o acordo observado, o κ de Cohen e a matriz, na divisão I/T contra E/R e nas quatro categorias, mais a lista de divergências. Cada divergência é examinada e a decisão final é registrada com o motivo. Se o κ ficar abaixo de 0,6, uma segunda amostra de 125 será sorteada e conferida da mesma forma.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `reteste_F1_20261116.xlsx` | Planilha para preencher, sem gabarito em aba oculta, comentário ou fórmula |
| `reteste_F1_20261116.csv` | Os mesmos 125 registros, como alternativa ao XLSX; não é preciso preencher os dois |
| `reteste_F1_20261116_manifesto.json` | Fonte, semente 20261116, algoritmo e IDs, para reproduzir o sorteio |

A conferência não decide a inclusão final da revisão. Essa decisão fica na planilha `leitura_F2_para_preencher.xlsx`: em 13/11/2026, dos 357 candidatos, 79 tinham proposta registrada (71 I e 8 E), ainda não conferida, e 278 seguiam em aberto.
