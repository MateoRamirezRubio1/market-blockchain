from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os


def create_contract_pdf(filename, contract_data):
    # Obtener la ruta absoluta desde la raíz del proyecto
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..", "pdfs")
    )
    # Crear la ruta completa para el archivo PDF en la carpeta 'pdfs' en la raíz
    pdf_file_path = os.path.join(base_path, filename)

    # Verificar si la carpeta 'pdfs' existe, si no, crearla
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Crear un documento PDF
    pdf = SimpleDocTemplate(pdf_file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Heading1"], fontSize=24, alignment=1, spaceAfter=20
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle", parent=styles["Heading2"], fontSize=16, spaceAfter=12
    )
    content_style = styles["BodyText"]
    highlight_style = ParagraphStyle(
        "Highlight",
        parent=styles["BodyText"],
        fontSize=14,
        textColor=colors.blue,
        fontName="Helvetica-Bold",
    )

    # Contenido del PDF
    elements = []

    # Título del contrato
    elements.append(Paragraph("Contrato de Transacción de Energía", title_style))
    elements.append(Spacer(1, 12))

    # Fecha de emisión
    elements.append(
        Paragraph(
            f"Fecha de Emisión del Contrato: {contract_data['confirmation_date']}",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 1: Partes Contratantes
    elements.append(Paragraph("1. Partes Contratantes", subtitle_style))
    elements.append(
        Paragraph(f"<b>Vendedor:</b> {contract_data['seller_name']}", content_style)
    )
    elements.append(
        Paragraph(f"<b>Comprador:</b> {contract_data['buyer_name']}", content_style)
    )
    elements.append(
        Paragraph(
            "Ambas partes acuerdan los términos y condiciones del presente contrato, actuando en buena fe y conforme a las disposiciones legales vigentes aplicables.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 2: Objeto del Contrato
    elements.append(Paragraph("2. Objeto del Contrato", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Hash de la Oferta en la red blockchain:</b> {contract_data['offer_hash']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            f"<b>Cantidad de Energía:</b> {contract_data['energy_amount']} kWh",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            f"<b>Precio por Unidad de Energía:</b> {contract_data['price_per_unit']} USD/kWh",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            f"<b>Tipo de Oferta:</b> {contract_data['offer_type']}", content_style
        )
    )
    elements.append(
        Paragraph(
            f"<b>Estado de la Oferta:</b> {contract_data['status']}", content_style
        )
    )
    elements.append(
        Paragraph(
            "Este contrato representa un compromiso vinculante para la compra-venta de la cantidad de energía indicada en las condiciones especificadas. La confirmación de la oferta implica aceptación total de estos términos.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 3: Condiciones de Cumplimiento
    elements.append(Paragraph("3. Condiciones de Cumplimiento", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Fecha y Hora de Transferencia de Energía:</b> {contract_data['transfer_datetime']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "Ambas partes acuerdan que, a la fecha y hora señaladas para la transferencia de energía, se procederá con la evaluación de cumplimiento de todas las condiciones estipuladas en este contrato. La verificación de cumplimiento será ejecutada por un tercero imparcial y registrado, en conformidad con las disposiciones establecidas.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 4: Penalización por Incumplimiento
    elements.append(Paragraph("4. Penalización por Incumplimiento", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Penalización que será aplicada:</b> {contract_data['penalty_reason']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "La penalización se aplicará en caso de que cualquiera de las partes incumpla las obligaciones estipuladas en este contrato en la fecha y hora designadas para la transferencia de energía. Dicha penalización será ejecutada conforme a las disposiciones legales aplicables, incluyendo cualquier disposición o normativa reguladora en vigor.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 5: Términos y Condiciones Generales
    elements.append(Paragraph("5. Términos y Condiciones Generales", subtitle_style))
    elements.append(
        Paragraph(
            contract_data["terms_conditions"],
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "Este contrato está sujeto a las leyes y regulaciones vigentes en la jurisdicción de las partes contratantes. Las partes acuerdan cumplir con cualquier disposición adicional impuesta por la regulación local o nacional.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 6: Resolución de Disputas
    elements.append(Paragraph("6. Resolución de Disputas", subtitle_style))
    elements.append(
        Paragraph(
            "Cualquier disputa surgida en relación con el cumplimiento, interpretación, o ejecución de este contrato será resuelta mediante conciliación entre las partes. En caso de no lograr una conciliación, las partes podrán acudir a los tribunales competentes o someterse a arbitraje, según sea aplicable y acordado por las partes.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Nota de Aprobación
    elements.append(
        Paragraph(
            f"Este contrato ha sido revisado y aprobado por ambas partes, {contract_data['seller_name']} (Vendedor) y {contract_data['buyer_name']} (Comprador), quienes declaran que entienden y aceptan todos los términos y condiciones aquí expuestos.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Fecha de Confirmación
    elements.append(
        Paragraph(
            f"Fecha de Confirmación: {contract_data['confirmation_date']}",
            content_style,
        )
    )

    # Generar el PDF
    pdf.build(elements)
