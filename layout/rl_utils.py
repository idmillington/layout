"""This module provides helper functions to render managers to one or
more pages of a reportlab canvas. To create multi-page documents, use
the :class:`layout.pages.output.PagesLM` class to wrap a series of
single-page managers."""

from layout.datatypes import output, Point, Rectangle
import layout.managers.root as root

try:
    from reportlab.pdfgen.canvas import Canvas
except ImportError:
    import warnings
    warnings.warn(
        "Reportlab not found - you will not be able to generate pdf documents.",
        ImportWarning
        )

def render_to_reportlab_canvas(rl_canvas, papersize_tuple, layout):
    """Renders the given layout manager on a page of the given canvas."""
    rl_canvas.setPageSize(papersize_tuple)
    layout.render(
        Rectangle(0, 0, *papersize_tuple),
        dict(output=ReportlabOutput(rl_canvas))
        )

def render_to_reportlab_document(output_filename, papersize_tuple, layout):
    """Create and save a document with contents of the given layout manager."""
    c = Canvas(output_filename, papersize_tuple)
    render_to_reportlab_canvas(c, papersize_tuple, layout)
    c.save()

class ReportlabOutput(output.OutputTarget):
    """An output adapter for ReportLab."""

    def __init__(self, rl_canvas):
        self.c = rl_canvas

    def _save_state(self):
        self.c.saveState()

    def _restore_state(self):
        self.c.restoreState()

    def translate(self, x, y):
        self.c.translate(x, y)

    def scale(self, x, y):
        self.c.scale(x, y)

    def rotate(self, degrees):
        self.c.rotate(degrees)

    def text_width(self, text, *, font_name, font_size):
        return self.c.stringWidth(text, font_name, font_size)

    def draw_text(self, text, x, y, *, font_name, font_size, fill):
        c = self.c
        c.saveState()
        c.setFont(font_name, font_size)
        c.setFillColorRGB(*fill)
        c.drawString(x, y, text)
        c.restoreState()

    def draw_line(
            self, x0, y0, x1, y1, *,
            stroke,
            stroke_width=1,
            stroke_dash=None):
        c = self.c
        c.saveState()
        c.setStrokeColorRGB(*stroke)
        c.setLineWidth(stroke_width)
        c.setDash(stroke_dash)
        c.line(x0, y0, x1, y1)
        c.restoreState()

    def draw_rect(
            self, x, y, w, h, *,
            stroke=None,
            stroke_width=1,
            stroke_dash=None,
            fill=None
            ) -> None:
        c = self.c
        c.saveState()
        if stroke is not None:
            c.setStrokeColorRGB(*stroke)
            c.setLineWidth(stroke_width)
            c.setDash(stroke_dash)
        if fill is not None:
            c.setFillColorRGB(*fill)
        c.rect(x,y, w,h, stroke=(stroke is not None), fill=(fill is not None))
        c.restoreState()

    def draw_image(self, img_filename, x, y, w, h):
        self.c.drawImage(img_filename, x, y, w, h)

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
        c.saveState()

        if stroke is not None:
            c.setStrokeColorRGB(*stroke)
            c.setLineWidth(stroke_width)
            c.setDash(stroke_dash)
        if fill is not None:
            c.setFillColorRGB(*fill)

        p = c.beginPath()
        fn = p.moveTo
        for x,y in zip(*[iter(pts)]*2):
            fn(x, y)
            fn = p.lineTo
        if close_path:
            p.close()

        c.drawPath(p, stroke=(stroke is not None), fill=(fill is not None))
        c.restoreState()

    def end_page(self):
        self.c.showPage()

    def clip_rect(self, x, y, w, h):
        c = self.c
        p = c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x + w, y)
        p.lineTo(x + w, y + h)
        p.lineTo(x, y + h)
        p.close()
        c.clipPath(p, stroke=False, fill=False)

# ----------------------------------------------------------------------
# RL-only elements.
# ----------------------------------------------------------------------

try:
    from pdfrw import PdfReader
    from pdfrw.buildxobj import pagexobj
    from pdfrw.toreportlab import makerl
except ImportError:
    import warnings
    warnings.warn(
        "PDFRW not found - you will not be able to use pdf image elements.",
        ImportWarning
        )

class PDFImage(root.LayoutElement):
    """A PDF file to be displayed at a fixed aspect ratio."""

    def __init__(self, filename):
        pages = PdfReader(filename).pages
        num_pages = len(pages)
        assert num_pages > 0
        if num_pages > 1:
            warning.warn("PDF file %s has %d pages, using only the first." % (
                filename, num_pages
                ))
        self.pagexobj = pagexobj(pages[0])

    def get_minimum_size(self, data):
        page = self.pagexobj
        return Point(page.BBox[2] - page.BBox[0], page.BBox[3] - page.BBox[1])

    def render(self, rectangle, data):
        page = self.pagexobj

        # Scale and translate.
        w, h = page.BBox[2] - page.BBox[0], page.BBox[3] - page.BBox[1]
        x_scale = rectangle.w / w
        y_scale = rectangle.h / h
        scale = min(x_scale, y_scale)
        extra_x = (rectangle.w - w * scale)*0.5
        extra_y = (rectangle.h - h * scale)*0.5

        # Include the pdf as a form.
        c = data['output']
        c.saveState()
        c.translate(rectangle.x, rectangle.y)
        c.translate(extra_x, extra_y)
        c.scale(scale, scale)
        c.translate(page.BBox[0], page.BBox[1])
        c.doForm(makerl(c, page))
        c.restoreState()
