"""Monta os slides da defesa final do Capstone I sobre os fundos do template do IDP.

Uso: python monta_slides_defesa_final.py TEMPLATE.pptx main.bbl SAIDA.pptx

Segue a ordem do texto do TCC (introdução, referencial teórico, procedimentos
metodológicos, conclusão e referências) e aplica os comentários da simulação de
24/11/2026: título sem pergunta, uma única hipótese baseada na literatura, sem o
termo "corpus", objetivos com verbos concretos, tabela de estudos, lacuna visual,
método em tabela, justificativa do Android, explicação do kappa de Fleiss,
revisão afunilada, próximos passos em tabela e todas as referências do texto.
"""
import copy
import re
import sys

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

TPL, BBL, SAIDA = sys.argv[1:4]

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
FUNDO = []  # fundo usado em cada slide novo, para a cor do número


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
    FUNDO.append(fundo)
    return sl


def _run(p, t, size, bold, cor, sub=False, italic=False):
    r = p.add_run()
    r.text = t
    f = r.font
    f.name = FONT
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = cor
    if sub:
        r.font._rPr.set("baseline", "-25000")
    return r


def texto(sl, x, y, w, h, paras, anchor="t"):
    """paras: lista de dicts {runs:[(texto, pt, negrito, cor[, sub])], align, after, before, spacing}."""
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
        for run in pd["runs"]:
            _run(p, *run)
    return box


def P(t, size=18, bold=False, cor=GREY, align="l", after=None, before=None, spacing=1.0):
    d = {"runs": [(t, size, bold, cor)], "align": align, "spacing": spacing}
    if after is not None:
        d["after"] = after
    if before is not None:
        d["before"] = before
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


def titulo(sl, t, x=0.9, y=0.7, w=11.6, size=40, cor=GREY, align="l", sub=None, sub_size=22):
    texto(sl, x, y, w, 0.85, [P(t, size, True, cor, align)])
    if sub:
        texto(sl, x, y + 0.8, w, 0.5, [P(sub, sub_size, False, GREY, align)])


def barra_titulo(sl, t, sub=None):
    """Título dentro da barra azul do fundo 13."""
    texto(sl, 0.65, 0.42, 11.0, 0.85, [P(t, 36, True, LIGHT)], anchor="m")
    if sub:
        texto(sl, 0.9, 1.6, 11.6, 0.42, [P(sub, 19, False, GREY)])


def notas(sl, *paragrafos):
    tf = sl.notes_slide.notes_text_frame
    tf.text = paragrafos[0]
    for extra in paragrafos[1:]:
        tf.add_paragraph().text = extra


def tabela(sl, x, y, larguras, cab, linhas, size=12, cab_size=13, primeira_negrito=True, alt_h=0.4, cab_h=0.45):
    """Tabela com cabeçalho azul-marinho e linhas alternadas, em Calibri."""
    nl, nc = len(linhas) + 1, len(cab)
    shp = sl.shapes.add_table(nl, nc, Inches(x), Inches(y), Inches(sum(larguras)), Inches(cab_h + alt_h * (nl - 1)))
    tbl = shp.table
    # sem estilo de tabela do tema: cores definidas célula a célula
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
                conteudo = linhas[i - 1][j]
                tam = size
                neg = primeira_negrito and j == 0
                cor = NAVY if neg else DARK
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            if isinstance(conteudo, list):  # runs
                for run in conteudo:
                    _run(p, *run)
            else:
                _run(p, conteudo, tam, neg, cor)
    return tbl


# ---------------------------------------------------------------- textos que se repetem
COLA = [
    "COLA PARA AS PERGUNTAS (não é para ler em voz alta).",
    "Números: 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · AndroZoo: 92 de 396 (23,2%) · piloto: 75%, 95% e 80% com rastreador; κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · revisão: 552 resultados, 413 sem repetidos, 210 à leitura completa.",
    "Por que 10%? Fica bem abaixo da literatura (Andow 42,4%; Samarasinghe 27%), que conta por aplicativo; eu conto por par. Um patamar baixo deixa o teste mais exigente. Não é limite da LGPD.",
    "Por que só Android? 73,76% dos celulares no Brasil (StatCounter, out. 2026); no iPhone os apps são criptografados e não há ferramenta pública para baixá-los em escala (Kollnig et al., 2022); a seção “Segurança dos dados” é da Google Play. Não quer dizer que o iPhone seja mais seguro.",
    "Por que uma hipótese só? Para concentrar o trabalho no que dá para provar no Capstone II: as declarações. A comparação dos aplicativos com dados sensíveis saiu do projeto.",
    "O κ de 0,52 não é baixo? É moderado. Por isso a concordância entre detectores é checagem do instrumento, com limiar de 0,6, e não uma hipótese.",
    "Ter o SDK no app prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos apps.",
    "Por que a revisão caiu de 1.531 para 552? Passei a exigir um termo do tema no título; os dez estudos de controle continuaram.",
    "Você leu todos os artigos? Não. A leitura completa está em andamento: já conferi parte das decisões lendo o texto inteiro e termino o restante em fevereiro, antes de qualquer resultado.",
    "Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”",
]

# ---------------------------------------------------------------- 1 capa (fundo 1)
s = nova(1)
texto(s, 0.84, 0.95, 6.9, 2.75, [P("Rastreamento por terceiros em aplicativos móveis governamentais brasileiros", 36, True, NAVY, spacing=0.92)], anchor="b")
texto(s, 0.84, 3.9, 6.9, 1.0, [P("SDKs embarcados e transparência das declarações de privacidade", 21, False, GREY, spacing=1.05)])
texto(s, 0.84, 5.25, 6.9, 1.2, [P("Claudio da Aparecida Meireles Filho", 18, True, NAVY, after=2),
                                P("Orientador: Prof. Eduardo Arthur Izycki", 16, False, GREY)])
texto(s, 8.75, 2.6, 4.1, 2.4, [P("PROJETO CAPSTONE I", 20, True, WHITE, after=6),
                               P("Defesa final", 18, False, LIGHT, after=18),
                               P("Ciência da Computação", 16, False, PALE),
                               P("IDP · 2026", 16, False, PALE)])
notas(s, "Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu trabalho é sobre rastreamento por terceiros nos aplicativos do governo brasileiro. Muitos desses aplicativos trazem, dentro deles, código de outras empresas, que pode coletar dados de quem usa. Eu quero descobrir que código é esse e se o governo avisa o cidadão sobre isso.")

# ---------------------------------------------------------------- 2 agenda (fundo 9)
s = nova(9)
texto(s, 1.15, 2.78, 2.34, 0.74, [P("AGENDA", 44, True, GREY)])
caps = [("1", "INTRODUÇÃO", ["Motivação", "Problema, objetivos e hipótese"]),
        ("2", "REFERENCIAL TEÓRICO", ["Estudos que orientam o projeto", "Lacuna e contribuição"]),
        ("3", "PROCEDIMENTOS METODOLÓGICOS", ["Etapas do método e escolha do Android", "Aplicativos, fonte dos pacotes e piloto",
                                              "Concordância entre detectores (κ de Fleiss)", "Revisão sistemática",
                                              "Limitações e próximos passos"]),
        ("4", "CONCLUSÃO E REFERÊNCIAS", [])]
