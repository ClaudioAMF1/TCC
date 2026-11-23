"""Monta a apresentação do Capstone I sobre os fundos do template do IDP.

Uso: python monta_template.py TEMPLATE.pptx DECK_ATUAL.pptx SAIDA.pptx
O conteúdo e as notas vêm do deck atual; o visual (fundos, Calibri, cores e
tamanhos) segue o template da disciplina, sem as fotos de pessoas.
"""
import copy
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

TPL, ATUAL, SAIDA = sys.argv[1:4]

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
BLANK = next(l for l in prs.slide_layouts if l.name == "BLANK")
atual = Presentation(ATUAL)
notas = []
for s in atual.slides:
    notas.append([p.text for p in s.notes_slide.notes_text_frame.paragraphs if p.text.strip()])
notas[8] = [t.replace("O gráfico apresenta a distribuição por esfera", "Os círculos mostram a distribuição por esfera") for t in notas[8]]
assert any("círculos" in t for t in notas[8]), notas[8]

def troca(i, a, b):
    alvo = [t for t in notas[i] if a in t]
    assert len(alvo) == 1, (i, a[:40])
    notas[i] = [t.replace(a, b) for t in notas[i]]


troca(10, "Uma adjudicação interna considerou 88 de 123 detecções do B potenciais falsos positivos, principalmente por domínios genéricos. Retirá-las na análise de sensibilidade elevou o kappa a 0,69, mas isso não constitui validação independente por padrão de referência.",
      "Conferi as detecções uma a uma, olhando a classe ou o domínio que gerou cada uma, e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por domínios genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas isso é só uma análise de sensibilidade: não existe uma referência independente que diga a resposta certa.")
troca(11, "medir defasagem e possibilitar reprodutibilidade onde os arquivos estiverem disponíveis.",
      "medir defasagem e possibilitar reprodutibilidade onde os arquivos estiverem disponíveis. Na prática, a coleta usa o apkeep, uma ferramenta aberta da EFF, com uma conta Google criada só para a pesquisa e acesso a partir do Brasil. Para cada aplicativo, registro o hash SHA-256 do arquivo, a versão, a data e, se o download falhar, o motivo; a falha também vira dado. Quando o app vem em pacotes divididos, guardo o APK base, que é onde está o código. Antes do corpus inteiro, testo a coleta em cinco aplicativos.")
troca(12, "A revisão sistemática seguiu o protocolo de Kitchenham e o relato PRISMA 2020.",
      "A revisão sistemática seguiu o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as strings e os critérios de seleção. O fluxo é relatado no modelo PRISMA 2020, que mostra quantos registros entraram e saíram em cada etapa.")


def nova(fundo):
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
    return sl


def texto(sl, x, y, w, h, paras, anchor="t"):
    """paras: lista de dicts {runs:[(texto, pt, negrito, cor)], align, after, before, spacing}."""
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
        if "before" in pd:
            p.space_before = Pt(pd["before"])
        p.line_spacing = pd.get("spacing", 1.0)
        for t, size, bold, cor in pd["runs"]:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(size)
            f.bold = bold
            f.color.rgb = cor
    return box


def P(t, size=18, bold=False, cor=GREY, align="l", after=None, before=None, spacing=1.0):
    d = {"runs": [(t, size, bold, cor)], "align": align, "spacing": spacing}
    if after is not None:
        d["after"] = after
    if before is not None:
        d["before"] = before
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


def notas_em(sl, idx):
    tf = sl.notes_slide.notes_text_frame
    ps = notas[idx]
    tf.text = ps[0]
    for extra in ps[1:]:
        tf.add_paragraph().text = extra


def titulo(sl, t, x=0.9, y=0.7, w=11.6, size=44, cor=GREY, align="l", sub=None, sub_size=24):
    texto(sl, x, y, w, 0.85, [P(t, size, True, cor, align)])
    if sub:
        texto(sl, x, y + 0.85, w, 0.5, [P(sub, sub_size, False, GREY, align)])


