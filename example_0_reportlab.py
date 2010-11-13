#!/usr/bin/env python

from reportlab_fb import ReportlabFB

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
WIDTH, HEIGHT = letter

c = canvas.Canvas('example_0_reportlab.pdf',pagesize=letter)

fb = ReportlabFB(c, inch)

dots = [
    (1,3,'1',0),
    (2,3,'2',0),
    (3,3,'3',0),
    (4,3,'4',0),
    (5,7,'g',0),
    (4,4,'R',0),
    (5,3,'X',1)
    ]

x = inch * 0.75
y = HEIGHT - (inch * (fb.u_height + 0.75))
fb.draw(x, y, dots)

c.showPage()
c.save()
