import cairo
import math
inch = 72.0
letter = (612.0, 792.0)

from base_fb import BaseFB

class CairoFB(BaseFB):
    def __init__(self, context, unit=inch):
        BaseFB.__init__(self, context, 1, unit)
    def _nut_line(self, x1, y1, x2, y2):
        self.c.save()
        self.c.set_source_rgba (*self.base_color)
        self.c.set_line_cap(cairo.LINE_CAP_ROUND)
        self.c.set_line_width(4)
        self.c.move_to(x1, y1)
        self.c.line_to(x2, y2)
        self.c.stroke()
    def _line(self, x1, y1, x2, y2):
        self.c.save()
        self.c.set_source_rgba (*self.base_color)
        self.c.set_line_cap(cairo.LINE_CAP_SQUARE)
        self.c.set_line_width(1)
        self.c.move_to(x1, y1)
        self.c.line_to(x2, y2)
        self.c.stroke()
        self.c.restore()
    def _circle(self, x, y, size, filled = True):
        self.c.new_sub_path()
        self.c.save()
        self.c.set_source_rgba (*self.base_color)
        self.c.translate (x, y)
        self.c.scale (size / 2.0, size / 2.0)
        self.c.arc (0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
        self.c.restore()
        self.c.set_line_width(1)
        if filled:
            self.c.fill()
        else:
            self.c.stroke()
    def _text(self, x, y, text, size, color='top', center_x=True, center_y=False):
        self.c.save()
        if color == 'top':
            self.c.set_source_rgba (*self.top_color)
        else:
            self.c.set_source_rgba (*self.base_color)
        self.c.select_font_face ("Sans",
                 cairo.FONT_SLANT_NORMAL,
                 cairo.FONT_WEIGHT_NORMAL)
        self.c.set_font_size(size)
        x_bearing, y_bearing, width, height, x_advance, y_advance = self.c.text_extents(text)
        if center_x:
            nx = (0.5 * x_advance)
        else:
            nx = 0
        if center_y:
            ny = (height / 2.0)
        else:
            ny = 0
        self.c.move_to(x - nx, y + ny)
        self.c.show_text(text)
        self.c.stroke()
        self.c.fill()
        self.c.restore()
