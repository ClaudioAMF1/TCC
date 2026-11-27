"""Monta os slides da defesa final do Capstone I sobre os fundos do template do IDP.

Uso: python monta_slides_defesa_final.py TEMPLATE.pptx main.bbl SAIDA.pptx

Os slides seguem a ordem do texto do TCC, no modelo do Capstone do IDP: uma divisória por
seção (1 Introdução, 2 Revisão bibliográfica, 3 Metodologia, 4 Resultados e discussão,
5 Conclusão) e, em cada slide, o número da subseção correspondente do texto. Os fundos são os
do template de slides do IDP. Os gráficos são nativos do PowerPoint (editáveis); as figuras
vêm dos artigos de acesso aberto citados, com a fonte embaixo (pasta recursos/figuras); os
ícones são do conjunto Lucide, de licença ISC (pasta recursos/icones, gerados por
recursos/gera_icones.js). As referências aparecem todas, numeradas no padrão IEEE, como no
texto; as citações dos slides usam os mesmos números, lidos do .bbl.

O script grava também, ao lado do .pptx, as notas do apresentador (notas-apresentador.txt) e
o roteiro (roteiro-defesa-final.md), e informa o tempo estimado de fala.
"""
import copy
import re
import sys
import unicodedata
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

TPL, BBL, SAIDA = sys.argv[1:4]
PASTA = Path(__file__).resolve().parent
ICONES = PASTA / "recursos" / "icones"
FIGURAS = PASTA / "recursos" / "figuras"
bbl = open(BBL, encoding="utf-8").read()
NUM = {k: i for i, k in enumerate(re.findall(r"\\bibitem\{([^}]+)\}", bbl), 1)}


def ref(*chaves):
    """Número IEEE de cada referência, na ordem em que aparece no texto do TCC."""
    return ", ".join(f"[{NUM[k]}]" for k in chaves)


# cores e fonte do template do IDP (as mesmas da versão anterior dos slides)
NAVY = RGBColor(0x00, 0x3D, 0x69)
MID = RGBColor(0x74, 0x99, 0xBF)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
GREY = RGBColor(0x7F, 0x7F, 0x7F)
DARK = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xDC, 0xE6, 0xF1)
SILVER = RGBColor(0xD0, 0xD0, 0xD0)
FONT = "Calibri"

prs = Presentation(TPL)
tpl_slides = list(prs.slides)
N_TPL = len(tpl_slides)
BLANK = next(l for l in prs.slide_layouts if l.name == "BLANK")
FUNDO = []    # fundo de cada slide novo, para a cor do número
TITULOS = []  # título de cada slide, para o roteiro
TIPO = []     # "fala", "divisoria", "referencias" ou "encerramento"


def nova(fundo, titulo, tipo="fala"):
    """Slide novo com o fundo (imagem) do slide `fundo` (1 a 14) do template."""
    sl = prs.slides.add_slide(BLANK)
    for sh in list(sl.shapes):
        sh._element.getparent().remove(sh._element)
    src = tpl_slides[fundo - 1]
    bg = copy.deepcopy(src._element.cSld.find(qn("p:bg")))
    blip = bg.find(".//" + qn("a:blip"))
    part = src.part.related_part(blip.get(qn("r:embed")))
    blip.set(qn("r:embed"), sl.part.relate_to(part, RT.IMAGE))
    cs = sl._element.cSld
    if cs.find(qn("p:bg")) is not None:
        cs.remove(cs.find(qn("p:bg")))
    cs.insert(0, bg)
    FUNDO.append(fundo)
    TITULOS.append(titulo)
    TIPO.append(tipo)
    return sl


def _run(p, t, size, bold, cor, sub=False, italico=False):
    r = p.add_run()
    r.text = t
    f = r.font
    f.name = FONT
    f.size = Pt(size)
    f.bold = bold
    f.italic = italico
    f.color.rgb = cor
    if sub:
        r.font._rPr.set("baseline", "-25000")
    return r


def texto(sl, x, y, w, h, paras, anchor="t"):
    """paras: lista de dicts {runs:[(texto, pt, negrito, cor[, sub, itálico])], align, after, spacing}."""
    box = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for i, pd in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[pd.get("align", "l")]
        if "after" in pd:
            p.space_after = Pt(pd["after"])
        p.line_spacing = pd.get("spacing", 1.0)
        for run in pd["runs"]:
            _run(p, *run)
    return box


def P(t, size=18, bold=False, cor=GREY, align="l", after=None, spacing=1.0):
    d = {"runs": [(t, size, bold, cor)], "align": align, "spacing": spacing}
    if after is not None:
        d["after"] = after
    return d


def R(runs, align="l", after=None, spacing=1.0):
    d = {"runs": runs, "align": align, "spacing": spacing}
    if after is not None:
        d["after"] = after
    return d


def forma(sl, x, y, w, h, cor, tipo=MSO_SHAPE.RECTANGLE, linha=None):
    sh = sl.shapes.add_shape(tipo, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = cor
    if linha is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = linha
        sh.line.width = Pt(1.25)
    st = sh._element.find(qn("p:style"))
    if st is not None:
        sh._element.remove(st)
    if sh.has_text_frame:
        sh.text_frame.text = ""
    return sh


def icone(sl, nome, cor, x, y, d, fundo=None, escala=0.58):
    """Ícone (recursos/icones/<nome>_<cor>.png) num círculo de diâmetro d, ou solto se fundo=None."""
    if fundo is not None:
        forma(sl, x, y, d, d, fundo, MSO_SHAPE.OVAL)
        s = d * escala
    else:
        s = d
    sl.shapes.add_picture(str(ICONES / f"{nome}_{cor}.png"), Inches(x + (d - s) / 2), Inches(y + (d - s) / 2), Inches(s), Inches(s))


def figura(sl, nome, x, y, w=None, h=None):
    """Figura de artigo (recursos/figuras/<nome>.png) com largura ou altura dada; devolve (w, h)."""
    pic = sl.shapes.add_picture(str(FIGURAS / f"{nome}.png"), Inches(x), Inches(y),
                                Inches(w) if w else None, Inches(h) if h else None)
    pic.line.color.rgb = SILVER
    pic.line.width = Pt(0.75)
    return pic.width / 914400, pic.height / 914400


def barra_titulo(sl, t, sub=None, num=None):
    """Título na barra azul do fundo 13, com o número da subseção do texto à esquerda."""
    runs = ([(num + "  ", 34, True, MID)] if num else []) + [(t, 34, True, LIGHT)]
    texto(sl, 0.65, 0.42, 11.2, 0.85, [R(runs)], anchor="m")
    if sub:
        texto(sl, 0.9, 1.88, 11.6, 0.4, [P(sub, 18, False, GREY)])


def titulo_livre(sl, t, num=None, cor=MID, x=1.0, y=0.55, w=6.0):
    """Título grande sem barra (fundos brancos 4 e 6), com o número da subseção em cima."""
    if num:
        texto(sl, x, y, w, 0.4, [P(num, 18, True, NAVY)])
    texto(sl, x, y + 0.38, w, 0.85, [P(t, 40, True, cor)])


def notas(sl, *paragrafos):
    tf = sl.notes_slide.notes_text_frame
    tf.text = paragrafos[0]
    for extra in paragrafos[1:]:
        tf.add_paragraph().text = extra


def tabela(sl, x, y, larguras, cab, linhas, size=13, cab_size=13, alt_h=0.6, cab_h=0.45):
    """Tabela com cabeçalho azul-marinho e linhas alternadas; primeira coluna em negrito."""
    nl, nc = len(linhas) + 1, len(cab)
    shp = sl.shapes.add_table(nl, nc, Inches(x), Inches(y), Inches(sum(larguras)), Inches(cab_h + alt_h * (nl - 1)))
    tbl = shp.table
    tblPr = tbl._tbl.tblPr
    for k in ("firstRow", "bandRow"):
        tblPr.set(k, "0")
    for j, w in enumerate(larguras):
        tbl.columns[j].width = Inches(w)
    for i in range(nl):
        tbl.rows[i].height = Inches(cab_h if i == 0 else alt_h)
        for j in range(nc):
            c = tbl.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.08)
            c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = NAVY
                conteudo, tam, neg, cor = cab[j], cab_size, True, WHITE
            else:
                c.fill.fore_color.rgb = PALE if i % 2 == 1 else WHITE
                conteudo, tam = linhas[i - 1][j], size
                neg = j == 0
                cor = NAVY if neg else DARK
            p = c.text_frame.paragraphs[0]
            c.text_frame.word_wrap = True
            p.alignment = PP_ALIGN.LEFT
            _run(p, conteudo, tam, neg, cor)
    return tbl


def _fonte(tf, tam, neg, cor):
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(tam)
            r.font.bold = neg
            r.font.color.rgb = cor


def barras(sl, x, y, w, h, cats, vals, cores, rotulos, horizontal=True, maximo=None, tam_cat=15, tam_rot=15,
           gap=55, cor_txt=DARK, cor_rot=NAVY):
    """Gráfico de barras nativo, de uma série, com cor e rótulo próprios em cada barra."""
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("valores", vals)
    tipo = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    ch = sl.shapes.add_chart(tipo, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    ch.has_legend = False
    ch.has_title = False
    ch.font.name = FONT
    ch.font.size = Pt(tam_cat)
    ch.font.color.rgb = cor_txt
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.vary_by_categories = False
    ser = plot.series[0]
    for i, (c, r) in enumerate(zip(cores, rotulos)):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = c
        pt.format.line.fill.background()
        dl = pt.data_label
        dl.has_text_frame = True
        dl.text_frame.text = r
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
        _fonte(dl.text_frame, tam_rot, True, cor_rot)
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    va.minimum_scale = 0
    if maximo:
        va.maximum_scale = maximo
    ca = ch.category_axis
    ca.has_major_gridlines = False
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = SILVER
    ca.tick_labels.font.size = Pt(tam_cat)
    ca.tick_labels.font.name = FONT
    ca.tick_labels.font.color.rgb = cor_txt
    if horizontal:
        ca.reverse_order = True
    return ch


def rosca(sl, x, y, d, vals, cores, buraco=66):
    """Gráfico de rosca nativo, sem legenda (os números vão em caixas de texto ao lado)."""
    cd = CategoryChartData()
    cd.categories = [str(i + 1) for i in range(len(vals))]
    cd.add_series("valores", vals)
    ch = sl.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(x), Inches(y), Inches(d), Inches(d), cd).chart
    ch.has_legend = False
    ch.has_title = False
    plot = ch.plots[0]
    plot.vary_by_categories = True
    for i, c in enumerate(cores):
        pt = plot.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = c
        pt.format.line.color.rgb = WHITE
    hs = plot._element.find(qn("c:holeSize"))
    hs.set("val", str(buraco))
    return ch


def seta(sl, x, y, w=0.3, h=0.3, cor=MID):
    forma(sl, x, y, w, h, cor, MSO_SHAPE.RIGHT_ARROW)


def divisoria(num, titulo, itens):
    """Divisória de seção, como as do texto: número grande, título e o que vem na seção."""
    s = nova(2, f"{num} {titulo}", "divisoria")
    texto(s, 0.7, 0.9, 3.5, 4.9, [P(num, 250, True, MID, "c")], anchor="m")
    texto(s, 4.45, 1.55, 8.3, 1.0, [P(titulo, 44, True, WHITE)], anchor="b")
    paras = [R([(f"{n}   " if n else "", 20, True, MID), (t, 20, False, PALE)], after=10) for n, t in itens]
    texto(s, 4.45, 2.85, 8.3, 3.4, paras)
    notas(s, f"LEMBRETE (não precisa falar). Divisória da Seção {num}: {titulo.lower()}. Passe direto para o próximo slide.")
    return s


