#!/usr/bin/env python

from reportlab_fb import ReportlabFB, FBFlowable

from arpeggio_arrays import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
WIDTH, HEIGHT = letter

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

styles = getSampleStyleSheet()
#print styles.list()
styleN = styles['Normal']
styleI = ParagraphStyle(name='',
    parent=styles['Italic'],
    alignment=2)
styleT = ParagraphStyle(name='Title',
    parent=styles['Title'], 
    fontName='Helvetica')
            


fb5 = ReportlabFB(None, inch)
fb5.u_height = 1.25
fb5.u_width = 5.75

fb7 = ReportlabFB(None, inch)
fb7.u_height = 1.1
fb7.u_width = 5.75

#Arpeggio Patterns

doc = SimpleDocTemplate("arpeggios.pdf", bottomMargin = 0.25*inch)
story = []

story.append(Paragraph('Major Arpeggio Patterns',styleT))
md = enumerate(major_dots)
for t,d in md:
    story.append(FBFlowable(fb5,d,label='Position %s'%(t+1),labelpos=0))
story.append(Paragraph(major_uri,styleI))
story.append(PageBreak())

story.append(Paragraph('Minor Arpeggio Patterns',styleT))
md = enumerate(minor_dots)
for t,d in md:
    story.append(FBFlowable(fb5,d,label='Position %s'%(t+1),labelpos=0))
story.append(Paragraph(minor_uri,styleI))
story.append(PageBreak())

story.append(Paragraph('13th Chord Arpeggios Patterns',styleT))
for d in thirteenth:
    story.append(FBFlowable(fb5,d))
story.append(Paragraph(thirteenth_uri,styleI))
story.append(PageBreak())

story.append(Paragraph('Sliding Arpeggio Patterns',styleT))
md = zip(('Amaj9','Fmaj7'),flying)
for t,d in md:
    story.append(FBFlowable(fb5,d,label=t,labelpos=0))
story.append(Paragraph(flying_uri,styleI))
story.append(PageBreak())

doc.build(story)

#mode Patterns
from mode_arrays import allmodes
diatonic = ('Ionian','Dorian','Phrygian','Lydian','Mixolydian','Aeolian','Locrian')
tonic = ('Lydian','Ionian','Mixolydian','Dorian','Aeolian','Phrygian','Locrian')

types = (diatonic,tonic,diatonic,tonic,diatonic,tonic,tonic,tonic,tonic)

gmajor = ('G','A','B','C','D','E','F#')
A = ['A']*7
B = ['B']*7
G = ['G']*7
notes = (gmajor,A,gmajor,A,gmajor,A,A,B,G)
titles = ('1 Octave Diatonic Modes (Low)','1 Octave Modes (Low)',
'1 Octave Diatonic Modes (High)','1 Octave Modes (High)',
'2 Octave Diatonic Modes','2 Octave Modes',
'1 Octave Modes Up',
'1 Octave Modes Down',
'3 Octave Modes'
)

doc = SimpleDocTemplate("modes.pdf", bottomMargin = 0.25*inch, topMargin = 0.75*inch)
story = []
for title,nn,t,m in zip(titles,notes,types,allmodes):
    story.append(Paragraph(title,styleT))
    for note, name, dots in zip(nn,t,m):
        label = ' '.join((note,name))
        story.append(FBFlowable(fb7,dots,label=label))
    story.append(PageBreak())
    
doc.build(story)