import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, PageBreak, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

OUT = sys.argv[1]

NAVY = colors.HexColor("#1c3359")
BLUE = colors.HexColor("#2f6db5")
INK = colors.HexColor("#2b3340")
GREY = colors.HexColor("#5a6472")
LINE = colors.HexColor("#c9d3e0")
ALT = colors.HexColor("#f5f8fc")
SOFT = colors.HexColor("#eaf1fa")

title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=NAVY)
sub = ParagraphStyle("s", fontName="Helvetica", fontSize=11, leading=15, textColor=GREY)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14.5, leading=19, textColor=BLUE, spaceBefore=16, spaceAfter=8)
h3 = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=INK, spaceBefore=10, spaceAfter=5)
body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, spaceAfter=6)
bullet = ParagraphStyle("bl", parent=body, leftIndent=14, spaceAfter=5)
cell = ParagraphStyle("c", fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK)
cellb = ParagraphStyle("cb", parent=cell, fontName="Helvetica-Bold")
headc = ParagraphStyle("hc", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
note = ParagraphStyle("n", parent=body, fontSize=8.5, leading=12, textColor=GREY)
big = ParagraphStyle("big", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=NAVY)
lab = ParagraphStyle("lab", fontName="Helvetica", fontSize=8.5, leading=11, textColor=GREY)


def table(rows, widths, head_bg):
    data = [[Paragraph(c, headc) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(r[0], cellb)] + [Paragraph(c, cell) for c in r[1:]])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), head_bg),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT]),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def m(x):
    return f"TT${x:,.2f}".replace(".00", "")



sig=ParagraphStyle("sig",parent=body,fontSize=9.5,leading=14)
def m(x): return f"TT${x:,.2f}".replace(".00","")
PRICE=1200; HALF=PRICE/2

summary = Table([[
    [Paragraph("TOTAL PRICE", lab), Paragraph(m(PRICE), big)],
    [Paragraph("PAY IN TWO PARTS", lab), Paragraph(f"{m(HALF)}<font size='11'> + {m(HALF)}</font>", big)],
    [Paragraph("QUOTE VALID UNTIL", lab), Paragraph("28 October 2026", ParagraphStyle("d", parent=body, fontSize=11, leading=24, fontName="Helvetica-Bold")), Paragraph("Issued 14 October 2026", lab)],
]], colWidths=[2.2*inch,2.4*inch,2.2*inch])
summary.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SOFT),("BOX",(0,0),(-1,-1),0.5,LINE),("LINEAFTER",(0,0),(1,0),0.5,LINE),
  ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),12),("LEFTPADDING",(0,0),(-1,-1),12),("VALIGN",(0,0),(-1,-1),"TOP")]))

def line(label):
    t=Table([[Paragraph(label,sig),""]],colWidths=[0.95*inch,2.35*inch],rowHeights=[30])
    t.setStyle(TableStyle([("LINEBELOW",(1,0),(1,0),0.7,INK),("VALIGN",(0,0),(-1,-1),"BOTTOM")]))
    return t

story=[
 Paragraph("Fygaro Setup Quote &amp; Service Agreement",title),
 Spacer(1,4),
 Paragraph("Prepared by Portside Digital for: ______________________________",sub),
 Spacer(1,14), summary,

 Paragraph("1. What You Get",h2),
 table([
  ["Service","What is included"],
  ["Fygaro account setup","Helping you create and submit your Fygaro merchant account in your own name, and setting up your business details, branding and the ways customers will pay you (such as payment links or buttons, as available on your Fygaro plan)"],
  ["Testing","A real test payment to confirm everything works and the money reaches the account you chose"],
  ["Training","A hands-on session showing you how to manage Fygaro yourself: receive and check payments, create payment requests, read your records, and see when your money is paid out to your bank"],
  ["Follow-up help","Questions about your setup answered by WhatsApp for 7 days after completion"],
 ],[1.7*inch,5.1*inch],NAVY),

 Paragraph("2. Payment",h2),
 table([
  ["Payment","When","Amount"],
  ["Part 1: start","Before work begins. This reserves your place.",m(HALF)],
  ["Part 2: completion","When setup, the test payment and the training are finished.",m(HALF)],
  ["Total","",f"<b>{m(PRICE)}</b>"],
 ],[1.7*inch,3.9*inch,1.2*inch],BLUE),
 Paragraph("Payment can be made in cash or by bank transfer. A receipt is given for every payment.",note),

 PageBreak(),
 Paragraph("3. Agreement",h2),
 Paragraph("By signing below, both parties agree to the following.",body),
 Paragraph("<b>1. Services.</b> Portside Digital will carry out the services in Section 1 for the price in Section 2.",bullet),
 Paragraph("<b>2. Completion.</b> The work is complete when your Fygaro account is set up, a test payment has worked, and the training session has been given.",bullet),
 Paragraph("<b>3. Your account is yours.</b> The Fygaro account is opened in your name and you control the login. Portside Digital will not keep your passwords after handover and cannot access your money.",bullet),
 Paragraph("<b>4. What you provide.</b> You will give accurate information and any documents Fygaro asks for (such as ID and business details) and attend the training session.",bullet),
 Paragraph("<b>5. Fygaro's decisions and fees.</b> Fygaro decides whether to approve an account and how long approval takes. Fygaro's fees are separate from this price and are paid by you. Portside Digital cannot guarantee approval. If Fygaro does not approve your account after we have completed our work, Part 1 is not refundable; no further payment is due and we will help you apply again where possible.",bullet),
 Paragraph("<b>6. Timing.</b> Work starts when Part 1 is received. Setup time depends on how quickly you provide your information and how quickly Fygaro responds.",bullet),
 Paragraph("<b>7. Extra work.</b> Anything not listed in Section 1, such as building a website or online shop, will be quoted separately before any work is done.",bullet),
 Paragraph("<b>8. Cancellation.</b> You may cancel at any time before work begins and Part 1 will be returned. After work has begun, Part 1 covers the work already done.",bullet),
 Paragraph("<b>9. Privacy.</b> Your information is used only to complete this work and is kept confidential.",bullet),
 Paragraph("<b>10. Law.</b> This agreement is governed by the laws of Trinidad and Tobago.",bullet),
 Spacer(1,8),
 KeepTogether([
  Paragraph("Signatures",h2),
  Table([[ [Paragraph("<b>Client</b>",sig),line("Full name:"),line("Signature:"),line("Date:"),line("Phone:")],
           [Paragraph("<b>Portside Digital</b>",sig),line("Name:"),line("Signature:"),line("Date:")] ]],
        colWidths=[3.5*inch,3.4*inch],style=TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("RIGHTPADDING",(0,0),(0,0),14)])),
  Spacer(1,8),
  Paragraph("Payment received:  Part 1 ____________ (date) ______ (TT$600)     Part 2 ____________ (date) ______ (TT$600)",note),
  Paragraph("Issued 14 October 2026. Prices are held until 28 October 2026. All amounts are in Trinidad and Tobago dollars (TTD). WhatsApp: 868-259-1409.",note),
 ]),
]
doc=SimpleDocTemplate(OUT,pagesize=letter,leftMargin=0.75*inch,rightMargin=0.75*inch,topMargin=0.6*inch,bottomMargin=0.6*inch,title="Fygaro Setup Quote and Service Agreement")
doc.build(story)
