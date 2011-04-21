#!/usr/bin/env python

from reportlab.lib.units import inch,mm
import pyPdf
import notepdf
import itertools

def translate_pdf_page(page, delta_x, delta_y):
    content = pyPdf.pdf.ContentStream(page["/Contents"].getObject(), page.pdf)
    content.operations.insert(0, [[], '1 0 0 1 %s %s cm' % (delta_x,delta_y)] )
    page[pyPdf.generic.NameObject('/Contents')] = content


w = 4.25*inch
h = 2.75*inch

#ugly hack: duplicate the first card on each page off the page to fix font handling
offsets = [(-1*w,-1*h)] + [(w*x,h*y) for y in range(4) for x in [0,1]]
offsets2 = [(-1*w,-1*h)] + [(w*x,h*y) for y in range(4) for x in [1,0]]


def make_pdfscript(clef, start_note, start_octave, end_note, end_octave):
    notes = [clef+x[0]+str(x[1]) for x in notepdf.note_range(start_note, start_octave, end_note, end_octave)]
    output = pyPdf.pdf.PdfFileWriter()
    
    pages = []
    subpages=[]
    while notes:
        group = notes[:8]
        group = [group[0]] + group
        notes = notes[8:]
        
        
        pages.append(pyPdf.pdf.PdfFileReader(file("pdfs/letter.pdf","rb")).getPage(0))
        for name, (x,y) in zip(group,offsets2):
            subpages.append(pyPdf.pdf.PdfFileReader(file("pdfs/name_"+name+".pdf","rb")).getPage(0))
            translate_pdf_page(subpages[-1], x, y)
            pages[-1].mergePage(subpages[-1])
        output.addPage(pages[-1])
                
        pages.append(pyPdf.pdf.PdfFileReader(file("pdfs/letter.pdf","rb")).getPage(0))
        for name, (x,y) in zip(group,offsets):
            subpages.append(pyPdf.pdf.PdfFileReader(file("pdfs/"+name+".pdf","rb")).getPage(0))
            translate_pdf_page(subpages[-1], x, y)
            pages[-1].mergePage(subpages[-1])
        output.addPage(pages[-1])
        

            
    
    outputStream = file(clef+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    


if __name__ == "__main__":
    make_pdfscript('treble', "e",2,"e",7)
    make_pdfscript('bass', "b",0,"g",5)