y = 0.55
for num, cab, lista in caps:
    forma(s, 6.0, y, 0.46, 0.46, NAVY, MSO_SHAPE.OVAL)
    texto(s, 6.0, y, 0.46, 0.46, [P(num, 17, True, WHITE, "c")], anchor="m")
    texto(s, 6.65, y, 5.9, 0.46, [P(cab, 18, True, NAVY)], anchor="m")
    y += 0.52
    for it in lista:
        texto(s, 6.65, y, 5.9, 0.38, [P(it, 17, False, DARK)], anchor="m")
        y += 0.38
    y += 0.16
notas(s, "Vou seguir a mesma ordem do texto do TCC. Na introdução, a motivação, o problema, os objetivos e a hipótese. No referencial teórico, os estudos que orientam o projeto e a lacuna que eles deixam. Nos procedimentos metodológicos, as etapas do método, por que escolhi o Android, os aplicativos selecionados, a fonte dos pacotes e o piloto, como leio a concordância entre os detectores, a revisão sistemática, as limitações e os próximos passos. Fecho com a conclusão e as referências.")

# ---------------------------------------------------------------- 3 motivação (fundo 6)
s = nova(6)
titulo(s, "MOTIVAÇÃO", x=1.0, y=0.85, w=6.9, size=44, sub="Por que olhar o que os apps públicos declaram", sub_size=22)
texto(s, 1.0, 2.75, 6.6, 3.4, [
    P("Previdência, saúde e documentos públicos são acessados por aplicativos: Meu INSS e Meu SUS Digital passam de 50 milhões de instalações cada.", 18, False, DARK, after=12),
    P("Esses aplicativos embutem SDKs de outras empresas, que podem coletar identificadores e dados de uso.", 18, False, DARK, after=12),
    P("O cidadão não escolhe outro prestador. A presença no APK, sozinha, não demonstra transmissão.", 18, True, NAVY)])
caixas = [("Aplicativo do governo", "o que o cidadão instala"), ("SDK de terceiro embutido", "análise de uso, mapas, anúncios"), ("Servidor da empresa", "para onde os dados podem ir")]
cy = 1.68
for i, (a, b) in enumerate(caixas):
    forma(s, 8.82, cy, 3.45, 0.78, WHITE)
    texto(s, 8.92, cy + 0.04, 3.25, 0.7, [P(a, 17, True, NAVY, "c"), P(b, 13, False, GREY, "c")], anchor="m")
    if i < 2:
        forma(s, 10.4, cy + 0.83, 0.3, 0.26, MID, MSO_SHAPE.DOWN_ARROW)
    cy += 1.14
texto(s, 8.75, 4.75, 3.6, 0.75, [P("Foco: os SDKs embarcados estão declarados ao cidadão?", 15, True, WHITE, "c", spacing=1.05)], anchor="m")
notas(s, "Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada. Só que esses aplicativos não têm só o código do órgão: eles trazem pedaços prontos de outras empresas, os SDKs, para coisas como mapas, notificações e estatísticas de uso. Alguns desses SDKs podem coletar dados de quem usa. No governo isso pesa mais, porque o cidadão não tem como trocar de aplicativo. E um detalhe importante: o SDK estar dentro do aplicativo não prova que ele enviou dados.")

# ---------------------------------------------------------------- 4 problema e objetivo geral (fundo 13)
s = nova(13)
barra_titulo(s, "PROBLEMA E OBJETIVO GERAL")
texto(s, 0.9, 1.75, 11.6, 0.35, [P("PROBLEMA DE PESQUISA", 14, True, MID)])
texto(s, 0.9, 2.1, 11.6, 1.2, [P("Em que medida os SDKs de rastreamento de terceiros embarcados nos aplicativos Android oficiais do governo brasileiro estão declarados nas políticas de privacidade e na seção “Segurança dos dados” da Google Play?", 21, True, NAVY, spacing=1.0)])
texto(s, 0.9, 3.45, 11.6, 0.35, [P("OBJETIVO GERAL", 14, True, MID)])
texto(s, 0.9, 3.8, 11.6, 1.0, [P("Medir a proporção de pares aplicativo–SDK de rastreamento sem declaração compatível nos aplicativos Android governamentais brasileiros, comparando os SDKs encontrados no código com a política de privacidade e a seção “Segurança dos dados”, à luz da LGPD.", 18, False, DARK, spacing=1.05)])
# o que é um par aplicativo–SDK
forma(s, 0.9, 5.0, 11.6, 1.25, PALE)
texto(s, 1.15, 5.05, 3.1, 1.15, [P("Par aplicativo–SDK", 18, True, NAVY), P("a unidade que será contada", 14, False, DARK)], anchor="m")
exemplo = [("Aplicativo X", NAVY), ("SDK de estatísticas", MID), ("SDK de mapas", MID), ("SDK de notificações", MID)]
forma(s, 4.45, 5.3, 1.75, 0.65, NAVY)
texto(s, 4.45, 5.3, 1.75, 0.65, [P("Aplicativo X", 15, True, WHITE, "c")], anchor="m")
for k, nome in enumerate(["estatísticas", "mapas", "notificações"]):
    x0 = 6.6 + k * 1.95
    forma(s, x0 - 0.33, 5.51, 0.28, 0.24, MID, MSO_SHAPE.RIGHT_ARROW)
    forma(s, x0, 5.3, 1.75, 0.65, WHITE, linha=MID)
    texto(s, x0, 5.3, 1.75, 0.65, [P("SDK de " + nome, 13, True, NAVY, "c")], anchor="m")
texto(s, 6.27, 5.97, 6.0, 0.3, [P("1 aplicativo com 3 SDKs = 3 pares; cada par é conferido nas declarações", 12, False, DARK, "c")])
notas(s, "O problema da pesquisa é este: em que medida os SDKs de rastreamento que estão dentro dos aplicativos oficiais do governo estão declarados para o cidadão, na política de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo geral é medir isso como uma proporção, à luz da LGPD. A unidade que eu conto é o par aplicativo–SDK: cada SDK encontrado em cada aplicativo forma um par. Um aplicativo com três SDKs, por exemplo, gera três pares. Para cada par, verifico se o que aquele SDK faz aparece nas declarações do aplicativo.")

