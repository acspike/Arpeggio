#!/usr/bin/env python

from reportlab_fb import ReportlabFB
from arpeggio_arrays import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
WIDTH, HEIGHT = letter

def chart_page(ctx, dots, color=(0,0,0,1)):
    fb = ReportlabFB(ctx, inch)
    fb.base_color = color

    x = inch * 0.75
    y = HEIGHT - (inch * (fb.u_height + 0.75))
    for i in range(len(dots)):
        fb.draw(x, y + (fb.v * i * (2 * inch)), dots[i])

    ctx.showPage()


ctx = canvas.Canvas('example_1_reportlab.pdf',pagesize=letter)

chart_page(ctx, major_dots)
chart_page(ctx, minor_dots)

chart_page(ctx, thirteenth)
chart_page(ctx, flying)

ctx.save()
