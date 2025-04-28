# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime

# Öl-data
beers = [
    {"namn": "Fjäderholmarnas Hazy IPA", "typ": "IPA", "brewery": "Fjärderholmarnas Bryggeri", "price": "0","description": "Humlearomatisk smak med tydlig beska, inslag av grapefrukt, tallbarr, ljust bröd, ananas och örter."},
    {"namn": "Skärpning på alla plan", "typ": "Pilsner", "brewery": "Fjärderholmarnas Bryggeri", "price": "0", "description": "Maltig smak med tydlig beska, inslag av knäckebröd, timjan, honung och citrusskal."},
    {"namn": "Sleipnir II", "typ": "Pale Ale", "brewery": "Keane Brewing", "price": "0", "description": "Maltig smak med tydlig beska, inslag av sirapslimpa, knäck, aprikos och apelsin."},
    {"namn": "Oden", "typ": "Lager", "brewery": "Keane Brewing", "price": "0", "description": "Maltig smak med tydlig beska, inslag av ljust knäckebröd, timjan och citrusskal."},
    {"namn": "Golden Hoppies", "typ": "IPA", "brewery": "Hop Notch Brewing", "price": "0", "description": "Fruktig smak med tydlig beska, inslag av passionsfrukt, ananas, honung, nektarin, rosmarin och grapefrukt."},
    {"namn": "C4", "typ": "Double IPA", "brewery": "Hop Notch Brewing", "price": "0", "description": "Humlearomatisk smak med tydlig beska och liten sötma, inslag av mango, grapefrukt, honung, tallbarr och sockerkaka."},
    {"namn": "Islay Whisky Cask Beer", "typ": "Amber Ale", "brewery": "Innis & Gunn", "price": "0", "description": "Maltig, rökig smak med liten sötma och fatkaraktär, inslag av kavring, dadlar, tjära, mörk choklad, kanel, charkuterier och honung."},
    {"namn": "Dellinger", "typ": "IPA", "brewery": "Keane Brewing", "price": "0", "description": "Fruktig smak med tydlig beska och liten sötma, inslag av papaya, sirapslimpa, apelsinskal och aprikos."}
]

# Rubrik och tidsstämpel
header_text = "Ölprovning 2025-04-26"
now = datetime.now()
currentTimestamp = now.strftime("%Y-%m-%d %H:%M:%S")

# PDF-inställningar
pdf_path = "beerProtocol_" + currentTimestamp + ".pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
page_width, page_height = A4

# A6-dimensioner
a6_width = page_width / 2
a6_height = page_height / 2

# Koordinater för fyra A6 per A4
positions = [
    (0, page_height / 2),
    (page_width / 2, page_height / 2),
    (0, 0),
    (page_width / 2, 0)
]

# Rita sidhuvud
def draw_header(c, text):
    c.setFont("Helvetica-Bold", 16)
    text_width = stringWidth(text, "Helvetica-Bold", 16)
    center_x = (page_width - text_width) / 2
    c.drawString(center_x, page_height - 15 * mm, text)

# En rad med siffror 1–5
def draw_rating_header(c, x, y):
    box_size = 4 * mm
    spacing = 5 * mm
    offset = 70
    c.setFont("Helvetica", 8)
    for i in range(10):
        box_x = x + offset + i * spacing
        c.drawCentredString(box_x + box_size / 2, y, str(i + 1))

# Rita en rad betygsboxar utan siffror
def draw_rating_row(c, label, x, y):
    box_size = 4 * mm
    spacing = 5 * mm
    offset = 70
    c.setFont("Helvetica", 8)
    c.drawString(x, y, label)
    for i in range(10):
        box_x = x + offset + i * spacing
        c.rect(box_x, y - 2, box_size, box_size)

def draw_description_rating_row(c, x, y):
    box_size = 4 * mm
    spacing = 7 * mm
    offset = 0  # Startpunkt lite längre ut så text och boxar inte krockar
    c.setFont("Helvetica", 8)
    c.drawString(x, y, "Stämmer beskrivningen? (1-10)")
    y -= 6 * mm
    for i in range(10):
        box_x = x + offset + i * spacing
        c.rect(box_x, y - 2, box_size, box_size)

# Rita en ölsektion (en A6-ruta)
def draw_a6_section(c, x, y, beer):
    margin = 10 * mm
    start_x = x + margin
    start_y = y + a6_height - margin
    line_height = 6 * mm
    max_width = a6_width - 2 * margin

    # Rita ram runt sektionen
    c.rect(x, y, a6_width, a6_height)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(start_x, start_y, f"{beer['namn']}")
    c.setFont("Helvetica", 8)
    start_y -= line_height
    c.drawString(start_x, start_y, f"{beer['typ']} - {beer['brewery']} - {beer['price']} kr")

    # Rita EN rad med siffror överst
    start_y -= line_height * 1.5
    draw_rating_header(c, start_x, start_y)
    start_y -= line_height * 0.9

    # Rita betygsrader
    draw_rating_row(c, "Färg", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Doft", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Beska", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Sötma", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Fyllighet", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Förpackning", start_x, start_y)
    start_y -= line_height * 1.2
    draw_rating_row(c, "Betyg", start_x, start_y)

    # Beskrivning
    start_y -= line_height * 2
    description_lines = simpleSplit(beer['description'], c._fontname, c._fontsize, max_width)
    for line in description_lines:
        c.drawString(start_x, start_y, line)
        start_y -= line_height

    # Efter beskrivning
    start_y -= line_height * 0.5
    draw_description_rating_row(c, start_x, start_y)
    start_y -= line_height * 2  # Avstånd ner till Kommentar

    # Kommentar
    start_y -= line_height * 0.5    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(start_x, start_y, "Kommentar:")

# Rita sidhuvud på första sidan
draw_header(c, header_text)

# Justering första sidan
first_page_offset = 20 * mm

# Rita öl, fyra per sida
for idx, beer in enumerate(beers):
    if idx > 0 and idx % 4 == 0:
        c.showPage()
        first_page_offset = 0  
    
    pos = positions[idx % 4]
    adjusted_y = pos[1] - first_page_offset if idx < 4 else pos[1]
    draw_a6_section(c, pos[0], adjusted_y, beer)

# Spara PDF
c.save()
