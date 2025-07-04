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
logo_path = os.path.join(templates_folder, "logo.png")
graph_path = os.path.join(templates_folder, "logo.png")
fonts_folder = os.path.join(templates_folder, "fonts")
arial = os.path.join(fonts_folder, "ARIAL.TTF")
arial_bold = os.path.join(fonts_folder, "ARIALBD.TTF")

mock_up_data = [
    {
        "score": 90,
        "text": "Tu evaluación refleja un conocimiento sólido y avanzado sobre los aspectos clave de la alfabetización tecnológica, lo cual es una fortaleza significativa en tu perfil profesional. Comprendes bien las implicaciones y aplicaciones de tecnologías, lo que te permite tomar decisiones informadas y estratégicas en tu organización. No obstante, es recomendable que sigas profundizando en áreas emergentes, como la automatización de procesos y la cadena de bloques, para mantenerte a la vanguardia de las innovaciones tecnológicas. También podrías centrarte en expandir tu capacidad para fomentar una cultura digital dentro de tu equipo, asegurando que todos estén alineados con las nuevas herramientas y tecnologías. Si continúas desarrollando tus habilidades en la gestión de riesgos tecnológicos y el cumplimiento de normativas globales de seguridad, podrás fortalecer aún más tu liderazgo digital y asegurar que tu organización se mantenga competitiva a largo plazo.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja un sólido conocimiento de la línea de tiempo en la evolución tecnológica y su impacto en la vida humana, lo que te posiciona bien para tomar decisiones estratégicas en un entorno altamente digitalizado. Para seguir avanzando, te sugiero que profundices en el impacto de la inteligencia artificial y la automatización en sectores específicos, como la atención médica, servicios y la manufactura o los que podrían aplicarse a tu organización. Estar al tanto de las últimas tendencias en IA te permitirá liderar la integración de estas tecnologías en tu organización para mejorar la productividad y la innovación. Además, sería beneficioso que investigaras más sobre las implicaciones éticas y sociales de la IA, especialmente en relación con la automatización del trabajo. De esta forma, podrás guiar a tu equipo y a tu organización hacia una adopción tecnológica sostenible, anticipando los desafíos del futuro del trabajo.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una sólida comprensión de la diferencia entre Internet y la World Wide Web (WWW), lo que te permite adoptar un enfoque estratégico más integral en la transformación digital y en las inversiones tecnológicas, súmate a los líderes que promueven este progreso. Tienes claro que la infraestructura de Internet va más allá de la WWW e incluye tecnologías como la computación en la nube, la IoT (internet de las cosas) y la cadena de bloques. Para seguir avanzando, te sugiero que continúes profundizando en el impacto de estas tecnologías emergentes, como la computación perimetral (edge computing) y la Internet industrial de las cosas (IIoT), que están remodelando el panorama digital. Al seguir desarrollando tu visión holística de cómo estas tecnologías interrelacionadas afectan la competitividad empresarial, podrás liderar de manera más efectiva la innovación, la protección de datos y las estrategias de crecimiento sostenible dentro de tu organización. ",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una sólida comprensión de los dispositivos digitales y sus aplicaciones, lo cual es una fortaleza clave en tu desempeño como líder. Seguramente utilizas herramientas de análisis de datos, colaboración en la nube y automatización de tareas de manera efectiva para optimizar tu tiempo y mejorar la productividad. Sin embargo, para continuar avanzando, te sugiero profundizar en el uso de aplicaciones avanzadas de IA, como asistentes virtuales personalizados o herramientas de análisis predictivo, que pueden ofrecerte nuevas formas de anticipar problemas y tomar decisiones más estratégicas. También es importante que compartas tus conocimientos con tu equipo, fomentando una cultura de adopción tecnológica y asegurándote de que todos estén alineados en el uso de estas herramientas. Esto fortalecerá aún más tu capacidad de liderazgo y tu impacto en la organización.",
    },
    {
        "score": 90,
        "text": "Tu evaluación indica que tienes una comprensión avanzada de la ciberseguridad y de su impacto en la estrategia organizacional, lo que te posiciona como un líder capaz de tomar decisiones clave para proteger los activos digitales de la empresa. Dominas conceptos clave como la gestión de riesgos, la protección de datos y el cumplimiento normativo, y has integrado estas prácticas en las operaciones de la organización. Para seguir avanzando, te recomendaría que lideres iniciativas de concientización sobre ciberseguridad dentro de tu equipo y entorno laboral, asegurándote de que todos, desde los empleados hasta los altos ejecutivos, comprendan la importancia de una cultura de seguridad. También sería valioso que continúes evaluando y mejorando los planes de respuesta a incidentes de la empresa, apoya a los que lideran las áreas de tecnología en todo lo que soliciten, e impulsa las simulaciones regulares para asegurar una respuesta rápida ante cualquier brecha.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una comprensión avanzada sobre la huella digital, lo que te coloca en una posición fuerte como líder en la protección de los activos digitales de la organización. Dominas las estrategias clave, como el uso de contraseñas seguras, la encriptación de datos y la implementación de políticas de acceso controlado, lo cual es esencial para minimizar los riesgos. Para seguir avanzando, te sugiero que continúes investigando las últimas tendencias en ciberseguridad. Además, lidera iniciativas educativas dentro de la organización, capacitando a tu equipo sobre los riesgos de la huella digital y las mejores prácticas de seguridad. Fomentar una cultura de ciberseguridad contribuirá a fortalecer aún más la protección de la organización y minimizará las vulnerabilidades humanas. Mantente también al tanto de las regulaciones de privacidad y seguridad, asegurando que tu empresa cumpla con los estándares internacionales.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una comprensión avanzada y un enfoque ejemplar sobre el uso responsable de la tecnología. Estás bien posicionado para liderar con ética en el ámbito digital, lo que es fundamental para fomentar una cultura de integridad y respeto en tu organización. Has demostrado un compromiso con la transparencia, la privacidad y la creación de un ambiente digital seguro, lo cual es crucial para generar confianza tanto interna como externamente. Para seguir avanzando, te sugiero que sigas promoviendo la educación continua sobre el comportamiento ético en el uso de la tecnología dentro de tu equipo, asegurándote de que todos comprendan su responsabilidad digital. Además, sería valioso que lideres más iniciativas sobre los beneficios y riesgos de las tecnologías emergentes, como la IA y el análisis de datos, y cómo estas pueden implementarse de manera ética en la organización. ",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una comprensión avanzada de las herramientas de colaboración en línea y su aplicación en un entorno de trabajo híbrido o remoto. Ya dominas las características clave de plataformas más comunes y eres capaz de utilizarlas para mejorar la eficiencia operativa y el rendimiento de tu equipo. Sin embargo, te sugiero que sigas explorando nuevas formas de integrar estas plataformas con otros sistemas de la organización, como CRM y ERP, para optimizar aún más los flujos de trabajo y automatizar tareas repetitivas. Te recomiendo que lideres la implementación de una estrategia de datos en tu organización. También sería beneficioso que continúes desarrollando tus habilidades en la gestión de equipos distribuidos, asegurando que el trabajo remoto e híbrido se gestione de manera eficiente y cohesionada. Siguiendo estos pasos, continuarás destacándote como un líder adaptado a las tendencias digitales y preparado para afrontar los retos futuros.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja un sólido conocimiento y comprensión de las tecnologías emergentes, como la inteligencia artificial, Realidad Virtual (RV) y la cadena de bloques, lo que te coloca en una posición destacada, podrías ser líder digital fuera del área de tecnología. Dominas los conceptos clave y estás bien informado sobre cómo estas tecnologías pueden impactar tu industria y mejorar las operaciones. Para seguir avanzando, te sugiero que te enfoques en implementar la IA de manera más estratégica dentro de tu organización, para mejorar la productividad y la toma de decisiones. Además, dado tu conocimiento sobre la cadena de bloques, podrías explorar formas de integrar contratos inteligentes y otras aplicaciones descentralizadas para optimizar los procesos y aumentar la transparencia en las operaciones de la empresa. También sería valioso que lideres iniciativas educativas ayudando a tu equipo a comprender cómo estas tecnologías pueden mejorar su trabajo. ",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja un conocimiento avanzado de las tecnologías de asistencia y su papel en la creación de una sociedad más inclusiva. Tienes una comprensión sólida de cómo estas herramientas, como los asistentes de voz, los lectores de pantalla y los dispositivos domésticos inteligentes, benefician a las personas con capacidades diferentes, facilitando su independencia y participación en la sociedad. Para seguir avanzando, te sugiero que tomes un enfoque proactivo en la implementación de estas tecnologías dentro de tu organización, garantizando que todos los empleados, independientemente de sus capacidades, tengan acceso a herramientas que mejoren su productividad y bienestar. Además, sería beneficioso que lideres iniciativas para aumentar la conciencia sobre la importancia de la accesibilidad digital y cómo se pueden integrar soluciones de tecnología de asistencia en la vida cotidiana de manera efectiva. ",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja una comprensión avanzada de los desafíos y oportunidades que presentan las redes sociales para los líderes en la era digital. Tus respuestas sugieren que manejas bien tu presencia en línea, lo que te permite influir positivamente en tu equipo, mejorar la percepción pública de la empresa y generar relaciones de confianza con clientes y socios. No obstante, te recomiendo que sigas perfeccionando tu enfoque al establecer límites aún más rigurosos en el tiempo que dedicas a las redes sociales, para que puedas concentrarte en las prioridades profesionales y reducir la presión psicológica de la conectividad constante. Además, dado tu conocimiento, sería valioso que lideres iniciativas dentro de tu organización para educar a tu equipo sobre el uso responsable de las plataformas digitales, promoviendo una cultura de bienestar y respeto en línea. Siguiendo estas prácticas, fortalecerás tu influencia como un líder responsable y equilibrado.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja un excelente dominio de las prácticas sostenibles relacionadas con la tecnología y el medio ambiente. Tienes una comprensión profunda de cómo la adopción de tecnologías ecológicas, como el uso de energías renovables y el reciclaje de equipos electrónicos, pueden beneficiar tanto al medio ambiente como a la sostenibilidad de la empresa. Te sugiero que tomes la iniciativa para liderar dentro de tu organización, implementando políticas más rigurosas que promuevan la eficiencia energética y la reducción de la huella de carbono. Además, puedes considerar la creación de una estrategia de sostenibilidad más robusta que incluya la optimización de recursos tecnológicos y la integración de soluciones más verdes en todos los aspectos de la operación empresarial. Sigue explorando nuevas tecnologías ecológicas y asegúrate de que tu empresa esté a la vanguardia en cuanto a sostenibilidad digital.",
    },
    {
        "score": 90,
        "text": "Tu evaluación refleja un nivel sobresaliente en cuanto a etiqueta digital, lo que indica que tienes una gran capacidad para comunicarte de manera respetuosa y profesional en plataformas digitales. Sabes manejar diferentes tipos de comunicación y eres consciente de la importancia de la rapidez y la claridad en las respuestas. Además, muestras una excelente habilidad para adaptarte a las expectativas de las diversas generaciones, lo que te permite gestionar equipos de manera efectiva en un entorno digital. Sin embargo, es importante que continúes perfeccionando tu capacidad para respetar los límites digitales, tanto para ti como para tu equipo, especialmente en un entorno remoto donde el trabajo puede fácilmente invadir el tiempo personal. Te sugiero que sigas promoviendo un uso responsable de las tecnologías y sigas modelando un comportamiento digital positivo para tu equipo. No olvides que liderar con el ejemplo es una ventaja única. ",
    }
]


