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

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/DejaVuSans.ttf'))

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
from single_octave_scales import scales

doc = SimpleDocTemplate("single_octave_scales.pdf",  pagesize=letter, bottomMargin = 0.25*inch, topMargin = 0.75*inch)
story = []
count = 0
for title, notes in scales:
    story.append(Paragraph(title,styleT))
    story.append(FBFlowable(fb7,notes))
    
    #if not '6th' in title:
    #    story.append(Spacer(1.5*inch, 1.5*inch)) 
    
doc.build(story)
