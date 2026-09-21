// Deck do seminário de análise de artigo científico.
//
// Os slides do item 3 seguem o formato dos exemplos fornecidos pela professora:
// reproduzem o TEXTO REAL do artigo e anotam, na margem, a função retórica de
// cada trecho. Não resumem. O texto do artigo fica no original; as anotações
// vão em português.
//
//   node scripts/gera_deck_seminario.js

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Claudio Meireles";
pres.title = "Seminario - Analise de Artigo Cientifico";

const W = 10, H = 5.63, M = 0.55;
const NAVY = "1B2A4A", TEAL = "2E86A8", GRAY = "5B6B7C";
const WHITE = "FFFFFF", CINZA = "F4F6F9", VERDE = "1E6B3A";
const SERIF = "Georgia", SANS = "Calibri", MONO = "Consolas";
const RAIZ = "/home/user/TCC/seminario/pesquisa/";

// ---------------------------------------------------------------- utilidades

function titulo(s, texto, numero) {
  if (numero) {
    s.addText(numero, {
      x: M, y: 0.32, w: 0.72, h: 0.42, isTextBox: true, margin: 0,
      fontFace: SERIF, fontSize: 19, bold: true, color: TEAL,
    });
  }
  s.addText(texto, {
    x: numero ? M + 0.74 : M, y: 0.28, w: W - M * 2 - 0.78, h: 0.48,
    isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 22, bold: true, color: NAVY,
  });
  s.addShape(pres.ShapeType.line, {
    x: M, y: 0.86, w: W - M * 2, h: 0, line: { color: "DDE3EA", width: 1 },
  });
}

function legenda(s, texto, y) {
  s.addText(texto, {
    x: M, y: y || 0.97, w: W - M * 2, h: 0.28, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 12, color: GRAY,
  });
}

function cartao(s, x, y, w, h, rotulo, texto, cor) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, fill: { color: CINZA },
    line: { color: cor || TEAL, width: 1 }, rectRadius: 0.05,
  });
  s.addText(rotulo, {
    x: x + 0.16, y: y + 0.11, w: w - 0.32, h: 0.24, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: cor || TEAL, charSpacing: 0.6,
  });
  s.addText(texto, {
    x: x + 0.16, y: y + 0.4, w: w - 0.32, h: h - 0.52, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 11, color: NAVY, valign: "top", lineSpacingMultiple: 1.12,
  });
}

// Slide do item 3, no formato dos exemplos da professora: texto real do artigo
// à esquerda, anotação da função retórica à direita.
function slideAnalise(n, tituloTexto, blocos, nota) {
  const s = pres.addSlide();
  titulo(s, tituloTexto, String(n));

  const larguraTexto = 6.15;
  const xAnot = M + larguraTexto + 0.28;
  const larguraAnot = W - M - xAnot;

  let y = 1.03;
  blocos.forEach((b) => {
    const alturaLinha = b.mono ? 0.16 : 0.178;
    const linhas = Array.isArray(b.texto) ? b.texto : [b.texto];
    const altura = Math.max(linhas.length * alturaLinha + 0.08, 0.3);

    s.addText(linhas.map((l, i) => ({
      text: l, options: { breakLine: i < linhas.length - 1 },
    })), {
      x: M, y, w: larguraTexto, h: altura, isTextBox: true, margin: 0,
      fontFace: b.mono ? MONO : SERIF, fontSize: b.mono ? 9 : 10.5,
      color: b.destaque ? NAVY : "33404F", bold: !!b.destaque,
      italic: !!b.citacao, valign: "top", lineSpacingMultiple: 1.0,
    });

    if (b.anota) {
      const hAnot = Math.min(altura, 0.66);
      s.addShape(pres.ShapeType.roundRect, {
        x: xAnot, y: y - 0.02, w: larguraAnot, h: hAnot,
        fill: { color: "EAF2F7" }, line: { color: TEAL, width: 0.75 }, rectRadius: 0.04,
      });
      s.addText(b.anota, {
        x: xAnot + 0.1, y: y - 0.02, w: larguraAnot - 0.2, h: hAnot,
        isTextBox: true, margin: 0,
        fontFace: SANS, fontSize: 9.5, bold: true, color: NAVY, valign: "middle",
      });
    }
    y += altura + 0.055;
  });

  if (nota) s.addNotes(nota);
  return s;
}

