# Instruções para a avaliação independente

Objetivo: comparar as classificações dos registros sem mostrar as decisões
anteriores ao segundo avaliador. Use os arquivos **cegos** de
`dados/segundo_avaliador/`: eles não têm colunas de sugestão, decisão ou
classificação automática.

**Ordem de trabalho:**

1. Conclua e salve as decisões antes de consultar respostas de outro avaliador.
2. Entregue ao segundo avaliador os arquivos cegos e os critérios abaixo.
3. Reúna as respostas em arquivos separados para calcular a concordância
   (κ de Cohen) e examinar as divergências.

**Amostras:** 150 artigos e 100 apps, sorteados com semente fixa. Os arquivos
completos contêm 1.249 artigos e 396 apps e podem ser usados quando houver
disponibilidade para uma avaliação integral.

| Arquivo | Instruções |
|---|---|
| `dados/segundo_avaliador/artigos_cego_amostra150.csv` | Triagem dos artigos |
| `dados/segundo_avaliador/apps_cego_amostra100.csv` | Classificação dos apps |
| `..._completo.csv` | Os mesmos critérios para a avaliação integral |

Os arquivos usam `;` como separador.

---

## 1. Triagem dos artigos

```
Você vai atuar como segundo avaliador independente na triagem de uma revisão
sistemática (Kitchenham e Charters, 2007). O arquivo CSV (separador ;)
contém registros de artigos: id, titulo, ano, veiculo, tipo, resumo e
palavras_chave. Para cada registro, decida se o artigo segue para a leitura do
texto completo, usando SÓ os critérios abaixo.

CONTEXTO DA PESQUISA
Trabalho de conclusão de curso que mede a presença de SDKs de rastreamento de
terceiros em aplicativos Android do governo brasileiro, compara com aplicativos
comerciais de mesma categoria e porte, confronta o que é detectado com o que a
política de privacidade declara, mede a concordância entre ferramentas de
detecção e discute a LGPD e a soberania de dados.

QUESTÕES DA REVISÃO
QR1. Como os estudos detectam SDKs de rastreamento e bibliotecas de terceiros em
apps Android, e como verificam a validade dessas detecções (verdade de
referência, conferência manual, concordância entre ferramentas)?
QR2. Que proporção de apps com rastreadores os estudos reportam, em que
populações, com que fonte de pacotes e contra que linha de base?
QR3. Como os estudos confrontam SDKs ou fluxos de dados detectados com a
política de privacidade ou com rótulos de privacidade da loja?
QR4. Que estudos examinam rastreamento por terceiros ou privacidade em apps
publicados por governos, inclusive os de COVID-19?
QR5. Que trabalhos tratam de rastreamento ou privacidade em apps no Brasil ou à
luz da LGPD, ou da transferência internacional de dados coletados por apps?

CRITÉRIO DE INCLUSÃO (IC1)
Estudo primário que mede, detecta ou analisa rastreamento por terceiros,
bibliotecas ou SDKs de terceiros, ou fluxos de dados pessoais para terceiros em
aplicativos móveis (QR1 a QR4); ou trabalho que analisa a LGPD ou a
transferência internacional de dados aplicada a aplicativos ou serviços digitais
(QR5). Também entram ferramentas de detecção de bibliotecas de terceiros
avaliadas com números (precisão, revocação).

CÓDIGOS DE EXCLUSÃO (use o mais específico; IC1 só quando nenhum outro serve)
IC1 = fora do tema das questões
EC1 = repetido ou versão anterior de outro registro do arquivo
EC2 = não trata de aplicativo móvel (só site, só computador, aparelho sem app)
EC3 = "rastreamento" em outro sentido: localização, olhar, objetos, saúde ou
      atividade física, rastreamento de contatos sem analisar apps reais
EC4 = usa bibliotecas de terceiros só para outro fim (malware, clones,
      atualização, recomendação), sem medir rastreamento nem avaliar a detecção
EC5 = mede só opinião ou intenção de uso das pessoas, nada sobre os apps
EC6 = resumo, pôster, demonstração, editorial ou preprint

DECISÕES
I = inclui
E = exclui (com o código)
T = talvez; na dúvida entre I e E, use T
R = revisão da literatura relevante para as questões (não é estudo primário)

REGRAS
- Decida só pelo título, resumo e palavras-chave do arquivo. Não pesquise na
  internet e não use o que você sabe sobre o artigo fora do arquivo.
- Leia cada registro. Não decida por busca de palavras nem escrevendo código.
- Trabalhe na ordem do arquivo, em lotes de 25 registros.
- Responda SÓ com linhas CSV, sem comentários antes ou depois, neste formato
  (cabeçalho só na primeira resposta):
  id;decisao;criterio;motivo
- "criterio" fica vazio quando a decisão não é E. "motivo" tem no máximo 12
  palavras e nenhum ponto e vírgula.
```

