
import tempfile

from google.appengine.api import app_identity

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

from datetime import datetime

# from config import temp_folder_name

#keep for later
default_font_size = 15
image_name = "/images/1.jpg"

def create_pdf(person, ong):
    """method used to create the pdf

    person: dict with the person's data 
        first_name
        father
        last_name
        street
        number
        bl
        sc
        et
        ap
        county
        city
        cnp


    ong: dict with the ngo's data
        name
        cif
        account
    """
    
    # packet = StringIO.StringIO()
    # we could also use StringIO
    packet = tempfile.TemporaryFile(mode='w+b')
    
    c = canvas.Canvas(packet, A4)
    width, height = A4 
    
    # add the image as background
    background = ImageReader( "http://{0}{1}".format(app_identity.get_default_version_hostname(), image_name) )
    c.drawImage(background, 0, 0, width=width, height=height)

    # the default font size
    c.setFontSize(default_font_size)

    # the year
    # this is the previous year, starting from 1 Jan until - 25 May ??
    year = str( datetime.now().year - 1 )
    start_x = 306
    for letter in year:
        c.drawString(start_x, 727, letter)
        start_x += 17

    # the first name
    if len(person["first_name"]) > 18:
        c.setFontSize(12)

    donor_block_x = 640

    c.drawString(66, donor_block_x, person["first_name"])
    c.setFontSize(default_font_size)

    # father's first letter
    c.drawString(299, donor_block_x, person["father"])

    # the last name
    last_name = person["last_name"]
    if len(last_name) > 34:
        c.setFontSize(10)

    c.drawString(66, donor_block_x-27, last_name)


    # =======================================
    # THIRD ROW
    # 
    third_row_x = donor_block_x - 58

    # the street
    street = person["street"]
    if len(street) > 40:
        c.setFontSize(8)
    elif len(street) in range(36, 40):
        c.setFontSize(10)
    elif len(street) in range(25, 35):
        c.setFontSize(12)

    c.drawString(66, third_row_x, street)
    c.setFontSize(default_font_size)

    # numar
    c.drawString(289, third_row_x, person["number"])
    # 
    # =======================================

    # =======================================
    # FOURTH ROW
    fourth_row_x = donor_block_x - 87

    c.setFontSize(14)
    # bloc
    c.drawString(49, fourth_row_x, person["bl"])
    # scara
    c.drawString(108, fourth_row_x, person["sc"])

    # etaj
    c.drawString(150, fourth_row_x, person["et"])

    # apartament
    c.drawString(185, fourth_row_x, person["ap"])

    # judet
    c.setFontSize(12)
    c.drawString(255, fourth_row_x, person["county"])
    c.setFontSize(default_font_size)
    # 
    # =======================================


    # oras
    c.drawString(68, donor_block_x - 115, person["city"])

    c.setFontSize(16)

    # cnp
    start_x = 336
    for letter in person["cnp"]:
        c.drawString(start_x, donor_block_x - 10, letter)
        start_x += 18.4
        

    # DRAW ONG DATA
    start_ong_x = 373

    # the x mark
    c.drawString(221, start_ong_x, "x")
    # the cif code
    c.drawString(409, start_ong_x - 1, ong["cif"])

    org_name = ong["name"]
    if len(org_name) > 79:
        c.setFontSize(10)
    elif len(org_name) > 65:
        c.setFontSize(13)

    c.drawString(118, start_ong_x - 28, org_name)

    c.setFontSize(11)

    account = ong["account"]
    for i, l in enumerate(account):
        if i%5 == 0:
            account = account[:i] + " " + account[i:]

    c.drawString(118, start_ong_x - 55, account)


    c.save()

    # go to the beginning of the file
    packet.seek(0)
    # packet.type = "application/pdf"

    return packet