def escala_landis(sl, x, y, w, marcas=(), limiar=True, h=0.5):
    """Escala de Landis e Koch em faixas, com o limiar do estudo (0,6) e marcas opcionais."""
    faixas = [("< 0", "pobre"), ("0–0,20", "leve"), ("0,21–0,40", "razoável"), ("0,41–0,60", "moderada"),
              ("0,61–0,80", "substancial"), ("0,81–1", "quase perfeita")]
    cores = [SILVER, RGBColor(0xC4, 0xD3, 0xE4), PALE, MID, RGBColor(0x2E, 0x5F, 0x8C), NAVY]
    fw = w / len(faixas)
    for k, ((faixa, nome), cor) in enumerate(zip(faixas, cores)):
        fx = x + k * fw
        forma(sl, fx, y, fw - 0.03, h, cor)
        ct = NAVY if k < 3 else WHITE
        texto(sl, fx, y, fw - 0.03, h, [P(nome, 14, True, ct, "c")], anchor="m")
        texto(sl, fx, y + h + 0.05, fw - 0.03, 0.3, [P(faixa, 13, False, DARK, "c")])

    def posicao(v):
        # 0 a 1 ocupa as faixas 2 a 6 (cinco faixas de 0,2); valores negativos ficam na primeira
        return x + fw + (w - fw) * max(0.0, min(1.0, v))

    if limiar:
        px = posicao(0.6)
        forma(sl, px - 0.03, y - 0.22, 0.06, h + 0.44, NAVY)
        texto(sl, px - 1.6, y - 0.55, 3.2, 0.3, [P("limiar do estudo: 0,6", 13, True, NAVY, "c")])
    for v, rot in marcas:
        px = posicao(v)
        forma(sl, px - 0.12, y + h + 0.38, 0.24, 0.2, NAVY, MSO_SHAPE.ISOSCELES_TRIANGLE)
        texto(sl, px - 0.9, y + h + 0.6, 1.8, 0.3, [P(rot, 13, True, NAVY, "c")])


COLA = [
    "COLA PARA AS PERGUNTAS (não é para ler em voz alta).",
    "Números: 590 aplicativos achados, 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · AndroZoo: 92 de 396 (23,2%), contra 160 de 190 comerciais (84,2%) · piloto: 75%, 95% e 80% com rastreador; κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · políticas acessíveis: 323 de 396 (81,6%) · nenhum dos 376 declara anúncios na Google Play, contra 33,2% dos 190 comerciais · revisão: 396 resultados, 312 sem repetidos, 148 à leitura completa, 35 lidos, 31 propostas de inclusão (8 já confirmadas) e 113 em aberto.",
    "Por que 10%? Fica bem abaixo da literatura (Andow 42,4%; Samarasinghe 27%), que conta aplicativos; eu conto pares, então é um patamar conservador. Se ficar abaixo, não dá para dizer que o governo é mais transparente que nos outros estudos, só que ficou abaixo do meu patamar. Não é limite da LGPD.",
    "Por que decidir pela proporção, e não pelo intervalo de confiança? Porque analiso todos os aplicativos oficiais, e não uma amostra. O intervalo mostra a precisão e entra como ressalva se incluir os 10%.",
    "Onde a LGPD obriga o órgão a declarar? Transparência (Art. 6º, VI); informação sobre o uso compartilhado e a finalidade (Art. 9º, V); e, no poder público, informar a previsão legal, a finalidade e as práticas, em veículos de fácil acesso (Art. 23, I). A lei não exige o nome do SDK; exige informar o tratamento e o compartilhamento.",
    "Por que só Android? 73,76% dos celulares no Brasil (StatCounter, out. 2026); no iPhone os aplicativos são criptografados e não há ferramenta pública para baixá-los em escala (Kollnig et al., 2022); a seção “Segurança dos dados” é da Google Play. Não quer dizer que o iPhone seja mais seguro.",
    "Como vai observar o tráfego sem celular Android? No emulador do Android Studio, no computador, com o mitmproxy registrando as conexões. Abro cada aplicativo sem login, sem conta pessoal. Se um aplicativo não funcionar no emulador, registro o motivo e reporto quantos foram.",
    "Por que uma hipótese só? Para concentrar o trabalho no que dá para provar no Capstone II: as declarações. A comparação dos aplicativos com dados sensíveis saiu do projeto.",
    "O κ de 0,52 não é baixo? É moderado. Por isso a concordância entre detectores é uma checagem do instrumento, com limiar de 0,6, e não uma hipótese.",
    "Ter o SDK no aplicativo prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos aplicativos.",
    "Quais são os riscos? Bloqueio do download na Google Play (teste em cinco aplicativos em fevereiro); aplicativo que não roda no emulador (motivo registrado e proporção reportada); κ instável com prevalência alta (reporto também as concordâncias positiva e negativa); política genérica (as cinco situações da classificação); achado grave (comunicação prévia ao órgão e, se couber, ao CTIR Gov e à ANPD, com o orientador).",
    "Por que a revisão caiu de 1.531 para 396? Exigi um termo do tema no título, comecei em 2018, quando o GDPR passou a valer e a LGPD foi sancionada, e tirei a questão sobre detecção de bibliotecas, que ficou como fundo no referencial. Os estudos de controle dentro desse escopo continuaram sendo achados.",
    "Você leu todos os artigos? Não. A leitura completa está em andamento: já confirmei parte das decisões lendo o texto inteiro e termino o restante em fevereiro, antes de qualquer resultado.",
    "Por que 63 referências? São 36 artigos sobre o tema (31 deles da revisão sistemática) e 27 de leis, guias da ANPD, ferramentas e métodos (estatística e protocolo da revisão).",
    "De onde vêm as figuras? Dos artigos citados, de acesso aberto, com a fonte embaixo de cada uma: Kollnig et al. (2021 e 2022), Andow et al. (2020) e Zhan et al. (2022). O gráfico das empresas de rastreamento é refeito a partir da Tabela 1 de Binns et al. (2018).",
    "Por que o texto mudou de formato? A disciplina pede o modelo LaTeX do Capstone do IDP: cinco seções e citações numeradas no padrão IEEE. O conteúdo é o mesmo; os resultados da preparação passaram para a seção de resultados.",
    "Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”",
]

# ================================================================ CAPA E AGENDA
# ---------------------------------------------------------------- capa (fundo 1)
s = nova(1, "Capa")
texto(s, 0.84, 0.95, 6.9, 2.75, [P("Rastreamento por terceiros em aplicativos móveis governamentais brasileiros", 36, True, NAVY, spacing=0.92)], anchor="b")
texto(s, 0.84, 3.9, 6.9, 1.0, [P("SDKs embarcados e transparência das declarações de privacidade", 21, False, GREY, spacing=1.05)])
texto(s, 0.84, 5.25, 6.9, 1.2, [P("Claudio da Aparecida Meireles Filho", 18, True, NAVY, after=2),
                                P("Orientador: Prof. Eduardo Arthur Izycki", 16, False, GREY)])
texto(s, 8.75, 2.6, 4.1, 2.4, [P("PROJETO CAPSTONE I", 20, True, WHITE, after=6),
                               P("Defesa final", 18, False, LIGHT, after=18),
                               P("Ciência da Computação", 16, False, PALE),
                               P("IDP · 2026", 16, False, PALE)])
notas(s, "Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu trabalho trata do rastreamento por terceiros nos aplicativos do governo brasileiro. Esses aplicativos trazem código de outras empresas, que pode coletar dados de quem usa. Quero descobrir que código é esse e se o governo avisa o cidadão sobre ele.")

# ---------------------------------------------------------------- agenda (fundo 9)
s = nova(9, "Agenda")
texto(s, 1.15, 2.78, 2.34, 0.74, [P("AGENDA", 44, True, GREY)])
caps = [("1", "INTRODUÇÃO", ["Motivação, problema e justificativa", "Objetivos e hipótese"]),
        ("2", "REVISÃO BIBLIOGRÁFICA", ["Fundamentação teórica e trabalhos correlatos", "Lacuna e contribuição"]),
        ("3", "METODOLOGIA", ["Etapas, plataforma, detecção e declarações", "Revisão sistemática e cronograma"]),
        ("4", "RESULTADOS E DISCUSSÃO", ["Resultados preliminares", "Resultados esperados e limitações"]),
        ("5", "CONCLUSÃO", ["Síntese e próximos passos; referências"])]
y = 0.5
for num, cab, lista in caps:
    forma(s, 6.0, y, 0.44, 0.44, NAVY, MSO_SHAPE.OVAL)
    texto(s, 6.0, y, 0.44, 0.44, [P(num, 16, True, WHITE, "c")], anchor="m")
    texto(s, 6.6, y, 5.95, 0.44, [P(cab, 17, True, NAVY)], anchor="m")
    y += 0.47
    for it in lista:
        texto(s, 6.6, y, 5.95, 0.34, [P(it, 15, False, DARK)], anchor="m")
        y += 0.34
    y += 0.1
notas(s, "A apresentação segue as cinco seções do texto, na ordem do modelo do Capstone. Começo pela introdução, com o problema, a justificativa, os objetivos e a hipótese. Depois vem a revisão bibliográfica, com a fundamentação, os estudos de base e a lacuna. Em seguida, a metodologia, os resultados preliminares e as limitações. No fim, a conclusão.")

# ================================================================ 1 INTRODUÇÃO
divisoria("1", "INTRODUÇÃO", [("", "Motivação"), ("1.1", "Problema de pesquisa"), ("1.2", "Justificativa"),
                              ("1.3", "Objetivos"), ("1.4", "Hipótese")])

# ---------------------------------------------------------------- motivação (fundo 6)
s = nova(6, "Motivação")
titulo_livre(s, "MOTIVAÇÃO", "1", cor=GREY)
texto(s, 1.0, 1.8, 6.9, 0.5, [P("Serviços públicos no celular", 22, False, GREY)])
texto(s, 1.0, 2.5, 6.6, 1.0, [R([("50 mi+", 54, True, NAVY)])], anchor="m")
texto(s, 1.0, 3.45, 6.6, 0.6, [P("instalações do Meu INSS e do Meu SUS Digital, cada um, na Google Play", 16, False, DARK)])
for k, (ic, txt) in enumerate([("sdk", "Os aplicativos embutem SDKs de outras empresas, que podem coletar identificadores e dados de uso."),
                               ("usuarios", "O cidadão nem sempre tem alternativa ao aplicativo oficial.")]):
    y0 = 4.15 + k * 0.78
    icone(s, ic, "branco", 1.0, y0, 0.58, NAVY)
    texto(s, 1.75, y0 - 0.04, 5.9, 0.68, [P(txt, 16, False, DARK)], anchor="m")
texto(s, 1.0, 5.75, 6.6, 0.6, [P("Um SDK no código não prova, sozinho, que houve envio de dados.", 16, True, NAVY)], anchor="m")
caixas = [("celular", "Aplicativo do governo", "o que o cidadão instala"), ("sdk", "SDK de terceiro", "mapas, estatísticas, anúncios"),
          ("servidor", "Servidor da empresa", "para onde os dados podem ir")]
cy = 1.68
for i, (ic, a, b) in enumerate(caixas):
    forma(s, 8.82, cy, 3.45, 0.78, WHITE)
    icone(s, ic, "marinho", 8.95, cy + 0.14, 0.5)
    texto(s, 9.6, cy + 0.04, 2.6, 0.7, [P(a, 16, True, NAVY), P(b, 13, False, GREY)], anchor="m")
    if i < 2:
        forma(s, 10.4, cy + 0.83, 0.3, 0.26, MID, MSO_SHAPE.DOWN_ARROW)
    cy += 1.14
