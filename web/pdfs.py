
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, Color, gray
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle

# def generar_template_presupuesto(response, datos):
#     p = canvas.Canvas(response, pagesize=A4)
#     width, height = A4

#     # Colores definidos
#     agua_color = Color(0.0, 194/255.0, 204/255.0)  # Color verde agua
#     light_agua_color = Color(180/255.0, 237/255.0, 238/255.0)  # Color verde agua más claro

#     # Configuraciones del Header
#     header_height = 4 * cm
#     logo_width = 6 * cm
#     left_box_width = width - logo_width - 3 * cm

#     # Dibuja el header
#     p.setStrokeColor(light_agua_color)
#     p.setLineWidth(1)
#     p.line(0, height - header_height, width, height - header_height)

#     # Rectángulo de la derecha (logo)
#     logo_height = header_height - 0.5 * cm
#     logo_x = left_box_width + (width - logo_width - left_box_width) / 2
#     logo_y = height - header_height + (header_height - logo_height) / 2

#     # Inserta la imagen del logo en el rectángulo derecho centrado
    

#     p.drawImage("web/static/web/img/LogoUnitronic.png", logo_x, logo_y, 
#                 width=logo_width - 0.5 * cm, height=logo_height, preserveAspectRatio=True)

#     # Rectángulos de la izquierda
#     p.setFillColor(light_agua_color)
#     p.rect(0, height - 2 * cm, left_box_width, 2 * cm, stroke=0, fill=1)

#     p.setFillColor(black)
#     p.setFont("Helvetica-Bold", 36)  # Fuente más grande para "Presupuesto"
#     text_width = p.stringWidth("Presupuesto", "Helvetica-Bold", 36)
#     p.drawString((left_box_width - text_width) / 2, height - 3.5 * cm, "Presupuesto")

#     # Configuración del Footer
#     footer_rect_height = 11 * cm
#     footer_width = width

#     # Rectángulo verde agua oscuro de 1 cm de ancho y 11 cm de alto
#     p.setFillColor(agua_color)
#     p.rect(0, 0, 1 * cm, footer_rect_height, stroke=0, fill=1)

#     # Rectángulo verde agua claro de 1 cm de alto, por el ancho restante
#     p.setFillColor(light_agua_color)
#     p.rect(1 * cm, 0, footer_width - 1 * cm, 1 * cm, stroke=0, fill=1)

#     # Información de contacto de la empresa
#     contact_y_position = 1.5 * cm  # Altura de los datos de contacto

#     p.setFillColor(black)
#     p.setFont("Helvetica", 8)
#     p.drawString(2 * cm, contact_y_position, "+54 9 11 4300 9500")
#     p.drawString(6 * cm, contact_y_position, "serviciotecnico@ecifra.com.ar")
#     p.drawString(12 * cm, contact_y_position, "Peru 1028 - San Telmo - CP 1068")
#     p.drawString(18 * cm, contact_y_position, "www.ecifra.com.ar")

#     # Nuevo rectángulo verde agua en el borde derecho de la hoja
#     p.setFillColor(agua_color)
#     p.rect(width - 1 * cm, footer_rect_height, 1 * cm, 8 * cm, stroke=0, fill=1)

#     # Placeholder para los datos dinámicos (sin rectángulos)
#     p.setFont("Helvetica", 10)
#     p.setFillColor(black)
#     # Presupuesto para
#     p.drawString(3 * cm, height - header_height - 1.5 * cm, "Presupuesto para:")

#     # Espacio para datos del cliente
#     p.setFont("Helvetica", 18)
#     p.drawString(3 * cm, height - header_height - 2.4 * cm, datos['cliente_nombre'])
    
#     p.setFont("Helvetica", 10)
#     p.drawString(3 * cm, height - header_height - 3.1 * cm, datos['cliente_telefono'])
#     p.drawString(3 * cm, height - header_height - 3.8 * cm, datos['cliente_email'])
    
#     # Información del presupuesto (en la misma línea)
#     p.drawString(width - 9 * cm, height - header_height - 1.5 * cm, f"Número de Presupuesto: {datos['presupuesto_numero']}")
#     p.drawString(width - 9 * cm, height - header_height - 2 * cm,   f"Fecha de Presupuesto: {datos['presupuesto_fecha']}")
#     p.drawString(width - 9 * cm, height - header_height - 2.5 * cm, f"Fecha de Ingreso:     {datos['ingreso_fecha']}")

#     # Términos y condiciones
#     stylesheet = getSampleStyleSheet()
#     custom_style = ParagraphStyle(
#         'CustomStyle',
#         parent=stylesheet['Normal'],
#         fontName='Helvetica',
#         fontSize=6,
#         leading=8,
#         alignment=4,  # Justificado
#         spaceAfter=6
#     )