// =====================================================================
// 1 — CAPA
// =====================================================================
let s = pres.addSlide();
s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: NAVY } });
s.addText("Análise de Artigo Científico", {
  x: M, y: 1.75, w: W - M * 2, h: 0.65, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 32, bold: true, color: WHITE,
});
s.addText("Freely Given Consent?  Avisos de consentimento de rastreamento\npor terceiros e as violações do GDPR em aplicativos Android", {
  x: M, y: 2.52, w: W - M * 2, h: 0.72, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 14, color: "9FC5DA", lineSpacingMultiple: 1.2,
});
s.addText("Claudio Meireles   ·   Projeto Capstone I   ·   IDP   ·   29 de setembro de 2026", {
  x: M, y: 4.3, w: W - M * 2, h: 0.3, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, color: "7FA8C4",
});

// =====================================================================
// 2 — ITEM 1: passo a passo da seleção
// =====================================================================
s = pres.addSlide();
titulo(s, "Como cheguei até este artigo", "1");
legenda(s, "Scopus, pelo portal da CAPES via CAFe, em 21 de setembro de 2026.");

const passoW = (W - M * 2 - 0.4) / 3;
[["funil-1-131.jpg", "131", "a expressão exata, sem filtro"],
 ["funil-2-70.jpg", "70", "ano, área e tipo de documento"],
 ["funil-3-5.jpg", "5", "palavras-chave do Scopus"]].forEach((p, i) => {
  const x = M + (passoW + 0.2) * i;
  s.addImage({ path: RAIZ + p[0], x, y: 1.3, w: passoW, h: passoW * 0.578 });
  s.addText([
    { text: p[1], options: { bold: true, color: TEAL, fontSize: 17 } },
    { text: "   " + p[2], options: { fontSize: 10, color: GRAY } },
  ], {
    x, y: 1.3 + passoW * 0.578 + 0.06, w: passoW, h: 0.34,
    isTextBox: true, margin: 0, fontFace: SANS, valign: "top",
  });
});

s.addText('Busca:   "third-party tracking"      campo: Article title, Abstract, Keywords', {
  x: M, y: 3.36, w: W - M * 2, h: 0.26, isTextBox: true, margin: 0,
  fontFace: MONO, fontSize: 9.5, color: NAVY,
});

s.addTable(
  [[{ text: "Os cinco finalistas", options: { bold: true } },
    { text: "Veículo", options: { bold: true } },
    { text: "Ano", options: { bold: true } },
    { text: "Cit.", options: { bold: true } },
    { text: "Decisão", options: { bold: true } }]].concat([
    ["Freely Given Consent?", "CCS", "2022", "52", "selecionado"],
    ["A fait accompli?", "SOUPS", "2021", "34", "veículo CORE B"],
    ["A Comprehensive Study on 3rd-Party Tracking", "ACM ICPS", "2023", "10", "menos citado"],
    ["Protecting privacy on the web", "Online Inf. Review", "2018", "23", "é web, não Android"],
    ["WhisperTest", "CCS", "2025", "0", "é iOS"],
  ].map((r, i) => r.map((c) => ({
    text: c, options: { bold: i === 0, color: i === 0 ? VERDE : NAVY },
  })))),
  {
    x: M, y: 3.72, w: W - M * 2, colW: [3.45, 1.5, 0.5, 0.5, 2.95],
    fontFace: SANS, fontSize: 9.5, border: { type: "solid", color: "DDE3EA", pt: 0.5 },
    fill: { color: WHITE }, rowH: 0.235, valign: "middle",
  }
);
s.addNotes("2 minutos. A busca tambem trouxe um artigo de 2026 no IEEE S&P com ZERO citacoes: e a prova de que recencia e citacoes se excluem por construcao. E trouxe o Kollnig 2021, a alternativa mais seria, descartada com numero.");

