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
s.addText("Cibersegurança — medição empírica", {
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
cartao(s, M + cq + 0.2, 3.05, cq, 1.55, "Dado sensível — Art. 11",
  "152 aplicativos\nsaúde 125 · previdência 28\nbiometria 17", TEAL);
cartao(s, M + (cq + 0.2) * 2, 3.05, cq, 1.55, "Instrumento",
  "81,6% das políticas\nacessíveis\n\npotência: 5,1 p.p.", TEAL);
cartao(s, M + (cq + 0.2) * 3, 3.05, cq, 1.55, "Fonte de APKs",
  "AndroZoo\nacesso concedido\n17/09/2026", "1E6B3A");
rodape(s, "1 minuto");
s.addNotes("Abra dizendo que o tema está em definição mas que a escolha do artigo não depende disso — o que se reaproveita é o método.");

// =====================================================================
// 3 — COMO CHEGUEI AQUI (preenchido)
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Como cheguei a este recorte", 2);
s.addText("Seis temas passaram por teste de viabilidade antes de virar projeto. Três caíram, um ficou inconclusivo.", {
  x: M, y: 1.0, w: W - M * 2, h: 0.32, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 12.5, color: GRAY,
});
const col = (W - M * 2 - 0.6) / 4;
cartao(s, M, 1.45, col, 2.55, "Descartado — ICS exposta",
  "Os mesmos hosts respondiam em Modbus, IEC-104 e EtherNet/IP ao mesmo tempo — " +
  "equipamento industrial real não faz isso.\n\nA variável independente (o setor do " +
  "operador) era inobservável.", "9B2C2C");
cartao(s, M + col + 0.2, 1.45, col, 2.55, "Descartado — abuso de marca",
  "20.007 entradas de log de Certificate Transparency analisadas.\n\n" +
  "Nenhuma imitação real encontrada: phishing moderno raramente põe a marca no " +
  "domínio, o que impõe teto de recall.", "9B2C2C");
cartao(s, M + (col + 0.2) * 2, 1.45, col, 2.55, "Inconclusivo — malware bancário",
  "O repositório rotula a CAMPANHA, não o payload.\n\n85% do acervo brasileiro são " +
  "containers, onde a métrica que eu usava nem existe. Erro meu, registrado.", "8A6D1F");
cartao(s, M + (col + 0.2) * 3, 1.45, col, 2.55, "Confirmado — apps de governo",
  "396 aplicativos, 71 publicadores públicos, três esferas.\n\nPublicador identificado " +
  "na origem: sem trabalho de atribuição — que foi o que matou o primeiro tema.", "1E6B3A");
s.addText(
  "Descartar com evidência é parte do método (Aula 04 — maturidade em pesquisa; " +
  "Aula 07 — evitar o fundamento vazio).", {
  x: M, y: 4.2, w: W - M * 2, h: 0.4, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, italic: true, color: TEAL,
});
rodape(s, "1 minuto  ·  não se alongue aqui — é contexto, não o conteúdo principal");
s.addNotes("Trinta segundos no máximo por tema descartado. O objetivo é mostrar que a escolha foi testada, não contar a história inteira.");

// =====================================================================
// 4 — PASSO A PASSO DA SELEÇÃO
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Passo a passo da seleção", 3);
s.addText("A atividade pede o processo, não só o resultado. Anote enquanto pesquisa — depois é irrecuperável.", {
  x: M, y: 1.0, w: W - M * 2, h: 0.32, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 12, color: GRAY,
});
preencher(s, M, 1.45, (W - M * 2 - 0.25) / 2, 3.45, "registre a sua busca", [
  "Base(s) usada(s) via CAFe: ACM DL, IEEE Xplore, Scopus, Web of Science…",
  "String de busca exata, com os operadores booleanos",
  "Filtros: período, tipo de documento, idioma, área",
  "Nº de resultados retornados",
  "Nº após leitura de título e resumo",
  "Nº após leitura do texto completo",
  "Critérios de inclusão e exclusão aplicados",
  "Data da consulta",
]);
preencher(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 1.45, (W - M * 2 - 0.25) / 2, 3.45,
  "por que este e não outro", [
    "Por que é artigo ORIGINAL e não revisão — aponte no texto onde isso fica claro (coleta própria, experimento, dados novos)",
    "Quais candidatos você descartou e por quê",
    "Print das telas de busca (guarde; ela pode pedir)",
  ]);
rodape(s, "2 minutos");
s.addNotes("Se você fizer a busca sem anotar, este slide fica impossível. Anote em um arquivo enquanto pesquisa.");

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
  "NGUYEN, T. T.; BACKES, M.; STOCK, B.   In: Proceedings of the 2022 ACM SIGSAC Conference " +
  "on Computer and Communications Security (CCS '22), 2022.   DOI: 10.1145/3548606.3560564\n" +
  "PDF aberto: swag.cispa.saarland   ·   artefato: github.com/cispa/consent-notices", {
  x: M + 0.25, y: 1.9, w: W - M * 2 - 0.5, h: 0.6, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, color: "9FC5DA", valign: "top",
});
cartao(s, M, 2.8, (W - M * 2 - 0.25) / 2, 1.55, "Por que é pesquisa original",
  "Coleta e análise próprias em larga escala: 239.381 aplicativos Android analisados, " +
  "13.082 com mecanismo de consentimento identificado. Primeiro estudo em escala sobre " +
  "avisos de consentimento no Android.", TEAL);
preencher(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 2.8, (W - M * 2 - 0.25) / 2, 1.55,
  "confirme ao ler o artigo", [
    "Paginação exata nos anais do CCS '22",
    "Como o corpus afunilou de 239.381 para 13.082",
    "Onde o artefato é citado no texto",
  ]);
rodape(s, "1 minuto  ·  CCS é CONFERÊNCIA — use h5 + Qualis + CORE Rank");
s.addNotes("Destaque a escala - 239 mil apps - e que CCS e uma das quatro principais conferencias de seguranca do mundo. O PDF e aberto e o artefato esta no GitHub.");

// =====================================================================
// 6 — RELEVÂNCIA QUANTITATIVA
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Relevância — critérios quantitativos", 5);
preencher(s, M, 1.05, W - M * 2, 1.5, "citações — anote as três, elas divergem", [
  "Google Scholar:  ______        Scopus:  ______        Web of Science:  ______",
  "Data da consulta: ____/____/2026   ·   Ano de publicação do artigo: 2022",
]);
cartao(s, M, 2.7, (W - M * 2 - 0.25) / 2, 1.75, "O que comentar sobre os números",
  "Divergência entre as bases é esperada e vale explicar: cada uma indexa um conjunto " +
  "diferente de veículos.\n\nCite sempre a base e a data junto do número.", NAVY);
cartao(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 2.7, (W - M * 2 - 0.25) / 2, 1.75,
  "Recência × citações: a troca",
  "Um artigo de 2025 teve um ano para ser citado; um muito citado é antigo por construção.\n\n" +
  "2022 em CCS é o ponto de equilíbrio — e 239 mil apps é critério quantitativo por si só.", NAVY);
rodape(s, "1,5 minuto");
s.addNotes("Não leia os números; interprete. Um número sem contexto não diz nada.");

// =====================================================================
// 7 — RELEVÂNCIA QUALITATIVA (preenchido)
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Relevância — critérios qualitativos", 6);
const c3 = (W - M * 2 - 0.4) / 3;
cartao(s, M, 1.05, c3, 2.5, "1 · O método é o que eu reuso",
  "Análise estática de APKs em escala, detecção de SDKs de rastreamento, verificação de " +
  "backend e inspeção manual de subamostra.\n\nÉ o pipeline que pretendo aplicar.", TEAL);
cartao(s, M + c3 + 0.2, 1.05, c3, 2.5, "2 · A lacuna que ele deixa",
  "Corpus de apps comerciais de controle parental.\n\nSem recorte governamental, sem " +
  "grupo de controle pareado e sem contexto brasileiro — exatamente onde meu trabalho entra.", TEAL);
cartao(s, M + (c3 + 0.2) * 2, 1.05, c3, 2.5, "3 · Já tenho um resultado",
  "0 de 396 apps de governo exibem anúncio. No controle comercial, 33,2%.\n\n" +
  "IC95% [0,000; 0,010] contra [0,269; 0,401] — não se sobrepõem.", "1E6B3A");
s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 3.75, w: W - M * 2, h: 0.85, fill: { color: NAVY }, rectRadius: 0.06,
});
s.addText(
  "Se o app de governo não monetiza, o rastreador que houver não é de publicidade — " +
  "é dependência técnica. Isso muda a pergunta.", {
  x: M + 0.25, y: 3.93, w: W - M * 2 - 0.5, h: 0.5, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 14.5, italic: true, color: WHITE, align: "center",
});
rodape(s, "1,5 minuto  ·  este é o slide mais forte da sua justificativa");
s.addNotes("O terceiro cartão é o diferencial: não é hipótese, é medida própria. Zero em 396 é um resultado limpo. Diga que isso descarta o enquadramento de que o governo vende dados e deixa a questão mais difícil: por que o rastreador está lá, então?");