# ---------------------------------------------------------------- 5 objetivos específicos (fundo 13)
s = nova(13)
barra_titulo(s, "OBJETIVOS ESPECÍFICOS")
objs = [
    ["1. Revisar a lista de aplicativos", "Conferir um a um os 376 aplicativos classificados como oficiais, pelo nome jurídico do desenvolvedor na Google Play, e a esfera de governo", "Lista final e taxa de erro da classificação automática"],
    ["2. Listar os SDKs de cada aplicativo", "Baixar a versão atual na Google Play (hash SHA-256, versão e data) e rodar três detectores baseados nas listas Exodus Privacy e Disconnect", "Pares aplicativo–SDK, com a evidência de cada detecção"],
    ["3. Classificar as declarações", "Ler a política de privacidade e a seção “Segurança dos dados” e pôr cada par em uma de cinco categorias, da menção pelo nome à política indisponível", "Proporção de pares sem declaração compatível, com IC95% (teste da H1)"],
    ["4. Registrar para onde os dados vão", "Instalar uma subamostra num celular Android de teste e gravar o tráfego de rede durante o uso", "Domínios, país de destino e se estão declarados"],
    ["5. Medir a concordância dos detectores", "Calcular o κ de Fleiss e as concordâncias positiva e negativa nos mesmos pacotes", "Quanto a taxa muda conforme a ferramenta"],
]
tabela(s, 0.75, 1.75, [3.0, 5.6, 3.3], ["Objetivo", "O que será feito e como", "Resultado"], objs, size=13, alt_h=0.8)
notas(s, "Para chegar lá, são cinco objetivos específicos. Primeiro, revisar um a um os 376 aplicativos que classifiquei como oficiais, pelo nome jurídico de quem publica na Google Play, e medir quanto a classificação automática errou. Segundo, baixar a versão atual de cada aplicativo, registrando o hash, que é a impressão digital do arquivo, e listar os SDKs com três detectores. Terceiro, ler a política de privacidade e a seção “Segurança dos dados” e classificar cada par em uma de cinco categorias: o SDK citado pelo nome; o tipo de dado e a finalidade declarados, sem citar o nome; nenhuma declaração compatível; informação insuficiente; ou política indisponível. É daí que sai a proporção que testa a hipótese. Quarto, instalar uma parte dos aplicativos num celular de teste e registrar para onde os dados vão. Quinto, medir se os três detectores concordam, com o kappa de Fleiss.")

# ---------------------------------------------------------------- 6 hipótese (fundo 4)
s = nova(4)
titulo(s, "HIPÓTESE", x=0.9, y=0.45, size=40, cor=MID)
forma(s, 0.9, 1.4, 5.6, 3.15, NAVY)
texto(s, 1.15, 1.55, 5.1, 2.9, [P("H1", 30, True, PALE, after=4),
                                P("Ao menos 10% dos pares aplicativo–SDK de rastreamento não terão declaração compatível na política de privacidade nem na seção “Segurança dos dados” da Google Play.", 18, True, WHITE, spacing=1.05)])
texto(s, 0.9, 4.75, 5.6, 0.35, [P("CRITÉRIO DE REJEIÇÃO", 13, True, MID)])
texto(s, 0.9, 5.08, 5.6, 1.4, [P("A H1 é rejeitada se o limite superior do IC95% da proporção ficar abaixo de 10%. O intervalo considera que um aplicativo pode ter vários SDKs.", 14, False, DARK, spacing=1.05)])
texto(s, 6.95, 1.4, 5.5, 0.35, [P("BASE NA LITERATURA", 13, True, MID)])
base = [("Andow et al. (2020)", "13.796 apps: até 42,4% omitiam ou declaravam errado fluxos de dados sensíveis"),
        ("Samarasinghe et al. (2022)", "1.166 apps de governo de 71 países: 27% enviavam informações sensíveis a terceiros ou sem criptografia"),
        ("Carlsson et al. (2022)", "32 apps do setor público finlandês: políticas divergiam dos dados enviados a terceiros"),
        ("Kollnig et al. (2022)", "24 mil apps Android e iOS: falta de transparência sobre o rastreamento nas duas plataformas")]
for k, (aut, txt) in enumerate(base):
    y0 = 1.78 + k * 1.0
    forma(s, 6.95, y0, 0.07, 0.86, MID)
    texto(s, 7.15, y0, 5.3, 0.9, [P(aut, 14, True, NAVY), P(txt, 13, False, DARK, spacing=1.0)])
forma(s, 6.95, 5.85, 5.5, 0.62, PALE)
texto(s, 7.1, 5.85, 5.25, 0.62, [P("Por que 10%? Bem abaixo das taxas acima, que contam por aplicativo, e não por par: um patamar conservador deixa o teste mais exigente.", 12, False, NAVY, spacing=1.0)], anchor="m")
notas(s, "A pesquisa tem uma hipótese só, e ela vem da literatura. Andow e colegas olharam quase 14 mil aplicativos e viram que até 42,4% deles omitiam ou declaravam errado para onde iam dados sensíveis. Samarasinghe e colegas estudaram 1.166 aplicativos de governo de 71 países e viram que 27% enviavam informações sensíveis a terceiros ou sem criptografia. Carlsson e colegas compararam 32 aplicativos do setor público da Finlândia com as políticas deles e acharam divergências. E Kollnig e colegas, em 24 mil aplicativos, apontaram a falta de transparência sobre rastreamento tanto no Android quanto no iPhone. A partir disso, a minha hipótese é: pelo menos 10% dos pares aplicativo–SDK não vão ter declaração compatível. O 10% fica bem abaixo dessas taxas de propósito: esses estudos contam por aplicativo, e eu conto por par, então não dá para comparar direto. Com um patamar baixo, o teste fica mais exigente: se nem 10% dos pares estiverem sem declaração, isso já mostra que os aplicativos brasileiros estão melhores do que a literatura faria esperar.",
      "LEMBRETE (não precisa falar). Como a H1 é testada: calculo a porcentagem de pares sem declaração, com intervalo de confiança de 95%. Os pares do mesmo aplicativo usam a mesma política, então o intervalo é calculado agrupando por aplicativo. A H1 só é rejeitada se até o limite de cima do intervalo ficar abaixo de 10%. O 10% é um critério do estudo, não um limite da LGPD.")

