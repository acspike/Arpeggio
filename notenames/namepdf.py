#!/usr/bin/env python

import notepdf

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

         
def make_page(clef, note):
    #create the basic page and frames
    doc = BaseDocTemplate('name_'+clef+note+'.pdf', pagesize=(4.25*inch,2.75*inch), leftMargin=0, bottomMargin=0, topMargin=0, rightMargin=0)
    margin = 0.25 * inch
    frameCount = 1
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
    
    story = [CText(frameWidth,2.75*inch,note.upper(),clef + ' clef')]
    doc.build(story)

def make_pdfscript(clef, start_note, start_octave, end_note, end_octave):
    for note, octave_number in notepdf.note_range(start_note, start_octave, end_note, end_octave):
        make_page(clef, note+str(octave_number))
        
        
        
if __name__ == "__main__":
    make_pdfscript('treble', "e",2,"e",7)
    make_pdfscript('bass', "b",0,"g",5)