// =====================================================================
// 8 — MÉTRICAS E QUALIS
// =====================================================================
s = pres.addSlide();
tituloSlide(s, "Métricas do veículo e Qualis", 7);
cartao(s, M, 1.02, (W - M * 2 - 0.25) / 2, 1.62, "OS TRÊS OBRIGATÓRIOS — todos levantados em 17/09/2026",
  "1 · h5 = 90   (mediana 146)   posição 5 de 20\n" +
  "2 · Qualis = A1   (ver o limiar ao lado)\n" +
  "3 · CORE = A*   ICORE2026", "1E6B3A");
cartao(s, M, 2.8, (W - M * 2 - 0.25) / 2, 2.05, "Por que A1, e não A2",
  "Com N=20 o percentil dá 75 (A2) — mas 20 é lista TRUNCADA, não população. Esse 75 é " +
  "PISO: universo maior só empurra para cima.\n\n" +
  "A1 exige percentil 87,5.  (N-5)/N >= 0,875  ->  N >= 40.\n" +
  "Basta a área ter 40 veículos. Tem centenas. Logo A1 — limite, não estimativa.", NAVY);
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
  { text: "As áreas podem ajustar até 30% dos estratos — o valor publicado pode divergir da tabela.", options: {} },
], {
  x: M + (W - M * 2 - 0.25) / 2 + 0.25, y: 2.58, w: (W - M * 2 - 0.25) / 2, h: 2.1,
  isTextBox: true, margin: 0, fontFace: SANS, fontSize: 10.5, color: GRAY, paraSpaceAfter: 4,
});
rodape(s, "2 minutos  ·  use a figura original no slide — é fonte primária");
s.addNotes("Mostre a tabela na tela e aponte onde o seu veículo cai. Mencione a ressalva da estimativa por h5.");

