import datatypes

def render_to_reportlab_canvas(c, manager, papersize_tuple):
    manager.render(datatypes.Rectangle(0, 0, papersize_tuple), dict(output=c))

def render_to_reportlab_document(filename, manager, papersize_tuple):
    
