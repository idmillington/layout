import os.path
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..', '..')))

import random

from layout.elements import *
from layout.managers import *
from layout.managers.root import *
from layout.datatypes import *
from layout.pages.imposition import *
from layout.pages.output import *

def create_book(page_size):
    pages = []
    for i in range(64):
        recto = (i%2 == 1)
        page_number = TextLine(
            str(i+1), font_size=72, color=(0.9, 0.9, 0.9),
            align=TextBase.ALIGN_CENTER
            )
        rotated = \
            AnyRotationLM(-0.4 if recto else 0.4, element=page_number)
        aligned = \
            AlignLM(0, 0, AlignLM.ALIGN_LEFT if recto else AlignLM.ALIGN_RIGHT,
                    AlignLM.ALIGN_BOTTOM, element=rotated)
                    
        inner_content = RecursionStopperLM(1)
        inner_overlay = OverlayLM([
            Border(width=0.25, background=(1.0, 1.0, 1.0)),
            ClipLM(UnstableRandomJitterLM(math.pi*0.05, 0, 0, 
                ScaleLM(FixedSizeLM(Point(*A4), inner_content))
                )),
            ])
        text_block = VanDeGraafCanonLM(recto, inner_overlay)
        
        page = OverlayLM([
            Border(width=0.25, background=(0.5, 1.0, 0)),
            aligned, 
            text_block
            ])
        inner_content.element = page
            
        pages.append(page)
        
    pages = get_page_impositions(
        FORMAT_16_PAGE,
        fold_then_collate=False, sheets_per_sig=2,
        signature_mark=1, elements=pages
        )
    pp = PagesLM(pages)

    c = Canvas(os.path.join(BASE_DIR, 'output', 'imposition.pdf'), page_size)
    pp.render(Rectangle(0, 0, *page_size), dict(output=c))
    c.save()

if __name__ == '__main__':
    from reportlab.pdfgen.canvas import Canvas
    path = os.path.join(BASE_DIR, 'output')
    if not os.path.exists(path): os.makedirs(path)
    
    create_book(landscape(A4))