# ---------------------------------------------------------------- 7 e 8 estudos que orientam o projeto (fundo 13)
CAB_EST = ["Estudo", "O que buscavam", "O que foi feito", "Como foi feito", "Resultados"]
LARG_EST = [2.0, 2.35, 2.35, 2.45, 2.85]
est1 = [
    ["Binns et al. (2018)", "Medir a extensão do rastreamento por terceiros em apps móveis", "Exame de 959 mil apps da Google Play dos EUA e do Reino Unido", "Análise estática: domínios de rastreadores procurados no código, sem executar os apps", "A maioria tem rastreamento; poucos rastreadores, como os do Google, estão na maior parte dos apps"],
    ["Kollnig et al. (2021)", "Ver se o rastreamento mudou depois do GDPR", "Comparação de quase 2 milhões de apps Android: 1 milhão de 2017 e 1 milhão de 2020", "Análise estática dos pacotes nos dois períodos", "Pouca mudança; a concentração em poucas grandes empresas persistiu"],
    ["Andow et al. (2020)", "Ver se as políticas declaram os fluxos de dados e quem os recebe", "Exame de 13.796 apps Android com a ferramenta PoliCheck", "Fluxos observados na execução comparados com a política, por destinatário", "Até 42,4% dos apps omitiam ou declaravam errado fluxos sensíveis"],
]
est2 = [
    ["Samarasinghe et al. (2022)", "Avaliar a privacidade de sites e apps de governo", "Exame de 1.166 apps Android governamentais de 71 países", "Análise estática dos SDKs e observação do tráfego de rede", "37% com rastreadores do Google; 27% enviavam informações sensíveis a terceiros ou sem criptografia; Brasil não separado"],
    ["Carlsson et al. (2022)", "Comparar o tráfego de apps do setor público com as políticas", "Exame de 32 apps do setor público finlandês", "Captura do tráfego de rede e leitura das políticas de privacidade", "Divergências entre políticas e dados enviados a terceiros; às vezes, dados fora da Europa quando a política negava"],
    ["Serrano et al. (2024)", "Caracterizar rastreadores e vazamentos em apps da COVID-19", "Exame de 595 apps obtidos de várias fontes", "Assinaturas do Exodus Privacy e análise do código das bibliotecas", "Rastreadores em 402 dos 595 apps; mistura de fontes exige registrar origem e versão"],
]
for parte, sub, linhas in [(1, "Rastreamento e declarações", est1), (2, "Aplicativos de governo", est2)]:
    s = nova(13)
    barra_titulo(s, f"ESTUDOS QUE ORIENTAM O PROJETO ({parte}/2)", sub=sub)
    tabela(s, 0.65, 2.15, LARG_EST, CAB_EST, linhas, size=13, alt_h=1.2)
    if parte == 1:
        notas(s, "No referencial teórico, a revisão sistemática selecionou os estudos que orientam o projeto. Separei seis em duas tabelas, com o que cada um buscava, o que fez, como fez e o que achou. Os três primeiros tratam de rastreamento e declarações. Binns e colegas examinaram 959 mil aplicativos da Google Play procurando rastreadores no código, sem executar os apps, e acharam rastreamento na maioria, concentrado em poucas empresas, como o Google. Kollnig e colegas compararam cerca de um milhão de aplicativos de 2017 com um milhão de 2020, antes e depois do GDPR, o regulamento europeu de proteção de dados, e viram pouca mudança. E Andow e colegas criaram o PoliCheck, que compara o que o aplicativo envia durante o uso com o que a política diz, olhando também quem recebe o dado: até 42,4% dos aplicativos omitiam ou declaravam errado fluxos sensíveis. É desse estudo que vem a ideia de comparar o declarado com o encontrado.")
    else:
        notas(s, "Os outros três estudaram aplicativos de governo. Samarasinghe e colegas examinaram 1.166 aplicativos de 71 países: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis a terceiros ou sem criptografia, mas o Brasil não aparece separado. Carlsson e colegas compararam o tráfego de 32 aplicativos do setor público finlandês com as políticas: acharam divergências e, em alguns casos, dados indo para fora da Europa quando a política dizia que não. É o estudo mais parecido com o meu. E Serrano e colegas acharam rastreadores em 402 de 595 aplicativos da COVID-19; como eles juntaram pacotes de várias fontes, o estudo mostra por que eu registro a origem e a versão de cada pacote.")

# ---------------------------------------------------------------- 9 lacuna e contribuição (fundo 4)
s = nova(4)
titulo(s, "LACUNA E CONTRIBUIÇÃO", x=0.9, y=0.45, size=40, cor=MID)
colunas = [("O que já existe", SILVER, DARK), ("O que falta", MID, WHITE), ("O que este TCC faz", NAVY, WHITE)]
X0, CW, GAP = 2.75, 3.05, 0.45
for j, (cab, cor, ctx) in enumerate(colunas):
    x0 = X0 + j * (CW + GAP)
    forma(s, x0, 1.45, CW, 0.5, cor)
    texto(s, x0, 1.45, CW, 0.5, [P(cab, 16, True, ctx, "c")], anchor="m")
eixos = [("Caso brasileiro",
          ["Estudo internacional de apps de governo; estudos de um app brasileiro por vez",
           "Medir o conjunto dos apps do governo brasileiro, por esfera",
           "Analisa os 376 apps oficiais: federais, estaduais e municipais"]),
         ("Declarado × encontrado",
          ["Comparação entre política e dados em apps comerciais e no setor público finlandês",
           "Comparar cada SDK com a política e a “Segurança dos dados” em apps brasileiros",
           "Classifica cada par aplicativo–SDK e testa a H1"]),
         ("Instrumento",
          ["Comparações de ferramentas de detecção de bibliotecas",
           "Concordância entre detectores de rastreadores nas mesmas versões",
           "Mede o κ de Fleiss entre três detectores"])]
RH = 1.38
for i, (eixo, cel) in enumerate(eixos):
    y0 = 2.12 + i * (RH + 0.13)
    forma(s, 0.75, y0, 1.85, RH, PALE)
    texto(s, 0.85, y0, 1.65, RH, [P(eixo, 15, True, NAVY, "c")], anchor="m")
    for j, txt in enumerate(cel):
        x0 = X0 + j * (CW + GAP)
        cor_f = [LIGHT, WHITE, PALE][j]
        forma(s, x0, y0, CW, RH, cor_f, linha=[SILVER, MID, NAVY][j])
        texto(s, x0 + 0.15, y0, CW - 0.3, RH, [P(txt, 14, j == 2, NAVY if j == 2 else DARK, "c", spacing=1.0)], anchor="m")
        if j < 2:
            forma(s, x0 + CW + 0.08, y0 + RH / 2 - 0.15, 0.29, 0.3, MID, MSO_SHAPE.RIGHT_ARROW)
texto(s, 1.3, 6.68, 10.9, 0.35, [P("Bases: Samarasinghe et al. (2022); Lemos et al. (2022); Vaz et al. (2022); Andow et al. (2020); Carlsson et al. (2022); Zhan et al. (2022).", 11, False, GREY)])
notas(s, "Comparando o que já existe com o que falta, aparecem três lacunas, e cada uma vira uma contribuição. No caso brasileiro, já há um estudo internacional de aplicativos de governo e estudos de um aplicativo brasileiro por vez, mas falta medir o conjunto; o trabalho analisa os 376 aplicativos oficiais, federais, estaduais e municipais. No confronto entre o declarado e o encontrado, isso já foi feito em aplicativos comerciais e no setor público da Finlândia, mas não nos aplicativos do governo brasileiro com a seção “Segurança dos dados”; o trabalho classifica cada par e testa a hipótese. E no instrumento, já há comparações de ferramentas que detectam bibliotecas, mas não de detectores de rastreadores nas mesmas versões; o trabalho mede o kappa entre três detectores. Vale lembrar: uma divergência não é prova de infração à LGPD; é um indício que merece ser examinado.")

