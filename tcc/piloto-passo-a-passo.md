# Piloto do AndroZoo: passo a passo

O piloto não rodou no ambiente onde o texto foi escrito: lá não há acesso ao
`androzoo.uni.lu` nem à API do Exodus. Ele roda no seu computador, com os
arquivos de `dados/` que já estão aí (a pasta não vai para o GitHub).

Tempo total: umas 2 horas, a maior parte esperando download.

---

## 0. Antes de começar

Confira se estes dois arquivos existem no seu computador:

```
dados/n3_corpus_20260917.csv
dados/n3_relatorio_20260917.json
```

São a saída do teste de 17/09. Se não existirem, rode antes
`python3 scripts/teste_viabilidade_n3_robusto.py` (leva horas e gera arquivos
com a data do dia; os números do texto passam a ser os da nova rodada).

Você precisa de Python 3.9 ou mais novo (`python3 --version`).

## 1. Preparar o ambiente (5 min)

```bash
cd TCC
git pull
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/piloto_androzoo.py autoteste
```

**Todo terminal novo precisa ativar o ambiente de novo**, antes de qualquer
etapa: `cd ~/Documents/TCC && source .venv/bin/activate`. O prompt passa a
mostrar `py TCC`. Sem isso aparece "Falta o Androguard" ou "command not found:
pip". O Androguard é pacote do Python: não existe no Homebrew.

Tem que aparecer `AUTOTESTE OK`. Se aparecer `AUTOTESTE FALHOU`, pare e me
mande a saída.

## 2. Baixar a lista do AndroZoo (30 a 60 min)

A lista é pública e tem alguns gigabytes. O `-C -` deixa retomar se cair.

```bash
mkdir -p dados/androzoo
curl -C - -o dados/androzoo/latest.csv.gz https://androzoo.uni.lu/static/lists/latest.csv.gz
```

Se der 404, o endereço da lista mudou: veja o atual em `androzoo.uni.lu/lists`.

## 3. Cobertura (10 a 20 min)

```bash
python3 scripts/piloto_androzoo.py cobertura --lista dados/androzoo/latest.csv.gz
```

**Anote o que ele imprime:** quantos dos 396 estão no AndroZoo, por esfera,
quantos do controle, e a defasagem em dias. É número para o texto e para o
orientador.

## 4. Sortear a amostra (1 min)

```bash
python3 scripts/piloto_androzoo.py amostra
```

Sorteia 14 apps de governo (espalhados por esfera e dado sensível) e 6 do
controle (3 com anúncio, 3 sem). A semente é fixa: rodar de novo dá a mesma
amostra.

## 5. Baixar os 20 APKs (10 a 30 min)

A chave só entra no terminal, nunca em arquivo. Este comando pede a chave sem
mostrar na tela e sem gravar no histórico:

```bash
# zsh (padrão do Mac)
read -s "ANDROZOO_API_KEY?Chave do AndroZoo: " && export ANDROZOO_API_KEY

# bash (Linux)
read -s -p "Chave do AndroZoo: " ANDROZOO_API_KEY && export ANDROZOO_API_KEY
```

Depois:

```bash
python3 scripts/piloto_androzoo.py baixar
```

Cada APK tem o SHA-256 conferido depois do download. Se der `HTTP 403`, a
chave está errada; se der `hash não confere`, rode de novo.

## 6. Detectar (5 min)

```bash
python3 scripts/piloto_androzoo.py detectar
```

Baixa as bases do Exodus e da Disconnect para `dados/bases/` (com a data, para
o registro) e roda os detectores A, B e C em cada APK.

## 7. MobSF, opcional (30 min)

Só se quiser o MobSF como quarto detector. Precisa do Docker. A chave do MobSF
é uma senha que você inventa agora; não tem nada a ver com a do AndroZoo.

