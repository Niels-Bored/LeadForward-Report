import os
import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import numpy as np


current_folder = os.path.dirname(__file__)
parent_folder = os.path.dirname(current_folder)
files_folder = os.path.join(parent_folder, "files")

# Create files folder in case it doesn't exist
os.makedirs(files_folder, exist_ok=True)

templates_folder = os.path.join(current_folder, "pdf_utils")
original_pdf = os.path.join(templates_folder, "template.pdf")
image_path = os.path.join(templates_folder, "logo.png")
fonts_folder = os.path.join(templates_folder, "fonts")
arial = os.path.join(fonts_folder, "ARIAL.TTF")
arial_bold = os.path.join(fonts_folder, "ARIALBD.TTF")


def generate_invoice(
    name: str, date: str, grade_code: str, cal: float, image_path: str, data: np.array
) -> str:
    """Generate invoice PDF from data

    Args:
        name (str): _description_
        date (str): _description_
        grade_code (str): _description_
        cal (str): _description_
        data (str): _description_

    Returns:
        str: Generated path file
    """

    packet = io.BytesIO()
    # Fonts with epecific path
    pdfmetrics.registerFont(TTFont("arial", arial))
    pdfmetrics.registerFont(TTFont("arialbd", arial_bold))

    c = canvas.Canvas(packet, legal)

    width, height = legal

    # Page 1
    c.setFont("arialbd", 22)
    c.drawRightString(width - 70, 300, name)
    c.drawRightString(width - 70, 270, date)

    image_width = 130
    x = (width - image_width) / 2
    c.drawImage(image_path, x, 115, width=image_width, height=image_width)

    c.showPage()
    c.save()

    packet.seek(0)

    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(original_pdf, "rb"))
    output = PdfWriter()

    # Page creation
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    new_pdf = os.path.join(files_folder, f"{name}.pdf")
    output_stream = open(new_pdf, "wb")
    output.write(output_stream)
    output_stream.close()
    print(f"File {name} generated correctly")

    return new_pdf


if __name__ == "__main__":
    generate_invoice(
        name="Abel Soto",
        date="30/12/2025",
        grade_code="MDP",
        cal= 38.9,
        image_path=image_path,
        data=np.array(
            [
                53.1,
                48.7,
                61.5,
                55.0,
                42.3,
                67.8,
                50.2,
                59.1,
                45.4,
                62.7,
                38.9,
                56.6,
                47.3,
                64.0,
                51.9,
                44.7,
                58.4,
                49.0,
                54.8,
                40.5,
            ]
        ),
    )

    generate_invoice(
        name="Abel Soto Martinez",
        date="30/12/2025",
        grade_code="P",
        cal= 50,
        image_path=image_path,
        data=np.array(
            [
                53.1,
                48.7,
                61.5,
                55.0,
                42.3,
                67.8,
                50.2,
                59.1,
                45.4,
                62.7,
                38.9,
                56.6,
                47.3,
                64.0,
                51.9,
                44.7,
                58.4,
                49.0,
                54.8,
                40.5,
            ]
        ),
    )

    generate_invoice(
        name="Abel Soto Martinez de la Cruz Parez de Dios",
        date="30/12/2025",
        grade_code="MEP",
        cal= 70,
        image_path=image_path,
        data=np.array(
            [
                53.1,
                48.7,
                61.5,
                55.0,
                42.3,
                67.8,
                50.2,
                59.1,
                45.4,
                62.7,
                38.9,
                56.6,
                47.3,
                64.0,
                51.9,
                44.7,
                58.4,
                49.0,
                54.8,
                40.5,
            ]
        ),
    ) 
