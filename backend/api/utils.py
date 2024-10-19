from collections import namedtuple
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def ingredients_list(recipe_list):
    ingredients = {}
    for recipe in recipe_list:
        for _ in recipe.recipe_ingredients.select_related('ingredient').all():
            key = (_.ingredient.name, _.ingredient.measurement_unit)
            if key not in ingredients:
                ingredients[key] = 0
            ingredients[key] += _.amount

    return [ShoppingListItem(name, amount, measurement_unit)
            for ((name, measurement_unit), amount) in ingredients.items()]


def pdf_shopping_list(shopping_list, user):

    def header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Arial', 12)
        header_text = 'Список покупок'
        footer_text = 'FoodGram @ 2024'
        w, h = doc.pagesize
        canvas.drawString(inch, h - 0.8 * inch, header_text)
        canvas.drawString(inch, 0.5 * inch, footer_text)
        canvas.restoreState()

    pdfmetrics.registerFont(
        TTFont('Arial', 'data_font/SpecialElite.ttf')
    )
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        title='Shopping List'
    )

    data = [
        ['Ингредиенты', 'Количество']
    ]

    for ingredient in shopping_list:
        data.append([ingredient[0], f'{ingredient[1]} {ingredient[2]}'])

    table = Table(data)
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (-1, 0), (0, 0), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 100),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ("FONTSIZE", (0, 0), (-1, -1), 13),
        ("LINEBELOW", (0, -1), (-1, -1), 1, colors.gray),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0, colors.white)
    ]))

    doc.build(
        [table],
        onFirstPage=header_footer,
        onLaterPages=header_footer
    )
    buffer.seek(0)

    return buffer


ShoppingListItem = namedtuple(
    'ShoppingListItem',
    ['name', 'amount', 'measurement_unit']
)
