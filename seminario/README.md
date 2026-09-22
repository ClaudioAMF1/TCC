# Seminário — Análise de Artigo Científico

**29/09 ou 01/10/2026** · 15 minutos · individual · **4 dos 6 pontos da AV1**

**Artigo:** NGUYEN, T. T.; BACKES, M.; STOCK, B. *Freely Given Consent? Studying
Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps.*
ACM CCS 2022, p. 2369–2383. DOI [10.1145/3548606.3560564](https://doi.org/10.1145/3548606.3560564).

**Estado: versão final da apresentação pronta.** Falta testar no aplicativo em que
vai apresentar e ensaiar. Ver `plano-de-execucao.md`.

---

## Por onde começar

| Se você quer... | Abra |
|---|---|
| **A apresentação** | [`apresentacao/seminario-analise-de-artigo.pptx`](apresentacao/seminario-analise-de-artigo.pptx), com notas do apresentador em todos os slides. O [`.pdf`](apresentacao/seminario-analise-de-artigo.pdf) é o backup |
| **O que falta fazer** e as perguntas prováveis | [`plano-de-execucao.md`](plano-de-execucao.md) |
| O que foi corrigido na versão final, com o antes e o depois | [`apresentacao/relatorio-de-revisao.pdf`](apresentacao/relatorio-de-revisao.pdf) |
| O que a professora pediu, ao pé da letra | [`enunciado-da-atividade.md`](enunciado-da-atividade.md) |

## Pasta por pasta

```
seminario/
├── README.md                   este índice
├── enunciado-da-atividade.md   enunciado transcrito, o que exige e o que não exige
├── plano-de-execucao.md        o que falta, ensaio cronometrado, perguntas prováveis
├── protocolo-de-busca.md       itens 1 e 2: busca, funil, finalistas, métricas
├── analise-da-estrutura.md     item 3: os sete blocos, com recortes do artigo
├── apresentacao/
│   ├── seminario-analise-de-artigo.pptx   versão final, 23 slides + 2 de apoio
│   ├── seminario-analise-de-artigo.pdf    a mesma, em PDF
│   └── relatorio-de-revisao.pdf           o que mudou na revisão final
├── pesquisa/                   prints da busca e das métricas, ver pesquisa/README.md
└── material-fornecido/         PDFs da professora, sem alteração
```

| Item do enunciado | Slides | Registro | Evidência |
|---|---|---|---|
| **1** — seleção e relevância | 2 e 3 (finalistas no 24) | [`protocolo-de-busca.md`](protocolo-de-busca.md) §2 e §3 | `pesquisa/0-acesso/`, `busca-1/` a `busca-3/`, `metricas/01` a `05` |
| **2** — h5, Qualis, CORE | 4 | [`protocolo-de-busca.md`](protocolo-de-busca.md) §4 | `pesquisa/metricas/06` a `11` |
| **3** — estrutura | 5 a 22 (discussão no 19) | [`analise-da-estrutura.md`](analise-da-estrutura.md) | o PDF do artigo, versão da ACM |

## Os números, num lugar só

| | Valor | Fonte | Data |
|---|---|---|---|
| Funil da busca | **131 → 70 → 39 → 5 → 1** | Scopus via CAFe, prints 18, 20, 21, 23 | 21/09/2026 |
| Citações | **42** ACM · **52** Scopus · **99** Google Acadêmico | página de cada base | 17/09/2026 |
| h5 | **90** (mediana 146), posição 5 em *Computer Security & Cryptography*, 3ª entre as conferências | Google Scholar Metrics | 17/09/2026 |
| Qualis | **A1** — Qualis **Eventos**, não Periódicos; ver `protocolo-de-busca.md` §4 | CAPES, Computação 2017–2020, p. 9 | 22/09/2026 |
| CORE | **A\*** (ICORE2026; A\* desde 2008, exceto ERA2010) | portal.core.edu.au | 17/09/2026 |
| SOUPS, a alternativa descartada | **A** no ICORE2026 (era B até o CORE2023) | portal.core.edu.au | 22/09/2026 |

## O que não está aqui, e por quê

**O PDF do artigo.** A página 1 diz *"Publication rights licensed to ACM"*: não é
licença aberta, então não vai para o repositório. Baixe pelo DOI acima, com acesso
livre na ACM Digital Library. **Use a versão da ACM**: a cópia dos autores no CISPA
difere pelo menos na segunda pergunta de pesquisa, e as páginas do deck seguem a ACM.

**Os rascunhos da preparação** (o deck anterior e o script que o gerava, o roteiro
escrito para ele, a estratégia de antes da busca e o prompt usado na revisão final)
foram removidos em 22/09, quando a versão final os substituiu. Estão no histórico do
git.