// =====================================================================
// 3 — ITEM 1: o artigo e por que é original
// =====================================================================
s = pres.addSlide();
titulo(s, "O artigo selecionado");
s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 1.0, w: W - M * 2, h: 1.48, fill: { color: NAVY }, rectRadius: 0.05,
});
s.addText("Freely Given Consent? Studying Consent Notice of Third-Party Tracking and Its Violations of GDPR in Android Apps", {
  x: M + 0.25, y: 1.14, w: W - M * 2 - 0.5, h: 0.58, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 16, bold: true, color: WHITE,
});
s.addText("NGUYEN, Trung Tin; BACKES, Michael; STOCK, Ben. In: CCS '22, Proceedings of the 2022 ACM SIGSAC\nConference on Computer and Communications Security. Los Angeles, 7 a 11 nov. 2022, p. 2369-2383.\nDOI 10.1145/3548606.3560564      15 páginas      acesso livre", {
  x: M + 0.25, y: 1.76, w: W - M * 2 - 0.5, h: 0.62, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 10.5, color: "9FC5DA", valign: "top", lineSpacingMultiple: 1.15,
});

cartao(s, M, 2.66, (W - M * 2 - 0.25) / 2, 1.9, "POR QUE É ARTIGO ORIGINAL",
  "Original é o que relata pela primeira vez uma pesquisa inédita. Três fontes confirmam:\n\n" +
  "ACM Digital Library, etiqueta RESEARCH-ARTICLE\n" +
  "Scopus, tipo de documento Conference Paper\n" +
  "O próprio artigo: corpus e ferramenta feitos pelos autores", VERDE);

cartao(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 2.66, (W - M * 2 - 0.25) / 2, 1.9,
  "A ESCALA",
  "239.381 aplicativos Android analisados.\n\n" +
  "É o primeiro estudo em larga escala sobre avisos de consentimento no Android, " +
  "duas ordens de grandeza acima das alternativas que apareceram na busca.", TEAL);
s.addNotes("1 minuto. A etiqueta RESEARCH-ARTICLE e a propria base classificando, nao interpretacao minha.");

// =====================================================================
// 4 — ITEM 1: relevância para o TCC
// =====================================================================
s = pres.addSlide();
titulo(s, "Relevância do artigo para o meu TCC");
legenda(s, "O enunciado pede critérios quantitativos e/ou qualitativos. Trago os dois.");

cartao(s, M, 1.33, (W - M * 2 - 0.25) / 2, 1.5, "QUANTITATIVO      citações em 17/09/2026",
  "ACM Digital Library        42\n" +
  "Scopus                     52\n" +
  "Google Acadêmico           99      (9 versões)\n\n" +
  "A ordem reflete a cobertura de cada base.", TEAL);

cartao(s, M + (W - M * 2 - 0.25) / 2 + 0.25, 1.33, (W - M * 2 - 0.25) / 2, 1.5,
  "QUALITATIVO      o que eu reuso e o que falta",
  "Reuso o método: análise estática e dinâmica em escala, com detecção de bibliotecas de terceiros.\n\n" +
  "A lacuna é a minha contribuição: o artigo não tem grupo de controle nem recorte governamental.", TEAL);

s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 3.03, w: W - M * 2, h: 1.55, fill: { color: NAVY }, rectRadius: 0.05,
});
s.addText("E eu já tenho um resultado preliminar", {
  x: M + 0.28, y: 3.18, w: W - M * 2 - 0.56, h: 0.28, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 9.5, bold: true, color: "9FC5DA", charSpacing: 0.6,
});
s.addText("Nenhum dos 396 aplicativos de governo que levantei exibe anúncio. No grupo de controle comercial, 33,2% exibem.\n" +
  "Os intervalos de confiança não se sobrepõem: [0,000; 0,010] contra [0,269; 0,401].\n\n" +
  "Se houver rastreador num aplicativo de governo, ele não está lá para vender publicidade. É dependência técnica.", {
  x: M + 0.28, y: 3.48, w: W - M * 2 - 0.56, h: 1.0, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, color: WHITE, valign: "top", lineSpacingMultiple: 1.2,
});
s.addNotes("2 minutos. Este e o momento mais forte da apresentacao. Ensaie separado.");

