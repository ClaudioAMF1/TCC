# Revisão sistemática: passo a passo das buscas e da triagem

O protocolo está em [`protocolo-revisao-sistematica.md`](protocolo-revisao-sistematica.md).
As strings que você vai colar estão nas Seções 4.2 a 4.4 dele.

Antes de tudo, em todo terminal novo:

```bash
cd ~/Projetos/TCC
git pull
source .venv/bin/activate
```

---

## Parte 1. Preparar (5 min)

```bash
mkdir -p dados/revisao/buscas
python3 scripts/revisao_triagem.py autoteste
```

Tem de terminar com `AUTOTESTE OK`.

**Acesso ao Scopus.** No Portal de Periódicos da CAPES
(`https://www.periodicos.capes.gov.br`), entre pelo **Acesso CAFe** com a conta
do IDP e procure a base **Scopus** na lista de bases. Se o IDP não aparecer na
lista do CAFe ou o Scopus não abrir, me avise antes de seguir: o protocolo tem
uma contingência (Seção 3).

---

## Parte 2. Rodar as buscas e exportar (1 h 30 a 2 h)

São 22 buscas. Para cada uma:

1. cole a string;
2. **anote o número de resultados que a base mostra**;
3. exporte;
4. renomeie e mova o arquivo para `dados/revisao/buscas/`.

O nome do arquivo segue sempre o padrão `<base>_<string>_<AAAAMMDD>`. O script
usa o nome para saber de onde veio cada registro; nome fora do padrão é
ignorado.

```bash
# exemplo, depois de exportar a S1 do Scopus em 05/11:
mv ~/Downloads/scopus.csv dados/revisao/buscas/scopus_S1_20261105.csv
```

### 2.1 Scopus: S1, S2, S3, S4a, S4b, S5a, S5b (7 buscas)

1. Abra a **busca avançada** (*Advanced document search*).
2. Cole a string da Seção 4.2 **e, logo depois dela, o filtro F**, na mesma
   caixa.
3. Clique em **Search** e anote o número de resultados.
4. Marque **All** (todos os resultados) e clique em **Export** > **CSV**.
5. Na janela de campos, marque **Citation information**, **Bibliographical
   information** e **Abstract & keywords**. Exporte.
6. Renomeie para `scopus_S1_AAAAMMDD.csv` (troque S1 pela string da vez) e mova.

### 2.2 ACM Digital Library: S1, S2, S3, S4a, S4b (5 buscas)

> **Não usada desde 06/11 (protocolo 1.1).** A exportação exige assinatura que o
> IDP não tem; os anais da ACM ficam cobertos pelo Scopus. Os passos ficam como
> registro.

1. Abra `https://dl.acm.org/search/advanced`.
2. No topo, escolha a coleção **The ACM Guide to Computing Literature**.
3. Abra a edição da consulta (**Edit Query**) e cole a string da Seção 4.3,
   com o `Abstract:(...)`.
4. Em **Publication Date**, escolha de 2015 a 2026. Pesquise e anote o número.
5. Ponha **50 resultados por página**, marque **Select All** e clique em
   **Export Citations** > **BibTeX** > **Download**.
6. Se houver mais de uma página, repita em cada uma e numere:
   `acm_S1_AAAAMMDD_p1.bib`, `acm_S1_AAAAMMDD_p2.bib`...

Se a ACM recusar a consulta, me mande a mensagem de erro.

### 2.3 IEEE Xplore: S1, S2, S3, S4a, S4b (5 buscas)

1. Abra `https://ieeexplore.ieee.org/search/advanced/command`
   (**Command Search**).
2. Cole a string da Seção 4.3 **sem** o `Abstract:(` do começo e o `)` do fim.
3. Pesquise. Na barra lateral, filtre **Year** de 2015 a 2026 e, em **Content
   Type**, deixe só **Conferences**, **Journals** e **Early Access Articles**.
   Anote o número.
4. Clique em **Export** > aba **Search Results** > **CSV** > **Download**.
5. Renomeie para `ieee_S1_AAAAMMDD.csv` e mova.

Se o IEEE disser que há termos ou curingas demais, me mande a mensagem: eu
divido a string em duas.

### 2.4 SOL e BDTD: SOL1 a SOL3, BDTD1 e BDTD2 (5 buscas)

- **SOL**: `https://sol.sbc.org.br`, caixa de busca do topo.
- **BDTD**: `https://bdtd.ibict.br`, busca avançada, campo **Todos os campos**.

Anote o número de resultados. Se a base oferecer **Exportar** (a BDTD costuma
oferecer), use **RIS** e salve como `bdtd_BDTD1_AAAAMMDD.ris`. Se não oferecer,
copie o modelo e preencha uma linha por resultado:

```bash
cp tcc/revisao/modelo-registro-manual.csv dados/revisao/buscas/sol_SOL1_AAAAMMDD.csv
```

As colunas são `titulo;autores;ano;veiculo;doi;url;resumo`. Copie **todos** os
resultados, não só os que parecem bons: a seleção acontece na planilha de
triagem, com o critério registrado. Se uma busca trouxer mais de 50, me avise
antes de copiar.

**Me mande:** a lista dos 22 números anotados (base, string, resultados).

---

## Parte 3. Juntar e conferir o controle (2 min)

