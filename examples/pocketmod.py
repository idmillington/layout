import os.path
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

from layout.elements import *
from layout.managers import *
from layout.managers.root import *
from layout.datatypes import *
from layout.pages.imposition import *
from layout.pages.output import *
from layout import rl_utils

def create_pocketmod(papersize):
    pages = [
        OverlayLM([
                Border(),
                TextLine(str(i+1), font_size=72, align=TextBase.ALIGN_CENTER)
                ])
        for i in range(8)
        ]

    pps = []
    for i in range(4):
        pps.extend(get_pocketmod_pages(pages, i % 2 > 0, i // 2 > 0))
    pp = PagesLM(pps)

    out = os.path.join(BASE_DIR, 'pocketmod.pdf')
    rl_utils.render_to_reportlab_document(out, papersize, pp)

if __name__ == '__main__':
    mm = 72 / 25.4
    papersize = (297*mm, 210*mm)
    create_pocketmod(papersize)
