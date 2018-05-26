# -*- coding: utf-8 -*-

"""Cairo support.

Cairo uses a coordinate system where y increases from the bottom     of the
page upwards. Layout assumes the opposite coordinate system. So     the
context will be reversed in the y direction, and then text will     need to
be reversed back.
"""

import math

from layout.datatypes import output, Rectangle

try:
    import cairocffi as cairo
except ImportError:
    try:
        import cairo
    except ImportError:
        import warnings
        warnings.warn(
            "Cairo not found - you will not be able to generate documents.",
            ImportWarning
            )

def render_to_cairo_context(cairo_context, papersize_tuple, layout):
    """Renders the given layout manager on a page of the given context.

    Assumes the given context has not yet been reversed in the y-direction
    (i.e. it is still the default for Cairo, where y increases up
    from the bottom of the page). This method performs the reversal and
    resets it before it returns.
    """
    try:
        cairo_context.save()
        cairo_context.translate(0, papersize_tuple[1])
        cairo_context.scale(1, -1)
        layout.render(
            Rectangle(0, 0, *papersize_tuple),
            dict(output=CairoOutput(cairo_context))
            )
    finally:
        cairo_context.restore()

def render_to_cairo_document(output_filename, papersize_tuple, layout):
    """Create and save a document with contents of the given layout manager."""
    doc = cairo.PDFSurface(output_filename, *papersize_tuple)
    c = cairo.Context(doc)
    render_to_cairo_context(c, papersize_tuple, layout)

class CairoOutput(output.OutputTarget):
    """An output adapter for Cairo.

    Assumes the Cairo context has already been reversed in the y-direction
    (i.e. so y increases downwards from the top of the page).
    """
    def __init__(self, cairo_context):
        self.c = cairo_context

    def _save_state(self):
        self.c.save()

    def _restore_state(self):
        self.c.restore()

    def translate(self, x, y):
        self.c.translate(x, y)

    def scale(self, x, y):
        self.c.scale(x, y)

    def rotate(self, degrees):
        self.c.rotate(degrees * math.pi / 180)

    def text_width(self, text, *, font_name, font_size):
        c = self.c
        c.save()
        c.select_font_face(font_name)
        c.set_font_size(font_size)
        _, _, _, _, x_adv, _ = c.text_extents(text)
        c.restore()
        return x_adv

    def draw_text(self, text, x, y, *, font_name, font_size, fill):
        c = self.c
        c.save()
        c.select_font_face(font_name)
        c.set_font_size(font_size)
        c.set_source_rgb(*fill)
        c.translate(x, y)
        c.move_to(0, 0)
        c.scale(1, -1)
        c.show_text(text)
        c.restore()

    def _fill_and_stroke(self, stroke, stroke_width, stroke_dash, fill):
        c = self.c
        if fill:
            c.set_source_rgb(*fill)
            c.fill_preserve()
        if stroke:
            c.set_source_rgb(*stroke)
            c.set_line_width(stroke_width)
            if stroke_dash:
                c.set_dash(stroke_dash)
            c.stroke()
        c.new_path()

    def draw_line(
            self, x0, y0, x1, y1, *,
            stroke,
            stroke_width=1,
            stroke_dash=None):
        c = self.c
        c.save()
        c.new_path()
        c.move_to(x0, y0)
        c.line_to(x1, y1)
        self._fill_and_stroke(stroke, stroke_width, stroke_dash, None)
        c.restore()

    def draw_rect(
            self, x, y, w, h, *,
            stroke=None,
            stroke_width=1,
            stroke_dash=None,
            fill=None
            ):
        c = self.c
        c.save()
        c.new_path()
        c.rectangle(x, y, w, h)
        self._fill_and_stroke(stroke, stroke_width, stroke_dash, fill)
        c.restore()

    def draw_image(self, img_filename, x, y, w, h):
        raise NotImplemented()

    def draw_polygon(
            self,
            *pts,
            close_path=True,
            stroke=None,
            stroke_width=1,
            stroke_dash=None,
            fill=None
            ) -> None:
        """Draws the given polygon."""
        c = self.c
        c.save()
        c.new_path()
        for x,y in zip(*[iter(pts)]*2):
            c.line_to(x, y)
        if close_path:
            c.close_path()
        self._fill_and_stroke(stroke, stroke_width, stroke_dash, fill)
        c.restore()

    def end_page(self):
        self.c.show_page()

    def clip_rect(self, x, y, w, h):
        c = self.c
        c.rectangle(x, y, w, h)
        c.clip()
