#!/usr/bin/env python

from reportlab_fb import ReportlabFB, FBFlowable

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

from reportlab.platypus import Spacer, BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.flowables import Flowable

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'))

class CText(Flowable):
    def __init__(self, width, height, note='', string=''):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.note = note
        self.string = string

    def draw(self):
        #draw border
        #self.canv.rect(0, 0, self.width, self.height)
        #centre the text
        font = 'DejaVuSans'
        #font = 'Helvetica'
        g = 0
        color = Color(g,g,g)
        self.canv.setFillColor(color)
        self.canv.setStrokeColor(color)
        self.canv.setFont(font, 72)
        self.canv.drawCentredString(0.5*self.width, 0.45*self.height, self.note)
        self.canv.setFont(font, 24)
        self.canv.drawCentredString(0.5*self.width, 0.3*self.height, self.string)

          

#create the basic page and frames
doc = BaseDocTemplate('flashcards.pdf', pagesize=landscape(letter), leftMargin=0, bottomMargin=0, topMargin=0, rightMargin=0)
margin = 0.25 * inch
frameCount = 2
frameWidth = (doc.width / frameCount) - (2.0 * margin)
frameHeight = doc.height
frames = []
#construct a frame for each column
for frame in range(frameCount):
    leftMargin = margin + frame * (frameWidth + (2.0 * margin))
    column = Frame(leftMargin, doc.bottomMargin, frameWidth, frameHeight, topPadding=0, bottomPadding=0, rightPadding=0, leftPadding=0)
    frames.append(column)

template = PageTemplate(frames=frames)
doc.addPageTemplates(template) 


fbfc = ReportlabFB(None, inch)
fbfc.u_height = 1
fbfc.u_width = (frameWidth/inch) * 0.98
fbfc.do_fret_markers = True
fbfc.numbered_frets = []
g = 0
fbfc.base_color = (g,g,g,1)

def add_string(l,s):
    return [(x[0],s+' String',x[1],x[2]) for x in l]

sharp = u"\u266F" 
flat = u"\u266D"

def add_accidental(n):
    n = unicode(n)
    notes = u'ABCDEFGA'
    start = n[0]
    next = notes[notes.index(start)+1]
    return start + sharp + u'/'+ next + flat + n[1]
    
def add_accidentals(strings):
    for x in strings:
        yield x
        n, s, sn, f = x
        if n[0] not in ('E','B') and f < 17:
            yield (add_accidental(n),s,sn,f+1)
    

string6 = [('E2',6,0),('F2',6,1),('G2',6,3),('A2',6,5),('B2',6,7),('C3',6,8),('D3',6,10),('E3',6,12),('F3',6,13),('G3',6,15),('A3',6,17)]
string5 = [('A2',5,0),('B2',5,2),('C3',5,3),('D3',5,5),('E3',5,7),('F3',5,8),('G3',5,10),('A3',5,12),('B3',5,14),('C4',5,15),('D4',5,17)]
string4 = [('D3',4,0),('E3',4,2),('F3',4,3),('G3',4,5),('A3',4,7),('B3',4,9),('C4',4,10),('D4',4,12),('E4',4,14),('F4',4,15),('G4',4,17)]
string3 = [('G3',3,0),('A3',3,2),('B3',3,4),('C4',3,5),('D4',3,7),('E4',3,9),('F4',3,10),('G4',3,12),('A4',3,14),('B4',3,16),('C5',3,17)]
string2 = [('B3',2,0),('C4',2,1),('D4',2,3),('E4',2,5),('F4',2,6),('G4',2,8),('A4',2,10),('B4',2,12),('C5',2,13),('D5',2,15),('E5',2,17)]
string1 = [('E4',1,0),('F4',1,1),('G4',1,3),('A4',1,5),('B4',1,7),('C5',1,8),('D5',1,10),('E5',1,12),('F5',1,13),('G5',1,15),('A5',1,17)]

strings = add_string(string6,'6th') + add_string(string5,'5th') + add_string(string4,'4th') + add_string(string3,'3rd') + add_string(string2,'2nd') + add_string(string1,'1st')

strings = add_accidentals(strings)

names = []
notes = []
for x in strings:
    names.append(CText(frameWidth,2.833*inch,x[0],x[1]))

    notes.extend([Spacer(5*inch,0.75*inch),FBFlowable(fbfc,[(x[2],x[3],'',0)],label=''),Spacer(5*inch,0.75*inch)])

story = []
while names:
    these_notes = notes[:3*6]
    notes = notes[3*6:]
    these_names = names[:6]
    names = names[6:]

    #account for fewer than 6 cards left    
    if not names:
        num_blanks = 6 - len(these_names)
        these_names += [Spacer(5*inch,2.833*inch)] * num_blanks
        these_notes += [Spacer(5*inch,0.75*inch),Spacer(5*inch,1*inch),Spacer(5*inch,0.75*inch)] * num_blanks
    
    story.extend(these_notes)
    story.extend(these_names[3:])
    story.extend(these_names[:3])

    
doc.build(story)
