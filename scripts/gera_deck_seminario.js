const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";           // 10" x 5.625"
pres.author = "Claudio Meireles";
pres.title  = "Seminario - Analise de Artigo Cientifico";

// Paleta: azul-marinho dominante, teal de apoio, âmbar SÓ para o que falta preencher.
const NAVY = "1B2A4A", TEAL = "2E86A8", AMBER = "C8860D", AMBER_BG = "FDF4E0";
const LIGHT = "F4F6F9", GRAY = "5A6472", WHITE = "FFFFFF";
const SERIF = "Cambria", SANS = "Calibri";

const W = 10, M = 0.55;                 // largura e margem

// ---------- helpers ----------
function tituloSlide(s, texto, num) {
  s.addText(String(num).padStart(2, "0"), {
    x: M, y: 0.32, w: 0.5, h: 0.4, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 15, bold: true, color: TEAL, align: "left",
  });
  s.addText(texto, {
    x: M + 0.52, y: 0.28, w: W - M * 2 - 0.52, h: 0.5, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 25, bold: true, color: NAVY, align: "left",
  });
}

// Bloco âmbar = "você preenche isto"
function preencher(s, x, y, w, h, titulo, itens) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, fill: { color: AMBER_BG }, line: { color: AMBER, width: 1, dashType: "dash" },
    rectRadius: 0.06,
  });
  s.addText("A PREENCHER  ·  " + titulo, {
    x: x + 0.18, y: y + 0.12, w: w - 0.36, h: 0.26, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: AMBER, charSpacing: 1,
  });
  s.addText(itens.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < itens.length - 1 },
  })), {
    x: x + 0.18, y: y + 0.42, w: w - 0.36, h: h - 0.56, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 11.5, color: GRAY, paraSpaceAfter: 5, valign: "top",
  });
}

// Cartão de conteúdo já pronto
function cartao(s, x, y, w, h, cabecalho, corpo, corCabecalho) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, fill: { color: LIGHT }, line: { color: "DDE3EA", width: 1 }, rectRadius: 0.06,
  });
  s.addText(cabecalho, {
    x: x + 0.2, y: y + 0.14, w: w - 0.4, h: 0.3, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, color: corCabecalho || NAVY,
  });
  s.addText(corpo, {
    x: x + 0.2, y: y + 0.48, w: w - 0.4, h: h - 0.64, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 11.5, color: GRAY, valign: "top", paraSpaceAfter: 4,
  });
}

function rodape(s, texto) {
  s.addText(texto, {
    x: M, y: 5.16, w: W - M * 2, h: 0.26, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 9.5, color: "98A2B3", align: "left",
  });
}

// =====================================================================
// 1 — CAPA
// =====================================================================
let s = pres.addSlide();
s.background = { color: NAVY };
s.addText("Análise de Artigo Científico", {
  x: M, y: 1.75, w: W - M * 2, h: 0.75, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 40, bold: true, color: WHITE,
});
s.addText("Segurança e privacidade em aplicativos móveis", {
  x: M, y: 2.52, w: W - M * 2, h: 0.4, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 17, color: "9FC5DA",
});
s.addShape(pres.ShapeType.rect, { x: M, y: 3.15, w: 0.85, h: 0.035, fill: { color: TEAL } });
s.addText([
  { text: "Claudio Meireles", options: { breakLine: true, bold: true } },
  { text: "Projeto Capstone I  ·  Ciência da Computação  ·  IDP", options: { breakLine: true } },
  { text: "Profa. Ma. Patrícia da Silva Oliveira  ·  setembro de 2026", options: {} },
], {
  x: M, y: 3.45, w: W - M * 2, h: 1.0, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 12.5, color: "CFE0EA", paraSpaceAfter: 3,
});
s.addNotes("Confirme seu nome completo e a data da sua apresentação (29/09 ou 01/10).");

