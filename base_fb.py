
class BaseFB(object):
    def __init__(self, context, vertical, unit):
        self.c = context
        self.v = vertical
        self.u = unit
        
        self.u_width = 7.0
        self.u_height = 1.5
        self.u_to_top = 0.0
        self.num_frets = 18.0
        self.num_strings = 6.0
        
        self.current_abs_top = 0.0
        self.current_left = 0.0

        self.numbered_frets = [3,5,7,9,12,15,17]

        self.base_color = (0,0,0,1)
        self.top_color = (1,1,1,1)
        
        self.do_fret_markers = False

    def _top(self):
        return self.current_abs_top + (self.u * self.u_to_top)
    top = property(_top)
    def _height(self):
        return self.u * self.u_height
    height = property(_height)
    def _fullheight(self):
        return self.height + 1.5 * self.ring_size
    fullheight = property(_fullheight)
    def _width(self):
        return self.u * self.u_width
    width = property(_width)
    def _string_separation(self):
        return self.height / (self.num_strings - 1)
    string_separation = property(_string_separation)
    def _fret_separation(self):
        return self.width / self.num_frets
    fret_separation = property(_fret_separation)
    def _bottom(self):
        return self.top + (self.v * self.height)
    bottom = property(_bottom)
    def _right(self):
        return self.current_left + self.width
    right = property(_right)
    def _dot_size(self):
        return self.string_separation * 0.7
    dot_size = property(_dot_size)
    def _ring_size(self):
        return self.string_separation * 0.9
    ring_size = property(_ring_size)
    def _fret_number_size(self):
        return 0.5 * self.dot_size
    fret_number_size = property(_fret_number_size)
    def _fret_to_x(self, f):
        return (self.current_left + self.fret_separation) + (f * self.fret_separation)
    def _string_to_y(self, s):
        return self.top + (self.v * s * self.string_separation)
    
    def _nut_line(self, x1, y1, x2, y2):
        raise NotImplementedError
    def _line(self, x1, y1, x2, y2):
        raise NotImplementedError
    def _circle(self, x, y, size, filled = True):
        raise NotImplementedError
    def _text(self, x, y, text, size, color='top', center_x=True, center_y=False):
        raise NotImplementedError
        
    def _dot(self, x, y, label='', with_ring=False):
        x = x - (0.5 * self.fret_separation)
        self._circle(x, y, self.dot_size)
        if with_ring:
            self._circle(x, y, self.ring_size, False)
        if label:
            self._text(x, y, label, 0.8 * self.dot_size, 'top', True, True)
    
    def draw(self, x, y, dots=[], context=None):
        if context:
            self.c = context
        self.current_left = x
        self.current_abs_top = y
        if self.v < 0:
            self.current_abs_top += (self.fullheight - (0.5 * self.ring_size))
        
        # string lines
        for i in range(int(self.num_strings)):
            self._line(self.current_left+self.fret_separation, self._string_to_y(i), self.right, self._string_to_y(i))
        
        # fret lines
        self._nut_line(self._fret_to_x(0), self.top, self._fret_to_x(0), self.bottom)
        for i in range(1, int(self.num_frets)):
            self._line(self._fret_to_x(i), self.top, self._fret_to_x(i), self.bottom)
        
        #fret markers
        if self.do_fret_markers:
            for i in [3,5,7,9,15,17]:
                x = self._fret_to_x(i) - (0.5 * self.fret_separation)
                y = (self._string_to_y(0) + self._string_to_y(int(self.num_strings) - 1))/2.0
                self._circle(x, y, self.dot_size, False)
            for i in [12]:
                x = self._fret_to_x(i) - (0.5 * self.fret_separation)
                first = self._string_to_y(0)
                last = self._string_to_y(int(self.num_strings) - 1)
                base = min(first, last)
                spread = max(first, last) - base
                spacing = spread / 10.0
                y1 = base + (spacing * 3)
                y2 = base + (spacing * 7)
                self._circle(x, y1, self.dot_size, False)
                self._circle(x, y2, self.dot_size, False)
        
        for d in dots:
            string_num, fret_num, label, with_ring = d
            self._dot(self._fret_to_x(fret_num), self._string_to_y(string_num-1), label=label, with_ring=with_ring)

        for x in self.numbered_frets:
            self._text(self._fret_to_x(x), self.bottom + (self.v * 1.5 * self.fret_number_size), str(x), self.fret_number_size, 'base', True, False)
