from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.graphics.charts.textlabels import _text2Path

from reportlab.platypus.flowables import Flowable

'''
TODO:
test flowable
add x margin to allow for black keys on the sides
allow differnt span of keys
allow multi octave spans
write text on keys
'''

def _bit(val):
    if val:
        return 1
    else:
        return 0

def text_extents(text, face, size):
    p = _text2Path(text, 0, 0, face, size)
    return p.getBounds()

black = Color(0,0,0)
gray = Color(.5,.5,.5)
white = Color(1,1,1)

# 32nds
white_key = 27
spacings = 2
black_key = 13
d_gap = 17
ag_gap = 15.75
black_key_offsets = [None, -2.5, 2.5, None, -3.75, 0, 3.75]
def bkoffset(index):
    return black_key_offsets[index % 7]


class ReportlabKB(object):
    def __init__(self, context, unit):
        self.c = context
        self.u = unit
        self.width = 3 * unit
        self.height = 2 * unit
        self.x_rate = self.width / ((white_key * 7) + (spacings * 8))
        
    def _text(self, x, y, text, size, center_x=True, center_y=False):
        FACE = 'Helvetica'
        self.c.saveState()
        self.c.setFillColor(gray)
        self.c.setStrokeColor(gray)
        self.c.setFont(FACE, size)
        
        x1,y1,x2,y2 = text_extents(text, FACE, size)
        height = y2 - y1
        mid = y2 - (0.5 * height)
        
        if center_y:
            ny = mid
        else:
            ny = 0.0
        if center_x:
            self.c.drawCentredString(x, (y - ny), text)
        else:
            self.c.drawString(x, (y - ny), text)
        self.c.restoreState()
    
    def draw(self, xoffset, yoffset, context=None):
        if context:
            self.c = context
        self.c.saveState()
        self.c.setFillColor(white)
        self.c.setStrokeColor(black)
        self.c.setLineWidth(spacings)
        for k in range(7):
            x = (((spacings/2.0) + (k * (white_key + spacings))) * self.x_rate)
            self.c.rect(xoffset + x, yoffset, self.x_rate * (white_key + spacings), self.height)
        self.c.setFillColor(black)
        for k in range(7):
            if black_key_offsets[k] is not None:
                x = (((spacings/2.0) + (k * (white_key + spacings))) - ((spacings/2.0) + (black_key/2.0)) + black_key_offsets[k]) * self.x_rate
                self.c.rect(xoffset + x, yoffset + (self.height*2.0/5.0), self.x_rate * (black_key + spacings), self.height*3.0/5.0, 1, 1)
        self.c.restoreState()
        
class KBFlowable(Flowable):
    def __init__(self, kb):
        self.kb = kb
    def wrap(self, *args, **kwargs):
        w = self.kb.width
        h = self.kb.height
        return (w, h)
    def split(self, *args, **kwargs):
        return []
    def draw(self):
        self.kb.draw(0, 0, context=self.canv)
    def drawOn(self, *args, **kwargs):
        #print args, kwargs
        canv, x, y = args
        #canv.rect(x,y, self.fb.width, self.fb.fullheight)
        Flowable.drawOn(self, *args, **kwargs)


if __name__=='__main__':
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    WIDTH, HEIGHT = letter

    c = canvas.Canvas('example_6_reportlab.pdf',pagesize=letter)

    kb = ReportlabKB(c, inch)
    kb.draw()

    c.showPage()
    c.save()
