import os.path
import sys
import random

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

from layout.elements import *
from layout.managers import *
from layout.managers.root import *
from layout.datatypes import *
from layout.pages.imposition import *
from layout.pages.output import *
from layout import rl_utils

def create_book(papersize):
    pages = []
    for i in range(64):
        recto = (i%2 == 1)
        page_number = TextLine(
            str(i+1), font_size=72, color=(0.4, 0.4, 0.4),
            align=TextBase.ALIGN_CENTER
            )
        rotated = AnyRotationLM(-0.4 if recto else 0.4, element=page_number)
        aligned = AlignLM(
            0, 0,
            AlignLM.ALIGN_LEFT if recto else AlignLM.ALIGN_RIGHT,
            AlignLM.ALIGN_BOTTOM, element=rotated)

        inner_content = RecursionStopperLM(8)
        inner_overlay = OverlayLM([
            Border(width=0, background=(1.0, 1.0, 1.0)),
            ClipLM(
                UnstableRandomJitterLM(math.pi*0.05, 0, 0, inner_content)
                ),
            Border(width=0.25),
            ])
        text_block = VanDeGraafCanonLM(recto, inner_overlay)

        page = ScaleLM(FixedSizeLM(Point(*papersize), OverlayLM([
            Border(width=0, background=(0.85, 1.0, 0.7)),
            aligned,
            text_block,
            Border(width=0.25)
            ])))
        inner_content.element = page

        pages.append(page)

    pages = get_page_impositions(
        FORMAT_16_PAGE,
        fold_then_collate=False, sheets_per_sig=2,
        signature_mark=1, elements=pages
        )
    pp = PagesLM(pages)

    out = os.path.join(BASE_DIR, 'imposition.pdf')
    rl_utils.render_to_reportlab_document(out, papersize, pp)

if __name__ == '__main__':
    mm = 72 / 25.4
    papersize = (297*mm, 210*mm)
    create_book(papersize)