#     terms = """
#     <b>Condiciones Generales del Servicio Técnico de Unitronic S.A</b><br/>
#     1. Los presupuestos son sin cargo.<br/>
#     2. La garantía de reparación es de 3 (tres) meses a partir de la fecha en que retiran el equipo. Dicha garantía cubre la reparación específica realizada.<br/>
#     3. La atención de equipos en garantía de venta se realizan exclusivamente con la presentación de la factura de venta.<br/>
#     4. Para retirar los equipos en reparación se debe presentar esta planilla.<br/>
#     5. Las garantías de reparación se realizan en nuestros laboratorios.<br/>
#     6. Pasados los 30 días de reparado el equipo y no es retirado se podrá cobrar almacenaje.<br/>
#     7. Los presupuestos emitidos vía whatsapp o mail no respondidos dentro de los 30 días derivarán en la devolución del equipo con el flete a cargo del cliente.<br/>
#     8. Cuando el cliente retira el equipo reparado o no, firma el comprobante de entrega presentando conformidad sobre el estado y accesorios presentes. No se aceptan reclamos posteriores salvo en lo especificado en el ítem garantía de reparación.<br/>
#     """
#     frame = Frame(2 * cm, 3 * cm, width - 6 * cm, 3 * cm, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
#     terms_paragraph = Paragraph(terms, custom_style)
#     frame.addFromList([terms_paragraph], p)

#     # Datos del equipo
#     table_data = [
#         ['DETALLE EQUIPO', '', '', '', ''],
#         ['Categoría:', datos['equipo_categoria'], '', 'Accesorios:', datos['equipo_accesorio1']],
#         ['Subcategoría:', datos['equipo_subcategoria'], '', '', datos['equipo_accesorio2']],
#         ['Modelo:', datos['equipo_modelo'], '', '', datos['equipo_accesorio3']],
#         ['Número de Serie:', datos['equipo_numero_serie'], '', '', datos['equipo_accesorio4']],
#         ['Garantía:', datos['equipo_garantia'], '', 'Insumos:', datos['equipo_insumos']],
#         ['Notas:', datos['equipo_notas'], '', '', ''],
#     ]

#     table = Table(table_data, colWidths=[3 * cm, 5 * cm, 0.5 * cm, 2.5 * cm, 4 * cm])
#     table_style = TableStyle([
#         ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
#         ('TEXTCOLOR', (0, 0), (-1, -1), black),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#         ('LINEBELOW', (0, 0), (-1, -1), 0.5, gray, 1, None, None),
#         ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 12),
#         ('SPAN', (0, 0), (1, 0)),
#     ])

#     table.setStyle(table_style)

#     # Ajustar posiciones
#     table.wrapOn(p, width, height)
#     table.drawOn(p, 3 * cm, height - header_height - 11 * cm)

#     # Datos del presupuesto
#     table_data = [
#         ['DESCRIPCION'],  # Title row
#         [datos['presupuesto_descripcion']],  # Description row
#         [f"TOTAL: ${datos['presupuesto_total']}"]  # Total row
#     ]

#     table = Table(table_data, colWidths=[15 * cm], rowHeights=[1 * cm, 4 * cm, 1 * cm])
#     table_style = TableStyle([
#         ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
#         ('TEXTCOLOR', (0, 0), (-1, -1), black),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
#         ('LINEBELOW', (0, 0), (-1, -1), 0.5, gray, 1, None, None),
#         ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 12),
#         ('SPAN', (0, 0), (0, 0)),
#         ('ALIGN', (0, 2), (-1, 2), 'RIGHT'), 
#         ('VALIGN', (0, 1), (0, 1), 'TOP'),
#         ('FONT', (0, 2), (-1, 2), 'Helvetica-Bold')  
#     ])

#     table.setStyle(table_style)

#     # Ajustar la posición de la nueva tabla
#     table.wrapOn(p, width, height)
#     table.drawOn(p, 3 * cm, height - header_height - 18 * cm)

#     p.showPage()
#     p.save()
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, Color, gray
from reportlab.platypus import Table, TableStyle, Paragraph, Frame
from io import BytesIO

