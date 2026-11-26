"""Monta os slides da defesa final do Capstone I sobre os fundos do template do IDP.

Uso: python monta_slides_defesa_final.py TEMPLATE.pptx main.bbl SAIDA.pptx

Os slides seguem as seções do texto do TCC, no modelo do Capstone do IDP: introdução
(motivação, problema, objetivos e hipótese), revisão bibliográfica (estudos de base,
lacuna e contribuição), metodologia (etapas, plataforma, kappa de Fleiss, declarações e
revisão sistemática), resultados e discussão (aplicativos, pacotes, piloto e
limitações), conclusão (próximos passos) e todas as referências do texto, numeradas
no padrão IEEE, como no texto; as citações dos slides usam os mesmos números. Os slides de conteúdo usam o mesmo título na barra azul do
template; as notas do apresentador cabem em cerca de 14 minutos de fala.
"""
import copy
import re
import sys
import unicodedata

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

TPL, BBL, SAIDA = sys.argv[1:4]
bbl = open(BBL, encoding="utf-8").read()
NUM = {k: i for i, k in enumerate(re.findall(r"\\bibitem\{([^}]+)\}", bbl), 1)}


def ref(*chaves):
    """Número IEEE de cada referência, na ordem em que aparece no texto do TCC."""
    return ", ".join(f"[{NUM[k]}]" for k in chaves)

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
FUNDO = []  # fundo de cada slide novo, para a cor do número


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
    """paras: lista de dicts {runs:[(texto, pt, negrito, cor[, sub])], align, after, spacing}."""
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


def barra_titulo(sl, t, sub=None):
    """Título na barra azul do fundo 13, igual em todos os slides de conteúdo."""
    texto(sl, 0.65, 0.42, 11.0, 0.85, [P(t, 34, True, LIGHT)], anchor="m")
    if sub:
        texto(sl, 0.9, 1.7, 11.6, 0.4, [P(sub, 18, False, GREY)])


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


COLA = [
    "COLA PARA AS PERGUNTAS (não é para ler em voz alta).",
    "Números: 396 candidatos e 376 oficiais (85 federais, 199 estaduais, 92 municipais) · AndroZoo: 92 de 396 (23,2%) · piloto: 75%, 95% e 80% com rastreador; κ 0,52, ou 0,69 sem os 88 possíveis falsos positivos do B · políticas acessíveis: 323 de 396 (81,6%) · revisão: 396 resultados, 312 sem repetidos, 148 à leitura completa, 31 propostas de inclusão (8 já confirmadas).",
    "Por que 10%? Fica bem abaixo da literatura (Andow 42,4%; Samarasinghe 27%), que conta aplicativos; eu conto pares, então é um patamar conservador. Se ficar abaixo, não dá para dizer que o governo é mais transparente que nos outros estudos, só que ficou abaixo do meu patamar. Não é limite da LGPD.",
    "Por que decidir pela proporção, e não pelo intervalo de confiança? Porque analiso todos os aplicativos oficiais, e não uma amostra. O intervalo mostra a precisão e entra como ressalva se incluir os 10%.",
    "Onde a LGPD obriga o órgão a declarar? Transparência (Art. 6º, VI); informação sobre o uso compartilhado e a finalidade (Art. 9º, V); e, no poder público, informar a previsão legal, a finalidade e as práticas, em veículos de fácil acesso (Art. 23, I). A lei não exige o nome do SDK; exige informar o tratamento e o compartilhamento.",
    "Por que só Android? 73,76% dos celulares no Brasil (StatCounter, out. 2026); no iPhone os aplicativos são criptografados e não há ferramenta pública para baixá-los em escala (Kollnig et al., 2022); a seção “Segurança dos dados” é da Google Play. Não quer dizer que o iPhone seja mais seguro.",
    "Como vai observar o tráfego sem celular Android? No emulador do Android Studio, no computador, com o mitmproxy registrando as conexões. Abro cada aplicativo sem login, sem conta pessoal. Se um aplicativo não funcionar no emulador, registro o motivo e reporto quantos foram.",
    "Por que uma hipótese só? Para concentrar o trabalho no que dá para provar no Capstone II: as declarações. A comparação dos aplicativos com dados sensíveis saiu do projeto.",
    "O κ de 0,52 não é baixo? É moderado. Por isso a concordância entre detectores é uma checagem do instrumento, com limiar de 0,6, e não uma hipótese.",
    "Ter o SDK no aplicativo prova que dados foram enviados? Não. O envio só é observado na análise de tráfego de uma parte dos aplicativos.",
    "Por que a revisão caiu de 1.531 para 396? Exigi um termo do tema no título, comecei em 2018, quando o GDPR passou a valer e a LGPD foi sancionada, e tirei a questão sobre detecção de bibliotecas, que ficou como fundo no referencial. Os estudos de controle dentro desse escopo continuaram sendo achados.",
    "Você leu todos os artigos? Não. A leitura completa está em andamento: já confirmei parte das decisões lendo o texto inteiro e termino o restante em fevereiro, antes de qualquer resultado.",
    "Por que o texto mudou de formato? A disciplina pede o modelo LaTeX do Capstone do IDP: cinco seções e citações numeradas no padrão IEEE. O conteúdo é o mesmo; os resultados da preparação passaram para a seção de resultados.",
    "Se não souber: “Isso ainda não medi; está previsto para o Capstone II.”",
]

# ================================================================ INTRODUÇÃO
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
notas(s, "Bom dia. Meu nome é Claudio, e meu orientador é o professor Eduardo. Meu trabalho trata do rastreamento por terceiros nos aplicativos do governo brasileiro. Esses aplicativos trazem código de outras empresas, que pode coletar dados de quem usa. Quero descobrir que código é esse e se o governo avisa o cidadão sobre ele.")

# ---------------------------------------------------------------- 2 agenda (fundo 9)
s = nova(9)
texto(s, 1.15, 2.78, 2.34, 0.74, [P("AGENDA", 44, True, GREY)])
caps = [("1", "INTRODUÇÃO", ["Motivação", "Problema, objetivos e hipótese"]),
        ("2", "REVISÃO BIBLIOGRÁFICA", ["Estudos que orientam o projeto", "Lacuna e contribuição"]),
        ("3", "METODOLOGIA", ["Etapas, escolha do Android e κ de Fleiss", "Declarações e revisão sistemática"]),
        ("4", "RESULTADOS E DISCUSSÃO", ["Aplicativos, pacotes e piloto", "Limitações"]),
        ("5", "CONCLUSÃO E REFERÊNCIAS", ["Próximos passos no Capstone II"])]
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
notas(s, "A apresentação segue as cinco seções do texto, no modelo do Capstone. Começo pela introdução, com o problema, os objetivos e a hipótese. Depois vem a revisão bibliográfica, com os estudos de base e a lacuna. Em seguida, a metodologia, os resultados preliminares e as limitações. No fim, a conclusão e os próximos passos.")

