from layout import datatypes
from . import root

class FixedSizeLM(root.LayoutManager):
    """
    A layout manager that always renders its children at a specific
    size, regardless of whether it is given enough room or not.

    This layout manager is useful for displaying illustrations of a page
    within another page. It draws the inner page at a specific size.

    Because this layout manager basically ignores the size of the
    rectangle that it is given, it may draw content overlapping into
    surrounding content. It is common, therefore, to place this layout
    manager into one of the scaling layout managers in
    :mod:`layout.managers.transform`, to make sure it fits.
    """
    def __init__(self, size, element=None):
        self.size = size
        self.element = element

    def get_minimum_size(self, data):
        return self.size

    def render(self, rectangle, data):
        rect = datatypes.Rectangle(
            rectangle.x, rectangle.y,
            self.size.x, self.size.y
            )
        self.element.render(rect, data)

class AbsolutePositionLM(root.LayoutManager):
    """
    A layout manager that positions it children at specific
    positions.

    Because this layout manager basically ignores the size of the
    rectangle that it is given, it may draw content overlapping into
    surrounding content. It is common, therefore, to place this layout
    manager into one of the scaling layout managers in
    :mod:`layout.managers.transform`, to make sure it fits.
    """
    def __init__(self):
        self.elements = []

    def add_element(self, element, rect):
        """Sets the position of the given element. The same element
        can be added multiple times in different positions."""
        self.elements.append((element, rect))

    def get_minimum_size(self):
        # To calculate this, we simply find its farthest right and
        # down, ignoring any element that starts to the left or below
        # zero.
        max_x, max_y = 0, 0
        for item, rect in self.elements:
            max_x = max(max_x, rect.r)
            max_y = max(max_y, rect.t)
        return datatypes.Point(max_x, max_y)

    def render(self, rectangle, data):
        for item, rect in self.elements:
            item.render(rect, data)