# ---------------------------------------------------------------- 1 capa (fundo 1)
s = nova(1)
texto(s, 0.84, 1.55, 6.9, 2.2, [P("Quem mais está dentro do aplicativo?", 44, True, NAVY, spacing=0.9)], anchor="b")
texto(s, 0.84, 3.95, 6.9, 1.0, [P("Rastreamento por terceiros e soberania de dados em aplicativos móveis governamentais brasileiros", 20, False, GREY, spacing=1.05)])
texto(s, 0.84, 5.25, 6.9, 1.2, [P("Claudio da Aparecida Meireles Filho", 18, True, NAVY, after=2),
                                P("Orientador: Prof. Eduardo Arthur Izycki", 16, False, GREY)])
texto(s, 8.75, 2.6, 4.1, 2.4, [P("PROJETO CAPSTONE I", 20, True, WHITE, after=6),
                               P("Simulação de defesa", 18, False, LIGHT, after=18),
                               P("Ciência da Computação", 16, False, PALE),
                               P("IDP · 2026", 16, False, PALE)])
notas_em(s, 0)

# ---------------------------------------------------------------- 2 agenda (fundo 9)
s = nova(9)
texto(s, 0.79, 2.55, 3.4, 0.9, [P("AGENDA", 44, True, GREY)])
texto(s, 0.79, 3.45, 3.4, 1.2, [P("O que será apresentado", 26, False, GREY)])
itens = [("O PROBLEMA", ["Por que olhar os apps públicos", "O que a literatura já mostrou", "Lacuna e contribuição", "Pergunta, objetivos e hipóteses"]),
         ("O MÉTODO E O QUE JÁ FOI FEITO", ["Etapas, pacotes e detectores", "Corpus, anúncios, piloto e fonte dos APKs", "Onde e como a literatura foi buscada", "Limitações, próximos passos e conclusão"])]
y = 0.75
n = 1
for cab, lista in itens:
    texto(s, 6.0, y, 6.4, 0.4, [P(cab, 16, True, MID)])
    y += 0.47
    for it in lista:
        forma(s, 6.0, y + 0.04, 0.44, 0.44, NAVY if n <= 4 else MID, MSO_SHAPE.OVAL)
        texto(s, 6.0, y + 0.04, 0.44, 0.44, [P(str(n), 16, True, WHITE, "c")], anchor="m")
        texto(s, 6.65, y, 5.8, 0.52, [P(it, 19, False, DARK)], anchor="m")
        y += 0.56
        n += 1
    y += 0.22
notas_em(s, 1)

# ---------------------------------------------------------------- 3 motivação + fluxo (fundo 6)
s = nova(6)
titulo(s, "MOTIVAÇÃO", x=1.0, y=0.85, w=6.9, sub="Por que investigar as declarações dos apps públicos")
texto(s, 1.0, 2.75, 6.6, 3.4, [
    P("Previdência, saúde e documentos públicos são acessados por aplicativos: Meu INSS e Meu SUS Digital passam de 50 milhões de instalações cada.", 18, False, DARK, after=12),
    P("Esses aplicativos embutem SDKs de outras empresas, que podem coletar identificadores e dados de uso.", 18, False, DARK, after=12),
    P("O cidadão não escolhe outro prestador. A presença no APK, sozinha, não demonstra transmissão.", 18, True, NAVY)])
# fluxo dentro do quadrado azul-marinho do fundo (x 8.47-12.62, y 1.47-5.62)
caixas = [("Aplicativo do governo", "o que o cidadão instala"), ("SDK de terceiro embutido", "análise de uso, mapas, anúncios"), ("Servidor da empresa", "para onde os dados podem ir")]
cy = 1.68
for i, (a, b) in enumerate(caixas):
    forma(s, 8.82, cy, 3.45, 0.78, WHITE)
    texto(s, 8.92, cy + 0.04, 3.25, 0.7, [P(a, 17, True, NAVY, "c"), P(b, 13, False, GREY, "c")], anchor="m")
    if i < 2:
        forma(s, 10.4, cy + 0.83, 0.3, 0.26, MID, MSO_SHAPE.DOWN_ARROW)
    cy += 1.14