# ---------------------------------------------------------------- 3 motivação (fundo 6)
s = nova(6)
texto(s, 1.0, 0.85, 6.9, 0.85, [P("MOTIVAÇÃO", 44, True, GREY)])
texto(s, 1.0, 1.7, 6.9, 0.5, [P("Serviços públicos no celular", 22, False, GREY)])
texto(s, 1.0, 2.75, 6.6, 3.4, [
    P("O Meu INSS e o Meu SUS Digital passam de 50 milhões de instalações cada um.", 18, False, DARK, after=12),
    P("Esses aplicativos embutem SDKs de outras empresas, que podem coletar identificadores e dados de uso.", 18, False, DARK, after=12),
    P("O cidadão nem sempre tem alternativa ao aplicativo oficial. E um SDK no código não prova, sozinho, que houve envio de dados.", 18, True, NAVY)])
caixas = [("Aplicativo do governo", "o que o cidadão instala"), ("SDK de terceiro", "mapas, estatísticas, anúncios"), ("Servidor da empresa", "para onde os dados podem ir")]
cy = 1.68
for i, (a, b) in enumerate(caixas):
    forma(s, 8.82, cy, 3.45, 0.78, WHITE)
    texto(s, 8.92, cy + 0.04, 3.25, 0.7, [P(a, 17, True, NAVY, "c"), P(b, 13, False, GREY, "c")], anchor="m")
    if i < 2:
        forma(s, 10.4, cy + 0.83, 0.3, 0.26, MID, MSO_SHAPE.DOWN_ARROW)
    cy += 1.14
texto(s, 8.75, 4.75, 3.6, 0.75, [P("Pergunta: em que medida esses SDKs estão declarados ao cidadão?", 15, True, WHITE, "c", spacing=1.05)], anchor="m")
notas(s, "Hoje muita coisa do governo se resolve pelo celular. O Meu INSS e o Meu SUS Digital, por exemplo, passam de 50 milhões de instalações cada um. Esses aplicativos não têm só o código do órgão: trazem componentes prontos de outras empresas, os SDKs, para mapas, notificações e estatísticas de uso. Alguns desses SDKs coletam dados de quem usa. No governo isso pesa mais, porque o cidadão muitas vezes não tem outro aplicativo para usar. Um cuidado importante: o SDK estar no código não prova que ele enviou dados.")

# ---------------------------------------------------------------- 4 problema e objetivo geral (fundo 13)
s = nova(13)
barra_titulo(s, "PROBLEMA E OBJETIVO GERAL")
texto(s, 0.9, 1.75, 11.6, 0.35, [P("PROBLEMA DE PESQUISA", 14, True, MID)])
texto(s, 0.9, 2.1, 11.6, 1.2, [P("Em que medida os SDKs de rastreamento de terceiros embarcados nos aplicativos Android oficiais do governo brasileiro estão declarados nas políticas de privacidade e na seção “Segurança dos dados” da Google Play?", 21, True, NAVY)])
texto(s, 0.9, 3.45, 11.6, 0.35, [P("OBJETIVO GERAL", 14, True, MID)])
texto(s, 0.9, 3.8, 11.6, 1.0, [P("Medir a proporção de pares aplicativo–SDK de rastreamento sem declaração compatível, comparando os SDKs encontrados no código com a política de privacidade e a seção “Segurança dos dados”, à luz da LGPD.", 18, False, DARK, spacing=1.05)])
forma(s, 0.9, 5.0, 11.6, 1.25, PALE)
texto(s, 1.15, 5.05, 3.1, 1.15, [P("Par aplicativo–SDK", 18, True, NAVY), P("a unidade que será contada", 14, False, DARK)], anchor="m")
forma(s, 4.45, 5.3, 1.75, 0.65, NAVY)
texto(s, 4.45, 5.3, 1.75, 0.65, [P("Aplicativo X", 15, True, WHITE, "c")], anchor="m")
for k, nome in enumerate(["estatísticas", "mapas", "notificações"]):
    x0 = 6.6 + k * 1.95
    forma(s, x0 - 0.33, 5.51, 0.28, 0.24, MID, MSO_SHAPE.RIGHT_ARROW)
    forma(s, x0, 5.3, 1.75, 0.65, WHITE, linha=MID)
    texto(s, x0, 5.3, 1.75, 0.65, [P("SDK de " + nome, 14, True, NAVY, "c")], anchor="m")
texto(s, 6.27, 5.97, 6.0, 0.3, [P("1 aplicativo com 3 SDKs = 3 pares, e cada par é classificado", 13, False, DARK, "c")])
notas(s, "O problema da pesquisa é: em que medida os SDKs de rastreamento dos aplicativos oficiais do governo estão declarados ao cidadão, na política de privacidade e na seção “Segurança dos dados” da Google Play? O objetivo geral é medir isso como uma proporção, à luz da LGPD. A unidade é o par aplicativo–SDK: cada SDK encontrado em cada aplicativo forma um par. Um aplicativo com três SDKs gera três pares, e cada par é classificado de acordo com as declarações.")

# ---------------------------------------------------------------- 5 objetivos específicos (fundo 13)
s = nova(13)
barra_titulo(s, "OBJETIVOS ESPECÍFICOS")
objs = [
    ["a) Revisar a lista de aplicativos", "Confirmar órgão e esfera dos 376 aplicativos pelo nome jurídico na Google Play", "Lista final e taxa de erro da classificação"],
    ["b) Listar os SDKs", "Baixar a versão atual e rodar três detectores (bases Exodus Privacy e Disconnect)", "Pares aplicativo–SDK, com a evidência"],
    ["c) Classificar as declarações", "Ler a política de privacidade e a “Segurança dos dados” e classificar cada par", "Proporção de pares sem declaração: teste da H1"],
    ["d) Registrar o tráfego", "Executar uma subamostra no emulador Android e registrar as conexões", "Destinos, país e se estão declarados"],
    ["e) Medir a concordância dos detectores", "Calcular o κ de Fleiss nos mesmos pacotes", "Quanto a taxa depende da ferramenta"],
]
tabela(s, 0.75, 1.75, [3.0, 5.6, 3.3], ["Objetivo", "O que será feito", "Resultado"], objs, size=15, cab_size=15, alt_h=0.8)
notas(s, "São cinco objetivos específicos. Primeiro, revisar os 376 aplicativos oficiais e medir quanto a classificação automática errou. Segundo, baixar a versão atual de cada aplicativo e listar os SDKs com três detectores. Terceiro, ler as declarações e classificar cada par; é daí que sai a proporção que testa a hipótese. Quarto, executar uma parte dos aplicativos num emulador Android, no computador, e registrar para onde os dados vão. Quinto, medir se os detectores concordam, com o kappa de Fleiss.")

