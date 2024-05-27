from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.conf import settings
import os

def generate_collection_report(collection, books):
    """
    Генерирует PDF-отчет о коллекции книг.

    Args:
        collection: Объект коллекции.
        books: Список объектов книг в коллекции.
    """
    # Путь для сохранения файла
    report_name = f'collection_{collection.id}_report.pdf'
    media_root = settings.MEDIA_ROOT
    report_path = os.path.join(media_root, report_name)

    doc = SimpleDocTemplate(report_path, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Заголовок отчета
    story.append(Paragraph(f"Отчет по коллекции: {collection.name}", styles['Heading1']))
    story.append(Spacer(1, 0.5 * inch))

    # Информация о каждой книге
    for book in books:
        story.append(Paragraph(f"Название: {book.title}", styles['Normal']))
        authors = ", ".join([author.name for author in book.authors.all()])
        story.append(Paragraph(f"Авторы: {authors}", styles['Normal']))
        publishers = ", ".join([publisher.name for publisher in book.publishers.all()])
        story.append(Paragraph(f"Издательство: {publishers}", styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)

    return report_name, report_path