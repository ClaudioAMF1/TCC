# TCC I: o texto

**Estado em 28/10/2026:** resumo, abstract, introdução, metodologia das etapas
executadas e plano de atividades escritos. Piloto concluído: κ de Fleiss 0,52
com os detectores como são e 0,69 depois da conferência manual; 72% das
detecções do detector B eram falso positivo.

| Arquivo | O que é |
|---|---|
| [`tcc1-projeto-de-pesquisa.md`](tcc1-projeto-de-pesquisa.md) | **O texto.** Identificação, resumo, abstract, Cap. 1 Introdução, Cap. 2 Metodologia do que foi feito, Cap. 3 Plano de atividades, referências |
| [`piloto-passo-a-passo.md`](piloto-passo-a-passo.md) | Como rodar o piloto do AndroZoo, comando por comando |

## O que mudou em relação à proposta

| Ponto | Proposta (16/09) | Texto atual | Por quê |
|---|---|---|---|
| Fonte dos APKs | AndroZoo | AndroZoo para os 92 apps de governo do acervo (23,2%); Google Play direta, com hash, para os outros 304 | Cobertura medida em 26/10. Ver Seção 2.10 |
| Detectores da H4 | MobSF, Androguard, Exodus | A (Exodus, código), B (Exodus, rede), C (Disconnect, rede); MobSF como verificação | O MobSF usa a base e a regra do Exodus; o Androguard só extrai. Ver Seção 2.9 |
| Medida principal | (não definida) | Detector A; C como verificação independente; B só para medir o efeito do método | No piloto, 72% das detecções de B foram falso positivo e B não vê o Firebase Analytics. **Decisão a levar ao orientador** |
| Menor diferença detectável | 5,1 p.p. | 6,0 a 12,3 p.p., conforme a taxa de base | O 5,1 usava taxa de base de 1% (a de anúncios) |
| Dado sensível | 152 apps | 152 pelo critério automático; a validação aplica o Art. 5º, II | Previdência e assistência social não são dado sensível por si |
| Suporte comum | 92,4% | 92,4% por faixa; 27,4% por categoria | Os dois números vão lado a lado; ampliar o controle está no plano |
| Escopo | Rastreadores **e** falhas de configuração de segurança | Só rastreadores | Nenhuma das hipóteses H1 a H4 mede postura de segurança: ela não tinha hipótese nem critério de decisão. Para voltar, precisa de hipótese própria |
| H3 | "não apresentam postura de proteção superior" | "não apresentam menos rastreadores" | "Postura de proteção" não tinha medida definida |
| Título | "...postura de segurança e soberania de dados..." | "...e soberania de dados..." | Segue o escopo |

**Essas três últimas mudanças são decisão sua e do orientador.** Se quiser
manter a postura de segurança, ela volta ao título, aos objetivos e ganha uma
hipótese.

## O que falta no texto

- Datas de acesso da LGPD e do Exodus nas referências (anotar o dia em que abrir cada link).
- Passar para o modelo ABNT da instituição antes de 03/12.
- **Língua.** O regulamento v.2026-05 (Art. 32, §3º) pede o trabalho final em
  inglês; o §4º aceita outra língua com anuência da Coordenação e endosso do
  orientador. Se a regra mudou para o TCC I, vale ter isso por escrito.
- **Uso de IA.** O Art. 19, X e o Art. 49 do regulamento tratam do uso indevido
  de inteligência artificial. Combine com o orientador como declarar o uso e
  reescreva o texto com as suas palavras antes da entrega.
