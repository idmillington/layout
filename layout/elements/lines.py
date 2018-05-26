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
        data['output'].draw_line(
            rect.left, rect.middle, rect.right, rect.middle,
            stroke=self.color, stroke_width=self.width, stroke_dash=self.dash
            )

class VerticalLine(LineBase):
    """Draws a vertical line in the center of any space it is given."""

    def get_minimum_size(self, data):
        return datatypes.Point(self.width, 0)

    def render(self, rect, data):
        data['output'].draw_line(
            rect.center, rect.bottom, rect.center, rect.top,
            stroke=self.color, stroke_width=self.width, stroke_dash=self.dash
            )

class Border(LineBase):
    """Draws a line surrounding the space, with an optional additional
    color for fill."""

    def __init__(self, color=(0,0,0), background=None, width=1, dash=None,
                 top=True, right=True, bottom=True, left=True):
        super(Border, self).__init__(color, width, dash)
        self.background = background
        self.directions = (top, right, bottom, left)
        self.full_box = top and right and bottom and left

    def get_minimum_size(self, data):
        return datatypes.Point(self.width*2, self.width*2)

    def render(self, rect, data):
        c = data['output']
        with c:
            if self.full_box:
                c.draw_rect(
                    *rect.get_data(),
                     stroke=self.color, stroke_width=self.width,
                     stroke_dash=self.dash,
                     fill=self.background
                     )
            else:
                if self.background is not None:
                    c.draw_rect(
                        *rect.get_data(),
                         fill=self.background
                         )
                if self.color is not None:
                    def _line(pos1, pos2):
                        c.draw_line(
                            pos1.x, pos1.y, pos2.x, pos2.y,
                            stroke=self.color, stroke_width=self.width,
                            stroke_dash=self.dash
                            )
                    if self.directions[0]:
                        _line(rect.top_left, rect.top_right)
                    if self.directions[1]:
                        _line(rect.top_right, rect.bottom_right)
                    if self.directions[2]:
                        _line(rect.bottom_right, rect.bottom_left)
                    if self.directions[3]:
                        _line(rect.bottom_left, rect.top_left)

class Fill(Border):
    """
    Draws a solid color fill with no outline.
    """
    def __init__(self, color=(0, 0, 0)):
        super(Fill, self).__init__(None, color)
