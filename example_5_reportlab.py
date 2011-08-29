#!/usr/bin/env python

from reportlab_fb import ReportlabFB, FBFlowable

from arpeggio_arrays import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
WIDTH, HEIGHT = letter

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))

styles = getSampleStyleSheet()
#print styles.list()
styleN = styles['Normal']
styleI = ParagraphStyle(name='',
    parent=styles['Italic'],
    alignment=2)
styleT = ParagraphStyle(name='Title',
    parent=styles['Title'], 
    fontName='DejaVuSans', alignment=TA_LEFT)
            


fb7 = ReportlabFB(None, inch)
fb7.u_height = 1.1
fb7.u_width = 5.75
fb7.num_frets = 20.0


#mode Patterns
from segovia_scales import scales

sharp = u"\u266F" 
flat = u"\u266D"

doc = SimpleDocTemplate("segovia_scales.pdf",  pagesize=letter, bottomMargin = 0.25*inch, topMargin = 0.75*inch)
story = []
count = 0
for title,patterns in scales:
    title = title.replace("#",sharp).replace("b",flat)
    if count > 0 and count % 2 == 0:
        story.append(PageBreak())
    count += 1
    story.append(Paragraph(title,styleT))
    for kind,notes in patterns:
        story.append(FBFlowable(fb7,notes, label=kind))
    
doc.build(story)
