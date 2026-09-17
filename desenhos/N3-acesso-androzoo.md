# Solicitação de acesso ao AndroZoo

**Por que importa:** o AndroZoo é a fonte primária de APKs do desenho N3. Ele permite
**fixar a versão analisada por hash**, que é o que torna o estudo reprodutível — a loja
substitui o APK sem aviso, e um corpus coletado direto dela não pode ser reconstruído por
terceiros. É também o gargalo de prazo: a concessão leva dias ou semanas.

**Estado:** ✅ **concedido em 17/09/2026**, menos de seis horas após o envio.
Resposta de Marco Alecci (Universidade de Luxemburgo).

---

## 0. Obrigações que vieram junto da concessão

**A chave é de uso individual.** O e-mail de concessão é explícito: colegas,
alunos e orientadores que queiram acesso precisam **cada um enviar seu próprio
pedido**, do respectivo e-mail institucional. Compartilhar a chave viola a
condição de uso. Se o orientador quiser acesso, ele pede a dele.

**A chave nunca entra no repositório.** Só variável de ambiente:

```bash
export ANDROZOO_API_KEY="..."
```

O `.gitignore` já cobre `.env`, `*.key`, `secrets*` e `dados/`.

**Citação obrigatória.** O uso do acervo exige citar dois trabalhos, indicados na
concessão:

| Referência | DOI |
|---|---|
| Allix, Bissyandé, Klein & Le Traon. *AndroZoo: Collecting Millions of Android Apps for the Research Community.* MSR 2016. | `10.1145/2901739.2903508` |
| Trabalho sobre os **metadados** do acervo — exigido porque este TCC usa metadados, não só binários. Confirmar título e autores em `dl.acm.org/doi/10.1145/3643991.3644863` antes de citar. | `10.1145/3643991.3644863` |

> O segundo está registrado aqui pelo DOI de propósito: a referência completa
> precisa ser conferida na fonte, não reconstruída de memória.

**Documentação da API:** `androzoo.uni.lu/api_doc`

---

## 1. O requisito que trava tudo

O formulário pede **"Your Institutional Email Address"**. O domínio do e‑mail é como o
AndroZoo verifica o vínculo com instituição de pesquisa. Enviar de endereço pessoal
(`@gmail.com`) tende a não ser processado.

**Antes de enviar:** ativar e usar o e‑mail institucional do IDP. Se não houver um ativo,
resolver isso é o passo zero.

**Reforço que não custa nada:** pedir ao orientador que apareça na solicitação — como
remetente em cópia, ou nomeado no corpo. Uma solicitação de aluno com orientador
identificado é substancialmente mais forte que uma solicitação isolada, porque o que o
AndroZoo concede é acesso a uma coleção que inclui malware.

---

## 2. Texto da solicitação

**Para:** androzoo@uni.lu
**Cc:** orientador (institucional)
**Assunto:** AndroZoo access request — undergraduate research, IDP (Brazil)

```
{
  "name": "Claudio Meireles",
  "institution": "Instituto Brasiliense de Direito Público (IDP), Brazil",
  "email": "<SEU E-MAIL INSTITUCIONAL DO IDP>"
}
```

Dear AndroZoo team,

I am an undergraduate Computer Science student at Instituto Brasiliense de
Direito Público (IDP), Brasília, Brazil, currently developing my final-year
thesis under the supervision of Prof. Eduardo Arthur Izycki.

My study measures the prevalence of third-party tracking SDKs and security
misconfigurations in Brazilian government mobile applications, comparing them
against a control group of commercial applications matched by store category
and install tier. I have already assembled a candidate corpus of 396
applications from 71 distinct public-sector publishers, covering the federal,
state and municipal levels.

I am requesting access to AndroZoo because it allows the analysed APK version to
be pinned by hash, which makes the corpus reconstructible by other researchers.
Collecting directly from the store would not, since published APKs are replaced
without notice.

Analysis will be static (MobSF, Androguard, Exodus signature set), with a
dynamic subsample run on my own device and my own accounts. No third-party
personal data is collected, and findings attributable to a specific public body
will be disclosed to that institution before publication.

I am happy to provide any further information you may need.

Kind regards,
Claudio Meireles
Computer Science — Instituto Brasiliense de Direito Público (IDP)
<e-mail institucional>

---

## 3. Notas sobre o texto

- **O bloco JSON vem primeiro e literal.** A página avisa que solicitação sem o template
  pode não ser processada. Não reformatar, não traduzir as chaves.
- **O número do corpus está no corpo de propósito.** 396 aplicativos de 71 publicadores
  mostra que existe trabalho real por trás do pedido, não curiosidade.
- **A justificativa é técnica, não conveniência.** O argumento é reprodutibilidade por
  hash — que é exatamente a razão pela qual o AndroZoo existe. Dizer "seria mais fácil"
  seria um pedido pior.
- **O parágrafo de ética é deliberado.** O AndroZoo concede acesso a uma coleção que
  inclui malware; deixar claro que o uso é análise estática de artefatos públicos, sem
  coleta de dado pessoal de terceiros, remove uma objeção antes que ela apareça.

---

## 4. Plano B — não é mais necessário

Mantido como registro do raciocínio. O acesso saiu, então a limitação abaixo
**não** entra na monografia: o corpus é fixável por hash e reconstruível por
terceiros, como o desenho previa.

O desenho **não morre** sem AndroZoo — fica mais frágil em um ponto específico, e o texto
precisa dizer qual.

| Fonte alternativa | Custo |
|---|---|
| Coleta direta da Play Store, com SHA‑256 de cada APK registrado no repositório de dados | Perde a reconstrutibilidade por terceiros: quem quiser repetir o estudo não consegue obter a **mesma versão**, só a versão vigente. Vira ameaça à validade a ser declarada. |
| Espelhos públicos de APK | Procedência não verificável. Só serve com o hash conferido contra a coleta própria — ou seja, não substitui nada. |

Se cair no plano B, o congelamento do corpus por data e hash deixa de ser boa prática e
passa a ser **obrigatório**, e a limitação entra explicitamente na seção de ameaças à
validade da monografia.

---

## 5. Próximo passo

Com o acesso em mãos, o gargalo de prazo do Capstone I deixou de existir. O que
vem agora é o **piloto de 20 aplicativos** (entrega 6 da Seção 9 da proposta):
baixar por hash, passar pelos três detectores e produzir os números preliminares
de concordância.
