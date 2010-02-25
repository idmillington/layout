import layout.managers.root as root
import layout.datatypes as datatypes

class LineBase(root.LayoutElement):
    """The base class for various kinds of line."""

    def __init__(self, color=(0,0,0), width=1, dash=None):
        self.color = color
        self.width = width
        self.dash = dash

    def get_minimum_size(self, data):
        raise NotImplementedError()

class HorizontalLine(LineBase):
    """Draws a horizontal line in the center of any space it is given."""

    def get_minimum_size(self, data):
        return datatypes.Point(0, self.width)

    def render(self, rect, data):
        c = data['output']
        c.saveState()
        c.setStrokeColorRGB(*self.color)
        c.setLineWidth(self.width)
        c.setDash(self.dash)
        c.line(rect.left, rect.middle, rect.right, rect.middle)
        c.restoreState()

class VerticalLine(LineBase):
    """Draws a vertical line in the center of any space it is given."""

    def get_minimum_size(self, data):
        return datatypes.Point(self.width, 0)

    def render(self, rect, data):
        c = data['output']
        c.saveState()
        c.setStrokeColorRGB(*self.color)
        c.setLineWidth(self.width)
        c.setDash(self.dash)
        c.line(rect.center, rect.bottom, rect.center, rect.top)
        c.restoreState()
        
class Border(LineBase):
    """Draws a line surrounding the space, with an optional additional
    color for fill."""

    def __init__(self, color=(0,0,0), background=None, width=1, dash=None):
        super(Border, self).__init__(color, width, dash)
        self.background = background

    def get_minimum_size(self, data):
        return datatypes.Point(self.width*2, self.width*2)

    def render(self, rect, data):
        c = data['output']
        c.saveState()
        c.setStrokeColorRGB(*self.color)
        if self.background is not None: c.setFillColorRGB(*self.background)
        c.setLineWidth(self.width)
        c.setDash(self.dash)
        c.rect(*rect.get_data(),
                **dict(stroke=True, fill=(self.background is not None)))
        c.restoreState()
        