# ---------------------------------------------------------------- 6 hipótese (fundo 13)
s = nova(13)
barra_titulo(s, "HIPÓTESE")
forma(s, 0.9, 1.75, 5.6, 2.55, NAVY)
texto(s, 1.15, 1.9, 5.1, 2.3, [P("H1", 30, True, PALE, after=4),
                               P("Ao menos 10% dos pares aplicativo–SDK de rastreamento não terão declaração compatível na política de privacidade nem na seção “Segurança dos dados” da Google Play.", 20, True, WHITE, spacing=1.05)])
texto(s, 0.9, 4.5, 5.6, 0.35, [P("CRITÉRIO DE DECISÃO", 13, True, MID)])
texto(s, 0.9, 4.85, 5.6, 1.3, [P("Confirmada se a proporção de pares sem declaração compatível for de 10% ou mais; refutada se for menor. O IC95% mostra a precisão.", 16, False, DARK, spacing=1.05)])
texto(s, 6.95, 1.75, 5.5, 0.35, [P("BASE NA LITERATURA", 13, True, MID)])
base = [(f"Andow et al. {ref('andow2020')}", "13.796 aplicativos: até 42,4% omitiam ou declaravam errado fluxos de dados sensíveis"),
        (f"Samarasinghe et al. {ref('samarasinghe2022')}", "1.166 aplicativos de governo: 27% enviavam informações sensíveis a terceiros ou sem criptografia"),
        (f"Carlsson et al. {ref('carlsson2022')}", "32 aplicativos do setor público finlandês: políticas divergiam dos dados enviados a terceiros"),
        (f"Kollnig et al. {ref('kollnig2022ios')}", "24 mil aplicativos Android e iOS: falta de transparência sobre o rastreamento")]
for k, (aut, txt) in enumerate(base):
    y0 = 2.12 + k * 0.88
    forma(s, 6.95, y0, 0.07, 0.78, MID)
    texto(s, 7.15, y0, 5.3, 0.85, [P(aut, 14, True, NAVY), P(txt, 14, False, DARK)])
forma(s, 6.95, 5.62, 5.5, 0.78, PALE)
texto(s, 7.1, 5.62, 5.25, 0.78, [R([("Por que 10%? ", 14, True, NAVY), ("As taxas acima contam aplicativos, e não pares; por isso, um patamar bem mais baixo e conservador.", 14, False, NAVY)])], anchor="m")
notas(s, "A pesquisa tem uma hipótese só, construída a partir da literatura. Andow e colegas analisaram quase 14 mil aplicativos e viram que até 42,4% omitiam ou declaravam errado para onde iam dados sensíveis. Samarasinghe e colegas, em 1.166 aplicativos de governo, viram que 27% enviavam informações sensíveis a terceiros ou sem criptografia. Carlsson e colegas acharam divergências entre as políticas e o tráfego de aplicativos públicos da Finlândia. E Kollnig e colegas apontaram falta de transparência sobre rastreamento no Android e no iPhone. Daí a hipótese: pelo menos 10% dos pares aplicativo–SDK não terão declaração compatível. Ela se confirma se a proporção que eu encontrar for de 10% ou mais. O 10% fica bem abaixo dessas taxas de propósito: elas contam aplicativos, e eu conto pares, então escolhi um patamar conservador.",
      "LEMBRETE (não precisa falar). Como analiso todos os aplicativos oficiais, e não uma amostra, a decisão usa a proporção encontrada. O intervalo de confiança de 95% só mostra a precisão; ele é calculado agrupando por aplicativo, porque os pares do mesmo aplicativo usam a mesma política. Se der menos de 10%, só dá para dizer que ficou abaixo do meu patamar, não que o governo é mais transparente que nos outros estudos. O 10% é um critério do estudo, não um limite da LGPD.")

# ================================================================ REFERENCIAL TEÓRICO
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
    s = nova(13)
    barra_titulo(s, f"ESTUDOS QUE ORIENTAM O PROJETO ({parte}/2)", sub=sub)
    tabela(s, 0.65, 2.22, LARG_EST, CAB_EST, linhas, size=15, cab_size=15, alt_h=1.2)
    if parte == 1:
        notas(s, "No referencial, separei seis estudos que orientam o projeto, com o que cada um buscava, o que fez, como fez e o que achou. Os três primeiros tratam de rastreamento e declarações. Binns e colegas examinaram 959 mil aplicativos procurando rastreadores no código e acharam rastreamento na maioria, concentrado em poucas empresas. Kollnig e colegas compararam aplicativos de antes e de depois do GDPR, o regulamento europeu, e viram pouca mudança. E Andow e colegas compararam o que os aplicativos enviam com o que as políticas dizem: até 42,4% omitiam ou declaravam errado. É dessa linha que vem o meu método.")
    else:
        notas(s, "Os outros três estudaram aplicativos de governo. Samarasinghe e colegas examinaram 1.166 aplicativos de 71 países: 37% tinham rastreadores do Google, e 27% enviavam informações sensíveis a terceiros ou sem criptografia, mas o Brasil não aparece separado. Carlsson e colegas compararam o tráfego de 32 aplicativos públicos da Finlândia com as políticas e acharam divergências, às vezes com dados indo para fora da Europa. É o estudo mais parecido com o meu. E Serrano e colegas acharam rastreadores em 402 de 595 aplicativos da COVID-19.")

# ---------------------------------------------------------------- lacuna e contribuição (fundo 13)
s = nova(13)
barra_titulo(s, "LACUNA E CONTRIBUIÇÃO")
colunas = [("O que já existe", SILVER, DARK), ("O que falta", MID, WHITE), ("O que este TCC faz", NAVY, WHITE)]
X0, CW, GAP = 2.75, 3.05, 0.45
for j, (cab, cor, ctx) in enumerate(colunas):
    x0 = X0 + j * (CW + GAP)
    forma(s, x0, 1.72, CW, 0.45, cor)
    texto(s, x0, 1.72, CW, 0.45, [P(cab, 16, True, ctx, "c")], anchor="m")