# ---------------------------------------------------------------- 10 método (fundo 13)
s = nova(13)
barra_titulo(s, "ETAPAS DO MÉTODO", sub="Estudo quantitativo e observacional, em seis etapas")
etapas = [
    ["1. Seleção dos aplicativos", "Conferir a lista pelo nome jurídico do desenvolvedor na Google Play", "376 apps oficiais, com esfera de governo", "Obj. 1"],
    ["2. Download dos pacotes", "Baixar a versão atual com o apkeep, a partir do Brasil; AndroZoo quando tiver o app", "Pacote com hash SHA-256, versão e data", "Obj. 2"],
    ["3. Detecção dos SDKs", "Rodar três detectores: A (código, Exodus), B (domínios, Exodus) e C (domínios, Disconnect)", "Pares aplicativo–SDK com a evidência; κ de Fleiss", "Obj. 2 e 5"],
    ["4. Classificação das declarações", "Ler a política e a “Segurança dos dados”; cada par recebe uma de cinco categorias", "Matriz de declarações por par", "Obj. 3"],
    ["5. Observação do tráfego", "Instalar uma subamostra num celular de teste e registrar o tráfego durante o uso", "Destinos, país e se estão declarados", "Obj. 4"],
    ["6. Análise estatística", "Proporção de pares sem declaração compatível, com IC95% agrupado por aplicativo", "Decisão sobre a H1", "Obj. 3 e 5"],
]
tabela(s, 0.65, 2.15, [2.75, 5.0, 3.1, 1.15], ["Etapa", "O que será feito e como", "O que entrega", "Objetivo"], etapas, size=13, alt_h=0.62)
notas(s, "Nos procedimentos metodológicos, o estudo é quantitativo e observacional, em seis etapas. Na primeira, seleção, reviso a lista dos aplicativos pelo nome jurídico do desenvolvedor. Na segunda, baixo a versão atual de cada um na Google Play, com o apkeep, registrando o hash, a versão e a data. Na terceira, rodo os três detectores e guardo a evidência de cada detecção. Na quarta, leio a política e a seção “Segurança dos dados” e classifico cada par. Na quinta, numa parte dos aplicativos, instalo no celular de teste e registro o tráfego. E na sexta, calculo a proporção de pares sem declaração, com intervalo de confiança, e decido sobre a hipótese. Cada etapa responde a um objetivo específico.")

# ---------------------------------------------------------------- 11 por que só Android (fundo 4)
s = nova(4)
titulo(s, "POR QUE SÓ ANDROID", x=0.9, y=0.45, size=40, cor=MID, sub="Três motivos, e o que isso não significa", sub_size=20)
motivos = [("Abrangência", "73,76%", "dos celulares no Brasil usam Android (StatCounter, out. 2026)"),
           ("Acesso ao código", "iOS", "apps criptografados pela Apple; sem ferramenta pública para baixá-los em escala; decriptar exige aparelho físico e tem legalidade incerta (Kollnig et al., 2022)"),
           ("Declarações comparáveis", "Google Play", "a H1 usa a seção “Segurança dos dados”; a App Store tem rótulos em outro formato (Xiao et al., 2023)")]
for k, (cab, num, txt) in enumerate(motivos):
    x0 = 0.9 + k * 3.95
    forma(s, x0, 1.95, 3.7, 3.25, NAVY if k == 0 else (MID if k == 1 else PALE))
    ct = WHITE if k < 2 else NAVY
    texto(s, x0 + 0.25, 2.1, 3.2, 0.45, [P(cab.upper(), 14, True, ct)])
    texto(s, x0 + 0.25, 2.55, 3.2, 0.85, [P(num, 36 if k == 0 else 30, True, ct)], anchor="m")
    texto(s, x0 + 0.25, 3.5, 3.2, 1.65, [P(txt, 14, False, ct, spacing=1.05)])
forma(s, 0.9, 5.45, 11.6, 1.05, LIGHT)
texto(s, 1.15, 5.45, 11.1, 1.05, [R([("Não significa que o iPhone seja mais seguro: ", 15, True, NAVY),
                                     ("Kollnig et al. (2022) compararam 12 mil apps de cada plataforma e acharam rastreamento por terceiros comum nas duas, sem uma claramente melhor. As versões iOS ficam como trabalho futuro.", 15, False, DARK)], spacing=1.05)], anchor="m")
notas(s, "Uma pergunta natural é: por que só Android? São três motivos. Primeiro, abrangência: segundo a StatCounter, em outubro de 2026 o Android estava em 73,76% dos celulares no Brasil. Segundo, acesso ao código: Kollnig e colegas, que compararam 12 mil aplicativos de cada plataforma, explicam que no iPhone os aplicativos são criptografados pela Apple, não existe ferramenta pública para baixá-los em escala, e decriptar exige um aparelho físico e tem legalidade incerta. No Android, consigo baixar da Google Play, comparar com o AndroZoo e usar bases abertas de rastreadores. Terceiro, a hipótese usa a seção “Segurança dos dados”, que é da Google Play; a Apple tem rótulos de privacidade em outro formato. Isso não quer dizer que o iPhone seja mais seguro: o mesmo estudo achou rastreamento comum nas duas plataformas, sem uma claramente melhor. As versões iOS ficam como trabalho futuro.")

# ---------------------------------------------------------------- 12 aplicativos selecionados (fundo 11)
s = nova(11)
texto(s, 1.0, 0.95, 5.3, 0.85, [P("APLICATIVOS", 44, True, MID)])
texto(s, 1.0, 1.8, 5.3, 0.5, [P("396 candidatos, 376 oficiais", 24, False, GREY)])
texto(s, 1.0, 2.6, 5.0, 3.6, [
    P("Busca por 21 termos na Google Play e pelo catálogo de cada publicador oficial.", 17, False, DARK, after=10),
    P("Oficialidade conferida pelo nome jurídico em “Sobre o desenvolvedor”.", 17, False, DARK, after=10),
    P("Saíram 20: 13 empresas privadas e 7 contas de pessoa física.", 17, False, DARK, after=10),
    P("Lista revista de novo antes da coleta (objetivo 1).", 15, True, NAVY)])
texto(s, 6.61, 2.85, 3.61, 1.8, [P("376", 60, True, WHITE, "c"), P("apps oficiais", 18, False, PALE, "c")], anchor="m")
for (cx, cy), (num, leg) in zip([(10.68, 1.83), (11.63, 3.76), (10.68, 5.72)], [("85", "federais"), ("199", "estaduais"), ("92", "municipais")]):
    texto(s, cx - 0.86, cy - 0.5, 1.72, 1.0, [P(num, 26, True, NAVY, "c"), P(leg, 13, False, DARK, "c")], anchor="m")
notas(s, "Para montar a lista, busquei 21 termos ligados a serviço público na Google Play e depois todo o catálogo de cada publicador oficial. Encontrei 396 aplicativos candidatos. Conferindo o nome jurídico de quem publica, 376 ficaram como oficiais: 85 federais, 199 estaduais e 92 municipais. Vinte saíram: 13 eram de empresas privadas usando nome de serviço público e 7 estavam em contas de pessoa física. Essa lista ainda vai ser revista antes da coleta, como diz o primeiro objetivo.")

