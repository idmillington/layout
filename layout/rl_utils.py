import datatypes
from reportlab.pdfgen.canvas import Canvas

def render_to_reportlab_canvas(rl_canvas, papersize_tuple, manager):
    """Renders the given manager full size on a page of the given canvas."""
    manager.render(
        datatypes.Rectangle(0, 0, *papersize_tuple),
        dict(output=rl_canvas)
        )

def render_to_reportlab_document(output_filename, papersize_tuple, manager):
    """Creates a complete document in which to render the given manager."""
    c = Canvas(output_filename, papersize_tuple)
    render_to_reportlab_canvas(c, papersize_tuple, manager)
    c.save()
    
