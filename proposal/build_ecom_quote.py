import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

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
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14.5, leading=19, textColor=BLUE, spaceBefore=12, spaceAfter=6)
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
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def m(x):
    return f"TT${x:,.2f}".replace(".00", "")



PRICE = 16000
CARE = 600
DEP = PRICE * 0.30
BAL = PRICE - DEP
FEE = round(BAL * 0.05, 2)
T3 = BAL + FEE
M3 = round(T3 / 3, 2)
MS = round(PRICE / 3, 2)
MS_LAST = round(PRICE - 2 * MS, 2)

summary = Table([[
    [Paragraph("PROJECT FEE", lab), Paragraph(m(PRICE), big), Paragraph("or 2 phases: TT$10,500 + TT$5,500", lab)],
    [Paragraph("CARE PLAN (RECOMMENDED)", lab), Paragraph(f"{m(CARE)}<font size='11'> /month</font>", big)],
    [Paragraph("QUOTE VALID UNTIL", lab), Paragraph("12 November 2026", ParagraphStyle("d", parent=body, fontSize=11, leading=24, fontName="Helvetica-Bold")), Paragraph("Issued 13 October 2026", lab)],
]], colWidths=[2.35 * inch, 2.35 * inch, 2.1 * inch])
summary.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
    ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ("LINEAFTER", (0, 0), (1, 0), 0.5, LINE),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))

W3 = [1.75 * inch, 3.95 * inch, 1.1 * inch]
W4 = [1.6 * inch, 3.3 * inch, 1.9 * inch]

