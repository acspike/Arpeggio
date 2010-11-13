from reportlab.lib.units import inch
from reportlab.lib.colors import Color
from reportlab.graphics.charts.textlabels import _text2Path

from reportlab.platypus.flowables import Flowable

from base_fb import BaseFB

def _bit(val):
    if val:
        return 1
    else:
        return 0

def text_extents(text, face, size):
    p = _text2Path(text, 0, 0, face, size)
    return p.getBounds()

class ReportlabFB(BaseFB):
    def __init__(self, context, unit=inch):
        BaseFB.__init__(self, context, -1, unit)
    def _set_color(self, color='base'):
        if color == 'top':
            r,g,b,a = self.top_color
        else:
            r,g,b,a = self.base_color
        rlcolor = Color(r,g,b)
        self.c.setFillColor(rlcolor)
        self.c.setStrokeColor(rlcolor)

    def _nut_line(self, x1, y1, x2, y2):
        self.c.saveState()
        self._set_color()
        self.c.setLineCap(1)
        self.c.setLineWidth(4)
        self.c.line(x1, y1, x2, y2)
        self.c.restoreState()
    def _line(self, x1, y1, x2, y2):
        self.c.saveState()
        self._set_color()
        self.c.line(x1, y1, x2, y2)
        self.c.restoreState()
    def _circle(self, x, y, size, filled = True):
        self.c.saveState()
        self._set_color()
        m = 0.5 * size
        self.c.ellipse(x - m, y + m, x + m, y - m, _bit(not filled), _bit(filled))
        self.c.restoreState()
    def _text(self, x, y, text, size, color='top', center_x=True, center_y=False):
        FACE = 'Helvetica'
        self.c.saveState()
        self._set_color(color)
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

class FBFlowable(Flowable):
    def __init__(self, fb, dots=[], label='', labelFont=('Helvetica',12), labelpos='side'):
        self.fb = fb
        self.dots = dots
        self.label = label
        self.labelFont = labelFont
        self.labelpos = labelpos
    def wrap(self, *args, **kwargs):
        w = self.fb.width
        h = self.fb.fullheight
        if self.label and self.labelpos!='side':
            h += self.labelFont[1] * 1.5
        else:
            w += self.labelFont[1]
        return (w, h)
    def split(self, *args, **kwargs):
        return []
    def draw(self):
        self.fb.draw(0, 0, dots=self.dots, context=self.canv)
        self.canv.setFont(*self.labelFont)
        if self.label and self.labelpos!='side':
            try:
                left = self.fb.fret_separation * int(self.labelpos)
            except:
                left = 0
            top = self.fb.fullheight + (self.labelFont[1] * 0.5)
            self.canv.drawString(left, top, self.label)
        else:
            self.canv.rotate(90)
            self.canv.drawCentredString(0+((self.fb.top+self.fb.bottom)/2.0), 0, self.label)
    def drawOn(self, *args, **kwargs):
        #print args, kwargs
        canv, x, y = args
        #canv.rect(x,y, self.fb.width, self.fb.fullheight)
        Flowable.drawOn(self, *args, **kwargs)