eixos = [("Caso brasileiro",
          ["Estudo internacional de aplicativos de governo; estudos de um aplicativo brasileiro por vez",
           "Medir o conjunto dos aplicativos do governo brasileiro, por esfera",
           "Analisa os 376 aplicativos classificados como oficiais, nas três esferas"]),
         ("Declarado × encontrado",
          ["Comparação entre política e dados em aplicativos comerciais e no setor público finlandês",
           "Comparar cada SDK com a política e a “Segurança dos dados” no Brasil",
           "Classifica cada par aplicativo–SDK e testa a H1"]),
         ("Instrumento",
          ["Comparações de ferramentas que detectam bibliotecas",
           "Concordância entre detectores de rastreadores nas mesmas versões",
           "Mede o κ de Fleiss entre três detectores"])]
RH = 1.25
for i, (eixo, cel) in enumerate(eixos):
    y0 = 2.3 + i * (RH + 0.1)
    forma(s, 0.75, y0, 1.85, RH, PALE)
    texto(s, 0.85, y0, 1.65, RH, [P(eixo, 15, True, NAVY, "c")], anchor="m")
    for j, txt in enumerate(cel):
        x0 = X0 + j * (CW + GAP)
        forma(s, x0, y0, CW, RH, [LIGHT, WHITE, PALE][j], linha=[SILVER, MID, NAVY][j])
        texto(s, x0 + 0.15, y0, CW - 0.3, RH, [P(txt, 15, j == 2, NAVY if j == 2 else DARK, "c")], anchor="m")
        if j < 2:
            forma(s, x0 + CW + 0.08, y0 + RH / 2 - 0.15, 0.29, 0.3, MID, MSO_SHAPE.RIGHT_ARROW)
texto(s, 1.45, 6.4, 10.9, 0.3, [P(f"Bases: Samarasinghe et al. {ref('samarasinghe2022')}; Lemos et al. {ref('lemos2022')}; Vaz et al. {ref('vaz2022')}; Andow et al. {ref('andow2020')}; Carlsson et al. {ref('carlsson2022')}; Zhan et al. {ref('zhan2022')}.", 11, False, GREY)])
notas(s, "Juntando esses estudos, aparecem três lacunas, e cada uma vira uma contribuição. Primeiro, o caso brasileiro: há estudos de um aplicativo por vez, mas ninguém mediu o conjunto; o trabalho analisa os 376 aplicativos classificados como oficiais, das três esferas. Segundo, o confronto entre o declarado e o encontrado já foi feito em outros contextos, mas não aqui; o trabalho classifica cada par e testa a hipótese. Terceiro, o instrumento: o trabalho mede quanto o resultado depende do detector. E uma divergência não prova infração à LGPD; é um indício a ser examinado.")

# ================================================================ PROCEDIMENTOS METODOLÓGICOS
# ---------------------------------------------------------------- etapas do método (fundo 13)
s = nova(13)
barra_titulo(s, "ETAPAS DO MÉTODO", sub="Estudo quantitativo e observacional, em seis etapas")
etapas = [
    ["1. Seleção dos aplicativos", "Revisar cada aplicativo pelo nome jurídico do desenvolvedor", "376 aplicativos oficiais, por esfera", "a"],
    ["2. Obtenção dos pacotes", "Baixar a versão atual com o apkeep; AndroZoo quando houver", "Pacote com hash SHA-256, versão e data", "b"],
    ["3. Detecção dos SDKs", "Rodar os detectores A, B e C e medir a concordância", "Pares aplicativo–SDK; κ de Fleiss", "b, e"],
    ["4. Classificação das declarações", "Ler a política e a “Segurança dos dados”; classificar cada par", "Matriz de declarações", "c"],
    ["5. Observação do tráfego", "Subamostra no emulador do Android Studio, com o mitmproxy", "Destinos, país e se estão declarados", "d"],
    ["6. Análise estatística", "Calcular a proporção de pares sem declaração e comparar com 10%", "Decisão sobre a hipótese", "c, e"],
]
tabela(s, 0.65, 2.15, [2.75, 5.0, 3.1, 1.15], ["Etapa", "O que será feito e como", "O que entrega", "Objetivo"], etapas, size=15, cab_size=15, alt_h=0.63, cab_h=0.42)
notas(s, "O estudo é quantitativo e observacional, em seis etapas, e cada uma atende a um objetivo. Primeiro, a seleção dos aplicativos. Depois, o download da versão atual, com o hash, que é a impressão digital do arquivo. Em seguida, a detecção dos SDKs com três detectores e a classificação das declarações. A quinta etapa observa o tráfego de uma parte dos aplicativos num emulador Android, com o mitmproxy, que registra as conexões. Por fim, a análise estatística decide a hipótese.")

# ---------------------------------------------------------------- por que só Android (fundo 13)
s = nova(13)
barra_titulo(s, "POR QUE SÓ ANDROID", sub="Três motivos, e o que isso não significa")
motivos = [("Abrangência", "73,76%", f"dos celulares no Brasil usam Android (StatCounter {ref('statcounter2026')}, out. 2026)"),
           ("Acesso ao código", "iOS", f"Aplicativos criptografados pela Apple e sem ferramenta pública para baixá-los em escala; decriptar exige aparelho físico e tem legalidade incerta (Kollnig et al. {ref('kollnig2022ios')})"),
           ("Declarações comparáveis", "Google Play", f"A hipótese usa a seção “Segurança dos dados”; a App Store tem rótulos em outro formato (Xiao et al. {ref('xiao2023')})")]
for k, (cab, num, txt) in enumerate(motivos):
    x0 = 0.9 + k * 3.95
    forma(s, x0, 2.22, 3.7, 2.95, NAVY if k == 0 else (MID if k == 1 else PALE))
    ct = WHITE if k < 2 else NAVY
    texto(s, x0 + 0.25, 2.37, 3.2, 0.4, [P(cab.upper(), 14, True, ct)])
    texto(s, x0 + 0.25, 2.77, 3.2, 0.8, [P(num, 36 if k == 0 else 30, True, ct)], anchor="m")
    texto(s, x0 + 0.25, 3.62, 3.2, 1.5, [P(txt, 15, False, ct, spacing=1.0)])