texto(s, 8.75, 4.75, 3.6, 0.75, [P("Pergunta: em que medida esses SDKs estão declarados ao cidadão?", 15, True, WHITE, "c", spacing=1.05)], anchor="m")
notas(s, "Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada um. Esses aplicativos não têm só o código do órgão: trazem componentes prontos de outras empresas, os SDKs, para mapas, notificações e estatísticas de uso. Alguns desses SDKs coletam dados de quem usa. Um cuidado importante: o SDK estar no código não prova que ele enviou dados.")

# ---------------------------------------------------------------- 1.1 problema (fundo 13)
s = nova(13, "1.1 Problema de pesquisa")
barra_titulo(s, "PROBLEMA DE PESQUISA", num="1.1")
icone(s, "duvida", "branco", 0.9, 2.1, 0.95, NAVY)
texto(s, 2.15, 1.95, 10.3, 1.75, [P("Em que medida os SDKs de rastreamento de terceiros embarcados nos aplicativos Android oficiais do governo brasileiro estão declarados nas políticas de privacidade e na seção “Segurança dos dados” da Google Play?", 23, True, NAVY, spacing=1.05)], anchor="m")
forma(s, 0.9, 4.05, 11.55, 2.25, PALE)
texto(s, 1.15, 4.2, 3.1, 1.95, [P("Par aplicativo–SDK", 20, True, NAVY, after=4), P("a unidade que será contada e classificada", 15, False, DARK)], anchor="m")
forma(s, 4.35, 4.6, 1.9, 1.15, NAVY)
icone(s, "celular", "branco", 4.45, 4.82, 0.7)
texto(s, 5.1, 4.6, 1.15, 1.15, [P("Aplicativo X", 15, True, WHITE)], anchor="m")
for k, (ic, nome) in enumerate([("grafico", "estatísticas"), ("local", "mapas"), ("enviar", "notificações")]):
    y0 = 4.18 + k * 0.68
    seta(s, 6.4, y0 + 0.17, 0.32, 0.24)
    forma(s, 6.85, y0, 2.6, 0.56, WHITE, linha=MID)
    icone(s, ic, "marinho", 6.95, y0 + 0.08, 0.4)
    texto(s, 7.45, y0, 1.95, 0.56, [P("SDK de " + nome, 14, True, NAVY)], anchor="m")
forma(s, 9.75, 4.6, 2.45, 1.15, MID)
texto(s, 9.85, 4.6, 2.25, 1.15, [P("= 3 pares", 22, True, WHITE, "c"), P("cada um classificado", 13, False, WHITE, "c")], anchor="m")
notas(s, "O problema da pesquisa é: em que medida os SDKs de rastreamento dos aplicativos oficiais do governo estão declarados ao cidadão, na política de privacidade e na seção “Segurança dos dados” da Google Play? A unidade é o par aplicativo–SDK: cada SDK encontrado em cada aplicativo forma um par. Um aplicativo com três SDKs gera três pares, e cada par é classificado de acordo com as declarações.")

# ---------------------------------------------------------------- 1.2 justificativa (fundo 5)
s = nova(5, "1.2 Justificativa")
texto(s, 0.55, 0.5, 3.7, 0.4, [P("1.2", 18, True, MID)])
texto(s, 0.55, 0.85, 3.7, 0.7, [P("JUSTIFICATIVA", 30, True, NAVY)])
colj = [(0.55, 3.6, "lei", "marinho", NAVY, DARK, "Jurídica",
         "A LGPD trata dados de saúde como sensíveis (Art. 5º, II, e Art. 11), vincula o poder público à finalidade pública (Art. 23) e limita a transferência internacional (Art. 33). E o cidadão nem sempre tem alternativa ao aplicativo oficial."),
        (4.97, 3.55, "globo", "branco", WHITE, WHITE, "Soberania de dados",
         f"O rastreamento se concentra em poucas empresas estrangeiras, como Google e Facebook {ref('binns2018', 'kollnig2021before')}. Medir essa dependência é condição para qualquer debate sobre ela."),
        (9.41, 3.5, "comparar", "branco", WHITE, WHITE, "Metodológica",
         "Duas ferramentas podem achar quantidades diferentes de rastreadores no mesmo pacote. Antes de interpretar a taxa, é preciso saber quanto ela depende do detector.")]
for x0, w0, ic, cic, ccab, ctxt, cab, txt in colj:
    icone(s, ic, cic, x0, 1.95, 0.85)
    texto(s, x0, 3.0, w0, 0.55, [P(cab, 24, True, ccab)])
    texto(s, x0, 3.65, w0, 2.6, [P(txt, 16, False, ctxt, spacing=1.05)])
notas(s, "Por que isso importa? Primeiro, pela lei e pelo cidadão: a LGPD protege dados sensíveis, como os de saúde, cobra finalidade pública, e o cidadão nem sempre tem alternativa ao aplicativo oficial. Segundo, pela soberania de dados: o rastreamento se concentra em poucas empresas estrangeiras. Terceiro, por uma razão de método: ferramentas diferentes acham quantidades diferentes de rastreadores, e é preciso medir isso.")

# ---------------------------------------------------------------- 1.3 objetivos (fundo 13)
s = nova(13, "1.3 Objetivos")
barra_titulo(s, "OBJETIVOS", num="1.3")
forma(s, 0.9, 1.95, 11.55, 1.2, PALE)
icone(s, "alvo", "branco", 1.08, 2.18, 0.75, NAVY)
texto(s, 2.05, 2.02, 10.2, 0.32, [P("OBJETIVO GERAL", 13, True, NAVY)])
texto(s, 2.05, 2.32, 10.25, 0.8, [P("Medir a proporção de pares aplicativo–SDK de rastreamento sem declaração compatível, comparando os SDKs encontrados no código com a política de privacidade e a seção “Segurança dos dados”, à luz da LGPD.", 16, False, DARK, spacing=1.0)], anchor="m")
objs = [("a)", "Revisar a lista de aplicativos", "governo", "Confirmar órgão e esfera dos 376 aplicativos pelo nome jurídico", "Lista final e taxa de erro"),
        ("b)", "Listar os SDKs", "scan", "Baixar a versão atual e rodar três detectores", "Pares aplicativo–SDK, com a evidência"),
        ("c)", "Classificar as declarações", "documento", "Ler a política e a “Segurança dos dados” e classificar cada par", "Proporção sem declaração: teste da H1"),
        ("d)", "Registrar o tráfego", "rede", "Executar uma subamostra no emulador Android", "Destinos, país e se estão declarados"),
        ("e)", "Medir a concordância", "comparar", "Calcular o κ de Fleiss entre os detectores", "Quanto a taxa depende da ferramenta")]
CWo, GPo = 2.19, 0.15
for k, (letra, nome, ic, faz, res) in enumerate(objs):
    x0 = 0.9 + k * (CWo + GPo)
    forma(s, x0, 3.35, CWo, 0.78, NAVY)
    texto(s, x0 + 0.12, 3.35, CWo - 0.2, 0.78, [R([(letra + " ", 15, True, MID), (nome, 15, True, WHITE)], spacing=0.95)], anchor="m")
    forma(s, x0, 4.13, CWo, 2.17, WHITE, linha=SILVER)
    icone(s, ic, "marinho", x0 + 0.12, 4.25, 0.42)
    texto(s, x0 + 0.12, 4.75, CWo - 0.24, 0.95, [P(faz, 14, False, DARK, spacing=0.95)])
    texto(s, x0 + 0.12, 5.68, CWo - 0.24, 0.6, [P(res, 14, True, NAVY, spacing=0.95)], anchor="m")
notas(s, "O objetivo geral é medir a proporção de pares aplicativo–SDK sem declaração compatível, à luz da LGPD. São cinco objetivos específicos. Primeiro, revisar os 376 aplicativos oficiais e medir quanto a classificação automática errou. Segundo, baixar a versão atual de cada aplicativo e listar os SDKs com três detectores. Terceiro, ler as declarações e classificar cada par; é daí que sai a proporção que testa a hipótese. Quarto, registrar o tráfego de uma parte dos aplicativos num emulador. Quinto, medir se os detectores concordam, com o kappa de Fleiss.")

# ---------------------------------------------------------------- 1.4 hipótese (fundo 13)
s = nova(13, "1.4 Hipótese")
barra_titulo(s, "HIPÓTESE", num="1.4")
forma(s, 0.9, 1.95, 5.75, 2.35, NAVY)
texto(s, 1.15, 2.07, 5.3, 2.15, [P("H1", 30, True, MID, after=4),
                                 P("Ao menos 10% dos pares aplicativo–SDK de rastreamento não terão declaração compatível na política de privacidade nem na seção “Segurança dos dados” da Google Play.", 18, True, WHITE, spacing=1.05)])
texto(s, 0.9, 4.45, 5.75, 0.32, [P("CRITÉRIO DE DECISÃO", 13, True, MID)])
texto(s, 0.9, 4.77, 5.75, 0.8, [P("Confirmada se a proporção de pares sem declaração compatível for de 10% ou mais; refutada se for menor. O IC95% mostra a precisão.", 15, False, DARK, spacing=1.0)])
forma(s, 1.5, 5.62, 5.15, 0.72, PALE)
texto(s, 1.65, 5.62, 4.9, 0.72, [R([("Por que 10%? ", 14, True, NAVY), ("As taxas da literatura contam aplicativos, e não pares; por isso, um patamar bem mais baixo e conservador.", 14, False, NAVY)], spacing=0.95)], anchor="m")
texto(s, 7.05, 1.95, 5.4, 0.32, [P("BASE NA LITERATURA (% DE APLICATIVOS)", 13, True, MID)])
barras(s, 6.95, 2.25, 5.5, 2.15, [f"Andow et al. {ref('andow2020')}", f"Samarasinghe et al. {ref('samarasinghe2022')}", "Patamar da H1 (pares)"],
       [42.4, 27.0, 10.0], [NAVY, NAVY, MID], ["42,4%", "27%", "10%"], maximo=60, tam_cat=14, tam_rot=16, gap=45)
texto(s, 7.05, 4.42, 5.4, 0.95, [P("Andow: até 42,4% dos aplicativos omitiam ou declaravam errado fluxos de dados sensíveis (13.796). Samarasinghe: aplicativos de governo que enviavam informação sensível a terceiros ou sem criptografia (1.166).", 12, False, GREY, spacing=1.0)])
texto(s, 7.05, 5.45, 5.4, 0.9, [R([(f"Também apoiam: ", 13, True, NAVY), (f"Carlsson et al. {ref('carlsson2022')}, políticas que divergiam dos dados enviados em 32 aplicativos públicos finlandeses; Kollnig et al. {ref('kollnig2022ios')}, falta de transparência sobre o rastreamento no Android e no iOS.", 13, False, DARK)], spacing=1.0)])
notas(s, "A pesquisa tem uma hipótese só, construída a partir da literatura. Andow e colegas analisaram quase 14 mil aplicativos e viram que até 42,4% omitiam ou declaravam errado para onde iam dados sensíveis. Samarasinghe e colegas, em 1.166 aplicativos de governo, viram que 27% enviavam informações sensíveis a terceiros ou sem criptografia. Carlsson e colegas e Kollnig e colegas também apontaram divergências e falta de transparência. Daí a hipótese: pelo menos 10% dos pares aplicativo–SDK não terão declaração compatível; ela se confirma se a proporção for de 10% ou mais. O patamar é baixo de propósito: aquelas taxas contam aplicativos, e eu conto pares.",
      "LEMBRETE (não precisa falar). Como analiso todos os aplicativos oficiais, e não uma amostra, a decisão usa a proporção encontrada. O intervalo de confiança de 95% só mostra a precisão; ele é calculado agrupando por aplicativo, porque os pares do mesmo aplicativo usam a mesma política. Se der menos de 10%, só dá para dizer que ficou abaixo do meu patamar, não que o governo é mais transparente que nos outros estudos. O 10% é um critério do estudo, não um limite da LGPD.")