# ---------------------------------------------------------------- 13 fonte dos pacotes (fundo 2)
s = nova(2)
texto(s, 0.9, 0.95, 11.5, 0.85, [P("FONTE DOS PACOTES", 44, True, WHITE)])
texto(s, 0.9, 1.8, 11.5, 0.5, [P("Consulta histórica ao AndroZoo, acervo acadêmico de pacotes Android", 22, False, PALE)])
for x0, num, cor, leg in [(0.9, "23,2%", WHITE, "governo: 92 de 396 candidatos"), (4.7, "84,2%", MID, "comerciais: 160 de 190 (só contexto)")]:
    texto(s, x0, 2.45, 3.7, 1.1, [P(num, 66, True, cor)])
    texto(s, x0, 3.55, 3.7, 0.5, [P(leg, 16, False, PALE)])
texto(s, 8.75, 2.6, 3.7, 1.5, [P("Fonte principal: versão atual na Google Play", 19, True, WHITE, after=6),
                               P("AndroZoo: reprodutibilidade e defasagem", 16, False, PALE)])
forma(s, 0.9, 4.2, 11.5, 0.03, MID)
texto(s, 0.9, 4.32, 11.5, 0.35, [P("COMO SERÁ A COLETA", 14, True, PALE)])
passos_c = [("Conta da pesquisa", "Conta Google criada só para o estudo, com acesso a partir do Brasil"),
            ("Download com apkeep", "Ferramenta aberta da EFF; em pacotes divididos, guarda o APK base"),
            ("Registro", "SHA-256 do arquivo, versão, data e o motivo de cada falha"),
            ("Teste primeiro", "Cinco apps em fevereiro; depois todos os aplicativos")]
for i, (cab, txt) in enumerate(passos_c):
    x0 = 0.9 + i * 2.92
    forma(s, x0, 4.72, 2.75, 1.5, LIGHT)
    texto(s, x0 + 0.18, 4.84, 0.45, 0.45, [P(str(i + 1), 24, True, NAVY)], anchor="m")
    texto(s, x0 + 0.62, 4.84, 2.0, 0.45, [P(cab, 15, True, NAVY)], anchor="m")
    texto(s, x0 + 0.18, 5.36, 2.42, 0.85, [P(txt, 13, False, DARK, spacing=1.05)])
notas(s, "Um problema prático apareceu na hora de buscar os pacotes. O AndroZoo, um acervo acadêmico de aplicativos, tinha só 92 dos 396 do governo, ou 23,2%; dos comerciais, tinha 160 de 190, ou 84,2%. Dependendo só dele, muitos aplicativos do governo ficariam de fora. Por isso a fonte principal vai ser a versão atual da Google Play, que é a que o cidadão instala. O download vai ser feito com o apkeep, uma ferramenta aberta, com uma conta Google criada só para a pesquisa, a partir do Brasil. Para cada aplicativo, registro o hash, a versão, a data e, se falhar, o motivo; a falha também vira dado. O AndroZoo continua útil para reproduzir a análise. Antes de baixar todos, testo em cinco aplicativos.",
      "LEMBRETE (não precisa falar). Quando o app vem dividido em vários pacotes, guardo o APK base, que tem o código. O apkeep é da Electronic Frontier Foundation (EFF). Não redistribuo os pacotes.")

# ---------------------------------------------------------------- 14 piloto (fundo 13)
s = nova(13)
barra_titulo(s, "PILOTO DOS DETECTORES")
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
                             P("88 de 123 detecções de B marcadas como possíveis falsos positivos, sem referência independente", 14, False, LIGHT, "c", spacing=1.05)], anchor="m")
notas(s, "Fiz um piloto com 20 pacotes do AndroZoo e três detectores. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet escritos dentro do pacote. O C faz o mesmo que o B, com outra lista, a da Disconnect. Cada um deu uma taxa diferente: 75%, 95% e 80% dos pacotes com pelo menos um rastreador. A concordância entre eles, medida pelo kappa de Fleiss, foi 0,52. Conferi as detecções uma a uma e marquei 88 das 123 do B como possíveis falsos positivos, quase todas por endereços genéricos do Google ou do Facebook. Sem elas, o kappa sobe para 0,69, mas é só uma análise de sensibilidade, porque não há uma referência independente com a resposta certa. Conclusão: a ferramenta escolhida muda o resultado, e é por isso que comparar os detectores faz parte do método. No próximo slide, explico como ler esse número.",
      "LEMBRETE (não precisa falar). A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método). B não é tráfego, é texto dentro do pacote: um link para maps.google.com bastou para apontar Google Ads. C usa só as categorias publicidade, análise de uso e impressão digital. Exodus Privacy: base aberta de rastreadores com assinaturas de código e de rede. Disconnect: lista de domínios que coletam dados, separados por categoria.")

# ---------------------------------------------------------------- 15 kappa de Fleiss (fundo 4)
s = nova(4)
titulo(s, "COMO LER O κ DE FLEISS", x=0.9, y=0.45, size=40, cor=MID, sub="Concordância entre os três detectores, descontado o acaso (Fleiss, 1971)", sub_size=20)
forma(s, 0.9, 1.95, 5.5, 1.25, NAVY)
texto(s, 0.9, 1.95, 5.5, 1.25, [R([("κ = (P", 34, True, WHITE), ("o", 34, True, WHITE, True), (" − P", 34, True, WHITE), ("e", 34, True, WHITE, True),
                                   (") / (1 − P", 34, True, WHITE), ("e", 34, True, WHITE, True), (")", 34, True, WHITE)], align="c")], anchor="m")
defs = [[("P", 15, True, NAVY), ("o", 15, True, NAVY, True), (" — concordância observada: ", 15, True, NAVY),
         ("em cada app, a fração de pares de detectores que deram a mesma resposta (tem ou não tem rastreador); depois, a média dos apps.", 14, False, DARK)],
        [("P", 15, True, NAVY), ("e", 15, True, NAVY, True), (" — concordância esperada ao acaso: ", 15, True, NAVY),
         ("soma dos quadrados das proporções gerais de “tem” e de “não tem”.", 14, False, DARK)],
        [("Exemplo: ", 15, True, NAVY), ("os três dizem “tem” → 1; dois dizem “tem” e um “não tem” → 1/3.", 14, False, DARK)],
        [("Por que descontar o acaso? ", 15, True, NAVY), ("Se quase todo app tem rastreador, quem responde “tem” para tudo concorda sem medir nada.", 14, False, DARK)]]
texto(s, 0.9, 3.4, 5.5, 3.2, [R(d, after=9, spacing=1.0) for d in defs])
# escala de Landis e Koch (1977)
texto(s, 6.85, 1.95, 5.6, 0.4, [P("ESCALA DE LANDIS E KOCH (1977)", 13, True, MID)])
faixas = [("< 0", "pobre"), ("0–0,20", "leve"), ("0,21–0,40", "razoável"), ("0,41–0,60", "moderada"), ("0,61–0,80", "substancial"), ("0,81–1", "quase perfeita")]
cores_f = [RGBColor(0xE6, 0xE6, 0xE6), RGBColor(0xDC, 0xE6, 0xF1), RGBColor(0xB9, 0xCD, 0xE3), MID, RGBColor(0x2E, 0x5F, 0x8A), NAVY]
for k, ((fx, nome), cf) in enumerate(zip(faixas, cores_f)):
    y0 = 2.4 + k * 0.5
    forma(s, 6.85, y0, 1.55, 0.44, cf)
    texto(s, 6.85, y0, 1.55, 0.44, [P(fx, 13, True, WHITE if k >= 3 else NAVY, "c")], anchor="m")
    texto(s, 8.55, y0, 1.9, 0.44, [P(nome, 14, k in (3, 4), NAVY if k in (3, 4) else DARK)], anchor="m")