---

## 2. Classificação dos apps

```
Você vai atuar como segundo avaliador independente na classificação de
aplicativos Android candidatos a "aplicativo de governo brasileiro". O
arquivo CSV (separador ;) contém: appId, titulo, publicador_na_loja,
nome_juridico (o nome que a Google Play mostra em "Sobre o desenvolvedor"),
email, site, situacao e descricao (texto da ficha na Google Play). Para cada
app, decida três coisas, usando SÓ os critérios abaixo.

1. OFICIAL (S, N ou ?)
S quando quem publica é órgão ou entidade pública: administração direta,
autarquias, fundações, tribunais, polícias, empresas públicas ou de economia
mista de tecnologia do governo (por exemplo Celepar, Prodesp, Prodam, Procempa,
Serpro, PRODERJ, CIASC) e conselhos profissionais.
N quando o nome jurídico é de empresa privada (Ltda, S/S, ME...) ou de pessoa
física, mesmo que o app tenha nome de prefeitura ou de serviço público.
? quando os dados não permitem decidir.
O critério é QUEM PUBLICA (nome jurídico), não o nome do app nem o e-mail.

2. ESFERA (federal, estadual, municipal ou -)
A esfera do órgão responsável pelo serviço. O Distrito Federal conta como
estadual. Tribunais superiores, Justiça Federal, do Trabalho e Eleitoral são
federais; Tribunais de Justiça são estaduais. Se um serviço de prefeitura é
publicado na conta de empresa estadual ou federal, a esfera é municipal. Para
apps com OFICIAL = N, use "-".

3. SENSÍVEL (sim, não ou -)
"sim" quando o app trata dado de saúde ou biométrico DO USUÁRIO (Art. 5º, II da
LGPD): agendamento de consulta ou exame (inclusive exame médico ou psicológico
do Detran), resultado de exame, laudo, atestado, prontuário, vacina, perícia,
plano de saúde, deficiência, reconhecimento facial, prova de vida por selfie,
impressão digital. Não basta a palavra "saúde" no texto. O login por biometria
do próprio celular NÃO conta, porque o dado não sai do aparelho. Para apps com
OFICIAL = N, use "-".

REGRAS
- Decida só pelos dados do arquivo. Não pesquise na internet.
- Leia cada linha. Não decida por busca de palavras nem escrevendo código.
- Trabalhe na ordem do arquivo, em lotes de 25 apps.
- Responda SÓ com linhas CSV, sem comentários antes ou depois, neste formato
  (cabeçalho só na primeira resposta):
  appId;oficial;esfera;sensivel;certeza;motivo
- "certeza" é alta ou baixa. "motivo" tem no máximo 15 palavras, cita a
  evidência (ex.: "agenda exame médico", "nome jurídico é Ltda") e não tem ponto
  e vírgula.
```

---

## Depois

Junte as respostas de cada etapa num arquivo só, com o cabeçalho uma vez:

- `dados/segundo_avaliador/resposta_artigos_<identificador-do-avaliador>.csv`
- `dados/segundo_avaliador/resposta_apps_<identificador-do-avaliador>.csv`

**A sua parte** são as planilhas cegas, com as mesmas amostras e nenhuma
sugestão: `dados/segundo_avaliador/cega_artigos150_claudio.xlsx` e
`cega_apps100_claudio.xlsx`. Preencha as colunas em maiúsculas (SUA DECISÃO e
SEU CRITÉRIO; SEU OFICIAL, SUA ESFERA e SEU SENSÍVEL), salve com o mesmo nome e
faça `git add`, `commit` e `push`. Depois rode:

```bash
python3 scripts/segundo_avaliador.py comparar
```

O script dá, para artigos e apps:

- a concordância entre o autor e cada segundo avaliador (κ de Cohen), em cada coluna;
- a concordância com a classificação preliminar, para comparar;
- o κ de Fleiss entre as classificações disponíveis;
- a lista das divergências, em `divergencias_artigos.csv` e
  `divergencias_apps.csv`, para você olhar caso a caso.

Enquanto as suas planilhas estiverem em branco, o script não mostra nada, para
não influenciar as suas decisões. Os 5 apps da amostra que você já validou em
04/11 ficam fora da comparação com a classificação preliminar: nesses, a sugestão é a
sua própria validação.

**No texto do TCC**, reporte o procedimento, o tamanho da amostra, a
concordância e as divergências. Essa comparação complementa o reteste e a
conferência do orientador previstos no protocolo (Seção 7.2).