# ================================================================ 2 REVISÃO BIBLIOGRÁFICA
divisoria("2", "REVISÃO BIBLIOGRÁFICA", [("2.1", "Fundamentação teórica"), ("2.2", "Trabalhos correlatos e o que eles mostram"),
                                         ("2.2.4", "Revisão sistemática: lacuna e contribuição")])

# ---------------------------------------------------------------- 2.1 fundamentação (fundo 13)
s = nova(13, "2.1 Fundamentação teórica")
barra_titulo(s, "FUNDAMENTAÇÃO TEÓRICA", num="2.1")
CWf, GPf = 3.7, 0.225
cols_f = [("sdk", "Rastreamento por terceiros"), ("scan", "Detecção dos SDKs"), ("lei", "Proteção de dados (LGPD)")]
for k, (ic, cab) in enumerate(cols_f):
    x0 = 0.9 + k * (CWf + GPf)
    icone(s, ic, "branco", x0, 1.95, 0.6, NAVY)
    texto(s, x0 + 0.75, 1.95, CWf - 0.75, 0.6, [P(cab, 18, True, NAVY)], anchor="m")
x0 = 0.9
texto(s, x0, 2.7, CWf, 0.95, [P(f"SDKs que coletam dados de uso e permitem acompanhar o usuário entre serviços {ref('binns2018')}. Empresas com rastreadores na maioria dos aplicativos:", 14, False, DARK, spacing=1.0)])
barras(s, x0 - 0.05, 3.62, CWf + 0.05, 2.15, ["Alphabet (Google)", "Facebook", "Twitter", "Verizon"], [88.4, 42.6, 33.9, 26.3],
       [NAVY, MID, MID, MID], ["88,4%", "42,6%", "33,9%", "26,3%"], maximo=118, tam_cat=13, tam_rot=13, gap=40)
texto(s, x0, 5.8, CWf, 0.55, [P(f"% de ~959 mil aplicativos; todas dos EUA. Fonte: Binns et al. {ref('binns2018')}, Tabela 1.", 12, False, GREY, spacing=1.0)])
x0 = 0.9 + CWf + GPf
for k, (cab, txt) in enumerate([("Estática", "examina o código do pacote, sem executar; mostra que o código está lá, não que ele roda"),
                                ("Dinâmica", "executa o aplicativo e observa o tráfego; mostra o envio, mas exige rodar cada um")]):
    y0 = 2.7 + k * 1.3
    forma(s, x0, y0, CWf, 1.18, PALE)
    texto(s, x0 + 0.18, y0 + 0.05, CWf - 0.3, 1.08, [R([(cab + ": ", 15, True, NAVY), (txt, 15, False, DARK)], spacing=1.0)], anchor="m")
texto(s, x0, 5.35, CWf, 1.0, [R([("Ferramentas diferentes ", 15, True, NAVY), (f"podem dar respostas diferentes para o mesmo aplicativo {ref('zhan2022')}; por isso, três detectores.", 15, False, DARK)], spacing=1.0)])
x0 = 0.9 + 2 * (CWf + GPf)
for k, (art, txt) in enumerate([("Art. 6º, VI", "transparência ao titular"),
                                ("Art. 9º, V", "informar o uso compartilhado e sua finalidade"),
                                ("Art. 23, I", "poder público: finalidade e práticas em veículos de fácil acesso"),
                                ("Art. 33", f"transferência internacional só nos casos da lei {ref('anpd2024')}")]):
    y0 = 2.7 + k * 0.9
    forma(s, x0, y0, 1.15, 0.78, NAVY)
    texto(s, x0, y0, 1.15, 0.78, [P(art, 14, True, WHITE, "c")], anchor="m")
    texto(s, x0 + 1.28, y0, CWf - 1.28, 0.78, [P(txt, 14, False, DARK, spacing=0.95)], anchor="m")
texto(s, x0, 6.3 - 0.0, CWf, 0.3, [P(f"LGPD {ref('brasil2018')}; guias da ANPD {ref('anpd2023', 'anpd2022')}", 12, False, GREY)])
notas(s, "Na fundamentação, três conceitos. O rastreamento por terceiros: SDKs que coletam dados de uso e permitem acompanhar o usuário; Binns e colegas acharam empresas do grupo do Google em 88% dos aplicativos, e todas as maiores são dos Estados Unidos. A detecção: a análise estática olha o código, e a dinâmica observa o tráfego. E a LGPD, que exige transparência, informação sobre o compartilhamento e, no poder público, a publicação da finalidade e das práticas.")

# ---------------------------------------------------------------- 2.2 trabalhos correlatos (fundo 13)
CAB_EST = ["Estudo", "O que buscavam", "O que foi feito", "Como foi feito", "Resultados"]
LARG_EST = [2.0, 2.35, 2.35, 2.45, 2.85]
est1 = [
    [f"Binns et al. {ref('binns2018')}", "Medir o rastreamento por terceiros em escala", "959 mil aplicativos da Google Play (EUA e Reino Unido)", "Análise estática: domínios de rastreadores no código", "Rastreamento na maioria, concentrado em poucas empresas"],
    [f"Kollnig et al. {ref('kollnig2021before')}", "Comparar o rastreamento antes e depois do GDPR", "Quase 2 milhões de aplicativos, de 2017 e de 2020", "Análise estática nos dois períodos", "Pouca mudança; concentração em grandes empresas"],
    [f"Andow et al. {ref('andow2020')}", "Confrontar políticas com fluxos de dados e destinatários", "13.796 aplicativos Android, com a ferramenta PoliCheck", "Fluxos observados na execução comparados com a política", "Até 42,4% omitiam ou declaravam errado fluxos de dados sensíveis"],
]
est2 = [
    [f"Samarasinghe et al. {ref('samarasinghe2022')}", "Avaliar a privacidade de sites e aplicativos de governo", "1.166 aplicativos de governo de 71 países", "Análise estática dos SDKs e observação do tráfego", "37% com rastreadores do Google; 27% enviavam informações sensíveis; Brasil não separado"],
    [f"Carlsson et al. {ref('carlsson2022')}", "Comparar tráfego e políticas em aplicativos públicos", "32 aplicativos do setor público finlandês", "Captura do tráfego e leitura das políticas", "Divergências entre políticas e dados enviados; parte para fora da Europa"],
    [f"Serrano et al. {ref('serrano2024')}", "Caracterizar rastreadores em aplicativos da COVID-19", "595 aplicativos de várias fontes", "Assinaturas do Exodus e análise do código", "Rastreadores em 402 dos 595; origem e versão precisam ser registradas"],
]
for parte, sub, linhas in [(1, "Rastreamento e declarações", est1), (2, "Aplicativos de governo", est2)]:
    s = nova(13, f"2.2 Trabalhos correlatos ({parte}/2)")
    barra_titulo(s, f"TRABALHOS CORRELATOS ({parte}/2)", sub=sub, num="2.2")
    tabela(s, 0.65, 2.42, LARG_EST, CAB_EST, linhas, size=15, cab_size=15, alt_h=1.15)
    if parte == 1:
        notas(s, "Nos trabalhos correlatos, separei seis estudos, com o que cada um buscava, o que fez, como fez e o que achou. Binns e colegas acharam rastreamento na maioria de 959 mil aplicativos, concentrado em poucas empresas. Kollnig e colegas compararam aplicativos de antes e de depois do GDPR, o regulamento europeu, e viram pouca mudança. E Andow e colegas compararam o que os aplicativos enviam com o que as políticas dizem: até 42,4% omitiam ou declaravam errado. É dessa linha que vem o meu método.")
    else:
        notas(s, "Os outros três estudaram aplicativos de governo. Samarasinghe e colegas examinaram 1.166 aplicativos de 71 países: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis a terceiros ou sem criptografia, mas o Brasil não aparece separado. Carlsson e colegas compararam o tráfego de 32 aplicativos públicos da Finlândia com as políticas e acharam divergências; é o estudo mais parecido com o meu. E Serrano e colegas acharam rastreadores em 402 de 595 aplicativos da COVID-19.")

# ---------------------------------------------------------------- 2.2 o que os estudos mostram (fundo 13)
s = nova(13, "2.2 O que os estudos mostram")
barra_titulo(s, "O QUE OS ESTUDOS MOSTRAM", num="2.2")
w, h = figura(s, "kollnig2021_fig3", 0.9, 1.95, h=3.85)
texto(s, 0.9, 1.95 + h + 0.07, w, 0.5, [P(f"Empresas de rastreamento nos aplicativos em 2017 e 2020: pouca mudança após o GDPR. Fonte: Kollnig et al. {ref('kollnig2021before')}, Fig. 3.", 12, False, GREY, spacing=1.0)])
xa = 0.9 + w + 0.35
wa = 12.45 - xa
w2, h2 = figura(s, "andow2020_fig1", xa, 1.95, w=wa)
texto(s, xa, 1.95 + h2 + 0.07, wa, 0.55, [P(f"O PoliCheck classifica cada fluxo de dados como consistente (claro ou vago) ou não (omitido, incorreto ou ambíguo) com a política. Fonte: Andow et al. {ref('andow2020')}, Fig. 1.", 12, False, GREY, spacing=1.0)])
yz = 1.95 + h2 + 0.75
w3, h3 = figura(s, "zhan2022_fig5", xa, yz, h=6.3 - yz)
texto(s, xa + w3 + 0.2, yz, wa - w3 - 0.2, 6.3 - yz, [P(f"Taxa de detecção de bibliotecas de cinco ferramentas, em aplicativos com um ou vários arquivos DEX: de 3% a 60%. Fonte: Zhan et al. {ref('zhan2022')}, Fig. 5.", 12, False, GREY, spacing=1.0)], anchor="m")
notas(s, "Algumas figuras desses estudos resumem o ponto. À esquerda, Kollnig e colegas: as mesmas empresas dominam o rastreamento antes e depois do GDPR. À direita, em cima, o PoliCheck de Andow e colegas classifica cada fluxo de dados como consistente ou não com a política; a minha classificação segue essa ideia, por par aplicativo–SDK. Embaixo, Zhan e colegas mostram que ferramentas de detecção chegam a taxas muito diferentes.")

# ---------------------------------------------------------------- 2.2.4 lacuna e contribuição (fundo 13)
s = nova(13, "2.2.4 Lacuna e contribuição")
barra_titulo(s, "LACUNA E CONTRIBUIÇÃO", num="2.2.4")
texto(s, 0.9, 1.85, 11.6, 0.35, [P("A partir dos 31 estudos com proposta de inclusão na revisão sistemática", 16, False, GREY)])
colunas = [("O que já existe", SILVER, DARK), ("O que falta", MID, WHITE), ("O que este TCC faz", NAVY, WHITE)]
X0, CW, GAP = 2.95, 2.95, 0.4
for j, (cab, cor, ctx) in enumerate(colunas):
    x0 = X0 + j * (CW + GAP)
    forma(s, x0, 2.3, CW, 0.42, cor)
    texto(s, x0, 2.3, CW, 0.42, [P(cab, 15, True, ctx, "c")], anchor="m")