# marcações do piloto
texto(s, 10.25, 3.9, 2.3, 0.44, [P("← piloto: 0,52", 14, True, NAVY)], anchor="m")
texto(s, 10.25, 4.4, 2.3, 0.44, [P("← sensibilidade: 0,69", 14, True, NAVY)], anchor="m")
forma(s, 6.85, 5.5, 5.6, 1.05, PALE)
texto(s, 7.0, 5.5, 5.35, 1.05, [P("1 = concordância total · 0 = igual ao acaso. Limiar do estudo: 0,6, a passagem de moderada para substancial. Concordância alta não prova acerto: os três podem errar igual.", 13, False, NAVY, spacing=1.0)], anchor="m")
notas(s, "O kappa de Fleiss mede se vários avaliadores concordam, descontando o acordo que aconteceria por acaso. Aqui os avaliadores são os três detectores, e cada um responde se o aplicativo tem ou não tem rastreador. A fórmula compara duas coisas: P o, a concordância observada, e P e, a concordância esperada ao acaso. Para cada aplicativo, vejo quantos pares de detectores deram a mesma resposta: se os três dizem que tem, a concordância é 1; se dois dizem que tem e um diz que não tem, é um terço. P o é a média disso em todos os aplicativos. P e sai da proporção geral de respostas “tem” e “não tem”: é a chance de dois detectores concordarem só por sorte. Por que descontar o acaso? Se quase todo aplicativo tem rastreador, dois detectores que respondem “tem” para tudo concordariam quase sempre sem medir nada. O resultado chega no máximo a 1, que é concordância total; 0 é igual ao acaso. Para interpretar, uso a escala de Landis e Koch: até 0,20 é leve, até 0,40 razoável, até 0,60 moderada, até 0,80 substancial e acima disso quase perfeita. O piloto deu 0,52, moderada, e 0,69, substancial, na análise de sensibilidade. O meu limiar é 0,6, a passagem de moderada para substancial. E concordância alta não prova acerto: os três podem errar do mesmo jeito.",
      "LEMBRETE (não precisa falar). Fórmula por app: P i = soma de n ij vezes (n ij − 1), dividida por n vezes (n − 1), com n = 3 detectores e n ij = quantos deram a resposta j. P e = soma de p j ao quadrado, com p j = proporção de todas as respostas na categoria j. Junto do κ, reporto o IC95% e as concordâncias positiva e negativa, porque o κ fica instável quando quase todos os apps estão na mesma categoria. Na revisão, a conferência cega da triagem usa o κ de Cohen, a versão para dois avaliadores, com a mesma escala.")

# ---------------------------------------------------------------- 16 revisão sistemática (fundo 10)
s = nova(10)
cols = [("ONDE", "17 buscas em 4 bases: Scopus (principal), IEEE Xplore, SBC OpenLib e BDTD; 2015 a 2026; inglês e português"),
        ("COMO", "Strings com aplicativo, fenômeno e contexto; desde 25/11, termo do tema obrigatório no título do artigo"),
        ("VALIDAÇÃO", "11 estudos de controle: as buscas acharam os 10 que o Scopus indexa, e a restrição pelo título manteve os 10")]
for i, (cab, txt) in enumerate(cols):
    x0 = 0.75 + i * 3.62
    texto(s, x0, 0.55, 3.35, 0.4, [P(cab, 16, True, NAVY)])
    texto(s, x0, 0.98, 3.35, 1.55, [P(txt, 14, False, DARK, spacing=1.05)])
texto(s, 0.5, 2.6, 10.8, 2.27, [P("REVISÃO SISTEMÁTICA", 44, True, WHITE, "c"), P("Kitchenham e Charters (2007) · PRISMA 2020", 16, False, PALE, "c")], anchor="m")
fluxo = [("552", "resultados"), ("413", "sem repetidos"), ("210", "à leitura completa")]
for i, (num, leg) in enumerate(fluxo):
    x0 = 2.375 + i * 2.95
    texto(s, x0, 5.0, 2.3, 0.65, [P(num, 34, True, NAVY, "c")], anchor="m")
    texto(s, x0, 5.62, 2.3, 0.4, [P(leg, 14, False, GREY, "c")])
    if i < 2:
        forma(s, x0 + 2.42, 5.17, 0.38, 0.3, MID, MSO_SHAPE.RIGHT_ARROW)
notas(s, "Agora, como eu busquei a literatura. Fiz uma revisão sistemática, que é uma busca planejada e documentada, para que a escolha dos artigos não dependa de preferência pessoal. Segui o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as palavras de busca e os critérios de entrada e saída. Para mostrar o resultado, uso o PRISMA 2020, que é um fluxograma com quantos estudos entraram e saíram em cada etapa. Fiz 17 buscas em quatro bases: Scopus, IEEE Xplore e, para trabalhos brasileiros, SBC OpenLib e BDTD. Depois da simulação, deixei a busca mais focada: agora o título do artigo precisa ter um termo do tema, como rastreador, SDK, política de privacidade ou governo. Para testar as buscas, separei antes onze estudos que tinham de aparecer: elas acharam os dez que estão no Scopus, e a restrição pelo título manteve os dez. No fim, foram 552 resultados, 413 sem repetidos, e 210 passaram para a leitura completa, que está em andamento.",
      "Guia de Kitchenham: divide a revisão em três etapas. Planejamento, com as questões e o protocolo de inclusão e exclusão; condução, com a busca, a seleção, a avaliação de qualidade e a extração dos dados; e relatório, com a síntese dos resultados.",
      "PRISMA 2020: padroniza o relato da revisão num fluxograma, da identificação dos registros e remoção de duplicatas até a triagem por título e resumo, a leitura completa e os estudos incluídos.")

# ---------------------------------------------------------------- 17 limitações (fundo 12)
s = nova(12)
texto(s, 0.6, 0.7, 12.1, 0.85, [P("LIMITAÇÕES", 40, True, MID, "c")])
lims = [["SDK no código não prova envio de dados", "Análise do tráfego numa subamostra"],
        ["Só Android e Google Play", "Motivos justificados; iOS como trabalho futuro"],
        ["Políticas falam de tipos de dados, não do nome de cada SDK", "Cinco categorias; não citar o nome não conta como omissão"],
        ["Versões mudam entre coleta e análise", "Hash SHA-256, versão e data de cada pacote"],
        ["Revisão e classificações ainda em conferência", "Conclusão em fevereiro, antes de qualquer resultado"],
        ["Divergência não é prova de infração à LGPD", "Tratada como indício, com a evidência registrada"]]