```bash
export MOBSF_API_KEY="invente-uma-senha-local"
docker run -d --name mobsf -p 8000:8000 -e MOBSF_API_KEY \
  opensecurity/mobile-security-framework-mobsf:latest

mkdir -p dados/mobsf
for apk in dados/apks/*.apk; do
  sha=$(basename "$apk" .apk)
  md5=$(curl -s -F "file=@$apk" http://localhost:8000/api/v1/upload \
        -H "X-Mobsf-Api-Key: $MOBSF_API_KEY" | python3 -c "import sys,json; print(json.load(sys.stdin)['hash'])")
  curl -s -X POST http://localhost:8000/api/v1/scan --data "hash=$md5" \
       -H "X-Mobsf-Api-Key: $MOBSF_API_KEY" > /dev/null
  curl -s -X POST http://localhost:8000/api/v1/report_json --data "hash=$md5" \
       -H "X-Mobsf-Api-Key: $MOBSF_API_KEY" > "dados/mobsf/$sha.json"
  echo "ok $sha"
done

python3 scripts/piloto_androzoo.py detectar --mobsf dados/mobsf
docker stop mobsf && docker rm mobsf
```

A espera do Docker na primeira vez é longa (a imagem tem alguns GB).

## 8. Concordância (1 min)

```bash
python3 scripts/piloto_androzoo.py concordancia
```

Imprime, por detector, quantos apps têm ao menos um rastreador, o κ de Fleiss
e, por par de detectores, o τ de Kendall e as concordâncias positiva e
negativa.

## 9. Conferir as detecções à mão (1 a 2 h)

Sem esta etapa o κ não quer dizer nada. No piloto de 28/10 o κ deu 0,52, mas
três apps tiveram uma única detecção, só do detector B. Se essas três forem
falso positivo, o κ vai a 0,90.

```bash
python3 scripts/piloto_androzoo.py evidencias
```

Ele lista, app por app, cada detecção com o que a produziu (a classe, no
detector A; o domínio, em B e C) e grava `dados/piloto_conferencia_AAAAMMDD.csv`.
Domínios com cara de link de página já vêm com o aviso `⚠ link de uso geral?`.

Abra a planilha no Excel ou no Numbers e preencha a coluna `FALSO_POSITIVO_S_N`:

| Marque | Quando | Exemplos |
|---|---|---|
| **S** | o domínio é link para página, não endereço de SDK | `maps.google.com`, `www.facebook.com`, `play.google.com`, `www.google.com` |
| **N** | o domínio é endereço que o SDK chama | `app-measurement.com`, `graph.facebook.com`, `*.googleapis.com`, `*.doubleclick.net`, `*.crashlytics.com` |
| **N** | a classe é do próprio SDK (detector A: quase sempre é) | `com/google/firebase/analytics/...`, `com/facebook/appevents/...` |

Na dúvida, deixe em branco e me mande a linha. Pode salvar no formato que o
programa quiser (vírgula ou ponto e vírgula): o script lê os dois.

Depois:

```bash
python3 scripts/piloto_androzoo.py concordancia --conferencia
```

Ele mostra o κ e os pares de novo, já sem os falsos positivos, e o κ de antes
para comparar.

## 10. O que me mandar

- a saída da etapa `evidencias` (se quiser, eu indico quais parecem falso
  positivo antes de você marcar);
- depois da marcação, a saída de `concordancia --conferencia`.

Com isso eu atualizo a Seção 2.10 do texto.

**Não faça commit de nada de `dados/`.** APK, lista e bases ficam só no seu
computador.

---

## Alternativa: rodar aqui

Dá para eu rodar no ambiente da nuvem se três coisas forem feitas:

1. liberar os domínios `androzoo.uni.lu` e `reports.exodus-privacy.eu.org` nas
   configurações de rede do ambiente;
2. cadastrar a chave como segredo do ambiente, com o nome `ANDROZOO_API_KEY`
   (nunca colar a chave no chat);
3. subir para cá os dois arquivos da etapa 0, que hoje só existem no seu
   computador.

A forma mais simples continua sendo rodar aí.