def generar_template_presupuesto(response, datos):
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # (Resto del código de cabecera y pie de página aquí...)

    # Datos del equipo
    table_data = [
        ['DETALLE EQUIPO', '', '', '', ''],
        ['Categoría:', datos['equipo_categoria'], '', 'Accesorios:', datos['equipo_accesorio1']],
        ['Subcategoría:', datos['equipo_subcategoria'], '', '', datos['equipo_accesorio2']],
        ['Modelo:', datos['equipo_modelo'], '', '', datos['equipo_accesorio3']],
        ['Número de Serie:', datos['equipo_numero_serie'], '', '', datos['equipo_accesorio4']],
        ['Garantía:', datos['equipo_garantia'], '', 'Insumos:', datos['equipo_insumos']],
        ['Notas:', datos['equipo_notas'], '', '', ''],
    ]

    table = Table(table_data, colWidths=[3 * cm, 5 * cm, 0.5 * cm, 2.5 * cm, 4 * cm])
    table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, gray, 1, None, None),
        ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 12),
        ('SPAN', (0, 0), (1, 0)),
    ])
    table.setStyle(table_style)
    table.wrapOn(p, width, height)
    table.drawOn(p, 3 * cm, height - 11 * cm)

    # Sección de repuestos
    repuestos_data = [['Código', 'Nombre', 'Cantidad', 'Precio Unitario', 'Subtotal']]
    for repuesto in datos['repuestos']:
        repuestos_data.append([
            repuesto['codigo'],
            repuesto['nombre'],
            repuesto['cantidad'],
            f"${repuesto['precio_unitario']:.2f}",
            f"${repuesto['subtotal']:.2f}"
        ])

    repuestos_table = Table(repuestos_data, colWidths=[3 * cm, 5 * cm, 2.5 * cm, 3 * cm, 3 * cm])
    repuestos_table_style = TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),  # Cabecera en negrita
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, 0), black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, gray),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    repuestos_table.setStyle(repuestos_table_style)
    repuestos_table.wrapOn(p, width, height)
    repuestos_table.drawOn(p, 3 * cm, height - 18 * cm)

    p.showPage()
    p.save()