// =====================================================================
// 2 — CONTEXTO
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Onde este artigo se encaixa", 1);
s.addText("Área do TCC", {
  x: M, y: 1.05, w: 4.2, h: 0.3, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11, bold: true, color: TEAL, charSpacing: 1,
});
s.addText("Cibersegurança, na vertente de medição", {
  x: M, y: 1.38, w: 4.2, h: 0.5, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 21, bold: true, color: NAVY,
});
s.addText(
  "Não a vertente ofensiva, mas a de medir: coletar, caracterizar e comparar evidência " +
  "sobre sistemas reais.", {
  x: M, y: 1.95, w: 4.2, h: 0.8, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 12, color: GRAY, valign: "top",
});
cartao(s, 5.05, 1.05, W - M - 5.05, 1.75, "Tema do TCC",
  "Rastreamento por terceiros e soberania de dados em aplicativos móveis " +
  "governamentais brasileiros.\n\nQuando o cidadão usa o Meu SUS ou o Meu INSS, " +
  "quais empresas além do governo recebem dados dele?", NAVY);
const cq = (W - M * 2 - 0.6) / 4;
cartao(s, M, 3.05, cq, 1.55, "Corpus",
  "396 aplicativos\n71 publicadores públicos\ntrês esferas", TEAL);
cartao(s, M + cq + 0.2, 3.05, cq, 1.55, "Dado sensível, Art. 11",
  "152 aplicativos\nsaúde 125 · previdência 28\nbiometria 17", TEAL);
cartao(s, M + (cq + 0.2) * 2, 3.05, cq, 1.55, "Instrumento",
  "81,6% das políticas\nacessíveis\n\npotência: 5,1 p.p.", TEAL);
cartao(s, M + (cq + 0.2) * 3, 3.05, cq, 1.55, "Fonte de APKs",
  "AndroZoo\nacesso concedido\n17/09/2026", "1E6B3A");
s.addNotes("Abra dizendo que o tema está em definição mas que a escolha do artigo não depende disso — o que se reaproveita é o método.");

// =====================================================================
// 3 — COMO CHEGUEI AQUI (preenchido)
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Como cheguei a este recorte", 2);
s.addText("Testei quatro temas antes de escolher. Três não sobreviveram aos dados.", {
  x: M, y: 1.0, w: W - M * 2, h: 0.32, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 13, color: GRAY,
});
const col = (W - M * 2 - 0.6) / 4;
cartao(s, M, 1.45, col, 2.55, "Infraestrutura industrial",
  "Queria medir equipamento de indústria exposto na internet.\n\n" +
  "Os endereços que achei respondiam a três protocolos ao mesmo tempo. " +
  "Equipamento de verdade não faz isso: eram armadilhas e servidores de nuvem.", "9B2C2C");
cartao(s, M + col + 0.2, 1.45, col, 2.55, "Sites que imitam bancos",
  "Procurei endereços falsos em 20 mil registros de certificado digital.\n\n" +
  "Não achei nenhum. Golpe hoje quase nunca põe o nome do banco no endereço do site.", "9B2C2C");
cartao(s, M + (col + 0.2) * 2, 1.45, col, 2.55, "Vírus de banco brasileiro",
  "Quis medir o parentesco entre famílias de vírus.\n\n" +
  "Descobri que o repositório identifica a campanha do golpe, não o programa. " +
  "Eu estava medindo a coisa errada. Registrei o erro.", "8A6D1F");
cartao(s, M + (col + 0.2) * 3, 1.45, col, 2.55, "Apps de governo   ✓",
  "396 aplicativos de 71 órgãos públicos, nas três esferas.\n\n" +
  "A loja diz quem publicou cada um. Não preciso descobrir de quem é o app, " +
  "que foi justamente o que faltou nos outros três.", "1E6B3A");
s.addText("Descartar com evidência faz parte do método. É o que as aulas 04 e 07 chamam de maturidade em pesquisa.", {
  x: M, y: 4.2, w: W - M * 2, h: 0.4, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, italic: true, color: TEAL,
});
s.addNotes("1 minuto. Trinta segundos no maximo por tema. O objetivo e mostrar que a escolha foi testada, nao contar a historia inteira. Se alguem perguntar detalhe de algum deles, o registro completo esta no repositorio.");

