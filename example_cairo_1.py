#!/usr/bin/env python

from cairo_fb import CairoFB
from arpeggio_arrays import *

import cairo
inch = 72.0
letter = (612.0, 792.0)
WIDTH, HEIGHT = letter

def chart_page(ctx, dots, color=(0,0,0,1)):
    fb = CairoFB(ctx, inch)
    fb.base_color = color

    x = inch * 0.75
    y = inch * 0.75
    for i in range(len(dots)):
        fb.draw(x, y + (i * (2 * inch)), dots[i])

    ctx.show_page()

surface = cairo.PDFSurface('example_cairo_1.pdf', WIDTH, HEIGHT)
ctx = cairo.Context(surface)
chart_page(ctx, major_dots)
chart_page(ctx, minor_dots)
chart_page(ctx, thirteenth)
chart_page(ctx, flying)
surface.finish()