texto(s, 8.75, 4.75, 3.6, 0.75, [P("Pergunta central: o que está declarado é compatível com os SDKs?", 15, True, WHITE, "c", spacing=1.05)], anchor="m")
notas_em(s, 2)

# ---------------------------------------------------------------- 4 literatura (fundo 5: três colunas)
s = nova(5)
cols = [(0.0, "Binns et al. (2018)", "959 mil", "apps da Google Play", "A maioria tem rastreamento de terceiros, concentrado em poucos fornecedores.", NAVY, DARK),
        (4.44, "Kollnig et al. (2021)", "GDPR", "antes e depois da lei", "A presença de rastreadores mudou pouco; o desenho não prova efeito causal da lei.", WHITE, WHITE),
        (8.89, "Samarasinghe et al. (2022)", "1.166", "apps de governo, 71 países", "37% com rastreadores do Google; 27% enviavam dados sensíveis a terceiros ou sem criptografia.", WHITE, WHITE)]
for x0, autor, num, leg, txt, c1, c2 in cols:
    texto(s, x0 + 0.5, 1.0, 3.45, 0.45, [P(autor, 20, True, c1, "c")])
    texto(s, x0 + 0.5, 1.75, 3.45, 1.0, [P(num, 54, True, c1, "c")], anchor="m")
    texto(s, x0 + 0.5, 2.8, 3.45, 0.45, [P(leg, 18, False, c2, "c")])
    texto(s, x0 + 0.55, 3.65, 3.35, 2.2, [P(txt, 18, False, c2, "c", spacing=1.05)])
notas_em(s, 3)

# ---------------------------------------------------------------- 5 lacuna (fundo 7: três abas)
s = nova(7)
titulo(s, "LACUNA E CONTRIBUIÇÃO", x=0.9, y=0.75, w=11.5)
abas = [(1.83, "01", "Corpus brasileiro", "Apps federais, estaduais e municipais, com atenção aos que tratam dados sensíveis."),
        (5.43, "02", "Transparência", "SDKs identificados confrontados com as categorias de dados e finalidades declaradas."),
        (9.07, "03", "Checagem do método", "Detectores nas mesmas versões e, numa subamostra, os fluxos de rede observados.")]
for x0, num, cab, txt in abas:
    texto(s, x0 + 0.25, 2.75, 1.9, 0.6, [P(num, 30, True, LIGHT)])
    texto(s, x0 + 0.25, 3.45, 1.95, 1.2, [P(cab, 20, True, WHITE, spacing=0.95)])
    texto(s, x0 - 0.2, 5.1, 2.75, 1.3, [P(txt, 14, False, GREY, "c", spacing=1.05)])
texto(s, 1.5, 6.55, 10.4, 0.4, [P("Lacuna delimitada à literatura examinada até agora; sujeita à conclusão da revisão.", 13, False, GREY, "c")])
notas_em(s, 4)

# ---------------------------------------------------------------- 6 pergunta e objetivos (fundo 13: barra de título)
s = nova(13)
texto(s, 0.65, 0.42, 9.8, 0.85, [P("PERGUNTA E OBJETIVOS", 40, True, LIGHT)], anchor="m")
texto(s, 0.9, 1.95, 11.6, 0.35, [P("PERGUNTA DE PESQUISA", 14, True, MID)])
texto(s, 0.9, 2.3, 11.6, 1.2, [P("Em que medida os aplicativos móveis oficiais do governo brasileiro embarcam SDKs de rastreamento de terceiros e enviam dados a terceiros sem que isso esteja declarado em suas políticas de privacidade e na seção “Segurança dos dados” da Google Play?", 20, True, NAVY, spacing=1.0)])
texto(s, 0.9, 3.7, 11.6, 0.35, [P("OBJETIVO GERAL", 14, True, MID)])
texto(s, 0.9, 4.05, 11.6, 0.9, [P("Medir a proporção de SDKs de rastreamento e de envios de dados sem declaração compatível nos apps governamentais brasileiros, à luz da LGPD, distinguindo a evidência estática dos fluxos de rede observados.", 17, False, DARK)])
texto(s, 0.9, 5.1, 11.6, 0.35, [P("OBJETIVOS ESPECÍFICOS", 14, True, MID)])
objs = ["Conferir o corpus", "Detectar SDKs", "Comparar declarações", "Observar fluxos", "Verificar detectores"]
for i, o in enumerate(objs):
    x0 = 0.9 + i * 2.36
    forma(s, x0, 5.5, 2.2, 0.75, PALE)
    texto(s, x0 + 0.1, 5.5, 2.0, 0.75, [P(f"{i+1}. {o}", 15, True, NAVY, "c")], anchor="m")