def footer_setting(c: canvas.Canvas, name: str, width: float, color: Color):
    """Draw centered footer content

    Args:
        c (canvas.Canvas): PDF Canvas representation
        name (str): applicant's name
        width (float): PDF page width
        color (Color): RGB color to draw text
    """
    footer_text = f"Reporte AFT de {name}"
    text_width = c.stringWidth(footer_text, "arial", 9)
    x = (width - text_width) / 2 + 15
    c.setFont("arial", 9)
    c.setFillColor(color)  # we could also use Color(0.7, 0.7, 0.7)
    c.drawString(x, 53, footer_text)


# Función para justificar el texto y resaltar en negritas las frases clave
def justify_text(c, text, x, y, width=467, font="arial", font_size=11):
    c.setFont(font, font_size)

    words = text.split(" ")
    line = []
    line_width = 0
    space_width = c.stringWidth(" ", font, font_size)

    lines = []  # Almacena las líneas ya formadas

    for word in words:
        word_width = c.stringWidth(word, font, font_size)

        if line_width + word_width <= width:
            line.append(word)
            line_width += word_width + space_width
        else:
            lines.append(line)
            line = [word]
            line_width = word_width + space_width

    if line:
        lines.append(line)

    for i, line in enumerate(lines):
        final = i == len(lines) - 1
        draw_justified_line(c, line, x, y, width, font, font_size, final)
        y -= font_size + 4