forma(s, 0.9, 5.35, 11.6, 0.95, LIGHT)
texto(s, 1.15, 5.35, 11.1, 0.95, [R([("Não significa que o iPhone seja mais seguro: ", 15, True, NAVY),
                                    (f"Kollnig et al. {ref('kollnig2022ios')} compararam 12 mil aplicativos de cada plataforma e acharam rastreamento comum nas duas, sem uma claramente melhor. As versões iOS ficam como trabalho futuro.", 15, False, DARK)], spacing=1.05)], anchor="m")
notas(s, "Por que só Android? São três motivos. Primeiro, abrangência: segundo a StatCounter, o Android está em 73,76% dos celulares no Brasil. Segundo, acesso ao código: Kollnig e colegas explicam que, no iPhone, os aplicativos são criptografados, não há ferramenta pública para baixá-los em escala, e decriptar exige um aparelho físico e tem legalidade incerta. Terceiro, a hipótese usa a seção “Segurança dos dados”, que só existe na Google Play. Isso não quer dizer que o iPhone seja mais seguro: o mesmo estudo achou rastreamento nas duas plataformas. O iOS fica como trabalho futuro.")

# ---------------------------------------------------------------- aplicativos selecionados (fundo 11)
s = nova(11)
texto(s, 1.0, 0.6, 5.3, 1.3, [P("APLICATIVOS SELECIONADOS", 34, True, MID, spacing=0.9)], anchor="b")
texto(s, 1.0, 2.0, 5.3, 0.5, [P("396 candidatos, 376 oficiais", 22, False, GREY)])
texto(s, 1.0, 2.75, 5.0, 3.5, [
    P("Busca por 21 termos na Google Play e pelo catálogo de cada publicador oficial.", 17, False, DARK, after=10),
    P("Oficialidade confirmada pelo nome jurídico em “Sobre o desenvolvedor”.", 17, False, DARK, after=10),
    P("Saíram 20: 13 empresas privadas e 7 contas de pessoa física.", 17, False, DARK, after=10),
    P("Lista preliminar: será revista antes da coleta (objetivo a).", 15, True, NAVY)])
texto(s, 6.61, 2.85, 3.61, 1.8, [P("376", 60, True, WHITE, "c"), P("aplicativos oficiais", 18, False, PALE, "c")], anchor="m")
for (cx, cy), (num, leg) in zip([(10.68, 1.83), (11.63, 3.76), (10.68, 5.72)], [("85", "federais"), ("199", "estaduais"), ("92", "municipais")]):
    texto(s, cx - 0.86, cy - 0.5, 1.72, 1.0, [P(num, 26, True, NAVY, "c"), P(leg, 13, False, DARK, "c")], anchor="m")
notas(s, "Agora, os resultados preliminares, da preparação do estudo. Para montar a lista, busquei 21 termos ligados a serviço público na Google Play e depois o catálogo de cada publicador oficial. Foram 396 candidatos. Pelo nome jurídico de quem publica, ficaram 376 oficiais: 85 federais, 199 estaduais e 92 municipais. Saíram 20, de empresas privadas ou de contas de pessoa física. A lista é preliminar e será revista antes da coleta.")

# ---------------------------------------------------------------- fonte dos pacotes (fundo 2)
s = nova(2)
texto(s, 0.9, 0.95, 11.5, 0.85, [P("FONTE DOS PACOTES", 44, True, WHITE)])
texto(s, 0.9, 1.8, 11.5, 0.5, [P("Consulta ao AndroZoo, acervo acadêmico de pacotes Android", 22, False, PALE)])
for x0, num, cor, leg in [(0.9, "23,2%", WHITE, "governo: 92 de 396 candidatos"), (4.7, "84,2%", MID, "comerciais: 160 de 190, só como contexto")]:
    texto(s, x0, 2.45, 3.7, 1.1, [P(num, 66, True, cor)])
    texto(s, x0, 3.55, 3.7, 0.5, [P(leg, 16, False, PALE)])
texto(s, 8.75, 2.6, 3.7, 1.5, [P("Fonte principal: versão atual na Google Play", 19, True, WHITE, after=6),
                               P("AndroZoo: reprodutibilidade e defasagem", 16, False, PALE)])
forma(s, 0.9, 4.2, 11.5, 0.03, MID)
texto(s, 0.9, 4.32, 11.5, 0.35, [P("COMO SERÁ A COLETA", 14, True, PALE)])
passos_c = [("Conta da pesquisa", "Conta Google criada só para o estudo, com acesso a partir do Brasil"),
            ("Download com apkeep", "Ferramenta aberta da EFF; em pacotes divididos, guarda o APK base"),
            ("Registro", "Hash SHA-256, versão, data e o motivo de cada falha"),
            ("Teste primeiro", "Cinco aplicativos em fevereiro; depois, todos")]
for i, (cab, txt) in enumerate(passos_c):
    x0 = 0.9 + i * 2.92
    forma(s, x0, 4.72, 2.75, 1.5, LIGHT)
    texto(s, x0 + 0.18, 4.84, 0.45, 0.45, [P(str(i + 1), 24, True, NAVY)], anchor="m")
    texto(s, x0 + 0.62, 4.84, 2.0, 0.45, [P(cab, 15, True, NAVY)], anchor="m")
    texto(s, x0 + 0.18, 5.33, 2.42, 0.88, [P(txt, 14, False, DARK, spacing=1.0)])
notas(s, "Na hora de buscar os pacotes, apareceu um problema. O AndroZoo, um acervo acadêmico, tinha só 92 dos 396 aplicativos do governo, 23,2%, contra 84,2% dos comerciais. Dependendo só dele, a maioria ficaria de fora. Por isso, a fonte principal será a versão atual da Google Play, que é a que o cidadão instala, baixada com o apkeep, uma ferramenta aberta, com uma conta criada só para a pesquisa. Registro o hash, a versão, a data e o motivo de cada falha. O AndroZoo fica para a reprodutibilidade.",
      "LEMBRETE (não precisa falar). Quando o aplicativo vem dividido em vários pacotes, guardo o APK base, que tem o código. O apkeep é da Electronic Frontier Foundation (EFF). Não redistribuo os pacotes.")