tabela(s, 0.9, 1.85, [6.0, 5.6], ["Limitação", "Como é tratada"], lims, size=15, cab_size=15, alt_h=0.66)
notas(s, "Sobre as limitações, e como cada uma é tratada. Achar o SDK no código não prova que ele envia dados: por isso a análise de tráfego numa parte dos aplicativos. O estudo cobre só Android; os motivos estão justificados, e o iOS fica como trabalho futuro. As políticas costumam falar de tipos de dados, e não do nome de cada SDK: por isso as cinco categorias, e não citar o nome não conta como omissão. As versões mudam: registro o hash, a versão e a data de cada pacote. A revisão e as classificações ainda estão em conferência, e termino em fevereiro, antes de qualquer resultado. E uma divergência não é prova de infração à LGPD; é um indício.")

# ---------------------------------------------------------------- 18 próximos passos (fundo 13)
s = nova(13)
barra_titulo(s, "PRÓXIMOS PASSOS NO CAPSTONE II (2027.1)")
passos = [["Fevereiro", "Revisão sistemática", "Ler os 148 registros em aberto, fazer a bola de neve e a conferência cega da triagem", "Estudos incluídos; κ de Cohen"],
          ["Fevereiro", "1. Seleção", "Revisar os 376 apps; testar o download em cinco; definir com o orientador o detector principal", "Lista final e plano de análise"],
          ["Março", "2. Download e 3. Detecção", "Baixar todos os apps na Google Play; rodar os três detectores; calcular o κ de Fleiss", "Pacotes com hash; pares aplicativo–SDK"],
          ["Mar. e abr.", "4. Declarações", "Ler a política e a “Segurança dos dados” de cada app e classificar cada par", "Matriz de declarações"],
          ["Abril", "5. Tráfego", "Instalar a subamostra no celular de teste e registrar o tráfego", "Destinos e países"],
          ["Maio", "6. Análise", "Calcular a proporção com IC95% e decidir sobre a H1; avisar os órgãos de achados graves", "Resultado do teste da H1"],
          ["Junho", "Redação e defesa", "Escrever resultados e discussão à luz da LGPD; publicar dados e scripts", "Texto final e defesa"]]
tabela(s, 1.05, 1.8, [1.45, 2.3, 5.1, 2.75], ["Quando", "Etapa", "O que será feito", "Produto"], passos, size=13, alt_h=0.6)
notas(s, "Os próximos passos, mês a mês, no Capstone II. Em fevereiro, termino a revisão, com a leitura dos registros em aberto, a bola de neve e a conferência cega da triagem; e reviso a lista de aplicativos, testando o download em cinco deles e definindo com o orientador o detector principal. Em março, baixo todos os aplicativos, rodo os detectores e calculo o kappa. Entre março e abril, classifico as declarações de cada par. Em abril, observo o tráfego da subamostra. Em maio, faço a análise e decido sobre a hipótese; se aparecer algum achado grave, aviso o órgão antes de publicar. E em junho, redação, publicação dos dados e defesa.")

# ---------------------------------------------------------------- 19 conclusão (fundo 3)
s = nova(3)
texto(s, 0.9, 1.3, 11.4, 2.2, [P("Problema definido.", 44, True, WHITE), P("Método viável.", 44, True, WHITE), P("Hipótese pronta para o teste.", 44, True, NAVY)])
texto(s, 0.9, 4.0, 10.8, 1.2, [P("No Capstone II: medir quantos SDKs dos aplicativos do governo não estão declarados ao cidadão.", 22, False, WHITE, spacing=1.05)])
texto(s, 0.9, 5.55, 6.0, 0.6, [P("Obrigado.", 24, True, NAVY)])
notas(s, "Para concluir: o problema está definido, o método é viável e a hipótese está pronta para ser testada no Capstone II. O foco não é comparar o governo com o mercado, mas verificar se o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles realmente enviam. Obrigado.")


# ---------------------------------------------------------------- referências: todas as do texto (fundo 4)
def limpa(t):
    t = t.replace("{\\'\\i}", "í").replace("\\'\\i", "í")
    t = re.sub(r"\\url\{([^}]*)\}", r"\1", t)
    t = t.replace("$\\varepsilon$", "ε").replace("\\&", "&").replace("~", " ").replace("--", "–")
    t = t.replace("\\textendash", "–").replace("\\ ", " ")
    t = re.sub(r"\\[a-zA-Z]+\s*", "", t)
    t = t.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", t).strip()


bbl = open(BBL, encoding="utf-8").read()
refs = []
for m in re.finditer(r"\\bibitem\[.*?\]\{(.*?)\}\s*\\abntrefinfo\{.*?\}\{.*?\}\{.*?\}\s*\{(.*?)\}\s*(?=\\bibitem|\\end\{thebibliography\})", bbl, re.S):
    corpo = m.group(2)
    partes = re.split(r"\\textbf\{((?:[^{}]|\{[^{}]*\})*)\}", corpo)
    runs = []
    for k, pt in enumerate(partes):
        txt = limpa(pt) if k % 2 else limpa(pt)
        if not txt:
            continue
        if k % 2 == 0 and runs and not txt.startswith((".", ",", ":")):
            txt = " " + txt
        if k % 2 == 1 and runs and not runs[-1][0].endswith(" "):
            txt = " " + txt
        runs.append((txt, k % 2 == 1))
    refs.append(runs)
assert len(refs) >= 80, len(refs)
TAM_REF = 9.5
POR_COLUNA = 3000  # caracteres por coluna, estimativa para corpo 9,5 em 5,65 pol.
paginas, atual, col, usados = [], [[], []], 0, 0
for r in refs:
    n = sum(len(t) for t, _ in r) + 90
    if usados + n > POR_COLUNA and atual[col]:
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
    s = nova(4)
    titulo(s, f"REFERÊNCIAS ({k}/{len(paginas)})", x=0.9, y=0.35, size=32)
    for x0, coluna in [(0.9, c1), (6.85, c2)]:
        if coluna:
            texto(s, x0 + (0.25 if x0 < 1 else 0), 1.15, 5.45, 5.3, [{"runs": [(t, TAM_REF, b, DARK) for t, b in r], "align": "l", "spacing": 1.0, "after": 4} for r in coluna])
    notas(s, "Não é para ler. São todas as referências do texto do TCC, em ordem alfabética, no padrão ABNT. Pode passar direto para o slide de encerramento.", *COLA)

# ---------------------------------------------------------------- encerramento institucional (fundo 14)
s = nova(14)
notas(s, "Slide de encerramento do template. Pode ficar na tela durante as perguntas.", *COLA)

# ---------------------------------------------------------------- remove os slides de exemplo do template
lst = prs.slides._sldIdLst
for sid in list(lst)[:N_TPL]:
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)

# ---------------------------------------------------------------- número do slide (campo automático), menos na capa e no encerramento
ESCURO = {1, 2, 3, 5, 14}  # fundos com o canto inferior direito escuro: número em branco
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
print("ok:", n, "slides;", len(refs), "referências em", len(paginas), "slides")
