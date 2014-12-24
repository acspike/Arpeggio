#!/usr/bin/env python

from reportlab_fb import ReportlabFB, FBFlowable

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
fb7.num_frets = 14.0
fb7.numbered_frets = [3,5,7,9,12,]



import learn_notes as ln
days = zip(ln.strings + ln.strings, ln.notes, ln.frets + ln.frets)

doc = SimpleDocTemplate("12_days.pdf",  pagesize=letter, bottomMargin = 0.25*inch, topMargin = 0.75*inch)
story = []
count = 0
for i, day in enumerate(days):
    strings, notes, frets = day
    
    story.append(Paragraph('Day '+str(i+1),styleT))
    story.append(FBFlowable(fb7,notes))
    story.append(FBFlowable(fb7,strings))
    story.append(FBFlowable(fb7,frets))
    if i % 2 == 1:
        story.append(PageBreak()) 
    
doc.build(story)
