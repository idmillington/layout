import datatypes
from reportlab.pdfgen.canvas import Canvas

def render_to_reportlab_canvas(rl_canvas, manager, papersize_tuple):
    """Renders the given manager full size on a page of the given canvas."""
    manager.render(
        datatypes.Rectangle(0, 0, papersize_tuple),
        dict(output=rl_canvas)
        )

def render_to_reportlab_document(output_filename, manager, papersize_tuple):
    """Creates a complete document in which to render the given manager."""
    c = Canvas(output_filename, papersize_tuple)
    render_to_reportlab_canvas(c, manager, papersize_tuple)
    c.showPage()
    c.save()
    
