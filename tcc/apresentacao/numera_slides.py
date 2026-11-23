"""Acrescenta o número do slide (campo automático do PowerPoint) no canto inferior direito.
Uso: python numera.py ENTRADA.pptx SAIDA.pptx
Não numera a capa (1) nem o slide institucional final."""
import sys, copy
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
ENT, SAI = sys.argv[1:3]
prs = Presentation(ENT)
n = len(prs.slides)
ESCUROS = {1, 6, 11, 15, n}          # fundo escuro ou azul no canto: número em branco
W = prs.slide_width
for i, s in enumerate(prs.slides, 1):
    for sh in list(s.shapes):
        if sh.name == "Número do slide":
            sh._element.getparent().remove(sh._element)
    if i == 1 or i == n:
        continue
    box = s.shapes.add_textbox(W - Inches(1.05), Inches(6.93), Inches(0.75), Inches(0.38))
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
    etree.SubElement(fill, qn("a:srgbClr"), val="FFFFFF" if i in ESCUROS else "7F7F7F")
    etree.SubElement(rpr, qn("a:latin"), typeface="Calibri")
    t = etree.SubElement(fld, qn("a:t")); t.text = str(i)
prs.save(SAI)
print("ok", n, "slides; numerados 2 a", n - 1)
