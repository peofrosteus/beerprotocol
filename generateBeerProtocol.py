# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# Beer-data
beers = [
    {"namn": "Fjäderholmarnas Hazy IPA", "typ": "IPA", "description": "Humlearomatisk smak med tydlig beska, inslag av grapefrukt, tallbarr, ljust bröd, ananas och örter."},
    {"namn": "Skärpning på alla plan", "typ": "Pilsner", "description": "Maltig smak med tydlig beska, inslag av knäckebröd, timjan, honung och citrusskal."},
    {"namn": "Sleipnir II", "typ": "Pale Ale", "description": "Maltig smak med tydlig beska, inslag av sirapslimpa, knäck, aprikos och apelsin."},
    {"namn": "Oden", "typ": "Lager", "description": "Maltig smak med tydlig beska, inslag av ljust knäckebröd, timjan och citrusskal."},
    {"namn": "Golden Hoppies", "typ": "IPA", "description": "Fruktig smak med tydlig beska, inslag av passionsfrukt, ananas, honung, nektarin, rosmarin och grapefrukt."},
    {"namn": "C4", "typ": "Double IPA", "description": "Humlearomatisk smak med tydlig beska och liten sötma, inslag av mango, grapefrukt, honung, tallbarr och sockerkaka. "},
    {"namn": "Islay Whisky Cask Beer", "typ": "Amber Ale", "description": "Maltig, rökig smak med liten sötma och fatkaraktär, inslag av kavring, dadlar, tjära, mörk choklad, kanel, charkuterier och honung."},
    {"namn": "Dellinger", "typ": "IPA", "description": "Fruktig smak med tydlig beska och liten sötma, inslag av papaya, sirapslimpa, apelsinskal och aprikos."},
]

header_text = "Ölprotokoll 2025-04-26"

# PDF-inställningar
pdf_path = "beerProtocol.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
page_width, page_height = A4

# A6-dimensioner inom A4
a6_width = page_width / 2
a6_height = page_height / 2

# Koordinater för fyra A6-rutor per A4
positions = [
    (0, page_height / 2),
    (page_width / 2, page_height / 2),
    (0, 0),
    (page_width / 2, 0)
]

# Funktion för att rita en betygsrad med checkboxar
def draw_rating_row(c, label, x, y):
    box_size = 4 * mm
    spacing = 8 * mm
    offset = 70  # justerad position
    c.drawString(x, y, label)
    for i in range(5):
        c.rect(x + offset + i * spacing, y - 2, box_size, box_size)

# Rita en sektion i en A6-ruta
def draw_a6_section(c, x, y, beer):
    margin = 10 * mm
    start_x = x + margin
    start_y = y + a6_height - margin
    line_height = 6 * mm
    max_width = a6_width - 2 * margin

    c.rect(x, y, a6_width, a6_height)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(start_x, start_y, f"{beer['namn']}")
    c.setFont("Helvetica", 10)
    start_y -= line_height
    c.drawString(start_x, start_y, f"{beer['typ']}")

    start_y -= line_height * 1.5
    draw_rating_row(c, "Färg", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Klarhet", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Beska", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Sötma", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Fyllighet", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Betyg", start_x, start_y)

    start_y -= line_height * 2
    
    # Text wrapping for description
    description_lines = simpleSplit(beer['description'], c._fontname, c._fontsize, max_width)
    for line in description_lines:
        c.drawString(start_x, start_y, line)
        start_y -= line_height

    # Adjust the number of comment lines based on remaining space
    remaining_space = start_y - y - margin
    num_comment_lines = max(0, int(remaining_space / line_height))

    for _ in range(num_comment_lines):
        start_y -= line_height
        c.line(start_x, start_y, start_x + max_width, start_y)

# Rita alla öl, fyra per sida
for idx, beer in enumerate(beers):
    pos = positions[idx % 4]
    draw_a6_section(c, pos[0], pos[1], beer)
    if (idx + 1) % 4 == 0 and idx + 1 < len(beers):
        c.showPage()

c.save()
