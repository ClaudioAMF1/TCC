# Recursos dos slides da defesa final

Usados por `../monta_slides_defesa_final.py`. Os fundos, as cores e a fonte são os do template de
slides do IDP (`disciplina/modelos/Template slides IDP.pptx`); esta pasta guarda só o que o
template não tem.

## figuras/

Figuras recortadas das versões de acesso aberto de artigos citados no TCC. Nos slides, cada uma
aparece com a fonte embaixo, para fins de estudo e crítica (Lei nº 9.610/1998, art. 46, III).
O recorte pega só a área da figura, sem a legenda, da página renderizada a 250 dpi com o `pdftoppm`.

| Arquivo | Origem |
|---|---|
| `kollnig2021_fig3.png` | Kollnig et al. (2021), "Before and after GDPR: tracking in mobile apps", Internet Policy Review, Fig. 3 (versão no arXiv: 2112.11117) |
| `kollnig2022_fig6.png` | Kollnig et al. (2022), "Are iPhones really better for privacy?", Proceedings on Privacy Enhancing Technologies, Fig. 6 (arXiv: 2109.13722) |
| `andow2020_fig1.png` | Andow et al. (2020), PoliCheck, 29th USENIX Security Symposium, Fig. 1 (acesso aberto na USENIX) |
| `zhan2022_fig5.png` | Zhan et al. (2022), "A systematic assessment on Android third-party library detection tools", IEEE Transactions on Software Engineering, Fig. 5 (arXiv: 2108.01964) |

O gráfico das empresas de rastreamento (slide de fundamentação teórica) não é figura recortada: é
um gráfico do PowerPoint refeito com os números da Tabela 1 de Binns et al. (2018). Os demais
gráficos usam os números do próprio TCC.

## icones/

Ícones do conjunto Lucide (licença ISC), nas cores do template: branco, azul-marinho (#003D69) e
azul-médio (#7499BF). A pasta guarda só os ícones que o script usa. Para gerar de novo:

```bash
npm install react@18.3.1 react-dom@18.3.1 react-icons@5.4.0 sharp@0.33.5
node gera_icones.js icones
```