notas_em(s, 5)

# ---------------------------------------------------------------- 7 hipóteses (fundo 12: duas colunas)
s = nova(12)
texto(s, 1.0, 0.7, 11.3, 0.85, [P("HIPÓTESES", 44, True, MID, "c")])
blocos_e = [("H1 · principal · declarações", "Ao menos 1 em cada 10 pares aplicativo–SDK sem declaração compatível. IC95%; limiar do estudo, não da lei."),
            ("H2 · secundária · dados sensíveis", "Apps que tratam dados sensíveis não têm menor prevalência de SDKs que os demais apps governamentais.")]
blocos_d = [("Referência comercial · contexto", "252 apps comerciais descrevem o contexto. Não são grupo de controle nem base de teste."),
            ("Detectores · checagem do instrumento", "Concordância entre métodos e bases, com κ de Fleiss. Não é uma hipótese.")]
for x0, blocos, cor in [(0.9, blocos_e, NAVY), (7.05, blocos_d, MID)]:
    y0 = 2.15
    for cab, txt in blocos:
        forma(s, x0, y0 + 0.05, 0.09, 1.55, cor)
        texto(s, x0 + 0.3, y0, 5.1, 0.45, [P(cab, 19, True, cor)])
        texto(s, x0 + 0.3, y0 + 0.5, 5.1, 1.2, [P(txt, 17, False, DARK, spacing=1.05)])
        y0 += 2.05
texto(s, 0.9, 6.35, 11.6, 0.4, [P("Declaração compatível pode ser por categoria e finalidade; SDK no APK não comprova envio de dados.", 13, False, GREY, "c")])
notas_em(s, 6)

# ---------------------------------------------------------------- 8 procedimentos (fundo 4: branco)
s = nova(4)
titulo(s, "MÉTODO", x=0.9, y=0.55, sub="Seis etapas, em estudo quantitativo e observacional")
etapas = [("Corpus", "Google Play e catálogo de cada publicador; oficialidade conferida"),
          ("Caracterização", "Esfera de governo, tipo de serviço e dados sensíveis"),
          ("Pacotes atuais", "Versão atual da Google Play, com hash; AndroZoo para a defasagem"),
          ("Detectores", "Código e domínios; concordância entre ferramentas"),
          ("Declarado × detectado", "Política e “Segurança dos dados”: categorias e finalidades"),
          ("Análise", "Proporções com IC95% e subamostra dinâmica")]
W, H, G = 3.7, 1.95, 0.25
for i, (cab, txt) in enumerate(etapas):
    col, lin = i % 3, i // 3
    x0, y0 = 0.9 + col * (W + G), 2.3 + lin * (H + G)
    cor = NAVY if lin == 0 else MID
    forma(s, x0, y0, W, H, cor)
    texto(s, x0 + 0.25, y0 + 0.2, 0.6, 0.6, [P(str(i + 1), 30, True, WHITE)])
    texto(s, x0 + 0.85, y0 + 0.24, W - 1.05, 0.5, [P(cab, 19, True, WHITE)])
    texto(s, x0 + 0.85, y0 + 0.8, W - 1.05, 1.05, [P(txt, 14, False, LIGHT, spacing=1.05)])
