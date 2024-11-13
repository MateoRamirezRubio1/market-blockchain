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
    elements.append(Paragraph("Energy Transaction Agreement", title_style))
    elements.append(Spacer(1, 12))

    # Fecha de emisión
    elements.append(
        Paragraph(
            f"Date of Issue of the Contract: {contract_data['confirmation_date']}",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 1: Partes Contratantes
    elements.append(Paragraph("1. Contracting Parties", subtitle_style))
    elements.append(
        Paragraph(f"<b>Seller:</b> {contract_data['seller_name']}", content_style)
    )
    elements.append(
        Paragraph(f"<b>Buyer:</b> {contract_data['buyer_name']}", content_style)
    )
    elements.append(
        Paragraph(
            "Both parties agree to the terms and conditions of this contract, acting in good faith and in accordance with the applicable legal provisions in force.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 2: Objeto del Contrato
    elements.append(Paragraph("2. Subject Matter of the Contract", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Offering Hash on the blockchain network:</b> {contract_data['offer_hash']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            f"<b>Amount of energy:</b> {contract_data['energy_amount']} kWh",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            f"<b>Price per Unit of Energy:</b> {contract_data['price_per_unit']} USD/kWh",
            content_style,
        )
    )
    elements.append(
        Paragraph(f"<b>Type of Offer:</b> {contract_data['offer_type']}", content_style)
    )
    elements.append(
        Paragraph(f"<b>Bid Status:</b> {contract_data['status']}", content_style)
    )
    elements.append(
        Paragraph(
            "This contract represents a binding commitment for the purchase and sale of the indicated amount of energy under the specified conditions. Confirmation of the offer implies full acceptance of these terms.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 3: Condiciones de Cumplimiento
    elements.append(Paragraph("3. Conditions of Compliance", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Date and Time of Energy Transfer:</b> {contract_data['transfer_datetime']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "Both parties agree that, at the date and time indicated for the transfer of energy, the evaluation of compliance with all the conditions stipulated in this contract will be carried out. The verification of compliance will be performed by an impartial and registered third party, in accordance with the established provisions.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 4: Penalización por Incumplimiento
    elements.append(Paragraph("4. Penalty for noncompliance", subtitle_style))
    elements.append(
        Paragraph(
            f"<b>Penalty to be applied:</b> {contract_data['penalty_reason']}",
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "The penalty shall apply in the event that either party fails to comply with the obligations stipulated in this contract on the date and time designated for the transfer of energy. Such penalty shall be enforced in accordance with the applicable legal provisions, including any regulatory provisions or regulations in force.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 5: Términos y Condiciones Generales
    elements.append(Paragraph("5. General Terms and Conditions", subtitle_style))
    elements.append(
        Paragraph(
            contract_data["terms_conditions"],
            content_style,
        )
    )
    elements.append(
        Paragraph(
            "This contract is subject to the laws and regulations in force in the jurisdiction of the contracting parties. The parties agree to comply with any additional provisions imposed by local or national regulation.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Parte 6: Resolución de Disputas
    elements.append(Paragraph("6. Dispute Resolution", subtitle_style))
    elements.append(
        Paragraph(
            "Any dispute arising in connection with the performance, interpretation, or execution of this contract shall be settled by conciliation between the parties. In case of failure to reach a conciliation, the parties may resort to the competent courts or submit to arbitration, as applicable and agreed by the parties.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Nota de Aprobación
    elements.append(
        Paragraph(
            f"This contract has been reviewed and approved by both parties, {contract_data['seller_name']} (Seller) and {contract_data['buyer_name']} (Buyer), who represent that they understand and agree to all the terms and conditions set forth herein.",
            content_style,
        )
    )
    elements.append(Spacer(1, 12))

    # Fecha de Confirmación
    elements.append(
        Paragraph(
            f"Confirmation Date: {contract_data['confirmation_date']}",
            content_style,
        )
    )

    # Generar el PDF
    pdf.build(elements)
