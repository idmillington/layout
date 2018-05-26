import layout.managers.root as root
import layout.datatypes as datatypes

class Spacer(root.LayoutElement):
    """Reserves a specific amount of blank space.

    The space reserved is not proportional to the space provided, so this
    class is normally used with a scaling layout manager or to perform
    fine grained movement of elements on a page."""

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    def get_minimum_size(self, data):
        return datatypes.Point(self.width, self.height)

    def render(self, rect, data):
        pass