# ---------------------------------------------------------------- piloto dos detectores (fundo 13)
s = nova(13)
barra_titulo(s, "PILOTO DOS DETECTORES", sub="Ferramentas diferentes dão taxas diferentes")
barras = [("A · Exodus, código", 15, NAVY), ("B · Exodus, domínios", 19, MID), ("C · Disconnect, domínios", 16, NAVY)]
for i, (lab, k, cor) in enumerate(barras):
    y0 = 2.5 + i * 1.05
    texto(s, 0.9, y0, 2.75, 0.7, [P(lab, 16, True, DARK)], anchor="m")
    forma(s, 3.75, y0 + 0.08, 4.6, 0.54, LIGHT)
    forma(s, 3.75, y0 + 0.08, 4.6 * k / 20, 0.54, cor)
    texto(s, 3.85, y0 + 0.08, 4.4 * k / 20, 0.54, [P(f"{k} de 20 · {k*5}%", 15, True, WHITE, "r")], anchor="m")
texto(s, 0.9, 5.7, 7.6, 0.5, [P("Proporção dos 20 pacotes do piloto com ao menos um rastreador, por detector.", 14, False, GREY)])
forma(s, 9.0, 2.22, 3.6, 4.0, NAVY)
texto(s, 9.2, 2.4, 3.2, 3.6, [P("κ de Fleiss", 18, True, PALE, "c"),
                             P("0,52", 54, True, WHITE, "c", after=0),
                             P("moderada", 15, True, PALE, "c", after=8),
                             P("0,69 na análise de sensibilidade: substancial", 14, False, LIGHT, "c", after=12),
                             P("88 de 123 detecções de B marcadas como possíveis falsos positivos, sem referência independente", 14, False, LIGHT, "c", spacing=1.05)], anchor="m")
notas(s, "No piloto, testei três detectores em 20 pacotes. O A procura no código os SDKs da base do Exodus. O B usa a mesma base, mas procura endereços de internet dentro do pacote. O C faz o mesmo que o B, com a lista da Disconnect. As taxas foram diferentes: 75%, 95% e 80% dos pacotes com rastreador. Revisando as detecções uma a uma, 88 das 123 do B pareciam falsos positivos, quase todas por endereços genéricos do Google ou do Facebook. Ou seja, a ferramenta muda o resultado. O kappa de Fleiss entre os três foi 0,52, uma concordância moderada pela escala que mostrei; sem os possíveis falsos positivos do B, sobe para 0,69, substancial. Com só 20 pacotes, isso testa o instrumento, e não a hipótese.",
      "LEMBRETE (não precisa falar). A contra B mostra o efeito do método (mesma base); B contra C mostra o efeito da base (mesmo método). B não é tráfego, é texto dentro do pacote: um link para maps.google.com bastou para apontar Google Ads. C usa só as categorias publicidade, análise de uso e impressão digital. Exodus Privacy: base aberta de rastreadores, com assinaturas de código e de rede. Disconnect: lista de domínios que coletam dados, separados por categoria.")

# ---------------------------------------------------------------- kappa de Fleiss (fundo 13)
s = nova(13)
barra_titulo(s, "COMO LER O κ DE FLEISS", sub=f"Concordância entre os três detectores, descontado o acaso (Fleiss {ref('fleiss1971')})")
forma(s, 0.9, 2.22, 5.5, 1.0, NAVY)
texto(s, 0.9, 2.22, 5.5, 1.0, [R([("κ = (P", 32, True, WHITE), ("o", 32, True, WHITE, True), (" − P", 32, True, WHITE), ("e", 32, True, WHITE, True),
                                  (") / (1 − P", 32, True, WHITE), ("e", 32, True, WHITE, True), (")", 32, True, WHITE)], align="c")], anchor="m")
defs = [[("P", 15, True, NAVY), ("o", 15, True, NAVY, True), (" — concordância observada: ", 15, True, NAVY),
         ("em cada aplicativo, a fração de pares de detectores que concordam; depois, a média.", 14, False, DARK)],
        [("P", 15, True, NAVY), ("e", 15, True, NAVY, True), (" — concordância esperada ao acaso: ", 15, True, NAVY),
         ("soma dos quadrados das proporções de “tem” e de “não tem”.", 14, False, DARK)],
        [("Exemplo: ", 15, True, NAVY), ("os três dizem “tem” → 1; dois dizem “tem” e um “não tem” → 1/3.", 14, False, DARK)],
        [("Por que descontar o acaso? ", 15, True, NAVY), ("Se quase todo aplicativo tem rastreador, quem diz “tem” para tudo concorda sem medir nada.", 14, False, DARK)]]
texto(s, 0.9, 3.4, 5.5, 3.0, [R(d, after=6) for d in defs])
texto(s, 6.85, 2.22, 5.6, 0.35, [P(f"ESCALA DE LANDIS E KOCH {ref('landis1977')}", 13, True, MID)])
faixas = [("< 0", "pobre"), ("0–0,20", "leve"), ("0,21–0,40", "razoável"), ("0,41–0,60", "moderada"), ("0,61–0,80", "substancial"), ("0,81–1", "quase perfeita")]
cores_f = [RGBColor(0xE6, 0xE6, 0xE6), RGBColor(0xDC, 0xE6, 0xF1), RGBColor(0xB9, 0xCD, 0xE3), MID, RGBColor(0x2E, 0x5F, 0x8A), NAVY]
for k, ((fx, nome), cf) in enumerate(zip(faixas, cores_f)):
    y0 = 2.6 + k * 0.47
    forma(s, 6.85, y0, 1.55, 0.42, cf)
    texto(s, 6.85, y0, 1.55, 0.42, [P(fx, 13, True, WHITE if k >= 3 else NAVY, "c")], anchor="m")
    texto(s, 8.55, y0, 1.9, 0.42, [P(nome, 14, k in (3, 4), NAVY if k in (3, 4) else DARK)], anchor="m")
texto(s, 10.25, 2.6 + 3 * 0.47, 2.3, 0.84, [P("← limiar do estudo: 0,6", 14, True, NAVY)], anchor="m")
forma(s, 6.85, 5.52, 5.6, 0.85, PALE)
texto(s, 7.0, 5.52, 5.35, 0.85, [P("1 = concordância total; 0 = igual ao acaso. Limiar do estudo: 0,6. Concordância alta não prova acerto: os três podem errar igual.", 14, False, NAVY)], anchor="m")
notas(s, "Para medir a concordância entre os detectores, uso o kappa de Fleiss. Ele mede se vários avaliadores concordam, descontando o acordo que aconteceria por acaso; aqui, os avaliadores são os três detectores, e cada um diz se o aplicativo tem ou não rastreador. P o é a concordância observada: em cada aplicativo, a fração dos pares de detectores que concordam; se os três concordam, dá 1; se um discorda, dá um terço. P e é a concordância esperada só por acaso. Descontar o acaso importa porque, se quase todo aplicativo tem rastreador, concordar é fácil. Para ler o resultado, uso a escala de Landis e Koch, e meu limiar é 0,6, a passagem de moderada para substancial. O valor do piloto aparece nos resultados.",
      "LEMBRETE (não precisa falar). Fórmula por aplicativo: P i = soma de n ij vezes (n ij − 1), dividida por n vezes (n − 1), com n = 3 detectores e n ij = quantos deram a resposta j. P e = soma de p j ao quadrado, com p j = proporção de todas as respostas na categoria j. Junto do κ, reporto o IC95% e as concordâncias positiva e negativa, porque o κ fica instável quando quase todos os aplicativos estão na mesma categoria. Na revisão, a reclassificação às cegas da triagem usa o κ de Cohen, a versão para dois avaliadores, com a mesma escala.")