def generar_template_comprobante(response, datos):
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Colores definidos
    agua_color = Color(0.0, 194/255.0, 204/255.0)  # Color verde agua
    light_agua_color = Color(180/255.0, 237/255.0, 238/255.0)  # Color verde agua más claro

    # Configuraciones del Header
    header_height = 4 * cm
    logo_width = 6 * cm
    left_box_width = width - logo_width - 3 * cm

    # Dibuja el header
    p.setStrokeColor(light_agua_color)
    p.setLineWidth(1)
    p.line(0, height - header_height, width, height - header_height)

    # Rectángulo de la derecha (logo)
    logo_height = header_height - 0.5 * cm
    logo_x = left_box_width + (width - logo_width - left_box_width) / 2
    logo_y = height - header_height + (header_height - logo_height) / 2

    # Inserta la imagen del logo en el rectángulo derecho centrado
    

    p.drawImage("web/static/web/img/LogoUnitronic.png", logo_x, logo_y, 
                width=logo_width - 0.5 * cm, height=logo_height, preserveAspectRatio=True)

    # Rectángulos de la izquierda
    p.setFillColor(light_agua_color)
    p.rect(0, height - 2 * cm, left_box_width, 2 * cm, stroke=0, fill=1)

    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 26)  
    text_width = p.stringWidth("Orden de servicio", "Helvetica-Bold", 26)
    p.drawString((left_box_width - text_width) / 2, height - 3.5 * cm, "Orden de Servicio")

    # Configuración del Footer
    footer_rect_height = 11 * cm
    footer_width = width

    # Rectángulo verde agua oscuro de 1 cm de ancho y 11 cm de alto
    p.setFillColor(agua_color)
    p.rect(0, 0, 1 * cm, footer_rect_height, stroke=0, fill=1)

    # Rectángulo verde agua claro de 1 cm de alto, por el ancho restante
    p.setFillColor(light_agua_color)
    p.rect(1 * cm, 0, footer_width - 1 * cm, 1 * cm, stroke=0, fill=1)

    # Información de contacto de la empresa
    contact_y_position = 1.5 * cm  # Altura de los datos de contacto

    p.setFillColor(black)
    p.setFont("Helvetica", 8)
    p.drawString(2 * cm, contact_y_position, "+54 9 11 4300 9500")
    p.drawString(6 * cm, contact_y_position, "serviciotecnico@ecifra.com.ar")
    p.drawString(12 * cm, contact_y_position, "Peru 1028 - San Telmo - CP 1068")
    p.drawString(18 * cm, contact_y_position, "www.ecifra.com.ar")

    # Nuevo rectángulo verde agua en el borde derecho de la hoja
    p.setFillColor(agua_color)
    p.rect(width - 1 * cm, footer_rect_height, 1 * cm, 8 * cm, stroke=0, fill=1)

    # Placeholder para los datos dinámicos (sin rectángulos)
    p.setFont("Helvetica", 10)
    p.setFillColor(black)
    # Presupuesto para
    p.drawString(3 * cm, height - header_height - 1.5 * cm, "Cliente:")

    # Espacio para datos del cliente
    p.setFont("Helvetica", 18)
    p.drawString(3 * cm, height - header_height - 2.4 * cm, datos['cliente_nombre'])
    
    p.setFont("Helvetica", 10)
    p.drawString(3 * cm, height - header_height - 3.1 * cm, datos['cliente_telefono'])
    p.drawString(3 * cm, height - header_height - 3.8 * cm, datos['cliente_email'])
    
    # Información del presupuesto (en la misma línea)
    p.drawString(width - 9 * cm, height - header_height - 1.5 * cm, f"Número de Orden: {datos['orden_numero']}")
    p.drawString(width - 9 * cm, height - header_height - 2 * cm,   f"Fecha de Ingreso: {datos['ingreso_fecha']}")

    # Términos y condiciones
    stylesheet = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=stylesheet['Normal'],
        fontName='Helvetica',
        fontSize=6,
        leading=8,
        alignment=4,  # Justificado
        spaceAfter=6
    )

    terms = """
    <b>Condiciones Generales del Servicio Técnico de Unitronic S.A</b><br/>
    1. Los presupuestos son sin cargo.<br/>
    2. La garantía de reparación es de 3 (tres) meses a partir de la fecha en que retiran el equipo. Dicha garantía cubre la reparación específica realizada.<br/>
    3. La atención de equipos en garantía de venta se realizan exclusivamente con la presentación de la factura de venta.<br/>
    4. Para retirar los equipos en reparación se debe presentar esta planilla.<br/>
    5. Las garantías de reparación se realizan en nuestros laboratorios.<br/>
    6. Pasados los 30 días de reparado el equipo y no es retirado se podrá cobrar almacenaje.<br/>
    7. Los presupuestos emitidos vía whatsapp o mail no respondidos dentro de los 30 días derivarán en la devolución del equipo con el flete a cargo del cliente.<br/>
    8. Cuando el cliente retira el equipo reparado o no, firma el comprobante de entrega presentando conformidad sobre el estado y accesorios presentes. No se aceptan reclamos posteriores salvo en lo especificado en el ítem garantía de reparación.<br/>
    """
    frame = Frame(2 * cm, 3 * cm, width - 6 * cm, 3 * cm, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    terms_paragraph = Paragraph(terms, custom_style)
    frame.addFromList([terms_paragraph], p)

    # Datos del equipo
    table_data = [
        ['DETALLE EQUIPO', '', '', '', ''],
        ['Categoría:', datos['equipo_categoria'], '', 'Accesorios:', datos['equipo_accesorio1']],
        ['Subcategoría:', datos['equipo_subcategoria'], '', '', datos['equipo_accesorio2']],
        ['Modelo:', datos['equipo_modelo'], '', '', datos['equipo_accesorio3']],
        ['Número de Serie:', datos['equipo_numero_serie'], '', '', datos['equipo_accesorio4']],
        ['Garantía:', datos['equipo_garantia'], '', 'Insumos:', datos['equipo_insumos']],
        ['', '', '', ''],
        ['Notas:', datos['equipo_notas'], '', '', ''],
    ]

    table = Table(table_data, colWidths=[3 * cm, 5 * cm, 0.5 * cm, 2.5 * cm, 4 * cm])
    table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, gray, 1, None, None),
        ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 12),
        ('SPAN', (0, 0), (1, 0)),
    ])

    table.setStyle(table_style)

    # Ajustar posiciones
    table.wrapOn(p, width, height)
    table.drawOn(p, 3 * cm, height - header_height - 11 * cm)

    # notas de la orden
    table_data = [
        ['DESCRIPCION'],  # Title row
        [datos['equipo_notas']],  # Description row
    ]

    table = Table(table_data, colWidths=[15 * cm], rowHeights=[1 * cm, 4 * cm])
    table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, gray, 1, None, None),
        ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 12),
        ('SPAN', (0, 0), (0, 0)),
        ('ALIGN', (0, 2), (-1, 2), 'RIGHT'), 
        ('VALIGN', (0, 1), (0, 1), 'TOP'),
        ('FONT', (0, 2), (-1, 2), 'Helvetica-Bold')  
    ])

    table.setStyle(table_style)

    # Ajustar la posición de la nueva tabla
    table.wrapOn(p, width, height)
    table.drawOn(p, 3 * cm, height - header_height - 18 * cm)

    p.showPage()
    p.save()