eixos = [("governo", "Caso brasileiro",
          ["Estudo internacional de aplicativos de governo; estudos de um aplicativo brasileiro por vez",
           "Medir o conjunto dos aplicativos do governo brasileiro, por esfera",
           "Analisa os 376 aplicativos classificados como oficiais, nas três esferas"]),
         ("comparar", "Declarado × encontrado",
          ["Comparação entre política e dados em aplicativos comerciais e no setor público finlandês",
           "Comparar cada SDK com a política e a “Segurança dos dados” no Brasil",
           "Classifica cada par aplicativo–SDK e testa a H1"]),
         ("scan", "Instrumento",
          ["Comparações de ferramentas que detectam bibliotecas",
           "Concordância entre detectores de rastreadores nas mesmas versões",
           "Mede o κ de Fleiss entre três detectores"])]
RH = 1.02
for i, (ic, eixo, cel) in enumerate(eixos):
    y0 = 2.82 + i * (RH + 0.08)
    forma(s, 0.9, y0, 1.9, RH, PALE)
    icone(s, ic, "marinho", 1.0, y0 + (RH - 0.42) / 2, 0.42)
    texto(s, 1.5, y0, 1.25, RH, [P(eixo, 14, True, NAVY)], anchor="m")
    for j, txt in enumerate(cel):
        x0 = X0 + j * (CW + GAP)
        forma(s, x0, y0, CW, RH, [LIGHT, WHITE, PALE][j], linha=[SILVER, MID, NAVY][j])
        texto(s, x0 + 0.12, y0, CW - 0.24, RH, [P(txt, 14, j == 2, NAVY if j == 2 else DARK, "c", spacing=0.95)], anchor="m")
        if j < 2:
            seta(s, x0 + CW + 0.06, y0 + RH / 2 - 0.14, 0.28, 0.28)
texto(s, 1.5, 6.15, 10.95, 0.3, [P(f"Bases: Samarasinghe et al. {ref('samarasinghe2022')}; Lemos et al. {ref('lemos2022')}; Vaz et al. {ref('vaz2022')}; Andow et al. {ref('andow2020')}; Carlsson et al. {ref('carlsson2022')}; Zhan et al. {ref('zhan2022')}.", 12, False, GREY)])
notas(s, "Juntando esses estudos, aparecem três lacunas, e cada uma vira uma contribuição. Primeiro, o caso brasileiro: há estudos de um aplicativo por vez, mas ninguém mediu o conjunto; o trabalho analisa os 376 aplicativos classificados como oficiais, das três esferas. Segundo, o confronto entre o declarado e o encontrado já foi feito em outros contextos, mas não aqui; o trabalho classifica cada par e testa a hipótese. Terceiro, o instrumento: o trabalho mede quanto o resultado depende do detector. E uma divergência não prova infração à LGPD; é um indício a ser examinado.")

# ================================================================ 3 METODOLOGIA
divisoria("3", "METODOLOGIA", [("", "Etapas do método"), ("3.1", "Escolha da plataforma Android"), ("3.4", "Detecção dos SDKs e κ de Fleiss"),
                               ("3.5", "Classificação das declarações"), ("3.8", "Protocolo da revisão sistemática"),
                               ("3.11", "Cronograma do Capstone II")])

# ---------------------------------------------------------------- etapas do método (fundo 13)
s = nova(13, "3 Etapas do método")
barra_titulo(s, "ETAPAS DO MÉTODO", num="3", sub="Estudo quantitativo e observacional, em seis etapas; cada uma atende a um objetivo")
etapas = [("governo", "Seleção dos aplicativos", "Revisar cada aplicativo pelo nome jurídico do desenvolvedor", "376 aplicativos oficiais, por esfera", "a"),
          ("download", "Obtenção dos pacotes", "Versão atual com o apkeep; AndroZoo quando houver", "Pacote com hash SHA-256, versão e data", "b"),
          ("scan", "Detecção dos SDKs", "Detectores A, B e C e a concordância entre eles", "Pares aplicativo–SDK; κ de Fleiss", "b, e"),
          ("documento", "Classificação das declarações", "Ler a política e a “Segurança dos dados”; classificar cada par", "Matriz de declarações", "c"),
          ("rede", "Observação do tráfego", "Subamostra no emulador do Android Studio, com o mitmproxy", "Destinos, país e se estão declarados", "d"),
          ("grafico", "Análise estatística", "Proporção de pares sem declaração, comparada com 10%", "Decisão sobre a hipótese", "c, e")]
CWe, GPe = 1.78, 0.177
for k, (ic, nome, faz, ent, ob) in enumerate(etapas):
    x0 = 0.9 + k * (CWe + GPe)
    forma(s, x0, 2.42, CWe, 1.05, NAVY)
    icone(s, ic, "branco", x0 + 0.12, 2.52, 0.4)
    texto(s, x0 + 0.6, 2.47, CWe - 0.65, 0.4, [P(str(k + 1), 22, True, MID)], anchor="m")
    texto(s, x0 + 0.12, 2.92, CWe - 0.2, 0.55, [P(nome, 14, True, WHITE, spacing=0.92)], anchor="m")
    forma(s, x0, 3.47, CWe, 2.88, WHITE, linha=SILVER)
    texto(s, x0 + 0.12, 3.57, CWe - 0.24, 1.25, [P(faz, 14, False, DARK, spacing=0.95)])
    texto(s, x0 + 0.12, 4.82, CWe - 0.24, 0.3, [P("ENTREGA", 11, True, MID)])
    texto(s, x0 + 0.12, 5.1, CWe - 0.24, 0.8, [P(ent, 14, True, NAVY, spacing=0.95)])
    texto(s, x0 + 0.12, 5.95, CWe - 0.24, 0.32, [R([("objetivo ", 12, False, GREY), (ob, 12, True, NAVY)])])
    if k < 5:
        forma(s, x0 + CWe + 0.02, 2.8, GPe - 0.04, 0.3, MID, MSO_SHAPE.CHEVRON)
notas(s, "O estudo é quantitativo e observacional, em seis etapas, e cada uma atende a um objetivo. Primeiro, a seleção dos aplicativos. Depois, o download da versão atual, com o hash, que é a impressão digital do arquivo. Em seguida, a detecção dos SDKs com três detectores e a classificação das declarações. A quinta etapa observa o tráfego de uma parte dos aplicativos num emulador Android, com o mitmproxy, que registra as conexões. Por fim, a análise estatística decide a hipótese.")

# ---------------------------------------------------------------- 3.1 por que só Android (fundo 13)
s = nova(13, "3.1 Por que só Android")
barra_titulo(s, "POR QUE SÓ ANDROID", num="3.1")
rosca(s, 0.9, 1.95, 2.75, [73.76, 26.24], [NAVY, SILVER])
texto(s, 0.9, 2.85, 2.75, 0.95, [P("73,76%", 26, True, NAVY, "c"), P("Android", 13, False, DARK, "c")], anchor="m")
texto(s, 0.9, 4.75, 2.75, 0.62, [P(f"dos celulares no Brasil (StatCounter {ref('statcounter2026')}, out. 2026)", 13, False, GREY, "c", spacing=1.0)])
mot = [("cadeado", "Acesso ao código", f"No iPhone, os aplicativos são criptografados e não há ferramenta pública para baixá-los em escala; decriptar exige aparelho físico e tem legalidade incerta {ref('kollnig2022ios')}."),
       ("documento", "Declarações comparáveis", f"A hipótese usa a seção “Segurança dos dados”, que é da Google Play; a App Store tem rótulos em outro formato {ref('xiao2023')}.")]
for k, (ic, cab, txt) in enumerate(mot):
    y0 = 1.95 + k * 1.72
    forma(s, 3.95, y0, 4.3, 1.58, PALE)
    icone(s, ic, "branco", 4.1, y0 + 0.15, 0.5, NAVY)
    texto(s, 4.75, y0 + 0.13, 3.4, 0.5, [P(cab, 16, True, NAVY)], anchor="m")
    texto(s, 4.15, y0 + 0.7, 3.95, 0.85, [P(txt, 13, False, DARK, spacing=0.95)])
forma(s, 1.45, 5.55, 6.8, 0.8, LIGHT)
texto(s, 1.6, 5.55, 6.55, 0.8, [R([("Não quer dizer que o iPhone seja mais seguro: ", 14, True, NAVY), ("há rastreamento nas duas plataformas (figura). As versões iOS ficam como trabalho futuro.", 14, False, DARK)], spacing=0.95)], anchor="m")
w, h = figura(s, "kollnig2022_fig6", 8.65, 1.95, h=3.75)
texto(s, 8.5, 5.78, 3.95, 0.6, [P(f"Rastreamento no iOS e no Android, por empresa e país: concentrado em empresas dos EUA. Fonte: Kollnig et al. {ref('kollnig2022ios')}, Fig. 6.", 12, False, GREY, spacing=1.0)])
notas(s, "Por que só Android? São três motivos. Primeiro, abrangência: segundo a StatCounter, o Android está em 73,76% dos celulares no Brasil. Segundo, acesso ao código: no iPhone, os aplicativos são criptografados e não há ferramenta pública para baixá-los em escala. Terceiro, a hipótese usa a seção “Segurança dos dados”, que só existe na Google Play. Isso não quer dizer que o iPhone seja mais seguro: a figura de Kollnig e colegas mostra rastreamento nas duas plataformas. O iOS fica como trabalho futuro.")

# ---------------------------------------------------------------- 3.4 detecção e kappa de Fleiss (fundo 13)
s = nova(13, "3.4 Detecção dos SDKs e κ de Fleiss")
barra_titulo(s, "DETECÇÃO DOS SDKs E κ DE FLEISS", num="3.4", sub=f"Concordância entre os três detectores, descontado o acaso (Fleiss {ref('fleiss1971')})")
forma(s, 0.9, 2.45, 4.9, 1.2, NAVY)
texto(s, 0.9, 2.45, 4.9, 1.2, [R([("κ = (P", 30, True, WHITE), ("o", 30, True, WHITE, True), (" − P", 30, True, WHITE), ("e", 30, True, WHITE, True),
                                   (") / (1 − P", 30, True, WHITE), ("e", 30, True, WHITE, True), (")", 30, True, WHITE)], align="c")], anchor="m")
texto(s, 0.9, 3.78, 4.9, 0.8, [R([("1", 14, True, NAVY), (" = concordância total; ", 14, False, DARK), ("0", 14, True, NAVY), (" = igual ao acaso. Concordância alta não prova acerto: os três podem errar igual.", 14, False, DARK)], spacing=0.95)])
defs = [[("P", 15, True, NAVY), ("o", 15, True, NAVY, True), (" — concordância observada: ", 15, True, NAVY), ("em cada aplicativo, a fração dos pares de detectores que concordam; depois, a média.", 15, False, DARK)],
        [("P", 15, True, NAVY), ("e", 15, True, NAVY, True), (" — concordância esperada ao acaso: ", 15, True, NAVY), ("soma dos quadrados das proporções de “tem” e de “não tem”.", 15, False, DARK)],
        [("Por que descontar o acaso? ", 15, True, NAVY), ("Se quase todo aplicativo tem rastreador, quem diz “tem” para tudo concorda sem medir nada.", 15, False, DARK)]]
