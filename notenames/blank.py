from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

l8 = canvas.Canvas('letter8.pdf', pagesize=(4.25*inch,2.75*inch))
l = canvas.Canvas('letter.pdf', pagesize=letter)




l8.showPage()
l.showPage()





l8.save()
l.save()
