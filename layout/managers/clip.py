from . import root

class ClipLM(root.LayoutManager):
    """
    A ReportLab-specific layout manager that establishes a clipping
    box around its child element's content before rendering it.

    Because most elements and managers reserve the minimum amount of
    space they need to draw, this manager would have no effect. In
    some cases, particularly with managers in the
    :mod:`~layout.managers.fixed` or :mod:`~layout.managers.jitter`
    modules, the drawing is outside the reserved space, this manager
    ensures any content that does overlap is trimmed.
    """
    def __init__(self, element=None):
        self.element = element

    def get_minimum_size(self, data):
        return self.element.get_minimum_size(data)

    def render(self, rect, data):
        # Set the crop.
        c = data['output']
        with c:
            c.clip_rect(rect.x, rect.y, rect.w, rect.h)
            self.element.render(rect, data)
