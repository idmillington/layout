"""This module provides helper functions to render managers to one or
more pages of a reportlab canvas. To create multi-page documents, use
the :class:`layout.pages.output.PagesLM` class to wrap a series of
single-page managers."""

import datatypes

try:
    from reportlab.pdfgen.canvas import Canvas
except ImportError:
    import warnings
    warnings.warn(
        "Reportlab not found - you will not be able to generate pdf documents.",
        ImportWarning
        )

def render_to_reportlab_canvas(rl_canvas, papersize_tuple, manager):
    """Renders the given manager full size on a page of the given canvas."""
    rl_canvas.setPageSize(papersize_tuple)
    manager.render(
        datatypes.Rectangle(0, 0, *papersize_tuple),
        dict(output=rl_canvas)
        )

def render_to_reportlab_document(output_filename, papersize_tuple, manager):
    """Creates a complete document in which to render the given manager."""
    c = Canvas(output_filename, papersize_tuple)
    render_to_reportlab_canvas(c, papersize_tuple, manager)
    c.save()
