import layout.managers.root as root
from layout.datatypes import Rectangle

class SignatureMark(root.LayoutElement):
    """A signature mark.

    Signature marks appear on the ouside of the fold of a set of pages
    gathered into a signature for bookbinding. The signature mark allows
    the binder to quickly collate the signatures and to quickly see if
    any are in the wrong position.

    This signature mark should be overlaid on the first page of each
    signature. It appears in the left-hand margin. Note that the signature
    mark is drawn outside of the rendering rectangle it is given, so that
    it can be seen across the eventual fold. This means that if you render
    the mark in a manager that crops its contents, the cropped part of the
    mark will be lost, and its functionality might be compromised.

    Normally you don't deal with these marks manually, they are added for
    you by the page imposition system in :mod:`layout.pages.imposition`.

    Historically signature marks were not placed in the spine, but in the
    foot of the first page of each signature and were numbered.
    """
    def __init__(self, index, total, width=1, color=(0,0,0), margin=0.1):
        """
        Arguments:

        ``index``
            Which signature in the book is this?

        ``total``
            How many signatures are there in total?

        ``width``
            How wide should the mark be (the default, 1pt is usually fine).

        ``color``
            What color should the mark be (default (0,0,0) black).

        ``margin``
            How much of the spine at the top and bottm should be left
            unmarked (this figure is given as a proportion). This
            should be a fair size (0.1, by default), to stop the mark
            being visible when looking at the head or foot of the
            finished book.
        """
        self.index = index
        self.total = total
        self.width = width
        self.color = color
        self.margin = margin

    def get_minimum_size(self, data):
        return Rectangle()

    def render(self, rectangle, data):
        """Draws the signature mark.

        Note that this draws OUTSIDE the rectangle we're given. If
        cropping is involved, then this obviously won't work."""

        size = (1.0 - 2.0*self.margin) * rectangle.h
        offset = self.margin * rectangle.h
        per_mark = 1.0 / float(self.total)
        bottom = offset + size * float(self.index) * per_mark
        top = bottom + per_mark * size

        c = data['output']
        with c:
            c.translate(rectangle.x, rectangle.y)
            c.draw_polygon(
                0, top, -self.width, bottom, self.width, bottom,
                fill=self.color
                )