notas_em(s, 7)

# ---------------------------------------------------------------- 9 corpus (fundo 11: círculos)
s = nova(11)
texto(s, 1.0, 0.95, 5.3, 0.85, [P("CORPUS", 44, True, MID)])
texto(s, 1.0, 1.8, 5.3, 0.5, [P("396 candidatos, 376 oficiais", 24, False, GREY)])
texto(s, 1.0, 2.6, 5.0, 3.6, [
    P("Oficialidade conferida pelo nome jurídico em “Sobre o desenvolvedor”.", 17, False, DARK, after=10),
    P("Saíram 20: 13 empresas privadas e 7 contas de pessoa física.", 17, False, DARK, after=10),
    P("100 dos 376 com possível tratamento sensível (saúde ou biometria); 108 divergências em relação à regra automática.", 17, False, DARK, after=10),
    P("Classificação preliminar, conferida antes da coleta.", 15, True, NAVY)])
texto(s, 6.61, 2.85, 3.61, 1.8, [P("376", 60, True, WHITE, "c"), P("apps oficiais", 18, False, PALE, "c")], anchor="m")
for (cx, cy), (num, leg) in zip([(10.68, 1.83), (11.63, 3.76), (10.68, 5.72)], [("85", "federais"), ("199", "estaduais"), ("92", "municipais")]):
    texto(s, cx - 0.86, cy - 0.5, 1.72, 1.0, [P(num, 26, True, NAVY, "c"), P(leg, 13, False, DARK, "c")], anchor="m")
notas_em(s, 8)

# ---------------------------------------------------------------- 10 anúncios (fundo 8: faixa diagonal)
s = nova(8)
texto(s, 1.34, 1.0, 7.0, 0.85, [P("ANÚNCIOS", 44, True, GREY)])
texto(s, 1.34, 2.5, 6.0, 0.5, [P("O que a declaração mostra e o que não mostra", 22, False, GREY)])
for x0, num, cor, leg, ic in [(1.34, "0 de 376", NAVY, "apps de governo declaram anúncios", "IC95%: 0% a 1,0%"),
                              (4.25, "63 de 190", MID, "comerciais da referência inicial (33,2%)", "IC95%: 26,9% a 40,1%")]:
    forma(s, x0, 3.3, 2.7, 1.75, cor)
    texto(s, x0 + 0.15, 3.42, 2.4, 0.7, [P(num, 32, True, WHITE, "c")], anchor="m")
    texto(s, x0 + 0.15, 4.12, 2.4, 0.85, [P(leg, 13, False, WHITE, "c"), P(ic, 12, True, LIGHT, "c")])
texto(s, 1.34, 5.3, 5.5, 1.2, [P("A declaração é feita pelo próprio publicador e não informa os SDKs embarcados. A referência comercial é só contexto descritivo.", 15, False, DARK, spacing=1.05)])
notas_em(s, 9)

# ---------------------------------------------------------------- 11 piloto (fundo 13: barra de título)
s = nova(13)
texto(s, 0.65, 0.42, 9.8, 0.85, [P("PILOTO DOS DETECTORES", 40, True, LIGHT)], anchor="m")
texto(s, 0.9, 1.85, 7.5, 0.5, [P("Ferramentas diferentes dão taxas diferentes", 24, False, GREY)])
barras = [("A · Exodus, código", 15, NAVY), ("B · Exodus, domínios", 19, MID), ("C · Disconnect, domínios", 16, NAVY)]
for i, (lab, k, cor) in enumerate(barras):
    y0 = 2.75 + i * 1.05
    texto(s, 0.9, y0, 2.75, 0.7, [P(lab, 16, True, DARK)], anchor="m")
    forma(s, 3.75, y0 + 0.08, 4.6, 0.54, LIGHT)
    forma(s, 3.75, y0 + 0.08, 4.6 * k / 20, 0.54, cor)
    texto(s, 3.85, y0 + 0.08, 4.4 * k / 20, 0.54, [P(f"{k} de 20 · {k*5}%", 15, True, WHITE, "r")], anchor="m")