texto(s, 6.15, 2.45, 6.3, 2.2, [R(d, after=9, spacing=1.0) for d in defs])
texto(s, 1.6, 4.72, 10.0, 0.32, [P(f"ESCALA DE LANDIS E KOCH {ref('landis1977')}", 13, True, MID)])
escala_landis(s, 1.6, 5.45, 10.85)
notas(s, "Para medir a concordância entre os três detectores, uso o kappa de Fleiss. Ele mede se vários avaliadores concordam, descontando o acordo que aconteceria por acaso; aqui, cada detector diz se o aplicativo tem ou não rastreador. Descontar o acaso importa porque, se quase todo aplicativo tem rastreador, concordar é fácil. Para ler o resultado, uso a escala de Landis e Koch, e meu limiar é 0,6, a passagem de moderada para substancial. O valor do piloto aparece nos resultados.",
      "LEMBRETE (não precisa falar). Fórmula por aplicativo: P i = soma de n ij vezes (n ij − 1), dividida por n vezes (n − 1), com n = 3 detectores e n ij = quantos deram a resposta j. P e = soma de p j ao quadrado, com p j = proporção de todas as respostas na categoria j. Junto do κ, reporto o IC95% e as concordâncias positiva e negativa, porque o κ fica instável quando quase todos os aplicativos estão na mesma categoria. Na revisão, a reclassificação às cegas da triagem usa o κ de Cohen, a versão para dois avaliadores, com a mesma escala.")

# ---------------------------------------------------------------- 3.5 classificação das declarações (fundo 13)
s = nova(13, "3.5 Classificação das declarações")
barra_titulo(s, "CLASSIFICAÇÃO DAS DECLARAÇÕES", num="3.5", sub="Cada par aplicativo–SDK recebe uma de cinco situações")
sit = [("ok", "Menção nominal", "A política cita o SDK ou a empresa que o fornece"),
       ("documento", "Declaração por categoria", "O tipo de dado e a finalidade estão declarados, mesmo sem o nome do SDK"),
       ("nao", "Sem declaração compatível", "Documentos disponíveis, mas nenhum cobre o dado ou a finalidade do SDK"),
       ("duvida", "Informação insuficiente", "Documentos genéricos demais para decidir"),
       ("proibido", "Política indisponível", "Documento não obtido")]
for k, (ic, cab, txt) in enumerate(sit):
    y0 = 2.42 + k * 0.79
    destaque = k == 2
    fundo_c = NAVY if destaque else (PALE if k < 2 else LIGHT)
    forma(s, 0.9, y0, 7.1, 0.7, fundo_c)
    forma(s, 0.9, y0, 0.62, 0.7, MID if destaque else NAVY)
    texto(s, 0.9, y0, 0.62, 0.7, [P(str(k + 1), 20, True, WHITE, "c")], anchor="m")
    icone(s, ic, "branco" if destaque else "marinho", 1.67, y0 + 0.15, 0.4)
    texto(s, 2.2, y0, 5.7, 0.7, [R([(cab + ": ", 15, True, WHITE if destaque else NAVY), (txt, 14, False, WHITE if destaque else DARK)], spacing=0.95)], anchor="m")
forma(s, 8.35, 2.42, 4.1, 1.95, NAVY)
texto(s, 8.5, 2.5, 3.8, 1.8, [P("TESTE DA HIPÓTESE", 13, True, MID, "c", after=6),
                              P("proporção = (3) ÷ [(1) + (2) + (3)]", 18, True, WHITE, "c", after=6),
                              P("H1 confirmada se der 10% ou mais, com IC95% agrupado por aplicativo", 13, False, PALE, "c", spacing=1.0)], anchor="m")
rosca(s, 8.35, 4.55, 1.75, [81.6, 18.4], [NAVY, SILVER])
texto(s, 8.35, 5.12, 1.75, 0.6, [P("81,6%", 17, True, NAVY, "c")], anchor="m")
texto(s, 10.2, 4.6, 2.3, 1.65, [P("já verificado:", 13, True, NAVY), P("323 dos 396 candidatos têm política acessível", 13, False, DARK, spacing=1.0),
                                P("(4) e (5) ficam à parte, nas análises de sensibilidade", 12, False, GREY, spacing=1.0)])
notas(s, "Esta é a parte central do teste. Para cada par, leio a política de privacidade e a seção “Segurança dos dados” e escolho uma de cinco situações: o SDK é citado pelo nome; o tipo de dado e a finalidade estão declarados, mesmo sem o nome; não há declaração compatível; a informação é genérica demais; ou a política não está disponível. A proporção é a terceira situação dividida pelas três primeiras; se der 10% ou mais, a hipótese se confirma. As duas últimas ficam à parte, para não inflar nem esconder o problema. Não citar o nome do SDK, sozinho, não conta como omissão.")

# ---------------------------------------------------------------- 3.8 protocolo da revisão sistemática (fundo 10)
s = nova(10, "3.8 Protocolo da revisão sistemática")
blocos = [("base", "ONDE", "15 buscas em 4 bases: Scopus (principal), IEEE Xplore, SBC OpenLib e BDTD; 2018 a 2026; inglês e português"),
          ("filtro", "COMO", "Strings com aplicativo, fenômeno e contexto; termo do tema obrigatório no título; 4 questões de revisão"),
          ("ok", "VALIDAÇÃO", f"9 estudos de controle no escopo: as buscas acharam os 8 que o Scopus indexa; reclassificação às cegas de 32 registros (κ de Cohen {ref('cohen1960')})")]
for k, (ic, cab, txt) in enumerate(blocos):
    x0 = 1.0 + k * 3.55
    icone(s, ic, "branco", x0, 0.45, 0.5, NAVY)
    texto(s, x0 + 0.62, 0.45, 2.7, 0.5, [P(cab, 14, True, MID)], anchor="m")
    texto(s, x0, 1.05, 3.3, 1.5, [P(txt, 14, False, DARK, spacing=1.0)])
texto(s, 1.0, 2.72, 10.2, 0.75, [R([("3.8  ", 30, True, PALE), ("REVISÃO SISTEMÁTICA", 34, True, WHITE)])], anchor="m")
texto(s, 1.0, 3.5, 10.2, 0.45, [P(f"Kitchenham e Charters {ref('kitchenham2007')} · PRISMA 2020 {ref('page2021')}", 17, False, WHITE)])
fases = [("Planejamento", "questões, bases, strings e critérios no protocolo"),
         ("Condução", "busca, seleção, qualidade e extração dos dados"),
         ("Relatório", "síntese e fluxograma no formato PRISMA 2020")]
for k, (cab, txt) in enumerate(fases):
    x0 = 1.55 + k * 3.75
    forma(s, x0, 5.15, 3.4, 1.05, NAVY if k == 1 else PALE, MSO_SHAPE.CHEVRON if k else MSO_SHAPE.PENTAGON)
    ct = WHITE if k == 1 else NAVY
    texto(s, x0 + 0.45, 5.15, 2.55, 1.05, [P(cab, 16, True, ct, "c"), P(txt, 12, False, ct, "c", spacing=0.95)], anchor="m")
notas(s, "Para a literatura, fiz uma revisão sistemática, uma busca planejada e documentada. Segui o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as palavras de busca e os critérios; e o resultado segue o PRISMA 2020. Foram 15 buscas em quatro bases, de 2018 a 2026, exigindo um termo do tema no título. Para testar as buscas, separei estudos que tinham de aparecer: dos nove dentro do escopo, elas acharam os oito que estão no Scopus.",
      "Guia de Kitchenham: divide a revisão em planejamento (questões e protocolo), condução (busca, seleção, avaliação de qualidade e extração dos dados) e relatório (síntese dos resultados).",
      "PRISMA 2020: padroniza o relato da revisão num fluxograma, da identificação dos registros e remoção de duplicatas até a triagem, a leitura completa e os estudos incluídos.")

# ---------------------------------------------------------------- 3.11 cronograma (fundo 13)
s = nova(13, "3.11 Cronograma do Capstone II")
barra_titulo(s, "CRONOGRAMA DO CAPSTONE II (2027.1)", num="3.11")
meses = ["Fev", "Mar", "Abr", "Mai", "Jun"]
XL, WL, XM, WM, XP = 0.9, 3.05, 4.05, 1.08, 9.55
WP = 12.45 - XP
YC, HL = 2.0, 0.55
forma(s, XL, YC, 12.45 - XL, 0.42, NAVY)
texto(s, XL + 0.12, YC, WL, 0.42, [P("Etapa", 15, True, WHITE)], anchor="m")
for k, m in enumerate(meses):
    texto(s, XM + k * WM, YC, WM, 0.42, [P(m, 15, True, WHITE, "c")], anchor="m")
texto(s, XP + 0.12, YC, WP - 0.12, 0.42, [P("Produto", 15, True, WHITE)], anchor="m")
crono = [("Revisão sistemática", 0, 1, "Estudos incluídos; κ de Cohen"),
         ("1. Seleção dos aplicativos", 0, 1, "Lista final e plano de análise"),
         ("2 e 3. Pacotes e detecção", 1, 2, "Pares aplicativo–SDK; κ de Fleiss"),
         ("4. Declarações", 1, 3, "Matriz de declarações"),
         ("5. Tráfego no emulador", 2, 3, "Destinos e países"),
         ("6. Análise e teste da H1", 3, 4, "Resultado do teste da H1"),
         ("Redação e defesa", 4, 5, "Texto final e defesa")]
