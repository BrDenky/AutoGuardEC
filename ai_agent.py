from flask import Blueprint, request, jsonify, send_file, current_app
from openai import OpenAI
import os
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import json
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI con la API key desde .env
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/api/ai_agent', methods=['POST'])
def generate_report():
    from app import app, db
    from app import Policy

    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')

        with app.app_context():
            total_policies = db.session.query(Policy).count()
            total_policies = db.session.query(Policy).all()

        system_prompt = """Eres un experto analista de seguros que genera reportes profesionales.
Debes responder ÚNICAMENTE en formato JSON con esta estructura:
{
  "titulo": "Título del reporte",
  "resumen_ejecutivo": "Resumen breve del reporte (2-3 líneas)",
  "objetivos": ["Objetivo 1", "Objetivo 2", "Objetivo 3"],
  "analisis": "Análisis detallado (3-5 párrafos)",
  "observaciones": ["Observación 1", "Observación 2", "Observación 3"],
  "graficas": [
    {
      "tipo": "barras",
      "titulo": "Título de la gráfica",
      "datos": {"labels": ["A", "B"], "values": [10, 20]}
    }
  ],
  "conclusiones": "Conclusiones finales (2-3 párrafos)",
  "recomendaciones": ["Recomendación 1", "Recomendación 2"]
}"""

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n\nDatos disponibles: Total de pólizas registradas: {total_policies}"}
            ],
            temperature=0.7
        )

        response_text = completion.choices[0].message.content
        
        # Limpiar el texto si viene con markdown
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        report_data = json.loads(response_text)

        # Generar PDF profesional
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=14, spaceAfter=12))
        
        story = []

        # Portada
        story.append(Spacer(1, 2*inch))
        title = Paragraph(f"<b>{report_data.get('titulo', 'Reporte de Pólizas')}</b>", 
                         ParagraphStyle(name='Title', fontSize=24, alignment=TA_CENTER, spaceAfter=30))
        story.append(title)
        
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("<b>AutoGuardEC</b>", styles['Center']))
        story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", styles['Center']))
        story.append(PageBreak())

        # Resumen Ejecutivo
        story.append(Paragraph("<b>RESUMEN EJECUTIVO</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(report_data.get('resumen_ejecutivo', ''), styles['Justify']))
        story.append(Spacer(1, 20))

        # Objetivos
        story.append(Paragraph("<b>OBJETIVOS</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        for i, obj in enumerate(report_data.get('objetivos', []), 1):
            story.append(Paragraph(f"{i}. {obj}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 20))

        # Análisis
        story.append(Paragraph("<b>ANÁLISIS</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(report_data.get('analisis', ''), styles['Justify']))
        story.append(Spacer(1, 20))

        # Gráficas
        if report_data.get('graficas'):
            story.append(PageBreak())
            story.append(Paragraph("<b>ANÁLISIS GRÁFICO</b>", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            for grafica in report_data['graficas']:
                img_buffer = generar_grafica(grafica)
                if img_buffer:
                    img = Image(img_buffer, width=5*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 6))
                    story.append(Paragraph(f"<i>{grafica.get('titulo', '')}</i>", styles['Center']))
                    story.append(Spacer(1, 20))

        # Observaciones
        story.append(Paragraph("<b>OBSERVACIONES</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        for i, obs in enumerate(report_data.get('observaciones', []), 1):
            story.append(Paragraph(f"• {obs}", styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 20))

        # Conclusiones
        story.append(Paragraph("<b>CONCLUSIONES</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(report_data.get('conclusiones', ''), styles['Justify']))
        story.append(Spacer(1, 20))

        # Recomendaciones
        story.append(Paragraph("<b>RECOMENDACIONES</b>", styles['Heading1']))
        story.append(Spacer(1, 12))
        for i, rec in enumerate(report_data.get('recomendaciones', []), 1):
            story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            story.append(Spacer(1, 6))

        doc.build(story)
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name="reporte_profesional.pdf", mimetype='application/pdf')

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error al procesar la respuesta de IA: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generar_grafica(grafica_data):
    """Genera una gráfica usando matplotlib"""
    try:
        tipo = grafica_data.get('tipo', 'barras')
        titulo = grafica_data.get('titulo', '')
        datos = grafica_data.get('datos', {})
        labels = datos.get('labels', [])
        values = datos.get('values', [])

        fig, ax = plt.subplots(figsize=(8, 5))
        
        if tipo == 'barras':
            ax.bar(labels, values, color='#2E86AB')
        elif tipo == 'lineas':
            ax.plot(labels, values, marker='o', linewidth=2, color='#2E86AB')
        elif tipo == 'pie':
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        
        if tipo != 'pie':
            ax.set_xlabel('Categorías')
            ax.set_ylabel('Valores')
        
        ax.set_title(titulo)
        ax.grid(True, alpha=0.3)
        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        
        return img_buffer
    except Exception as e:
        print(f"Error generando gráfica: {e}")
        return None