// =====================================================================
// 4 — PASSO A PASSO DA SELEÇÃO
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Como cheguei até este artigo", 3);
s.addText("Scopus, pelo portal da CAPES via CAFe, em 21 de setembro de 2026.", {
  x: M, y: 0.98, w: W - M * 2, h: 0.28, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 12.5, color: GRAY,
});
s.addImage({
  path: "/home/user/TCC/seminario/pesquisa/busca-scopus-resultados.jpg",
  x: M, y: 1.32, w: 5.55, h: 3.21,
});
s.addText("Duas buscas, no campo título, resumo e palavras-chave:", {
  x: 5.85, y: 1.32, w: W - M - 5.85, h: 0.26, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 10.5, bold: true, color: NAVY,
});
s.addText([
  { text: '1.  "third-party tracking" AND consent AND android', options: { breakLine: true } },
  { text: "     4 resultados", options: { breakLine: true, bold: true, color: TEAL } },
  { text: "", options: { breakLine: true } },
  { text: '2.  "third party" AND tracking AND android AND', options: { breakLine: true } },
  { text: "     (consent OR GDPR)", options: { breakLine: true } },
  { text: "     12 resultados", options: { breakLine: true, bold: true, color: TEAL } },
], {
  x: 5.85, y: 1.64, w: W - M - 5.85, h: 1.15, isTextBox: true, margin: 0,
  fontFace: "Consolas", fontSize: 9, color: NAVY, valign: "top",
});
s.addTable(
  [[{ text: "Candidato", options: { bold: true } }, { text: "Ano", options: { bold: true } },
    { text: "Cit.", options: { bold: true } }, { text: "", options: { bold: true } }]].concat([
    ["WhisperTest", "2025", "0", "é iOS"],
    ["Third-Party User Tracking", "2023", "10", "menos citado"],
    ["Freely Given Consent?", "2022", "52", "escolhido"],
    ["A fait accompli?", "2021", "34", "veículo menor"],
  ].map((r, i) => r.map((c) => ({
    text: c, options: { bold: i === 2, color: i === 2 ? "1E6B3A" : NAVY },
  })))),
  {
    x: 5.85, y: 2.95, w: W - M - 5.85, colW: [1.75, 0.42, 0.42, 1.0],
    fontFace: SANS, fontSize: 9, border: { type: "solid", color: "D8DEE6", pt: 0.5 },
    fill: { color: "FFFFFF" }, rowH: 0.24, valign: "middle",
  }
);
s.addText("A busca também encontrou a alternativa que eu considerei e descartei.", {
  x: 5.85, y: 4.32, w: W - M - 5.85, h: 0.3, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 9.5, italic: true, color: TEAL, valign: "top",
});
s.addNotes("A busca encontrou o Kollnig et al. SOUPS 2021, que e a alternativa mais seria. Se perguntarem se voce avaliou outras opcoes, a resposta esta no proprio print: 34 citacoes contra 52, um ano mais velho, e SOUPS e CORE B contra A* do CCS.");

// =====================================================================
// 5 — O ARTIGO
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "O artigo selecionado", 4);
s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 1.05, w: W - M * 2, h: 1.55, fill: { color: NAVY }, rectRadius: 0.06,
});
s.addText("Freely Given Consent? Studying Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps", {
  x: M + 0.25, y: 1.22, w: W - M * 2 - 0.5, h: 0.62, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 16.5, bold: true, color: WHITE,
});
s.addText(
  "NGUYEN, Trung Tin; BACKES, Michael; STOCK, Ben.   In: CCS '22, Proceedings of the 2022 ACM " +
  "SIGSAC Conference on Computer and Communications Security. Los Angeles, 7–11 nov. 2022, " +
  "p. 2369–2383.   DOI: 10.1145/3548606.3560564\n" +
  "RESEARCH-ARTICLE  ·  FREE ACCESS  ·  15 páginas  ·  artefato: github.com/cispa/gdpr-consent", {
  x: M + 0.25, y: 1.9, w: W - M * 2 - 0.5, h: 0.6, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, color: "9FC5DA", valign: "top",
});
cartao(s, M, 2.8, (W - M * 2 - 0.25) / 2, 1.55, "Por que é pesquisa original",
  "Coleta e análise próprias em larga escala: 239.381 aplicativos Android analisados, " +
  "13.082 com mecanismo de consentimento identificado. Primeiro estudo em escala sobre " +
  "avisos de consentimento no Android.", TEAL);
cartao(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 2.8, (W - M * 2 - 0.25) / 2, 1.55,
  "Três fontes confirmam que é original",
  "ACM Digital Library:  etiqueta RESEARCH-ARTICLE\n" +
  "Scopus:  tipo de documento Conference Paper\n" +
  "O próprio artigo:  corpus e ferramenta construídos pelos autores", "1E6B3A");