for i, (et, ini, fim, prod) in enumerate(crono):
    y0 = YC + 0.42 + i * HL
    forma(s, XL, y0, 12.45 - XL, HL, PALE if i % 2 == 0 else WHITE)
    texto(s, XL + 0.12, y0, WL, HL, [P(et, 15, True, NAVY)], anchor="m")
    barra = forma(s, XM + ini * WM + 0.06, y0 + 0.12, (fim - ini) * WM - 0.12, HL - 0.24, MID if i == 0 else NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
    barra.adjustments[0] = 0.5
    texto(s, XP + 0.12, y0, WP - 0.12, HL, [P(prod, 14, False, DARK)], anchor="m")
for k in range(6):
    forma(s, XM + k * WM - 0.005, YC + 0.42, 0.01, HL * len(crono), SILVER)
notas(s, "A execução fica para o Capstone II. Em fevereiro, termino a revisão e reviso a lista de aplicativos, testando o download e o emulador. Em março, baixo os pacotes e rodo os detectores. Entre março e abril, classifico as declarações. Em abril, registro o tráfego da subamostra no emulador. Em maio, faço a análise e decido sobre a hipótese, avisando os órgãos se houver achado grave. Em junho, escrevo, publico os dados e defendo.")

# ================================================================ 4 RESULTADOS E DISCUSSÃO
divisoria("4", "RESULTADOS E DISCUSSÃO", [("4.1.1", "Aplicativos selecionados"), ("4.1.2", "Fonte dos pacotes"),
                                          ("4.1.3", "Piloto dos detectores"), ("4.1.5", "Andamento da revisão sistemática"),
                                          ("4.2 e 4.3", "Resultados esperados e limitações")])

# ---------------------------------------------------------------- 4.1.1 aplicativos selecionados (fundo 4)
s = nova(4, "4.1.1 Aplicativos selecionados")
titulo_livre(s, "APLICATIVOS SELECIONADOS", "4.1.1", w=11.0)
funil = [(590, "590", "aplicativos distintos", "21 termos na Google Play e catálogos dos publicadores", PALE, NAVY),
         (396, "396", "candidatos", "publicador classificado como órgão público (71 publicadores)", MID, WHITE),
         (376, "376", "oficiais", "nome jurídico conferido em “Sobre o desenvolvedor”", NAVY, WHITE)]
for k, (v, num, rot, txt, cor, ct) in enumerate(funil):
    wb = 5.9 * v / 590
    y0 = 2.0 + k * 1.05
    forma(s, 1.0, y0, wb, 0.88, cor)
    texto(s, 1.15, y0, 2.6, 0.88, [R([(num + " ", 28, True, ct), (rot, 15, True, ct)])], anchor="m")
    texto(s, 1.0 + wb + 0.2 if k else 1.0 + 2.95, y0, 6.9 - (wb + 0.2 if k else 2.95), 0.88,
          [P(txt, 13, False, DARK if k else NAVY, spacing=0.95)], anchor="m")
texto(s, 1.0, 5.25, 6.6, 1.05, [P("Saíram 20: 13 empresas privadas e 7 contas de pessoa física.", 15, False, DARK, after=4),
                                P("Lista preliminar: será revista antes da coleta (objetivo a).", 15, True, NAVY)])
rosca(s, 8.2, 1.85, 3.3, [85, 199, 92], [NAVY, MID, SILVER], buraco=60)
texto(s, 8.2, 3.05, 3.3, 0.9, [P("376", 30, True, NAVY, "c"), P("oficiais", 13, False, DARK, "c")], anchor="m")
for k, (cor, num, rot) in enumerate([(NAVY, "85", "federais"), (MID, "199", "estaduais"), (SILVER, "92", "municipais")]):
    x0 = 7.85 + k * 1.45
    forma(s, x0, 5.45, 0.28, 0.28, cor)
    texto(s, x0 + 0.36, 5.33, 1.05, 0.55, [P(num, 18, True, NAVY), P(rot, 12, False, DARK)])
notas(s, "Agora, os resultados preliminares, da preparação do estudo. Para montar a lista, busquei 21 termos ligados a serviço público na Google Play e depois o catálogo de cada publicador oficial. Foram 396 candidatos. Pelo nome jurídico de quem publica, ficaram 376 oficiais: 85 federais, 199 estaduais e 92 municipais. Saíram 20, de empresas privadas ou de contas de pessoa física. A lista é preliminar e será revista antes da coleta.")

# ---------------------------------------------------------------- 4.1.2 fonte dos pacotes (fundo 2)
s = nova(2, "4.1.2 Fonte dos pacotes")
texto(s, 0.9, 0.55, 11.5, 0.4, [P("4.1.2", 18, True, MID)])
texto(s, 0.9, 0.9, 11.5, 0.8, [P("FONTE DOS PACOTES", 40, True, WHITE)])
texto(s, 0.9, 1.7, 6.5, 0.45, [P("Aplicativos presentes no AndroZoo, acervo acadêmico de pacotes Android", 17, False, PALE)])
barras(s, 0.75, 2.2, 5.0, 2.55, ["Governo", "Comerciais"], [23.2, 84.2], [MID, PALE], ["23,2%", "84,2%"], horizontal=False,
       maximo=100, tam_cat=16, tam_rot=22, gap=70, cor_txt=WHITE, cor_rot=WHITE)
texto(s, 0.9, 4.8, 5.0, 0.6, [P("92 de 396 candidatos do governo × 160 de 190 comerciais (só como contexto)", 13, False, PALE, spacing=1.0)])
texto(s, 6.4, 2.35, 6.0, 2.2, [P("Fonte principal: versão atual na Google Play", 22, True, WHITE, after=8),
                               P("É a versão que o cidadão instala. O AndroZoo fica para a reprodutibilidade e para medir a defasagem entre versões.", 16, False, PALE, spacing=1.05)])
texto(s, 1.45, 5.45, 11.0, 0.32, [P("COMO SERÁ A COLETA", 13, True, PALE)])
passos_c = [("usuarios", "Conta da pesquisa", "criada só para o estudo, no Brasil"),
            ("download", "Download com apkeep", f"ferramenta aberta da EFF {ref('apkeep2026')}"),
            ("hash", "Registro", "hash SHA-256, versão, data e falhas"),
            ("ok", "Teste primeiro", "cinco aplicativos em fevereiro")]
for k, (ic, cab, txt) in enumerate(passos_c):
    x0 = 1.45 + k * 2.78
    icone(s, ic, "branco", x0, 5.82, 0.5, MID)
    texto(s, x0 + 0.6, 5.78, 2.1, 0.6, [P(cab, 14, True, WHITE), P(txt, 12, False, PALE, spacing=0.95)])
notas(s, "Na hora de buscar os pacotes, apareceu um problema. O AndroZoo, um acervo acadêmico, tinha só 92 dos 396 aplicativos do governo, 23,2%, contra 84,2% dos comerciais. Dependendo só dele, a maioria ficaria de fora. Por isso, a fonte principal será a versão atual da Google Play, que é a que o cidadão instala, baixada com o apkeep, uma ferramenta aberta, com uma conta criada só para a pesquisa. Registro o hash, a versão, a data e o motivo de cada falha. O AndroZoo fica para a reprodutibilidade.",
      "LEMBRETE (não precisa falar). Na mesma faixa de instalações, a razão de chances de um aplicativo do governo estar no acervo é 0,13 (IC95% de 0,07 a 0,24). Quando o aplicativo vem dividido em vários pacotes, guardo o APK base, que tem o código. O apkeep é da Electronic Frontier Foundation (EFF). Não redistribuo os pacotes.")

# ---------------------------------------------------------------- 4.1.3 piloto dos detectores (fundo 13)
s = nova(13, "4.1.3 Piloto dos detectores")
barra_titulo(s, "PILOTO DOS DETECTORES", num="4.1.3", sub="Pacotes com ao menos um rastreador, por detector (20 pacotes)")
barras(s, 0.75, 2.3, 6.1, 2.55, ["A · Exodus, código", "B · Exodus, domínios", "C · Disconnect, domínios"], [75, 95, 80],
       [MID, NAVY, MID], ["75%", "95%", "80%"], maximo=112, tam_cat=15, tam_rot=18, gap=45)
texto(s, 2.75, 4.85, 4.1, 0.3, [P("15, 19 e 16 de 20 pacotes", 12, False, GREY)])
forma(s, 7.25, 2.35, 5.2, 1.75, NAVY)
texto(s, 7.45, 2.4, 2.3, 1.65, [P("κ DE FLEISS", 13, True, MID), P("0,52", 48, True, WHITE), P("moderada", 15, False, PALE)], anchor="m")
seta(s, 9.65, 3.05, 0.4, 0.32, MID)
texto(s, 10.2, 2.4, 2.15, 1.65, [P("SEM OS POSSÍVEIS FALSOS POSITIVOS", 11, True, MID, spacing=0.95), P("0,69", 40, True, WHITE), P("substancial", 15, False, PALE)], anchor="m")
texto(s, 7.25, 4.18, 5.2, 0.82, [R([("Ferramentas diferentes dão taxas diferentes. ", 14, True, NAVY),
                                   ("A × B: mesma base, outro método; B × C: mesmo método, outra base. 88 de 123 detecções de B marcadas como possíveis falsos positivos.", 13, False, DARK)], spacing=0.95)])
escala_landis(s, 1.6, 5.62, 10.85, marcas=[(0.52, "0,52"), (0.69, "0,69")], h=0.38)
notas(s, "No piloto, testei três detectores em 20 pacotes. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet dentro do pacote. O C faz o mesmo que o B, com a lista da Disconnect. As taxas foram diferentes: 75%, 95% e 80%. E 88 das 123 detecções do B pareciam falsos positivos. O kappa de Fleiss entre os três foi 0,52, moderado; sem esses casos, sobe para 0,69, substancial. Com só 20 pacotes, isso testa o instrumento, e não a hipótese.",
      "LEMBRETE (não precisa falar). A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método). B não é tráfego, é texto dentro do pacote: um link para maps.google.com bastou para apontar Google Ads. C usa só as categorias publicidade, análise de uso e impressão digital. Exodus Privacy: base aberta de rastreadores, com assinaturas de código e de rede. Disconnect: lista de domínios que coletam dados, separados por categoria.")

# ---------------------------------------------------------------- 4.1.5 andamento da revisão (fundo 13)
s = nova(13, "4.1.5 Andamento da revisão sistemática")
barra_titulo(s, "ANDAMENTO DA REVISÃO SISTEMÁTICA", num="4.1.5", sub="Fluxo parcial, no formato do PRISMA 2020")
fluxo = [(396, "registros nas 15 buscas"), (312, "sem duplicatas, triados por título e resumo"), (148, "encaminhados à leitura completa"),
         (35, "textos lidos até agora"), (31, "propostas de inclusão (8 já confirmadas)")]
for k, (v, txt) in enumerate(fluxo):
    y0 = 2.4 + k * 0.78
    wb = max(1.25, 5.0 * v / 396)
    forma(s, 0.9, y0, wb, 0.66, NAVY if k == 4 else (MID if k else PALE))
    texto(s, 0.9, y0, 1.25, 0.66, [P(str(v), 22, True, NAVY if k == 0 else WHITE, "c")], anchor="m")
    texto(s, 0.9 + wb + 0.15, y0, 7.0 - wb - 0.15, 0.66, [P(txt, 14, False, DARK)], anchor="m")
texto(s, 7.55, 2.3, 4.9, 0.32, [P("31 PROPOSTAS POR QUESTÃO DA REVISÃO", 13, True, MID)])
barras(s, 7.4, 2.62, 5.1, 2.75, ["QR1", "QR2", "QR3", "QR4"], [11, 8, 10, 2], [NAVY, NAVY, NAVY, MID], ["11", "8", "10", "2"],
       horizontal=False, maximo=13.5, tam_cat=15, tam_rot=16, gap=60)
texto(s, 7.55, 5.42, 4.9, 0.95, [P("QR1: rastreadores e envio a terceiros · QR2: declarado × feito · QR3: governo, inclusive COVID-19 · QR4: Brasil, LGPD e transferência internacional. 113 registros em aberto, para fevereiro.", 12, False, GREY, spacing=1.0)])
notas(s, "Na revisão, as buscas trouxeram 396 resultados, 312 sem repetidos, e 148 seguiram para a leitura completa. Já li 35, e 31 receberam proposta de inclusão, distribuídas nas quatro questões da revisão. Os 113 restantes ficam para fevereiro.")

# ---------------------------------------------------------------- 4.2 e 4.3 resultados esperados e limitações (fundo 13)
s = nova(13, "4.2 e 4.3 Resultados esperados e limitações")
barra_titulo(s, "RESULTADOS ESPERADOS E LIMITAÇÕES", num="4.2 · 4.3")
esp = [("grafico", "Proporção sem declaração e decisão sobre a H1"), ("governo", "Rastreadores por esfera de governo"),
       ("globo", "Destinos dos dados na subamostra"), ("comparar", "Concordância entre os detectores"),
       ("base", "Dados e scripts reprodutíveis")]
CWr = (11.55 - 4 * 0.15) / 5
for k, (ic, txt) in enumerate(esp):
    x0 = 0.9 + k * (CWr + 0.15)
    forma(s, x0, 1.95, CWr, 1.0, PALE)
    icone(s, ic, "marinho", x0 + 0.12, 2.22, 0.45)
    texto(s, x0 + 0.68, 1.95, CWr - 0.76, 1.0, [P(txt, 13, True, NAVY, spacing=0.95)], anchor="m")
lim = [("SDK no código não prova envio de dados", "Observação do tráfego numa subamostra"),
       ("Alguns aplicativos podem não rodar no emulador", "Motivo registrado e proporção reportada"),
       ("Só Android e Google Play", "Motivos justificados; iOS como trabalho futuro"),
       ("Políticas citam tipos de dados, não o nome do SDK", "Classificação por categoria; não citar o nome não é omissão"),
       ("Versões mudam entre a coleta e a análise", "Hash SHA-256, versão e data de cada pacote"),
       ("Divergência não prova infração à LGPD", "Tratada como indício, com a evidência registrada")]
texto(s, 0.9, 3.12, 5.6, 0.32, [P("LIMITAÇÃO", 13, True, MID)])
texto(s, 6.95, 3.12, 5.5, 0.32, [P("COMO É TRATADA", 13, True, MID)])
for k, (a, b) in enumerate(lim):
    y0 = 3.45 + k * 0.48
    forma(s, 0.9, y0, 5.6, 0.42, LIGHT)
    icone(s, "alerta", "marinho", 0.98, y0 + 0.07, 0.28)
    texto(s, 1.36, y0, 5.1, 0.42, [P(a, 14, False, DARK)], anchor="m")
    seta(s, 6.57, y0 + 0.08, 0.3, 0.26)
    forma(s, 6.95, y0, 5.5, 0.42, PALE)
    icone(s, "ok", "marinho", 7.03, y0 + 0.07, 0.28)
    texto(s, 7.41, y0, 5.0, 0.42, [P(b, 14, True, NAVY)], anchor="m")
notas(s, "Ao final do Capstone II, espero ter a proporção de pares sem declaração, com a decisão sobre a hipótese, os destinos dos dados na subamostra e um conjunto de dados reprodutível. Sobre as limitações: achar o SDK no código não prova envio de dados, e por isso registro o tráfego de uma subamostra no emulador. As políticas falam de tipos de dados, e não do nome do SDK, então não citar o nome não conta como omissão. E uma divergência não prova infração à LGPD; é um indício.")

# ================================================================ 5 CONCLUSÃO
divisoria("5", "CONCLUSÃO", [("", "Síntese do projeto"), ("", "Próximos passos no Capstone II")])

# ---------------------------------------------------------------- conclusão (fundo 3)
s = nova(3, "5 Conclusão")
for k, frase in enumerate(["Problema definido.", "Método viável.", "Hipótese pronta para o teste."]):
    y0 = 1.25 + k * 0.95
    icone(s, "ok", "branco", 1.0, y0 + 0.12, 0.6, NAVY)
    texto(s, 1.8, y0, 10.5, 0.85, [P(frase, 40, True, WHITE)], anchor="m")
forma(s, 1.0, 4.45, 11.4, 1.25, NAVY)
texto(s, 1.25, 4.45, 10.9, 1.25, [R([("No Capstone II: ", 20, True, MID), ("medir a proporção de pares aplicativo–SDK sem declaração compatível e comparar o que os aplicativos públicos declaram com o que está dentro deles e, onde der para observar, com o que eles enviam.", 18, False, WHITE)], spacing=1.05)], anchor="m")
texto(s, 1.0, 5.82, 6.0, 0.5, [P("Obrigado.", 24, True, NAVY)], anchor="m")
notas(s, "Para concluir: o problema está definido, o método é viável, e a hipótese está pronta para ser testada no Capstone II. O foco é medir o quanto o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles enviam. Obrigado.")

# ================================================================ REFERÊNCIAS
ACENTO = {"'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303", '"': "\u0308"}


def limpa(t):
    # acentos do BibTeX ({\'\i}, {\'I}, {\'A}, {\'e}...) viram caracteres acentuados
    t = re.sub(r"\\i(?![a-zA-Z])", "i", t)
    t = re.sub(r"\{?\\(['`^~\"])\s*\{?([A-Za-z])\}?\}?", lambda m: m.group(2) + ACENTO[m.group(1)], t)
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\\url\{([^}]*)\}", r"\1", t)
    t = t.replace("\\_", "_").replace("\\%", "%").replace("\\#", "#")  # escapes dos endereços
    t = t.replace("``", "“").replace("''", "”")  # aspas do LaTeX
    t = t.replace("$\\varepsilon$", "ε").replace("\\&", "&").replace("~", " ").replace("--", "–")
    t = t.replace("\\textendash", "–").replace("\\ ", " ")
    t = re.sub(r"\\[a-zA-Z]+\s*", "", t)
    t = t.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", t).strip()


