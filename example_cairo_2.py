#!/usr/bin/env python

from cairo_fb import CairoFB

import cairo
inch = 72.0
letter = (612.0, 792.0)
WIDTH, HEIGHT = letter


def chart_page(ctx, dots, color=(0,0,0,1)):
    fb = CairoFB(ctx, inch)
    fb.base_color = color
    fb.u_height = 1.0
    fb.u_width = 5.75

    x = inch * 1.5
    y = inch * 1.0
    for i in range(len(dots)):
        fb.draw(x, y + (i * (1.3 * inch)), dots[i])

    ctx.show_page()

surface = cairo.PDFSurface('example_cairo_2.pdf', WIDTH, HEIGHT)
ctx = cairo.Context(surface)
chart_page(ctx, [[]] * 7, (0.4,0.4,0.4,1))
chart_page(ctx, [[]] * 7, (0.4,0.4,0.4,1))
surface.finish()