s.addNotes("Destaque a escala - 239 mil apps - e que CCS e uma das quatro principais conferencias de seguranca do mundo. O PDF e aberto e o artefato esta no GitHub.");

// =====================================================================
// 6 — RELEVÂNCIA QUANTITATIVA
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Por que este artigo importa: os números", 5);
cartao(s, M, 1.05, W - M * 2, 1.5, "CITAÇÕES levantadas nas três bases em 17/09/2026",
  "ACM Digital Library  42          Scopus  52          Google Acadêmico  99  (9 versões)\n\n" +
  "Publicado em 07/11/2022  ·  1.539 downloads na ACM  ·  239.381 apps analisados", "1E6B3A");
cartao(s, M, 2.7, (W - M * 2 - 0.25) / 2, 1.75, "Por que 42 < 52 < 99",
  "É a hierarquia de cobertura das bases.\n\n" +
  "A ACM conta só o próprio acervo. O Scopus acrescenta IEEE, Springer e Elsevier. O " +
  "Scholar agrupa 9 versões do trabalho e ainda conta teses e relatórios.", NAVY);
cartao(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 2.7, (W - M * 2 - 0.25) / 2, 1.75,
  "Recência × citações: a troca",
  "Um artigo de 2025 teve um ano para ser citado; um muito citado é antigo por construção.\n\n" +
  "2022 em CCS é o ponto de equilíbrio, e 239 mil apps já é critério quantitativo por si só.", NAVY);
s.addNotes("Não leia os números; interprete. Um número sem contexto não diz nada.");

// =====================================================================
// 7 — RELEVÂNCIA QUALITATIVA (preenchido)
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Por que este artigo importa: o conteúdo", 6);
const c3 = (W - M * 2 - 0.4) / 3;
cartao(s, M, 1.05, c3, 2.5, "1 · O método é o que eu reuso",
  "Análise estática de APKs em escala, detecção de SDKs de rastreamento, verificação de " +
  "backend e inspeção manual de subamostra.\n\nÉ o pipeline que pretendo aplicar.", TEAL);
cartao(s, M + c3 + 0.2, 1.05, c3, 2.5, "2 · A lacuna que ele deixa",
  "Corpus de aplicativos comerciais, estudados sob o GDPR.\n\nSem recorte governamental, sem " +
  "grupo de controle pareado e sem contexto brasileiro. É onde o meu trabalho entra.", TEAL);
cartao(s, M + (c3 + 0.2) * 2, 1.05, c3, 2.5, "3 · Já tenho um resultado",
  "0 de 396 apps de governo exibem anúncio. No controle comercial, 33,2%.\n\n" +
  "IC95% [0,000; 0,010] contra [0,269; 0,401]. Não se sobrepõem.", "1E6B3A");
s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 3.75, w: W - M * 2, h: 0.85, fill: { color: NAVY }, rectRadius: 0.06,
});
s.addText(
  "Se o app de governo não monetiza, o rastreador que houver não é de publicidade. " +
  "é dependência técnica. Isso muda a pergunta.", {
  x: M + 0.25, y: 3.93, w: W - M * 2 - 0.5, h: 0.5, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 14.5, italic: true, color: WHITE, align: "center",
});
s.addNotes("O terceiro cartão é o diferencial: não é hipótese, é medida própria. Zero em 396 é um resultado limpo. Diga que isso descarta o enquadramento de que o governo vende dados e deixa a questão mais difícil: por que o rastreador está lá, então?");

// =====================================================================
// 8 — MÉTRICAS E QUALIS
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Métricas do veículo e Qualis", 7);
cartao(s, M, 1.02, (W - M * 2 - 0.25) / 2, 1.85, "OS TRÊS OBRIGATÓRIOS, levantados em 17/09/2026",
  "1 · h5 = 90   (mediana 146)   posição 5 de 20\n" +
  "     (posição 19 é a AsiaCCS, h5 41, outro evento)\n" +
  "2 · Qualis = A1   (ver o limiar ao lado)\n" +
  "3 · CORE = A*   ICORE2026", "1E6B3A");
cartao(s, M, 3.02, (W - M * 2 - 0.25) / 2, 1.83, "Por que A1, e não A2",
  "Com N=20 o percentil dá 75, que seria A2. Mas 20 é lista TRUNCADA, não população. Esse 75 é " +
  "PISO: universo maior só empurra para cima.\n\n" +
  "A1 exige percentil 87,5.  (N-5)/N >= 0,875  ->  N >= 40.\n" +
  "Basta a área ter 40 veículos. Tem centenas. Logo A1. É limite, não estimativa.", NAVY);