// =====================================================================
// 5 — ITEM 2: métricas e classificação do veículo
// =====================================================================
s = pres.addSlide();
titulo(s, "Métricas e classificação do veículo", "2");
legenda(s, "CCS é conferência: o enunciado pede h5, o Qualis correspondente e o rank no CORE.");

const m3 = (W - M * 2 - 0.5) / 3;
[["ÍNDICE h5", "90", "mediana 146\nGoogle Acadêmico\nposição 5 de 20"],
 ["QUALIS", "A1", "derivado do percentil\ncritério abaixo"],
 ["CORE", "A*", "ICORE2026\nA* em todas as edições\ndesde 2008"]].forEach((c, i) => {
  const x = M + (m3 + 0.25) * i;
  s.addShape(pres.ShapeType.roundRect, {
    x, y: 1.33, w: m3, h: 1.42, fill: { color: CINZA },
    line: { color: TEAL, width: 1 }, rectRadius: 0.05,
  });
  s.addText(c[0], {
    x: x + 0.15, y: 1.43, w: m3 - 0.3, h: 0.24, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: TEAL, charSpacing: 0.6,
  });
  s.addText(c[1], {
    x: x + 0.15, y: 1.66, w: m3 - 0.3, h: 0.5, isTextBox: true, margin: 0,
    fontFace: SERIF, fontSize: 30, bold: true, color: NAVY,
  });
  s.addText(c[2], {
    x: x + 0.15, y: 2.16, w: m3 - 0.3, h: 0.52, isTextBox: true, margin: 0,
    fontFace: SANS, fontSize: 9.5, color: GRAY, valign: "top", lineSpacingMultiple: 1.1,
  });
});

s.addText("Por que A1", {
  x: M, y: 2.94, w: 3.0, h: 0.26, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 9.5, bold: true, color: NAVY, charSpacing: 0.6,
});
s.addText("O Qualis trabalha com percentil, não com h5 bruto. O Google Acadêmico publica apenas as 20 primeiras " +
  "publicações de cada subárea, então essa lista é truncada e não é a população.\n\n" +
  "Com 20 no denominador, a posição 5 dá percentil 75, que seria A2. Esse valor é um piso: qualquer universo maior " +
  "empurra o percentil para cima. O limiar do A1 é 87,5, e a posição 5 o atinge a partir de 40 veículos. " +
  "A subárea tem centenas.", {
  x: M, y: 3.2, w: 6.05, h: 1.35, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 10.5, color: "33404F", valign: "top", lineSpacingMultiple: 1.15,
});
s.addImage({
  path: "/home/user/TCC/seminario/qualis-faixas-de-percentil.png",
  x: 6.78, y: 3.28, w: W - M - 6.78, h: (W - M - 6.78) / 4.32,
});
s.addText("Figura 6, p. 13 do Documento Técnico do Qualis", {
  x: 6.78, y: 3.28 + (W - M - 6.78) / 4.32 + 0.05, w: W - M - 6.78, h: 0.24,
  isTextBox: true, margin: 0, fontFace: SANS, fontSize: 8.5, italic: true, color: GRAY,
});
s.addNotes("2 minutos. Nao existe Qualis oficial para conferencia: o Qualis Referencia classifica periodicos. O enunciado pede para derivar do h5, e a p.12 do Documento Tecnico reconhece que o Google Scholar nao fornece percentil dentro dos agrupamentos tematicos, motivo pelo qual a CAPES criou a base ampliada por area.");

// =====================================================================
// 6 a 12 — ITEM 3: análise da estrutura, no formato dos exemplos
// =====================================================================

