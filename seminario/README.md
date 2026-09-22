# Seminário — Análise de Artigo Científico

**29/09 ou 01/10/2026** · 15 minutos · individual · **4 dos 6 pontos da AV1**

**Artigo:** NGUYEN, T. T.; BACKES, M.; STOCK, B. *Freely Given Consent? Studying
Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps.*
ACM CCS 2022, p. 2369–2383. DOI [10.1145/3548606.3560564](https://doi.org/10.1145/3548606.3560564).

---

## Por onde começar

| Se você quer... | Abra |
|---|---|
| **A apresentação** | `apresentacao/seminario-analise-de-artigo.pptx` (e o `.pdf` de backup) |
| **O que falta fazer**, incluindo as correções pendentes no deck | `plano-de-execucao.md` |
| O que a professora pediu, ao pé da letra | `enunciado-da-atividade.md` |
| **Finalizar o deck com outro modelo** | `prompt-versao-final.md` — o prompt pronto e a lista de anexos |

## Pasta por pasta

```
seminario/
├── README.md                    este índice
├── enunciado-da-atividade.md    enunciado transcrito + o que exige e o que não exige
├── plano-de-execucao.md         estado, correções pendentes, ensaio, perguntas prováveis
├── prompt-versao-final.md       prompt para outro modelo aplicar as correções no deck
├── protocolo-de-busca.md        item 1 e item 2: busca, funil, finalistas, métricas
├── analise-da-estrutura.md      item 3: os sete blocos, com recortes do artigo
├── plano-do-seminario.md        estratégia: por que este artigo, recência × citações
├── roteiro-falado.md            o que dizer em cada parte
├── apresentacao/                o deck que vai ser apresentado
├── pesquisa/                    prints da busca e das métricas — ver pesquisa/README.md
└── material-fornecido/          PDFs da professora, sem alteração
```

| Item do enunciado | Registro | Evidência |
|---|---|---|
| **1** — seleção e relevância | `protocolo-de-busca.md` §2 e §3 | `pesquisa/0-acesso/` · `pesquisa/busca-1/` a `busca-3/` |
| **2** — h5, Qualis, CORE | `protocolo-de-busca.md` §4 | `pesquisa/metricas/` |
| **3** — estrutura | `analise-da-estrutura.md` | o próprio artigo |

## Os números, num lugar só

| | Valor | Fonte | Data |
|---|---|---|---|
| Funil da busca | **131 → 70 → 39 → 5 → 1** | Scopus via CAFe, prints 18, 20, 21, 23 | 21/09/2026 |
| Citações | **42** ACM · **52** Scopus · **99** Google Acadêmico | páginas de cada base | 17/09/2026 |
| h5 | **90** (mediana 146), posição 5 em *Computer Security & Cryptography* | Google Scholar Metrics | 17/09/2026 |
| Qualis | **A1** | CAPES, Qualis Eventos Computação 2017–2020, p. 9 | 22/09/2026 |
| CORE | **A\*** (ICORE2026; A\* em todas as edições desde 2008, exceto ERA2010) | portal.core.edu.au | 17/09/2026 |

## O que não está aqui, e por quê

**O PDF do artigo.** A página 1 diz *"Publication rights licensed to ACM"*: não é
licença aberta, então não vai para o repositório. Baixe pelo DOI acima — o acesso é
livre na ACM Digital Library.

**O gerador do deck anterior** (`scripts/gera_deck_seminario.js`) e o deck de 13
slides que ele produzia foram removidos em 22/09, quando a apresentação em
`apresentacao/` os substituiu. Estão no histórico do git, no commit `1fb039b`.