s.addText("Faixas de percentil → estrato  (Figura 6, p. 13 do Documento Técnico)", {
  x: M + (W - M * 2 - 0.25) / 2 + 0.25, y: 1.02, w: (W - M * 2 - 0.25) / 2, h: 0.3,
  isTextBox: true, margin: 0, fontFace: SANS, fontSize: 10.5, bold: true, color: NAVY,
});
s.addImage({
  path: "/home/user/TCC/seminario/qualis-faixas-de-percentil.png",
  x: M + (W - M * 2 - 0.25) / 2 + 0.25, y: 1.4, w: (W - M * 2 - 0.25) / 2, h: 1.0,
});
s.addText([
  { text: "Classes de 12,5% de amplitude.", options: { breakLine: true, bold: true } },
  { text: "Estrato C: periódicos sem nenhum dos indicadores do modelo.", options: { breakLine: true } },
  { text: "Com mais de um indicador, considera-se o MAIOR percentil.", options: { breakLine: true } },
  { text: "As áreas podem ajustar até 30% dos estratos, então o valor publicado pode divergir da tabela.", options: {} },
], {
  x: M + (W - M * 2 - 0.25) / 2 + 0.25, y: 2.58, w: (W - M * 2 - 0.25) / 2, h: 2.1,
  isTextBox: true, margin: 0, fontFace: SANS, fontSize: 10.5, color: GRAY, paraSpaceAfter: 4,
});
s.addNotes("Mostre a tabela na tela e aponte onde o seu veículo cai. Mencione a ressalva da estimativa por h5.");

