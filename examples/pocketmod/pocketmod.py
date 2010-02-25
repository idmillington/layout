import os.path
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..', '..')))

from layout.elements import *
from layout.managers import *
from layout.managers.root import *
from layout.datatypes import *
from layout.pages.imposition import *
from layout.pages.output import *


def get_text_block(text):
    overlay = OverlayLM()
    overlay.add_element(Border((0.4, 0.6, 0.2), (0.9, 0.95, 0.85)))
    margins = MarginsLM(3*mm, 3*mm, 3*mm, 3*mm)
    margins.element = TextBlock(text)
    overlay.add_element(margins)
    return overlay

def create_pocketmod(page_size):
    pages = [
        OverlayLM([
                Border(),
                TextLine(str(i+1), font_size=72, align=TextBase.ALIGN_CENTER)
                ])
        for i in range(8)
        ]
    
    pps = [
        PagesLM(get_pocketmod_pages(pages, i % 2 > 0, i // 2 > 0))
        for i in range(4)
        ]

    c = Canvas(os.path.join(BASE_DIR, 'output', 'pockedmod.pdf'), page_size)
    for pp in pps:
        pp.render(Rectangle(0, 0, *page_size), dict(output=c))
    c.save()
    
    
if __name__ == '__main__':
    from reportlab.pdfgen.canvas import Canvas
    path = os.path.join(BASE_DIR, 'output')
    if not os.path.exists(path): os.makedirs(path)
    
    create_pocketmod(landscape(A4))