slideAnalise(1, "ANÁLISE DA ESTRUTURA", [
  { texto: ["ABSTRACT", "1  Introduction"], anota: "Contextualiza o trabalho" },
  { texto: ["2  Legal Background of GDPR Consent",
            "      2.1  Legal Background",
            "      2.2  Legal Analysis of Potential GDPR Consent"],
    anota: "Marco teórico e jurídico" },
  { texto: ["3  Methodology",
            "      3.1  Collecting Privacy-Related User Interface",
            "      3.2  Identifying Consent Notices"],
    anota: "Procedimento metodológico" },
  { texto: ["4  Large-Scale Analysis",
            "      4.1  App Dataset Construction",
            "      4.2  Identifying Consent Notices In The Wild",
            "      4.3  Automating Potential GDPR Violations",
            "      4.4  Observed Potential Violations"],
    anota: "Desenvolvimento do trabalho e resultados obtidos" },
  { texto: ["5  Developer Notification"], anota: "Validação junto aos desenvolvedores" },
  { texto: ["6  Discussion"], anota: "Infere a partir dos dados obtidos" },
  { texto: ["7  Related Work", "8  Conclusion", "References"], anota: "Revisão e fechamento" },
], "50 segundos. Tres observacoes: Related Work e a secao 7 e nao a 2, porque o posicionamento na literatura e feito na introducao; metodo (3) vem separado da aplicacao em escala (4); e as duas juntas ocupam metade das 15 paginas, o que e consequencia da escala. Nao existe secao de Limitacoes nem de Etica: aparecem diluidas no corpo do texto.");

slideAnalise(2, "ANÁLISE DO RESUMO", [
  { texto: ["“Adopted in May 2018, the European Union's General Data Protection",
            "Regulation (GDPR) requires the consent for processing users' personal",
            "data to be freely given, specific, informed, and unambiguous.”"],
    citacao: true, anota: "Contextualiza" },
  { texto: ["“While prior work has shown that this often is not given (...), no",
            "research has systematically studied how consent notices are currently",
            "implemented and whether they conform to GDPR in mobile apps.”"],
    citacao: true, anota: "Declara a lacuna" },
  { texto: ["“To close this research gap, we perform the first large-scale study into",
            "consent notices for third-party tracking in Android apps (...)”"],
    citacao: true, anota: "Objetivo" },
  { texto: ["“(...) we propose a mostly automated and scalable approach to identify",
            "the currently implemented consent notices and apply it to a set of",
            "239,381 Android apps.”"],
    citacao: true, anota: "Método empregado" },
  { texto: ["“We find 30,160 apps do not even attempt to implement consent notices",
            "(...) out of 13,082 apps implemented consent notices, we identify 2,688",
            "(20.54%) apps violate at least one of the GDPR consent requirements.”"],
    citacao: true, anota: "Apresentação dos resultados" },
  { texto: ["KEYWORDS:   Android Security;  Consent;  GDPR;  User Privacy"],
    destaque: true, anota: "Palavras-chave" },
], "50 segundos. Cada movimento cabe em uma ou duas frases. As palavras-chave trazem Consent e GDPR, mas nao trazem tracking nem third-party, que estao no titulo: isso diz como os autores querem ser encontrados.");

slideAnalise(3, "ANÁLISE DA INTRODUÇÃO", [
  { texto: ["“Every time we load a page on a commercial website or use a mobile app,",
            "information about us and about what we are doing online will be",
            "broadcast to large numbers of companies, most notably for advertising",
            "purposes.”"],
    citacao: true, anota: "Contextualiza pelo fenômeno, não pela técnica" },
  { texto: ["“However, no study has systematically analyzed the current practices of",
            "implemented consent notices in mobile apps or, more importantly, whether",
            "these consent notices can be legally justified under GDPR.”"],
    citacao: true, anota: "Descreve a problemática e a lacuna" },
  { texto: ["“Our work is the first to close this research gap by answering the",
            "following research questions:”",
            "   •  Do mobile apps implement any form of consent notices?",
            "   •  Can these consent notices be legally justified under GDPR?",
            "   •  Are developers aware of the GDPR consent requirements and the",
            "      violations of their implementation?"],
    citacao: true, anota: "Objetivo, em três questões de pesquisa" },
  { texto: ["“In summary, our paper makes the following contributions: (...)”"],
    citacao: true, anota: "Contribuições, declaradas em lista" },
], "50 segundos. As tres questoes sao respondiveis por medicao, nao sao temas: e o que a Aula 05 e 06 chama de problema bem formulado. A terceira exige um metodo diferente das outras duas, o que justifica a existencia da secao 5. Mencionar a nota de rodape 1: eles dizem violacao POTENCIAL de proposito, para nao emitir juizo juridico, que seria consultoria legal regulada.");