story = [
    Paragraph("Your E-commerce Quote", title),
    Spacer(1, 4),
    Paragraph("Online boutique, admin dashboard and in-store point of sale", sub),
    Paragraph("Prepared for: ______________________________", sub),
    Spacer(1, 14),
    summary,

    Paragraph("1. What's Included", h2),
    Paragraph("A custom system designed in your brand colours, built for both your online boutique and your physical store. Your website and your shop use <b>one shared stock count</b>, so a sale in either place updates the other automatically.", body),
    table([
        ["Part", "What You Get", "Price"],
        ["Online Store", "Brand design based on your demo • product pages with size and colour options • shopping cart • secure card checkout through WiPay • delivery and pickup options • order confirmation emails • mobile friendly", m(6500)],
        ["Admin Dashboard", "Secure login for you and your staff • products with sizes, colours and individual SKUs • stock tracking for every variation • low-stock alerts • order management with status updates (e.g. paid, packed, out for delivery, collected) • discount codes and sale prices • sales reports (sales by day/month, best sellers, stock value)", m(6000)],
        ["In-Store Point of Sale", "Ring up walk-in sales on a tablet or phone • search or scan products • record cash, card or transfer payments • apply discounts • stock syncs instantly with the online store • daily sales summary", m(2500)],
        ["Setup &amp; Training", "Domain and email setup • loading up to 50 products with all variations • 2 training sessions • a simple how-to guide for you and your staff", m(1000)],
        ["Total", "", f"<b>{m(PRICE)}</b>"],
    ], W3, NAVY),

    KeepTogether([Paragraph("2. Option: Build in Two Phases", h2),
    Paragraph("If you would like to spread the cost, we can launch your online boutique first and add the in-store system when your physical store is ready. The total price stays the same.", body),
    table([
        ["Phase", "Includes", "Price"],
        ["Phase 1: Online Boutique", "Online store, admin dashboard (products, stock, low-stock alerts, orders, discount codes, basic sales reports), setup and training", m(10500)],
        ["Phase 2: Physical Store", "In-store point of sale, stock sync between store and website, combined in-store and online sales reports, staff training", m(5500)],
    ], W3, BLUE),
    Paragraph("Phase 2 can start any time after Phase 1 launches, at this price for up to 6 months from this quote.", note)]),

    Paragraph("3. Your Payment Options", h2),
    Paragraph("Choose whichever option suits your budget. The 3-Month Plan includes a 5% plan fee on the balance after your deposit; the other options have no extra fees. If you choose two phases, each phase is paid 50% to start and 50% before its launch.", body),
    table([
        ["Option", "What You Pay", "Total"],
        ["Standard (50 / 50)", f"{m(PRICE/2)} to start<br/>{m(PRICE/2)} before launch", m(PRICE)],
        ["Milestone Split", f"{m(MS)} to start<br/>{m(MS)} when you approve the design<br/>{m(MS_LAST)} before launch", m(PRICE)],
        ["3-Month Plan", f"{m(DEP)} to start<br/>then 3 monthly payments of {m(M3)} from launch", f"{m(DEP + T3)}<br/><font color='#5a6472'>includes {m(FEE)} plan fee</font>"],
    ], W4, NAVY),

    KeepTogether([
        Paragraph(f"4. Monthly Care Plan (Recommended): {m(CARE)}/month", h2),
        Paragraph("Because your store handles payments, stock and customer orders, regular care keeps it secure and running smoothly. The care plan is <b>separate from your project payments</b>, starts at launch, and you can stop it at any time.", body),
        table([
            ["", f"With the Care Plan ({m(CARE)}/month)", "Without the Care Plan"],
            ["Security &amp; backups", "Security updates, daily backups and uptime monitoring", "Not included"],
            ["Fixing problems", "Covered", "From TT$250 per fix"],
            ["Changes &amp; help", "Up to 2 hours of changes each month (new features, banners, promotions, page edits) and WhatsApp support", "TT$200 per hour"],
        ], [1.5 * inch, 2.65 * inch, 2.65 * inch], BLUE),
        Spacer(1, 6),
        Paragraph("• <b>Stop any time:</b> your store stays online and stays yours. Only the maintenance stops.", bullet),
        Paragraph(f"• <b>Save 10%:</b> pay for a year of care up front and pay {m(CARE * 12 * 0.9)} instead of {m(CARE * 12)}.", bullet),
    ]),

    KeepTogether([
        Paragraph("5. Running Costs (Paid Directly by You)", h2),
        Paragraph("These accounts are set up in <b>your name</b>, so you own them.", body),
        table([
            ["Item", "Details", "Cost"],
            ["Domain name", "Your web address, e.g. yourboutique.com", "About TT$75/year"],
            ["Hosting &amp; database", "Free to start; a paid plan is only needed as your store grows", "TT$0 to about TT$175/month"],
            ["Online card payments", "WiPay processing fee on each online sale", "Per transaction"],
            ["In-store card payments", "Use your existing bank card machine; the sale is recorded in the point of sale", "Your bank's fees"],
        ], [1.6 * inch, 3.6 * inch, 1.6 * inch], NAVY),
    ]),

    KeepTogether([
        Paragraph("6. Timeline: 4 to 6 Weeks", h2),
        table([
            ["Week", "What Happens"],
            ["Week 1", "Final design approved, accounts set up, product list collected"],
            ["Weeks 2 to 3", "Online store and admin dashboard built; you review progress"],
            ["Week 4", "Point of sale built and connected to stock"],
            ["Weeks 5 to 6", "Products loaded, full testing (orders, payments, stock, discounts), training, launch"],
        ], [1.6 * inch, 5.2 * inch], BLUE),
        Paragraph("The timeline starts once the first payment and your product information are received.", note),
    ]),

    KeepTogether([
        Paragraph("7. What You Need to Do", h2),
        Paragraph("• <b>Choose</b> the full build or two phases, and your payment option.", bullet),
        Paragraph("• <b>Pay your first payment</b> when you are ready to go ahead. Nothing is due until then. Payment is accepted by bank transfer, WiPay or Fygaro.", bullet),
        Paragraph("• <b>Send your product list:</b> names, prices, sizes, colours, current stock and photos (a simple spreadsheet template will be provided).", bullet),
        Paragraph("• <b>Set up a WiPay merchant account</b> for online payments (we will guide you through it).", bullet),
        Paragraph("• <b>Review and approve</b> the design and a test order before launch.", bullet),
    ]),

    Paragraph("Good to Know", h3),
    Paragraph("• Up to 50 products are loaded for you. Extra products are TT$30 each, or you can add them yourself in the dashboard.", bullet),
    Paragraph("• Features not listed in this quote (for example a customer loyalty programme or a mobile app) can be quoted separately.", bullet),
    Paragraph("• You may pay off the balance early at any time. On the 3-Month Plan, paying early removes the unused part of the plan fee.", bullet),
    Paragraph("• Full ownership of the website and its files transfers to you once the project fee is paid in full.", bullet),
    Paragraph("• If a payment is more than 14 days late we will contact you; after 30 days the store may be paused until the account is up to date.", bullet),
    Spacer(1, 6),
    Paragraph("This quote was issued on 13 October 2026 and its prices are held until 12 November 2026. No payment is due until you decide to go ahead. All amounts are in Trinidad and Tobago dollars (TTD).", note),
]

doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                        topMargin=0.7 * inch, bottomMargin=0.7 * inch, title="Your E-commerce Quote")
doc.build(story)
