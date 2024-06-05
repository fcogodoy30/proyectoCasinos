import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A7
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.shortcuts import render
from .models import CasinoColacion


def generar_ticket(request, usuario_id, fecha):
    try:
        datos = CasinoColacion.objects.get(id=usuario_id, fecha_servicio=fecha)
        # Creamos un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Adjuntamos el PDF al response con el nombre de archivo "ticket.pdf"
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

        # Creamos un objeto PDF usando ReportLab
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A7), rightMargin=5, leftMargin=5, topMargin=5, bottomMargin=5)
        styles = getSampleStyleSheet()

        # Definimos un estilo para los párrafos centrados
        centered_style = ParagraphStyle(name="Centered", alignment=TA_CENTER)

        # Agregamos el contenido al PDF
        content = []
        content.append(Paragraph("Ticket Menu", styles['Title']))
        content.append(Paragraph(f"Usuario: {datos.id}", centered_style))
        content.append(Paragraph(f"Fecha: {datos.fecha_servicio}", centered_style))
        # Agrega más detalles del ticket según tus necesidades

        doc.build(content)

        # Adjuntamos el contenido del objeto PDF al response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response
    except CasinoColacion.DoesNotExist:
        return render(request, 'error.html', {'message': 'Datos no encontrados'})