# Función para imprimir una línea con justificación y negritas
def draw_justified_line(c, words, x, y, width, font, font_size, final):
    total_spaces = len(words) - 1
    text_width = sum(c.stringWidth(word, font, font_size) for word in words)

    if total_spaces > 0:
        extra_space = (width - text_width) / total_spaces
    else:
        extra_space = 0

    if final:
        extra_space = 4

    current_x = x
    for word in words:
        c.drawString(current_x, y, word)
        current_x += c.stringWidth(word, font, font_size) + extra_space


def generate_report(
    name: str,
    date: str,
    grade_code: str,
    final_score: float,
    logo_path: str,
    graph_path: str,
    data: list,
    resulting_paragraphs: list
) -> str:
    """Generate PDF report from data

    Args:
        name (str): applicant's name
        date (str): report issue date
        grade_code (str): acronym for rating-based description
        final_score (str): applicant's final score
        logo_path (str): path to business logo
        graph_path (str): path to scores path
        data (list): applicants scores list
        resulting_paragraphs (list): list of score and paragraph dicts

    Returns:
        str: Generated path file
    """

    def footer_setting(c: canvas.Canvas, name: str, width: float, color: Color):
        """Draw centered footer content

        Args:
            c (canvas.Canvas): PDF Canvas representation
            name (str): applicant's name
            width (float): PDF page width
            color (Color): RGB color to draw text
        """
        footer_text = f"Reporte AFT de {name}"
        text_width = c.stringWidth(footer_text, "arial", 9)
        x = (width - text_width) / 2 + 15
        c.setFont("arial", 9)
        c.setFillColor(color)  # we could also use Color(0.7, 0.7, 0.7)
        c.drawString(x, 53, footer_text)

    packet = io.BytesIO()
    # Fonts with epecific path
    pdfmetrics.registerFont(TTFont("arial", arial))
    pdfmetrics.registerFont(TTFont("arialbd", arial_bold))

    c = canvas.Canvas(packet, legal)

    width, height = legal
    color_darkgrey = Color(153 / 255, 153 / 255, 153 / 255)

    # Page 1
    c.setFont("arialbd", 22)
    c.drawRightString(width - 70, 300, name)
    c.drawRightString(width - 70, 270, date)

    image_width = 130
    x = (width - image_width) / 2
    c.drawImage(logo_path, x, 115, width=image_width, height=image_width)

    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Page 2
    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Page 3
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

    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Page 4
    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Page 5
    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Page 6
    c.setFont("arialbd", 14)
    c.drawString(215, 707, name)

    image_width = width - 140
    x = (width - image_width) / 2
    c.drawImage(graph_path, x, 320, width=image_width, height=image_width - 100)

    # Draw footer content
    footer_setting(c, name, width, color_darkgrey)

    c.showPage()

    # Pages 7 - 19
    for i in range(13):
        score = resulting_paragraphs[i]["score"]
        c.setFont("arialbd", 12)
        c.drawString(142, 660, f"{score}%")

        text = resulting_paragraphs[i]["text"]
        justify_text(c, text, x=72, y=520)

        # Draw footer content
        footer_setting(c, name, width, color_darkgrey)

        c.showPage()

    c.save()

    packet.seek(0)

    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(original_pdf, "rb"))
    output = PdfWriter()

    # Pages creation
    for i in range(19):
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
        final_score=38.9,
        logo_path=logo_path,
        graph_path=graph_path,
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
        resulting_paragraphs=mock_up_data
    )

    generate_report(
        name="Abel Soto Martinez",
        date="30/12/2025",
        grade_code="P",
        final_score=50,
        logo_path=logo_path,
        graph_path=graph_path,
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
        resulting_paragraphs=mock_up_data
    )

    generate_report(
        name="Abel Soto Martinez de la Cruz Parez de Dios",
        date="30/12/2025",
        grade_code="MEP",
        final_score=70,
        logo_path=logo_path,
        graph_path=graph_path,
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
        resulting_paragraphs=mock_up_data
    )

    generate_report(
        name="Sample",
        date="30/12/2025",
        grade_code="MEP",
        final_score=70,
        logo_path=logo_path,
        graph_path=graph_path,
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
        resulting_paragraphs=mock_up_data
    )