// =====================================================================
// 9 a 14 — ANÁLISE DA ESTRUTURA
// =====================================================================
const blocos = [
  {
    n: 8, titulo: "Análise da estrutura",
    intro: "Reproduza o sumário do artigo e marque a função de cada seção.",
    rotulos: ["Contextualização", "Procedimento metodológico", "Desenvolvimento do trabalho",
              "Resultados obtidos", "Infere a partir dos dados obtidos"],
    dica: "No artigo do ACSAC, a estrutura é organizada POR TIPO DE SOLUÇÃO analisada " +
          "(rede, Android, Windows, extensões), não na sequência clássica. Comente isso: " +
          "método e resultados aparecem entrelaçados dentro de cada bloco.",
  },
  {
    n: 9, titulo: "Análise do resumo",
    intro: "Cole o abstract e marque cada trecho com sua função.",
    rotulos: ["Objetivos", "Método empregado", "Apresentação dos resultados", "Palavras-chave"],
    dica: "Verifique se o resumo cobre os quatro elementos. Se faltar algum, APONTE — " +
          "identificar o que falta também é análise.",
  },
  {
    n: 10, titulo: "Análise da introdução",
    intro: "Cole os parágrafos da introdução e marque cada movimento.",
    rotulos: ["Contextualiza o trabalho", "Descreve a problemática",
              "Objetivo e contribuição da proposta", "Estrutura e organização do artigo"],
    dica: "Quase toda introdução em Computação termina anunciando a organização das seções. " +
          "Confirme se esta tem, e onde.",
  },
  {
    n: 11, titulo: "Análise do método",
    intro: "Percorra as seções metodológicas e explique o que cada uma faz.",
    rotulos: ["Como o corpus foi montado", "Ferramentas e instrumentos",
              "Análise estática × dinâmica", "O que foi manual e o que foi automatizado"],
    dica: "No exemplo da professora, o avaliador anotou que o método NÃO estava numa seção " +
          "explícita e o reconstruiu a partir do texto. Se for o caso aqui, faça o mesmo — " +
          "é o tipo de observação que rende nota.",
  },
  {
    n: 12, titulo: "Análise dos resultados",
    intro: "O que foi encontrado e como os autores sustentam o achado.",
    rotulos: ["Achados principais", "Como foram validados",
              "Tabelas e figuras que sustentam", "Limitações reconhecidas"],
    dica: "Separe o que é medição do que é interpretação. Essa distinção é exatamente o que " +
          "você vai precisar fazer no seu próprio trabalho.",
  },
  {
    n: 13, titulo: "Análise da discussão",
    intro: "O enunciado nomeia a discussão. É o que separa o medido do que ele significa.",
    rotulos: ["Interpretação do resultado", "Confronto com a literatura anterior",
              "Implicação prática ou normativa", "Ameaças à validade"],
    dica: "Artigo de segurança com frequência funde discussão e resultados, ou a chama de " +
          "Implications. Se não houver seção autônoma, DIGA — apontar isso é análise de estrutura.",
  },
  {
    n: 14, titulo: "Análise da conclusão",
    intro: "Cole a conclusão e marque o que os autores inferem.",
    rotulos: ["Inferência a partir dos dados obtidos", "Trabalhos futuros",
              "O que ficou fora do escopo"],
    dica: "Pergunta clássica de banca: a conclusão vai além do que os dados sustentam? " +
          "Ter uma opinião formada aqui te protege.",
  },
];