// =====================================================================
// 9 a 14 — ANÁLISE DA ESTRUTURA
// =====================================================================
const blocos = [
  {
    n: 8, titulo: "A estrutura do artigo",
    intro: "Oito seções em quinze páginas. À direita, o que chama atenção.",
    conteudo: [
      "1  Introduction            p.1-3    contexto, 3 perguntas, contribuições",
      "2  Legal Background        p.3-4    define na lei as 4 violações que vai medir",
      "3  Methodology             p.4-6    como achar os avisos de consentimento",
      "4  Large-Scale Analysis    p.6-11   aplica em escala e mostra os resultados",
      "5  Developer Notification  p.11-12  avisa os desenvolvedores, coleta respostas",
      "6  Discussion              p.12-13  interpreta",
      "7  Related Work            p.13     revisão da literatura",
      "8  Conclusion              p.13     fecha",
    ],
    rotulos: ["A revisão da literatura é a seção 7, não a 2",
              "Método (3) vem separado da aplicação (4)",
              "As seções 3 e 4 ocupam metade do artigo",
              "Não existe seção de Limitações nem de Ética"],
    dica: "Num estudo de 239 mil aplicativos, método detalhado é consequência da escala. " +
          "No exemplo da professora o avaliador teve que reconstruir o método porque não havia seção.",
  },
  {
    n: 9, titulo: "O resumo",
    intro: "Seis movimentos, um por frase. É modelo de como escrever o meu.",
    conteudo: [
      "CONTEXTO      o GDPR exige consentimento livre, específico e informado",
      "LACUNA        ninguém estudou como os avisos são de fato implementados",
      "OBJETIVO      primeiro estudo em larga escala sobre esses avisos",
      "MÉTODO        abordagem automatizada aplicada a 239.381 aplicativos",
      "RESULTADO     30.160 sem aviso nenhum; 2.688 dos que têm, violam a lei",
      "IMPLICAÇÃO    falta transparência e falta apoio aos desenvolvedores",
      "",
      "Palavras-chave: Android Security, Consent, GDPR, User Privacy",
    ],
    rotulos: ["Cada movimento cabe em uma frase",
              "As palavras-chave trazem Consent e GDPR",
              "mas não trazem tracking nem third-party,",
              "que estão no título do artigo"],
    dica: "As palavras-chave mostram como os autores querem ser encontrados. " +
          "Compare com os termos que eu usei na minha busca.",
  },
  {
    n: 10, titulo: "A introdução",
    intro: "Abre pelo que acontece com o usuário, não pela técnica.",
    conteudo: [
      "\u0022Toda vez que abrimos uma página ou usamos um aplicativo, informação",
      " sobre nós é transmitida a um grande número de empresas.\u0022",
      "",
      "Depois declara três perguntas de pesquisa:",
      "",
      "  1  os aplicativos implementam algum tipo de aviso de consentimento?",
      "  2  esses avisos se justificam juridicamente sob o GDPR?",
      "  3  os desenvolvedores sabem que estão em violação?",
    ],
    rotulos: ["Contextualiza", "Descreve o problema", "Aponta a lacuna",
              "Declara objetivo e contribuições",
              "As 3 perguntas são respondíveis por medição"],
    dica: "Na nota de rodapé 1 eles explicam que dizem violação POTENCIAL de propósito, " +
          "para não emitir juízo jurídico. Mesmo cuidado que a LGPD vai exigir de mim.",
  },
  {
    n: 11, titulo: "O método, e o funil",
    intro: "Corpus vindo do AndroZoo, três critérios de entrada, dois instrumentos.",
    conteudo: [
      "5.800.000   nomes de aplicativos na lista do AndroZoo",
      "      ↓     mais de 10 mil downloads, pede permissão sensível,",
      "            atualizado depois de maio de 2018",
      "  250.972   aplicativos obtidos",
      "      ↓     a análise funcionou em 95,38% deles",
      "  239.381   analisados",
      "   13.082   têm aviso de consentimento   →   2.688 violam a lei",
      "   30.160   não têm aviso nenhum",
    ],
    rotulos: ["O AndroZoo é a mesma fonte que eu vou usar",
              "Três critérios de entrada declarados",
              "Dois instrumentos: a tela e o tráfego de rede",
              "Reportam quanto NÃO conseguiram analisar"],
    dica: "O denominador muda no meio do funil: os 2.688 são sobre os 13.082 que têm aviso, " +
          "não sobre os 239 mil. E os 30.160 são outra categoria, não têm aviso nenhum.",
  },
  {
    n: 12, titulo: "Os resultados",
    intro: "Cada afirmação é sustentada por dois instrumentos independentes.",
    conteudo: [
      "2.181   mandaram dado ANTES de o usuário consentir",
      "1.084   não oferecem nenhuma forma de recusar",
      "  134   mandaram dado DEPOIS de o usuário recusar",
      "",
      "Quase todas as violações envolvem o identificador de anúncio do Android.",
      "",
      "A tela prova que o aviso existe. O tráfego prova que o dado saiu.",
      "Um sozinho não sustenta a afirmação.",
    ],
    rotulos: ["Não tem intervalo de confiança",
              "Não tem tamanho de efeito",
              "Não tem grupo de controle",
              "e essa é a minha lacuna"],
    dica: "Presença não é transmissão. E o mesmo par de instrumentos que eu vou precisar: " +
          "detectar o SDK no aplicativo nao prova que ele enviou dado.",
  },
  {
    n: 13, titulo: "A discussão",
    intro: "Existe seção própria, com três subseções.",
    conteudo: [
      "6.1   a violação é generalizada, não é caso isolado",
      "6.2   o problema não é só ilegalidade, é falta de transparência",
      "6.3   falta ferramenta e orientação para o desenvolvedor cumprir a lei",
      "",
      "Depois de encontrar 2.688 violações, eles NÃO concluem que",
      "os desenvolvedores agem de má-fé. Usam as respostas que",
      "coletaram na seção 5 para deslocar a causa.",
    ],
    rotulos: ["Interpreta o resultado",
              "Confronta com a literatura",
              "Tira implicação prática",
              "Resiste à explicação fácil"],
    dica: "E o mesmo movimento que o meu resultado pede: nenhum dos 396 apps de governo tem " +
          "anuncio. Se houver rastreador, nao e para ganhar dinheiro, e dependencia tecnica.",
  },
  {
    n: 14, titulo: "A conclusão",
    intro: "Repete o resumo quase palavra por palavra. Com uma diferença.",
    conteudo: [
      "NO RESUMO:      2.688 aplicativos VIOLAM ao menos um requisito",
      "",
      "NA CONCLUSÃO:   2.688 aplicativos POTENCIALMENTE VIOLAM",
      "",
      "A nota de rodapé 1 diz que \u0022potencialmente\u0022 foi escolha deliberada,",
      "para não emitir juízo jurídico.",
      "",
      "Logo a conclusão está certa e o resumo escorrega.",
    ],
    rotulos: ["Retoma o objetivo", "Infere a partir dos dados",
              "Responde a terceira pergunta", "Tira implicação"],
    dica: "Comparar o que o resumo promete com o que a conclusao entrega e analise critica de " +
          "verdade. Aqui ela encontra uma inconsistencia real num artigo de conferencia A*.",
  },
];

