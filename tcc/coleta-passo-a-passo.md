# Ampliar o controle e coletar direto da Google Play: passo a passo

Dois scripts, nesta ordem. O primeiro não precisa de conta nem de token; o
segundo precisa de uma conta Google da pesquisa.

Antes de qualquer um, em todo terminal novo:

```bash
cd ~/Documents/TCC
git pull
source .venv/bin/activate
```

---

## Parte A. Ampliar o controle por categoria (1 a 2 h, quase tudo espera)

**Para quê:** hoje só 27,4% dos apps de governo têm um comercial da mesma
categoria na mesma amplitude de porte. O script procura comerciais exatamente
nas células categoria × faixa de instalações que faltam.

### A1. Testar e medir a falta (2 min)

```bash
python3 scripts/ampliar_controle.py --autoteste
python3 scripts/ampliar_controle.py --diagnostico
```

O diagnóstico não busca nada. Ele mostra a cobertura atual (deve dar perto dos
27,4% de setembro) e quantos comerciais faltam em cada categoria.

### A2. Buscar (1 a 2 h)

```bash
python3 scripts/ampliar_controle.py
```

Ele busca categoria por categoria e mostra quantos achou. Se a internet cair,
rode de novo: as fichas já lidas ficam guardadas e não são relidas.

No fim, mostra a cobertura antes e depois e grava
`dados/controle_ampliado_AAAAMMDD.json`. A partir daí, o piloto usa esse
controle sozinho.

### A3. Ver quantos dos novos estão no AndroZoo (1 min)

```bash
python3 scripts/piloto_androzoo.py cobertura --lista dados/androzoo/latest.csv.gz
```

**Me mande:** a saída do `--diagnostico`, o "RESULTADO" da busca e a nova
cobertura.

---

## Parte B. Coletar direto da Google Play (teste com 5 apps)

**Para quê:** o AndroZoo tem só 92 dos 396 apps de governo. O resto precisa vir
da loja, com o hash registrado. O teste mostra se a coleta funciona,
principalmente nos apps pequenos.

### B1. Criar uma conta Google para a pesquisa (10 min)

Crie um Gmail novo só para isso, no Brasil. **Não use a sua conta pessoal**: a
loja pode limitar contas que baixam muitos apps.

### B2. Instalar o apkeep (5 a 15 min)

O apkeep é a ferramenta de código aberto da EFF que baixa da loja.

```bash
brew install apkeep
```

Se aparecer "No available formula", instale pelo Rust:

```bash
brew install rust
cargo install apkeep
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

Confira:

```bash
apkeep --version
```

### B3. Gerar o token da conta (10 min, uma vez só)

1. No Chrome, abra `https://accounts.google.com/EmbeddedSetup`.
2. Abra as ferramentas do desenvolvedor (**Cmd + Option + I**) e vá na aba
   **Network**.
3. Entre com a conta da pesquisa. Se aparecer o termo de serviço, clique em
   **I agree** e espere uns segundos.
4. Na lista da aba Network, clique na **última** linha de `accounts.google.com`.
5. Vá em **Cookies** e copie o valor de `oauth_token` (começa com `oauth2_4/`).
6. No terminal, troque esse valor pelo token que vale daqui em diante:

```bash
apkeep -e 'conta.da.pesquisa@gmail.com' --oauth-token 'oauth2_4/COLE_AQUI'
```

Ele imprime o **token AAS**. Guarde no seu gerenciador de senhas. O
`oauth2_4/...` só serve uma vez; o AAS serve para sempre.

**O token não vai para o repositório nem para o chat.**

### B4. Rodar o teste (10 min)

```bash
python3 scripts/coleta_google_play.py autoteste
export GOOGLE_PLAY_EMAIL="conta.da.pesquisa@gmail.com"
read -s "GOOGLE_PLAY_AAS_TOKEN?Token AAS: " && export GOOGLE_PLAY_AAS_TOKEN
python3 scripts/coleta_google_play.py teste
```

Ele escolhe 5 apps de governo que não estão no AndroZoo, de faixas pequenas,
médias e grandes, e tenta baixar cada um. Para cada APK registra o SHA-256, a
versão e a data, e guarda o base em `dados/apks/`, junto com os do AndroZoo.

Se um app falhar com "indisponível para a conta ou a região", não é erro do
script: é um dado. Conta quantos apps de governo não dá para coletar assim.

### B5. Detectar os rastreadores nos APKs baixados (2 min)

```bash
python3 scripts/piloto_androzoo.py detectar --amostra dados/coleta_play_AAAAMMDD.csv
```

(troque `AAAAMMDD` pela data que aparecer no fim da etapa B4). O resultado vai
para um arquivo separado e não mexe no do piloto.

**Me mande:** a saída do B4 (o "RESULTADO") e do B5.

---

## Se der errado

| Mensagem | O que fazer |
|---|---|
| `Faltam as credenciais` | refazer os dois `export` do B4 no mesmo terminal |
| `falha de autenticação` em todos | o token AAS está errado: refazer o B3 |
| `Não achei o apkeep` | refazer o B2; ou passar o caminho: `--apkeep ~/.cargo/bin/apkeep` |
| `Não achei dados/n3_corpus_*.csv` | rodar da pasta do repositório, com `cd ~/Documents/TCC` |

**Não faça commit de nada de `dados/`.** APKs não podem ser redistribuídos; o
que se publica no fim é a lista de apps com o hash de cada um.