blocos.forEach((b) => {
  const sl = pres.addSlide();
  tituloSlide(sl, b.titulo, b.n);
  sl.addText(b.intro, {
    x: M, y: 0.98, w: W - M * 2, h: 0.3, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 12, color: GRAY,
  });
  // área grande para colar o texto do artigo
  sl.addShape(pres.ShapeType.roundRect, {
    x: M, y: 1.38, w: 6.05, h: 2.42,
    fill: { color: AMBER_BG }, line: { color: AMBER, width: 1, dashType: "dash" }, rectRadius: 0.06,
  });
  sl.addText("A PREENCHER  ·  cole aqui o texto do artigo", {
    x: M + 0.2, y: 1.52, w: 5.65, h: 0.26, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: AMBER, charSpacing: 1,
  });
  sl.addText(
    "Transcreva o trecho real do artigo e posicione os rótulos ao lado, ligando cada " +
    "anotação ao parágrafo correspondente — como nos dois exemplos fornecidos pela professora.", {
    x: M + 0.2, y: 1.85, w: 5.65, h: 0.7, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 11, italic: true, color: GRAY, valign: "top",
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
  rodape(sl, "~50 segundos por slide  ·  a análise da estrutura vale 5 dos 15 minutos");
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
  ["Recorte", "Aplico ao parque governamental brasileiro, que o artigo não cobre — com grupo de controle comercial pareado."],
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
