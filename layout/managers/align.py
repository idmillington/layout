from layout import datatypes
from . import root

class AlignLM(root.LayoutManager):
    """
    A layout manager that takes one element and aligns it according to
    the given parameters, optionally within a box of at least a given
    size. Several of the other layout managers do some alignment as
    part of their normal behavior.
    """
    #: Align the element to the top of the space.
    ALIGN_TOP = 0

    #: Align the element to the vertical middle of the space.
    ALIGN_MIDDLE = 1

    #: Align the element to the bottom of the space.
    ALIGN_BOTTOM = 2

    #: Align the element to top and bottom, making it grow vertically.
    GROW_Y = 3

    #: Align the element to the left of the space.
    ALIGN_LEFT = 10

    #: Align the element to the horizontal center of the space.
    ALIGN_CENTER = 11

    #: Align the element to the right of the space.
    ALIGN_RIGHT = 12

    #: Align the element to left and right, making it grow horizontally.
    GROW_X = 13

    def __init__(self,
                 min_width=0, min_height=0,
                 horizontal_align=ALIGN_LEFT,
                 vertical_align=ALIGN_TOP,
                 element=None):
        """
        Arguments:

        ``min_width``
            The minimum width to reserve, even if the managed element
            is smaller.

        ``min_height``
            The minimum height to reserve, even if the managed element
            is smaller.

        ``horizontal_align``
            One of the constants defined in this class for how the
            element should be aligned horizontally within its space
            (default: :data:`ALIGN_LEFT`)

        ``vertcal_align``
            One of the constants defined in this class for how the
            element should be aligned vertically within its space
            (default: :data:`ALIGN_TOP`)
        """
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.element = element
        self.min_width = min_width
        self.min_height = min_height

    def get_minimum_size(self, data):
        """Returns the minimum size of the managed element, as long as
        it is larger than any manually set minima."""
        size = self.element.get_minimum_size(data)
        return datatypes.Point(
            max(size.x, self.min_width),
            max(size.y, self.min_height)
            )

    def render(self, rect, data):
        """Draws the managed element in the correct alignment."""
        # We can't use our get minimum size, because that enforces
        # the size limits.
        size = self.element.get_minimum_size(data)

        # Assume we're bottom left at our natural size.
        x = rect.x
        y = rect.y
        w = size.x
        h = size.y

        extra_width = rect.w - w
        extra_height = rect.h - h

        if self.horizontal_align == AlignLM.ALIGN_CENTER:
            x += extra_width * 0.5
        elif self.horizontal_align == AlignLM.ALIGN_RIGHT:
            x += extra_width
        elif self.horizontal_align == AlignLM.GROW_X:
            w = rect.w

        if self.vertical_align == AlignLM.ALIGN_MIDDLE:
            y += extra_height * 0.5
        elif self.vertical_align == AlignLM.ALIGN_TOP:
            y += extra_height
        elif self.vertical_align == AlignLM.GROW_Y:
            h = rect.h

        self.element.render(datatypes.Rectangle(x, y, w, h), data)