slideAnalise(4, "ANÁLISE DO MÉTODO", [
  { texto: ["“we crawled all free Android apps from October 2021 to March 2022 on the",
            "Google Play store (EEA country location-based) based on the list of apps",
            "from AndroZoo [1] (which has 5,8M of Android apps' names).”"],
    citacao: true, anota: "Fonte do corpus" },
  { texto: ["“Apps have at least 10,000 downloads (...)”",
            "“Apps request sensitive permission such as GPS location, contact (...)”",
            "“Apps have the latest update later than May 2018, when GDPR went into",
            "effect (...)”"],
    citacao: true, anota: "Três critérios de inclusão, declarados" },
  { texto: ["“we successfully analyzed about 239,381 (95.38% of 250,972) apps by",
            "using dynamic analysis”"],
    citacao: true, anota: "Reportam a taxa de sucesso da ferramenta" },
  { mono: true, destaque: true, texto: [
      "5.800.000    nomes na lista do AndroZoo",
      "  250.972    após os três critérios",
      "  239.381    analisados com sucesso   (95,38%)",
      "   13.082    com aviso de consentimento",
      "    2.688    violam ao menos um requisito   (20,54% dos 13.082)",
      "   30.160    não têm aviso nenhum"],
    anota: "O funil amostral" },
], "50 segundos. Dois pontos: o denominador MUDA no meio do funil, os 20,54% sao sobre os 13.082 e nao sobre os 239 mil; e os 30.160 sao categoria separada, nao tem aviso nenhum. O AndroZoo e a mesma fonte que eu vou usar no meu TCC.");

slideAnalise(5, "ANÁLISE DOS RESULTADOS", [
  { texto: ["“2,181 (16,67% of 13,082) apps sent personal data to third-party data",
            "controllers before given explicit consent.”"],
    citacao: true, anota: "Envio antes do consentimento" },
  { texto: ["“1,084 (8.28% of 13,082) apps sent to third-party data controllers in",
            "which their consent notices do not offer a way to refuse consent.”"],
    citacao: true, anota: "Sem forma de recusar" },
  { texto: ["“Further, 134 apps that still sent data after explicitly opting out of",
            "the data sharing from the consent user interface.”"],
    citacao: true, anota: "Envio depois da recusa" },
  { texto: ["“nearly 99% of apps at least sharing this personal data”",
            "         (o identificador de anúncio do Android, o AAID)"],
    citacao: true, anota: "Qual dado é compartilhado" },
  { texto: ["Como validam:  a tela prova que o aviso existe; o tráfego de rede prova",
            "que o dado saiu. Um instrumento sozinho não sustentaria a afirmação.",
            "",
            "Não há intervalo de confiança, não há tamanho de efeito e não há grupo",
            "de controle. É exatamente a lacuna que o meu trabalho preenche."],
    destaque: true, anota: "O que falta, e é a minha contribuição" },
], "50 segundos. Presenca nao e transmissao: detectar a biblioteca no aplicativo nao prova que ela enviou dado. E o mesmo par de instrumentos que eu vou precisar.");