texto(s, 0.9, 5.95, 7.6, 0.5, [P("Proporção dos 20 pacotes de teste com ao menos um rastreador, por detector.", 13, False, GREY)])
forma(s, 9.0, 2.0, 3.6, 4.25, NAVY)
texto(s, 9.2, 2.2, 3.2, 3.9, [P("κ de Fleiss", 18, True, PALE, "c"),
                             P("0,52", 54, True, WHITE, "c", after=2),
                             P("0,69 na análise de sensibilidade", 15, False, LIGHT, "c", after=14),
                             P("88 de 123 detecções de B questionadas na conferência interna, sem referência independente", 14, False, LIGHT, "c", spacing=1.05)], anchor="m")
notas_em(s, 10)

# ---------------------------------------------------------------- 12 fonte dos APKs (fundo 2: azul-marinho)
s = nova(2)
texto(s, 0.9, 0.95, 11.5, 0.85, [P("FONTE DOS APKS", 44, True, WHITE)])
texto(s, 0.9, 1.8, 11.5, 0.5, [P("Consulta histórica ao AndroZoo, acervo acadêmico de pacotes", 22, False, PALE)])
for x0, num, cor, leg in [(0.9, "23,2%", WHITE, "governo: 92 de 396 candidatos"), (4.7, "84,2%", MID, "referência inicial: 160 de 190 (contexto)")]:
    texto(s, x0, 2.45, 3.7, 1.1, [P(num, 66, True, cor)])
    texto(s, x0, 3.55, 3.7, 0.5, [P(leg, 16, False, PALE)])
texto(s, 8.75, 2.6, 3.7, 1.5, [P("Fonte principal: versão atual na Google Play", 19, True, WHITE, after=6),
                               P("AndroZoo: reprodutibilidade e defasagem", 16, False, PALE)])
forma(s, 0.9, 4.2, 11.5, 0.03, MID)
texto(s, 0.9, 4.32, 11.5, 0.35, [P("COMO SERÁ A COLETA", 14, True, PALE)])
passos_c = [("Conta da pesquisa", "Conta Google criada só para o estudo, com acesso a partir do Brasil"),
            ("Download com apkeep", "Ferramenta aberta da EFF; em pacotes divididos, guarda o APK base"),
            ("Registro", "SHA-256 do arquivo, versão, data e o motivo de cada falha"),
            ("Teste primeiro", "Cinco apps em fevereiro; depois o corpus inteiro")]
for i, (cab, txt) in enumerate(passos_c):
    x0 = 0.9 + i * 2.92
    forma(s, x0, 4.72, 2.75, 1.5, LIGHT)
    texto(s, x0 + 0.18, 4.84, 0.45, 0.45, [P(str(i + 1), 24, True, NAVY)], anchor="m")
    texto(s, x0 + 0.62, 4.84, 2.0, 0.45, [P(cab, 15, True, NAVY)], anchor="m")
    texto(s, x0 + 0.18, 5.36, 2.42, 0.85, [P(txt, 13, False, DARK, spacing=1.05)])
notas_em(s, 11)

# ---------------------------------------------------------------- 13 revisão (fundo 10: faixa central)
s = nova(10)
cols = [("ONDE", "4 bases e 17 buscas: Scopus (principal), IEEE Xplore, SBC OpenLib e BDTD; 2015 a 2026; inglês e português; 6/11/2026"),
        ("COMO", "Strings em três blocos: aplicativo AND fenômeno (rastreador, SDK, política) AND contexto (governo, COVID-19 ou Brasil)"),
        ("VALIDAÇÃO", "11 estudos de controle: as buscas acharam os 10 que o Scopus indexa. Protocolo de Kitchenham e fluxo PRISMA 2020")]