# ---------------------------------------------------------------- classificação das declarações (fundo 13)
s = nova(13)
barra_titulo(s, "CLASSIFICAÇÃO DAS DECLARAÇÕES", sub="Cada par aplicativo–SDK recebe uma de cinco situações")
situacoes = [("Menção nominal", "A política cita o SDK ou a empresa que o fornece", PALE, NAVY, DARK),
             ("Declaração por categoria", "O tipo de dado e a finalidade estão declarados, mesmo sem o nome do SDK", PALE, NAVY, DARK),
             ("Sem declaração compatível", "Documentos disponíveis, mas nenhum cobre o dado ou a finalidade do SDK", NAVY, WHITE, LIGHT),
             ("Informação insuficiente", "Documentos genéricos demais para decidir", LIGHT, DARK, DARK),
             ("Política indisponível", "Documento não obtido", LIGHT, DARK, DARK)]
for k, (nome, desc, fundo_c, c_nome, c_desc) in enumerate(situacoes):
    y0 = 2.22 + k * 0.83
    forma(s, 0.9, y0, 7.6, 0.73, fundo_c)
    forma(s, 1.02, y0 + 0.13, 0.47, 0.47, WHITE if k != 2 else MID, MSO_SHAPE.OVAL)
    texto(s, 1.02, y0 + 0.13, 0.47, 0.47, [P(str(k + 1), 16, True, NAVY if k != 2 else WHITE, "c")], anchor="m")
    texto(s, 1.65, y0, 2.75, 0.73, [P(nome, 15, True, c_nome)], anchor="m")
    texto(s, 4.45, y0, 3.95, 0.73, [P(desc, 14, False, c_desc)], anchor="m")
forma(s, 8.85, 2.22, 3.75, 2.4, NAVY)
texto(s, 9.05, 2.3, 3.35, 2.25, [P("TESTE DA HIPÓTESE", 13, True, PALE, "c", after=6),
                                P("proporção = (3) ÷ [(1) + (2) + (3)]", 16, True, WHITE, "c", after=8),
                                P("H1 confirmada se der 10% ou mais", 14, False, LIGHT, "c", after=4),
                                P("com IC95% agrupado por aplicativo", 14, False, LIGHT, "c")], anchor="m")
forma(s, 8.85, 4.77, 3.75, 0.85, LIGHT)
texto(s, 9.0, 4.77, 3.45, 0.85, [P("(4) e (5): reportados à parte e nas análises de sensibilidade", 14, False, NAVY, "c")], anchor="m")
texto(s, 8.85, 5.75, 3.75, 0.55, [P("Já verificado: 323 dos 396 candidatos (81,6%) têm política acessível.", 13, False, GREY, "c")], anchor="m")
notas(s, "Esta é a parte central do teste. Para cada par, leio a política de privacidade e a seção “Segurança dos dados” e escolho uma de cinco situações: o SDK é citado pelo nome; o tipo de dado e a finalidade estão declarados, mesmo sem o nome; não há declaração compatível; a informação é genérica demais; ou a política não está disponível. A proporção é a terceira situação dividida pelas três primeiras; se der 10% ou mais, a hipótese se confirma. As duas últimas ficam à parte, para não inflar nem esconder o problema. Não citar o nome do SDK, sozinho, não conta como omissão.")

# ---------------------------------------------------------------- revisão sistemática (fundo 10)
s = nova(10)
cols = [("ONDE", "15 buscas em 4 bases: Scopus (principal), IEEE Xplore, SBC OpenLib e BDTD; 2018 a 2026; inglês e português"),
        ("COMO", "Strings com aplicativo, fenômeno e contexto, e termo do tema obrigatório no título do artigo"),
        ("VALIDAÇÃO", "9 estudos de controle: as buscas acharam os 8 que o Scopus indexa")]
for i, (cab, txt) in enumerate(cols):
    x0 = 0.75 + i * 3.62
    texto(s, x0, 0.55, 3.35, 0.4, [P(cab, 16, True, NAVY)])
    texto(s, x0, 0.98, 3.35, 1.55, [P(txt, 15, False, DARK, spacing=1.0)])
texto(s, 0.5, 2.6, 10.8, 2.27, [P("REVISÃO SISTEMÁTICA", 44, True, WHITE, "c"), P(f"Kitchenham e Charters {ref('kitchenham2007')} · PRISMA 2020 {ref('page2021')}", 16, False, PALE, "c")], anchor="m")
fluxo = [("396", "resultados"), ("312", "sem repetidos"), ("148", "à leitura completa, em andamento")]
for i, (num, leg) in enumerate(fluxo):
    x0 = 2.375 + i * 2.95
    texto(s, x0, 5.0, 2.3, 0.65, [P(num, 34, True, NAVY, "c")], anchor="m")
    texto(s, x0, 5.62, 2.3, 0.4, [P(leg, 14, False, GREY, "c")])
    if i < 2:
        forma(s, x0 + 2.42, 5.17, 0.38, 0.3, MID, MSO_SHAPE.RIGHT_ARROW)
notas(s, "Para a literatura, fiz uma revisão sistemática: uma busca planejada e documentada, para que a escolha dos artigos não dependa de preferência pessoal. Segui o guia de Kitchenham: antes de buscar, escrevi um protocolo com as perguntas, as bases, as palavras de busca e os critérios. O resultado segue o PRISMA 2020, um fluxograma do que entrou e saiu em cada etapa. Foram 15 buscas em quatro bases, de 2018 a 2026, exigindo um termo do tema no título. Para testar as buscas, separei estudos que tinham de aparecer: dos nove dentro do escopo, elas acharam os oito que estão no Scopus. Foram 396 resultados, 312 sem repetidos, e 148 seguiram para a leitura completa, que está em andamento.",
      "Guia de Kitchenham: divide a revisão em planejamento (questões e protocolo), condução (busca, seleção, avaliação de qualidade e extração dos dados) e relatório (síntese dos resultados).",
      "PRISMA 2020: padroniza o relato da revisão num fluxograma, da identificação dos registros e remoção de duplicatas até a triagem, a leitura completa e os estudos incluídos.")