slideAnalise(6, "ANÁLISE DA DISCUSSÃO", [
  { texto: ["“Our results thus far have shown that many apps do not even attempt to",
            "implement consent notices (...). Given these insights, we now discuss",
            "further the problems.”"],
    citacao: true, anota: "Retoma o resultado antes de interpretar" },
  { texto: ["6.1  Widespread Violation of GDPR Consent",
            "“On the legal side, EU regulators have already been active. Recently,",
            "the Norwegian DPA imposed a fine of $7.17M on Grindr (...). The France",
            "DPA fined Google $170M and Facebook $68M (...)”"],
    citacao: true, anota: "Confronta com casos reais, não só com a literatura" },
  { texto: ["6.2  Transparency of Processing Users' Data"],
    destaque: true, anota: "Implicação normativa" },
  { texto: ["6.3  Lack of Support for Developers",
            "“Based on the received responses, there is a clear need for better",
            "information and documentation from third-party services and assurance",
            "tools that help developers comply with strict law standards (...)”"],
    citacao: true, anota: "Desloca a causa, em vez de acusar" },
], "50 segundos. O movimento mais interessante e a 6.3: depois de medir 2.688 violacoes, eles NAO concluem que os desenvolvedores agem de ma-fe. Usam as respostas coletadas na secao 5 para reenquadrar a causa. E o mesmo movimento que o meu proprio resultado pede.");

slideAnalise(7, "ANÁLISE DA CONCLUSÃO", [
  { texto: ["“In this paper, we performed a systematic study into consent notices of",
            "third-party tracking in 239,381 Android apps in the wild to understand",
            "the current practices and the current state of GDPR's consent",
            "violations.”"],
    citacao: true, anota: "Retoma objetivo e escala" },
  { texto: ["“We found 30,160 apps do not even attempt to implement consent notices",
            "(...) we identified 2,688 (20.54%) apps potentially violate at least one",
            "of the GDPR consent requirements (...)”"],
    citacao: true, anota: "Infere a partir dos dados obtidos" },
  { texto: ["“Our study showed the urgent need for more transparent processing of",
            "personal data and supporting developers in this endeavor (...)”"],
    citacao: true, anota: "Implicação normativa" },
  { texto: ["Comparando o resumo com a conclusão:",
            "",
            "   RESUMO         “2,688 apps VIOLATE at least one (...)”",
            "   CONCLUSÃO      “2,688 apps POTENTIALLY VIOLATE at least one (...)”",
            "",
            "A nota de rodapé 1 diz que “potential” foi escolha deliberada, para não",
            "emitir juízo jurídico. A conclusão está correta e o resumo escorrega."],
    destaque: true, anota: "O que o resumo promete e o que a conclusão entrega" },
], "50 segundos. Esta e a observacao mais forte da apresentacao: uma inconsistencia real num artigo de conferencia A*, encontrada comparando resumo e conclusao.");

// =====================================================================
// 13 — FECHAMENTO
// =====================================================================
s = pres.addSlide();
titulo(s, "O que este artigo muda no meu TCC");

const f3 = (W - M * 2 - 0.5) / 3;
[["MÉTODO", "Adoto o par estático e dinâmico: detectar a biblioteca no aplicativo e confirmar no tráfego que o dado saiu."],
 ["ESCRITA", "Copio a disciplina de reportar a taxa de sucesso da ferramenta e o cuidado de linguagem ao falar de lei."],
 ["LACUNA", "Aplico ao parque governamental brasileiro, que o artigo não cobre, e acrescento grupo de controle pareado."]]
.forEach((c, i) => {
  cartao(s, M + (f3 + 0.25) * i, 1.15, f3, 1.8, c[0], c[1], TEAL);
});

s.addShape(pres.ShapeType.roundRect, {
  x: M, y: 3.2, w: W - M * 2, h: 1.32, fill: { color: NAVY }, rectRadius: 0.05,
});
s.addText("E me deixa uma pergunta que eu não tinha antes:", {
  x: M + 0.3, y: 3.4, w: W - M * 2 - 0.6, h: 0.3, isTextBox: true, margin: 0,
  fontFace: SANS, fontSize: 11.5, color: "9FC5DA",
});
s.addText("se o rastreamento nos aplicativos de governo não é comercial, o que explica ele estar lá?", {
  x: M + 0.3, y: 3.72, w: W - M * 2 - 0.6, h: 0.55, isTextBox: true, margin: 0,
  fontFace: SERIF, fontSize: 16, italic: true, color: WHITE,
});
s.addNotes("30 segundos. Fecha e para de falar.");

// =====================================================================
const saida = "/home/user/TCC/seminario/seminario-analise-de-artigo.pptx";
pres.writeFile({ fileName: saida }).then(() => console.log("gerado:", saida));