blocos.forEach((b) => {
  const sl = pres.addSlide();
  tituloSlide(sl, b.titulo, b.n);
  sl.addText(b.intro, {
    x: M, y: 0.98, w: W - M * 2, h: 0.3, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 12, color: GRAY,
  });
  // conteúdo real extraído do artigo
  sl.addShape(pres.ShapeType.roundRect, {
    x: M, y: 1.38, w: 6.05, h: 2.42,
    fill: { color: "F4F6F9" }, line: { color: TEAL, width: 1 }, rectRadius: 0.06,
  });
  sl.addText(b.conteudo.map((linha, i) => ({
    text: linha, options: { breakLine: i < b.conteudo.length - 1 },
  })), {
    x: M + 0.18, y: 1.5, w: 5.7, h: 2.2, isTextBox: true, margin: 0,
    fontFace: "Consolas", fontSize: 9.5, color: NAVY, lineSpacingMultiple: 1.22,
    valign: "top",
  });
  // rótulos de anotação
  sl.addText("Rótulos a usar", {
    x: 6.85, y: 1.38, w: W - M - 6.85, h: 0.28, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 10.5, bold: true, color: TEAL, charSpacing: 1,
  });
  sl.addText(b.rotulos.map((t, i) => ({
    text: t, options: { bullet: true, breakLine: i < b.rotulos.length - 1 },
  })), {
    x: 6.85, y: 1.72, w: W - M - 6.85, h: 2.08, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 11, color: NAVY, paraSpaceAfter: 7, valign: "top",
  });
  cartao(sl, M, 3.95, W - M * 2, 1.15, "Observação para esta seção", b.dica, TEAL);
  sl.addNotes("Não leia o texto colado em voz alta. Aponte os rótulos e explique a função de cada trecho.");
});

// =====================================================================
// 15 — FECHAMENTO
// =====================================================================
s = pres.addSlide();
s.background = { color: NAVY };
s.addText("O que este artigo muda no meu TCC", {
  x: M, y: 0.85, w: W - M * 2, h: 0.6, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 30, bold: true, color: WHITE,
});
s.addShape(pres.ShapeType.rect, { x: M, y: 1.58, w: 0.85, h: 0.035, fill: { color: TEAL } });
const fechos = [
  ["Método", "Adoto o pipeline de análise estática de APKs com detecção de SDKs de rastreamento e validação manual de subamostra."],
  ["Recorte", "Aplico ao parque governamental brasileiro, que o artigo não cobre, e acrescento grupo de controle comercial pareado."],
  ["Próximo passo", "Validar manualmente os 396 aplicativos e rodar o piloto com os 20 maiores."],
];
fechos.forEach(([rot, txt], i) => {
  const y = 1.95 + i * 0.95;
  s.addShape(pres.ShapeType.ellipse, { x: M, y: y + 0.04, w: 0.3, h: 0.3, fill: { color: TEAL } });
  s.addText(String(i + 1), {
    x: M, y: y + 0.04, w: 0.3, h: 0.3, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle",
  });
  s.addText(rot, {
    x: M + 0.45, y: y, w: 1.7, h: 0.3, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, color: "9FC5DA",
  });
  s.addText(txt, {
    x: M + 2.2, y: y, w: W - M - 2.2 - M, h: 0.72, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 12.5, color: "E6EEF4", valign: "top",
  });
});
s.addText("Obrigado.", {
  x: M, y: 4.75, w: W - M * 2, h: 0.4, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 16, italic: true, color: TEAL,
});
s.addNotes("Feche conectando o artigo ao seu próximo passo concreto. Deixe claro que há trabalho já feito, não só plano.");

pres.writeFile({ fileName: "/home/user/TCC/seminario/seminario-analise-de-artigo.pptx" })
  .then(f => console.log("gerado:", f));