corpo = bbl[bbl.index("\\bibitem"):bbl.index("\\end{thebibliography}")]
refs = []
for m in re.finditer(r"\\bibitem\{(.*?)\}\s*(.*?)(?=\\bibitem\{|\Z)", corpo, re.S):
    t = m.group(2)
    t = re.sub(r"\\hskip[^\\]*\\relax", " ", t)                 # espaços elásticos do IEEEtran
    t = re.sub(r"\\BIBforeignlanguage\{[^}]*\}", "", t)
    t = t.replace("------", "———")                               # mesmo autor da referência anterior
    partes = re.split(r"\\emph\{((?:[^{}]|\{[^{}]*\})*)\}", t)  # ímpares: itálico
    runs = [(f"[{NUM[m.group(1)]}] ", False)]
    for k, pt in enumerate(partes):
        txt = limpa(pt)
        if not txt:
            continue
        if runs and not runs[-1][0].endswith(" ") and not txt.startswith((".", ",", ":", ";", ")")):
            txt = " " + txt
        runs.append((txt, k % 2 == 1))
    refs.append(runs)
assert len(refs) == bbl.count("\\bibitem") and len(refs) >= 50, (len(refs), bbl.count("\\bibitem"))
TAM_REF = 9.5
LINHAS_COLUNA = 35  # linhas de corpo 9,5 que cabem numa coluna de 5,45 pol., acima do logo


def linhas(r):
    """Estimativa de linhas de uma referência; endereços longos quebram em linhas próprias."""
    txt = "".join(t for t, _ in r)
    urls = re.findall(r"https?://\S+", txt)
    for u in urls:
        txt = txt.replace(u, "")
    return -(-len(txt) // 96) + sum(-(-len(u) // 86) for u in urls) + 0.4


paginas, atual, col, usados = [], [[], []], 0, 0
for r in refs:
    n = linhas(r)
    if usados + n > LINHAS_COLUNA and atual[col]:
        if col == 0:
            col, usados = 1, 0
        else:
            paginas.append(atual)
            atual, col, usados = [[], []], 0, 0
    atual[col].append(r)
    usados += n
if atual[0]:
    paginas.append(atual)
for k, (c1, c2) in enumerate(paginas, 1):
    s = nova(4, f"Referências ({k}/{len(paginas)})", "referencias")
    texto(s, 0.9, 0.35, 11.6, 0.7, [P(f"REFERÊNCIAS ({k}/{len(paginas)})", 32, True, GREY)])
    for x0, coluna in [(1.15, c1), (6.85, c2)]:
        if coluna:
            texto(s, x0, 1.15, 5.45, 5.3, [{"runs": [(t, TAM_REF, False, DARK, False, it) for t, it in r], "align": "l", "spacing": 1.0, "after": 4} for r in coluna])
    notas(s, "Não é para ler. São todas as referências do texto do TCC, numeradas na ordem em que aparecem no texto, no padrão IEEE do modelo do Capstone. Pode passar direto para o slide de encerramento.", *COLA)

# ---------------------------------------------------------------- encerramento institucional (fundo 14)
s = nova(14, "Encerramento", "encerramento")
notas(s, "Slide de encerramento do template. Pode ficar na tela durante as perguntas.", *COLA)

# ---------------------------------------------------------------- remove os slides de exemplo do template
lst = prs.slides._sldIdLst
for sid in list(lst)[:N_TPL]:
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)

# ---------------------------------------------------------------- número do slide (campo automático), menos na capa e no encerramento
ESCURO = {2, 3, 5, 14}  # fundos com o canto inferior direito escuro: número em branco
W = prs.slide_width
slides = list(prs.slides)
n = len(slides)
for i, (sl, fundo) in enumerate(zip(slides, FUNDO), 1):
    if i == 1 or i == n:
        continue
    box = sl.shapes.add_textbox(W - Inches(1.05), Inches(6.93), Inches(0.75), Inches(0.38))
    box.name = "Número do slide"
    tf = box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    fld = etree.SubElement(p._p, qn("a:fld"))
    fld.set("id", "{5C1D2E4B-7A3F-4C21-9B8E-1F2A3B4C5D6E}")
    fld.set("type", "slidenum")
    rpr = etree.SubElement(fld, qn("a:rPr"), lang="pt-BR", sz="1400", b="1", dirty="0")
    fill = etree.SubElement(rpr, qn("a:solidFill"))
    etree.SubElement(fill, qn("a:srgbClr"), val="FFFFFF" if fundo in ESCURO else "7F7F7F")
    etree.SubElement(rpr, qn("a:latin"), typeface="Calibri")
    t = etree.SubElement(fld, qn("a:t"))
    t.text = str(i)

prs.save(SAIDA)

# ---------------------------------------------------------------- notas do apresentador e roteiro
saida = Path(SAIDA)
textos = [sl.notes_slide.notes_text_frame.text.strip() for sl in slides]
assert all(textos), [i + 1 for i, t in enumerate(textos) if not t]
blocos = [f"SLIDE {i} — {TITULOS[i - 1]}\n{textos[i - 1]}" for i in range(1, n + 1)]
(saida.parent / "notas-apresentador.txt").write_text("\n\n".join(blocos) + "\n", encoding="utf-8")

partes_r = ["# Roteiro da defesa final (Capstone I)\n\n"
            "Mesmo texto das notas do apresentador do arquivo `apresentacao-defesa-final.pptx`, slide a slide, na ordem "
            "das seções do texto do TCC. Tempo estimado: cerca de 13 minutos (limite da defesa: 15 minutos de apresentação "
            "e 15 de perguntas). As divisórias das seções e os slides de referências não têm fala. As linhas marcadas com "
            "LEMBRETE e a cola das perguntas não são para ler em voz alta.\n"]
primeira_ref = True
for i in range(1, n + 1):
    tipo, linhas_n = TIPO[i - 1], textos[i - 1].split("\n")
    if tipo == "divisoria":
        partes_r.append(f"## Slide {i}: {TITULOS[i - 1]}\n\n(Divisória da seção: não precisa falar.)\n")
    elif tipo == "referencias":
        if primeira_ref:
            partes_r.append(f"## Slides {i} a {n - 1}: Referências\n\n{linhas_n[0]}\n")
            primeira_ref = False
    elif tipo == "encerramento":
        partes_r.append(f"## Slide {i}: Encerramento\n\n{linhas_n[0]}\n")
    else:
        partes_r.append(f"## Slide {i}: {TITULOS[i - 1]}\n\n" + "\n\n".join(linhas_n) + "\n")
partes_r.append("## Cola para as perguntas\n\n" + "\n".join(f"- {c}" for c in COLA[1:]) + "\n")
(saida.parent / "roteiro-defesa-final.md").write_text("\n".join(partes_r), encoding="utf-8")

# tempo estimado: só as falas (sem LEMBRETE, definições, divisórias, referências e encerramento)
palavras = 0
for t, tipo in zip(textos, TIPO):
    if tipo != "fala":
        continue
    for par in t.split("\n"):
        if par.startswith("LEMBRETE") or re.match(r"^(Guia de Kitchenham|PRISMA 2020):", par):
            continue
        palavras += len(par.split())
print(f"ok: {n} slides ({sum(1 for t in TIPO if t == 'fala')} com fala, {TIPO.count('divisoria')} divisórias, "
      f"{len(paginas)} de referências); {len(refs)} referências; {palavras} palavras faladas "
      f"≈ {palavras / 130:.1f} min a 130 palavras/min, {palavras / 145:.1f} min a 145")