# ---------------------------------------------------------------- limitações (fundo 13)
s = nova(13)
barra_titulo(s, "LIMITAÇÕES")
lims = [["SDK no código não prova envio de dados", "Observação do tráfego numa subamostra"],
        ["Alguns aplicativos podem não rodar no emulador", "Motivo registrado e proporção reportada"],
        ["Só Android e Google Play", "Motivos justificados; iOS como trabalho futuro"],
        ["Políticas citam tipos de dados, não o nome do SDK", "Classificação por categoria; não citar o nome não é omissão"],
        ["Versões mudam entre a coleta e a análise", "Hash SHA-256, versão e data de cada pacote"],
        ["Divergência não prova infração à LGPD", "Tratada como indício, com a evidência registrada"]]
tabela(s, 0.85, 1.75, [5.95, 5.85], ["Limitação", "Como é tratada"], lims, size=16, cab_size=16, alt_h=0.66)
notas(s, "Sobre as limitações: achar o SDK no código não prova envio de dados, e por isso registro o tráfego de uma subamostra no emulador. Alguns aplicativos podem não rodar no emulador; nesse caso, registro o motivo. O estudo cobre só Android, pelos motivos que mostrei. As políticas falam de tipos de dados, e não do nome do SDK, então não citar o nome não conta como omissão. Registro a versão de cada pacote, porque eles mudam. E uma divergência não prova infração à LGPD; é um indício.")

# ---------------------------------------------------------------- próximos passos (fundo 13)
s = nova(13)
barra_titulo(s, "PRÓXIMOS PASSOS NO CAPSTONE II (2027.1)")
passos = [["Fevereiro", "Revisão sistemática", "Ler os registros em aberto; bola de neve; reclassificar às cegas 32 registros", "Estudos incluídos; κ de Cohen"],
          ["Fevereiro", "1. Seleção", "Revisar os 376 aplicativos; testar download e emulador; definir o detector principal", "Lista final e plano de análise"],
          ["Março", "2 e 3. Pacotes e detecção", "Baixar os aplicativos; rodar os três detectores; calcular o κ de Fleiss", "Pares aplicativo–SDK"],
          ["Mar. e abr.", "4. Declarações", "Ler as declarações e classificar cada par", "Matriz de declarações"],
          ["Abril", "5. Tráfego", "Executar a subamostra no emulador e registrar o tráfego", "Destinos e países"],
          ["Maio", "6. Análise", "Calcular a proporção, comparar com 10% e decidir sobre a H1; avisar órgãos de achados graves", "Resultado do teste da H1"],
          ["Junho", "Redação e defesa", "Escrever resultados e discussão; publicar dados e scripts", "Texto final e defesa"]]
tabela(s, 0.75, 1.75, [1.55, 2.55, 5.35, 2.45], ["Quando", "Etapa", "O que será feito", "Produto"], passos, size=14, cab_size=14, alt_h=0.6)
notas(s, "Os próximos passos ficam no Capstone II. Em fevereiro, termino a revisão e reviso a lista de aplicativos, testando o download e o emulador. Em março, baixo os pacotes e rodo os detectores. Entre março e abril, classifico as declarações. Em abril, registro o tráfego da subamostra no emulador. Em maio, faço a análise e decido sobre a hipótese, avisando os órgãos se houver achado grave. Em junho, escrevo, publico os dados e defendo.")

# ================================================================ CONCLUSÃO
s = nova(3)
texto(s, 0.9, 1.3, 11.4, 2.2, [P("Problema definido.", 44, True, WHITE), P("Método viável.", 44, True, WHITE), P("Hipótese pronta para o teste.", 44, True, NAVY)])
texto(s, 0.9, 4.0, 10.8, 1.2, [P("No Capstone II: medir a proporção de pares aplicativo–SDK sem declaração compatível.", 22, False, WHITE, spacing=1.05)])
texto(s, 0.9, 5.55, 6.0, 0.6, [P("Obrigado.", 24, True, NAVY)])
notas(s, "Para concluir: o problema está definido, o método é viável, e a hipótese está pronta para ser testada no Capstone II. O foco é medir o quanto o que os aplicativos públicos declaram sobre os dados bate com o que está dentro deles e, onde der para observar, com o que eles enviam. Obrigado.")


# ================================================================ REFERÊNCIAS: todas as do texto (fundo 4)
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
    s = nova(4)
    texto(s, 0.9, 0.35, 11.6, 0.7, [P(f"REFERÊNCIAS ({k}/{len(paginas)})", 32, True, GREY)])
    for x0, coluna in [(1.15, c1), (6.85, c2)]:
        if coluna:
            texto(s, x0, 1.15, 5.45, 5.3, [{"runs": [(t, TAM_REF, False, DARK, False, it) for t, it in r], "align": "l", "spacing": 1.0, "after": 4} for r in coluna])
    notas(s, "Não é para ler. São todas as referências do texto do TCC, numeradas na ordem em que aparecem no texto, no padrão IEEE do modelo do Capstone. Pode passar direto para o slide de encerramento.", *COLA)

# ---------------------------------------------------------------- encerramento institucional (fundo 14)
s = nova(14)
notas(s, "Slide de encerramento do template. Pode ficar na tela durante as perguntas.", *COLA)

# ---------------------------------------------------------------- remove os slides de exemplo do template
lst = prs.slides._sldIdLst
for sid in list(lst)[:N_TPL]:
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)

# ---------------------------------------------------------------- ordem das seções do texto
# criação: 0-8 introdução e revisão; 9 etapas; 10 Android; 11 aplicativos; 12 pacotes;
# 13 piloto; 14 kappa; 15 declarações; 16 revisão sistemática; 17 limitações;
# 18 próximos passos; 19 conclusão; depois, referências e encerramento
ORDEM = list(range(9)) + [9, 10, 14, 15, 16] + [11, 12, 13, 17] + [18, 19]
ORDEM += list(range(20, len(lst)))
assert sorted(ORDEM) == list(range(len(lst)))
ids = list(lst)
for sid in ids:
    lst.remove(sid)
for i in ORDEM:
    lst.append(ids[i])
FUNDO = [FUNDO[i] for i in ORDEM]

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