```bash
python3 scripts/revisao_triagem.py juntar
python3 scripts/revisao_triagem.py controle
```

O `juntar` lê tudo o que está em `dados/revisao/buscas/`, tira as duplicatas e
grava `dados/revisao/triagem_AAAAMMDD.csv`. O `controle` diz quais dos 11
estudos do conjunto de controle vieram e por qual string.

Confira se o número de registros de cada arquivo bate com o que você anotou.
Se não bater, a exportação veio incompleta.

**Me mande:** a saída dos dois comandos. Se algum estudo de controle não veio,
eu vejo com você se a string falhou ou se a base não tem o artigo, e só depois
começa a triagem.

---

## Parte 4. Triagem por título e resumo, F1 (6/11 a 10/11)

Abra `dados/revisao/triagem_AAAAMMDD.csv` no Excel ou no Numbers. Para cada
linha, preencha:

| Coluna | O que pôr |
|---|---|
| `decisao_f1` | `I` inclui, `E` exclui, `T` talvez, `R` revisão da literatura |
| `criterio_f1` | Se `E`: o código do critério (EC1 a EC7), o primeiro que se aplica |
| `observacao` | Opcional: o porquê, em poucas palavras, quando não for óbvio |

Os critérios, em uma linha cada (o texto completo está na Seção 6 do
protocolo):

| Código | Exclui quando |
|---|---|
| EC1 | é duplicata ou versão anterior de outro registro |
| EC2 | não trata de aplicativo móvel (só web, só desktop) |
| EC3 | "rastreamento" é outra coisa: localização, olhar, objetos, saúde, atividade física |
| EC4 | usa bibliotecas de terceiros só para outro fim (malware, clones), sem medir rastreamento nem avaliar a detecção |
| EC5 | só mede opinião ou intenção de uso das pessoas, nada sobre os aplicativos |
| EC6 | é resumo, pôster, artigo de até 4 páginas, editorial ou preprint |
| EC7 | (só na F2) o texto completo não está disponível |

Regras práticas:

- **Na dúvida, `T`.** Excluir cedo é o erro que não se corrige depois.
- Não mexa nas colunas `id`, `doi` e `strings`.
- Salve sempre como CSV, no mesmo arquivo.
- Pode parar e continuar quando quiser. Se rodar o `juntar` de novo (por
  exemplo, depois de acrescentar uma busca), as decisões já marcadas são
  mantidas.

No fim da F1:

```bash
python3 scripts/revisao_triagem.py prisma
```

**Me mande:** a saída do `prisma`.

---

## Parte 5. Texto completo, F2 (10/11 a 13/11)

Para cada registro com `I` ou `T` na F1, abra o artigo (DOI, CAFe ou Google
Acadêmico) e preencha `decisao_f2` (`I` ou `E`) e `criterio_f2`. Se não achar
o texto, mande um e-mail ao autor; sem resposta em 7 dias, `E` com `EC7`.

Guarde os PDFs em `dados/revisao/pdf/`, com o `id` no nome (`R0042.pdf`). Eles
não vão para o repositório.

---

## Parte 6. Bola de neve, F3 (13/11 a 15/11)

Para cada incluído na F2:

- **para trás:** leia a lista de referências;
- **para a frente:** no Google Acadêmico, clique em **Citado por**.

Os candidatos novos vão para um arquivo à mão, no mesmo modelo, com a base
`bola`:

```bash
cp tcc/revisao/modelo-registro-manual.csv dados/revisao/buscas/bola_B1_AAAAMMDD.csv
```

Depois rode o `juntar` de novo: o que já estava na planilha é reconhecido
como duplicata, e o que é novo entra com id novo para passar pela F1 e pela F2.

---

## Parte 7. Conferências da triagem

**Reteste (16/11, uma semana depois da F1):**

```bash
python3 scripts/revisao_triagem.py amostra --nome reteste
```

Abra o arquivo `dados/revisao/conferencia_reteste_AAAAMMDD.csv`, que vem sem as
decisões antigas, e decida de novo cada linha na coluna `decisao`. Depois:

```bash
python3 scripts/revisao_triagem.py concordancia dados/revisao/conferencia_reteste_AAAAMMDD.csv
```

**Orientador (no 2º ou 3º encontro):**

```bash
python3 scripts/revisao_triagem.py amostra --nome orientador --n 20 --semente 7
```

Leve a planilha para ele decidir e rode o `concordancia` com ela.

O protocolo pede κ ≥ 0,6 nas duas. Abaixo disso, me mande as divergências que
o script lista.

---

## Se der errado

| Mensagem | O que fazer |
|---|---|
| `Nenhuma exportação em ...` | os arquivos não estão em `dados/revisao/buscas/`, ou estão com outra extensão |
| `Arquivos com nome fora do padrão (ignorados)` | renomeie para `<base>_<string>_<AAAAMMDD>` |
| número de registros não bate com o da base | exporte de novo; no Scopus, confira se marcou **All** |
| `Não achei dados/revisao/triagem_*.csv` | rode o `juntar` antes |

**Não faça commit de nada de `dados/`.** As exportações trazem resumos, que os
termos de uso das bases não permitem redistribuir. O que entra no repositório
no fim é a lista dos estudos incluídos, com as decisões.