for i, (cab, txt) in enumerate(cols):
    x0 = 0.75 + i * 3.62
    texto(s, x0, 0.55, 3.35, 0.4, [P(cab, 16, True, NAVY)])
    texto(s, x0, 0.98, 3.35, 1.55, [P(txt, 14, False, DARK, spacing=1.05)])
texto(s, 0.5, 2.6, 10.8, 2.27, [P("REVISÃO SISTEMÁTICA", 44, True, WHITE, "c")], anchor="m")
fluxo = [("1.531", "registros"), ("1.249", "sem duplicatas"), ("357", "à leitura completa"), ("71", "propostas de inclusão")]
for i, (num, leg) in enumerate(fluxo):
    x0 = 0.9 + i * 2.95
    texto(s, x0, 5.0, 2.3, 0.65, [P(num, 34, True, NAVY, "c")], anchor="m")
    texto(s, x0, 5.62, 2.3, 0.4, [P(leg, 14, False, GREY, "c")])
    if i < 3:
        forma(s, x0 + 2.42, 5.17, 0.38, 0.3, MID, MSO_SHAPE.RIGHT_ARROW)
texto(s, 1.4, 6.25, 10.6, 0.45, [P("Os 278 registros em aberto e a bola de neve ficam para o Capstone II; as 71 são propostas, não inclusões finais.", 13, False, GREY, "c")])
notas_em(s, 12)

# ---------------------------------------------------------------- 14 limitações e próximos passos (fundo 12)
s = nova(12)
texto(s, 0.6, 0.7, 12.1, 0.85, [P("LIMITAÇÕES E PRÓXIMOS PASSOS", 40, True, MID, "c")])
texto(s, 0.9, 2.05, 5.4, 0.45, [P("Limitações declaradas", 20, True, NAVY)])
lims = ["SDK no APK não comprova transmissão", "Só Android e Google Play", "Políticas nem sempre nomeiam SDKs", "Versões e fontes podem divergir", "Classificações e revisão ainda em conferência"]
texto(s, 0.9, 2.6, 5.5, 3.6, [P("•  " + l, 17, False, DARK, after=10) for l in lims])
texto(s, 7.05, 2.05, 5.4, 0.45, [P("Próximas etapas", 20, True, NAVY)])
passos = [("Até 03/12", "Ajustes do orientador e da simulação"), ("Fev/2027", "Concluir a revisão e conferir o corpus"), ("Mar–Abr/2027", "Coleta atual, SDKs e declarações"), ("Mai–Jun/2027", "Análise, discussão jurídica e defesa")]
for i, (q, o) in enumerate(passos):
    y0 = 2.62 + i * 0.86
    forma(s, 7.05, y0, 1.75, 0.6, NAVY if i == 0 else MID)
    texto(s, 7.05, y0, 1.75, 0.6, [P(q, 14, True, WHITE, "c")], anchor="m")
    texto(s, 9.0, y0, 3.5, 0.6, [P(o, 16, False, DARK)], anchor="m")
notas_em(s, 13)

# ---------------------------------------------------------------- 15 conclusão (fundo 3: azul médio)
s = nova(3)
texto(s, 0.9, 1.3, 11.4, 2.2, [P("Problema definido.", 44, True, WHITE), P("Método viável.", 44, True, WHITE), P("Resultados ainda preliminares.", 44, True, NAVY)])
texto(s, 0.9, 4.0, 10.8, 1.2, [P("O que os aplicativos do governo declaram é compatível com os SDKs identificados e os fluxos observados?", 22, False, WHITE, spacing=1.05)])
texto(s, 0.9, 5.55, 6.0, 0.6, [P("Obrigado. Perguntas?", 24, True, NAVY)])
notas_em(s, 14)

# ---------------------------------------------------------------- 16 encerramento institucional (fundo 14)
s = nova(14)
s.notes_slide.notes_text_frame.text = "Slide de encerramento do template. Pode ficar na tela durante as perguntas."

# remove os 14 slides de exemplo do template
lst = prs.slides._sldIdLst
for sid in list(lst)[:14]:
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)
prs.save(SAIDA)
print("ok", len(prs.slides), "slides")
