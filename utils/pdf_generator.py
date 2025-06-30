import os
import io
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, black, darkgray
import numpy as np
from graphics_generator import generate_bell_curve_plot


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


def generate_report(
    name: str, date: str, grade_code: str, final_score: float, image_path: str, data: list
) -> str:
    """Generate PDF report from data

    Args:
        name (str): applicant's name
        date (str): report issue date
        grade_code (str): acronym for rating-based description
        final_score (str): applicant's final score
        data (list): applicants scores list

    Returns:
        str: Generated path file
    """

    packet = io.BytesIO()
    # Fonts with epecific path
    pdfmetrics.registerFont(TTFont("arial", arial))
    pdfmetrics.registerFont(TTFont("arialbd", arial_bold))

    c = canvas.Canvas(packet, legal)

    width, height = legal
    color_darkgrey = Color(153/255, 153/255, 153/255)

    # Page 1
    c.setFont("arialbd", 22)
    c.drawRightString(width - 70, 300, name)
    c.drawRightString(width - 70, 270, date)

    image_width = 130
    x = (width - image_width) / 2
    c.drawImage(image_path, x, 115, width=image_width, height=image_width)

    # Footer setting
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15
    c.setFont("arial", 9)
    c.setFillColor(color_darkgrey)  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)

    c.showPage()

    #Página 2
    # Footer setting
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15
    c.setFont("arial", 9)
    c.setFillColor(Color(153/255, 153/255, 153/255))  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)
    c.showPage()

    #Página 3
    c.setFont("arialbd", 11)
    c.drawString(73, 675, f'"{name}".')

    data = np.array(data)

    bell_plot_path = generate_bell_curve_plot(final_score, data.mean(), data)
    image_width = 400
    x = (width - image_width) / 2
    c.drawImage(bell_plot_path, x, 390, width=image_width, height=200)


    c.setFont("arialbd", 30)
    c.drawString(68, 328, "□")

    c.setFont("arialbd", 30)
    c.drawString(68, 295, "□")

    c.setFont("arialbd", 30)
    c.drawString(68, 263, "□")
    
    c.setFont("arialbd", 30)
    c.drawString(68, 231, "□")

    c.setFont("arialbd", 30)
    c.drawString(68, 200, "□")

    if grade_code == "MDP":
        c.setFont("arialbd", 30)
        c.drawString(68, 328, "■")
    elif grade_code == "DP":
        c.setFont("arialbd", 30)
        c.drawString(68, 295, "■")
    elif grade_code == "P":
        c.setFont("arialbd", 30)
        c.drawString(68, 263, "■")
    elif grade_code == "AP":
        c.setFont("arialbd", 30)
        c.drawString(68, 231, "■")
    elif grade_code == "MEP":
        c.setFont("arialbd", 30)
        c.drawString(68, 200, "■")

    c.setFont("arialbd", 11)
    c.drawString(275, 150, f'"{name}".')

    # Footer setting
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15                
    c.setFont("arial", 9)
    c.setFillColor(Color(153/255, 153/255, 153/255))  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)
    c.showPage()

    #Página 4
    # Footer setting
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15
    c.setFont("arial", 9)
    c.setFillColor(Color(153/255, 153/255, 153/255))  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)
    c.showPage()

    #Página 5
    # Footer setting
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15
    c.setFont("arial", 9)
    c.setFillColor(Color(153/255, 153/255, 153/255))  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)
    c.showPage()

    c.save()

    packet.seek(0)

    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(original_pdf, "rb"))
    output = PdfWriter()

    # Pages creation
    for i in range(5):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    new_pdf = os.path.join(files_folder, f"{name}.pdf")
    output_stream = open(new_pdf, "wb")
    output.write(output_stream)
    output_stream.close()
    print(f"File {name} generated correctly")

    return new_pdf


if __name__ == "__main__":
    generate_report(
        name="Abel Soto",
        date="30/12/2025",
        grade_code="MDP",
        final_score= 38.9,
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

    generate_report(
        name="Abel Soto Martinez",
        date="30/12/2025",
        grade_code="P",
        final_score= 50,
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

    generate_report(
        name="Abel Soto Martinez de la Cruz Parez de Dios",
        date="30/12/2025",
        grade_code="MEP",
        final_score= 70,
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
