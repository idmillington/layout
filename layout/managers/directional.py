from layout import datatypes
from . import root

class VerticalLM(root.GroupLayoutManager):
    """
    Keeps a set of elements above one another. We can control
    how they are distributed vertically, as well as their horizontal
    alignment.
    """
    #: Align the elements so they are bunched at the top of the
    #: available space.
    ALIGN_TOP = 0

    #: Align the elements so they are in the middle of the available
    #: space.
    ALIGN_MIDDLE = 1

    #: Align the elements so they sit at the bottom of the available
    #: space.
    ALIGN_BOTTOM = 2

    #: Align the elements vertcially so that any extra space is
    #: distributed equally between the elements.
    ALIGN_EQUAL_SPACING = 3

    #: Align the elements vertically so that each gets the same amount
    #: of extra space, if the layout is taller than the elements need it
    #: to be.
    ALIGN_EQUAL_GROWTH = 4

    #: Align each element to the left of the layout.
    ALIGN_LEFT = 10

    #: Align each element to the center of the layout.
    ALIGN_CENTER = 11

    #: Align each element to the right of the layout.
    ALIGN_RIGHT = 12

    #: Align each element so that it stretches horizontally to fill
    #: the layout.
    ALIGN_GROW = 13


    # A tuple of align type values so we can distinguish between the
    # simple an complex cases.
    _ALIGN_SIMPLE_SET = (ALIGN_TOP, ALIGN_MIDDLE, ALIGN_BOTTOM)

    _VALID_ALIGN_HORIZONTAL = (
        ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT, ALIGN_GROW
        )

    _VALID_ALIGN_VERTICAL = _ALIGN_SIMPLE_SET + (
        ALIGN_EQUAL_SPACING, ALIGN_EQUAL_GROWTH
        )

    def __init__(self, margin=0,
                 horizontal_align=ALIGN_GROW,
                 vertical_align=ALIGN_EQUAL_GROWTH,
                 elements=[]):
        """
        Arguments:

        ``margin``
            The amount of space to place between elements.

        ``horizontal_align``
            How elements should be aligned horizontally within the
            stack (default: :data:`ALIGN_GROW`).

        ``vertical_align``
            How elements should be aligned vertically in the stack,
            and how extra space should be distributed between them
            (default: :data:`ALIGN_EQUAL_GROWTH`).
        """

        super(VerticalLM, self).__init__(elements)
        self.margin = margin
        self.vertical_align = vertical_align
        self.horizontal_align = horizontal_align

    def get_minimum_size(self, data):
        """
        Minimum height is the total height + margins, minimum width
        is the largest width.
        """
        min_width = 0
        height = 0
        for element in self.elements:
            size = element.get_minimum_size(data)
            min_width = max(min_width, size.x)
            height += size.y
        height += (len(self.elements)-1)*self.margin
        return datatypes.Point(min_width, height)

    def render(self, rect, data):
        """
        Displays the elements according to the align properties.
        """
        # Make sure we're aligned correctly
        if self.horizontal_align not in VerticalLM._VALID_ALIGN_HORIZONTAL:
            raise ValueError('Horizontal align is not valid.')
        if self.vertical_align not in VerticalLM._VALID_ALIGN_VERTICAL:
            raise ValueError('Vertical align is not valid.')

        # Work out the extra height we have to distribute
        extra_height = rect.h - self.get_minimum_size(data).y
        num_elements = len(self.elements)
        if num_elements == 0:
            return
        elif num_elements > 1:
            per_margin = 1.0 / float(num_elements-1)
        else:
            per_margin = 0.0
        per_element = 1.0 / float(num_elements)

        # Work out the starting y coordinate
        y = rect.y
        if self.vertical_align == VerticalLM.ALIGN_MIDDLE:
            y = rect.y + extra_height*0.5
        elif self.vertical_align == VerticalLM.ALIGN_TOP:
            y = rect.y + extra_height

        # Render each child element
        for element in reversed(self.elements):
            size = element.get_minimum_size(data)

            # Work out the x-coordinates
            if self.horizontal_align == VerticalLM.ALIGN_LEFT:
                x = rect.x
                w = size.x
            elif self.horizontal_align == VerticalLM.ALIGN_CENTER:
                x = rect.center - size.x*0.5
                w = size.x
            elif self.horizontal_align == VerticalLM.ALIGN_RIGHT:
                x = rect.right - size.x
                w = size.x
            else:
                assert self.horizontal_align == VerticalLM.ALIGN_GROW
                x = rect.x
                w = rect.w

            # Work out the y-coordinates
            if self.vertical_align in VerticalLM._ALIGN_SIMPLE_SET:
                h = size.y
                next_y = y + size.y + self.margin
            elif self.vertical_align == VerticalLM.ALIGN_EQUAL_SPACING:
                h = size.y
                next_y = y + size.y + self.margin + extra_height*per_margin
            else:
                assert self.vertical_align == VerticalLM.ALIGN_EQUAL_GROWTH
                h = size.y + extra_height*per_element
                next_y = y + h + self.margin

            # Render and move on.
            element.render(datatypes.Rectangle(x, y, w, h), data)
            y = next_y

class HorizontalLM(root.GroupLayoutManager):
    """
    Keeps a set of elements alongside one another. We can control
    how they are distributed horizontally, as well as their vertical
    alignment.
    """
    #: Align the elements so they are bunched at the left of the
    #: available space.
    ALIGN_LEFT = 10

    #: Align the elements so they are in the center of the available
    #: space.
    ALIGN_CENTER = 11

    #: Align the elements so they sit at the right of the available
    #: space.
    ALIGN_RIGHT = 12

    #: Align the elements horizontally so that any additional space is
    #: distributed equally between the elements.
    ALIGN_EQUAL_SPACING = 13

    #: Align the elements horizontally so that each gets the same
    #: amount of extra space, if the layout is taller than the
    #: elements need it to be.
    ALIGN_EQUAL_GROWTH = 14

    #: Align each element to the top of the layout.
    ALIGN_TOP = 0

    #: Align each element to the middle of the layout.
    ALIGN_MIDDLE = 1

    #: Align each element to the bottom of the layout.
    ALIGN_BOTTOM = 2

    #: Align each element so that it stretches vertically to fill
    #: the layout.
    ALIGN_GROW = 3


    # A tuple of align type values so we can distinguish between the
    # simple and complex cases.
    _ALIGN_SIMPLE_SET = (ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT)

    _VALID_ALIGN_HORIZONTAL = _ALIGN_SIMPLE_SET + (
        ALIGN_EQUAL_SPACING, ALIGN_EQUAL_GROWTH
        )
    _VALID_ALIGN_VERTICAL = (ALIGN_TOP, ALIGN_MIDDLE, ALIGN_BOTTOM, ALIGN_GROW)

    def __init__(self, margin=0,
                 vertical_align=ALIGN_GROW,
                 horizontal_align=ALIGN_EQUAL_GROWTH,
                 elements=[]):
        """
        Arguments:

        ``margin``
            The amount of space to place between elements.

        ``vertical_align``
            How elements should be aligned vertically in the layout
            (default: :data:`ALIGN_GROW`).

        ``horizontal_align``
            How elements should be aligned horizontally within the
            layout, and how extra space should be distributed between
            them (default: :data:`ALIGN_EQUAL_GROWTH`).
        """

        super(HorizontalLM, self).__init__(elements)
        self.margin = margin
        self.vertical_align = vertical_align
        self.horizontal_align = horizontal_align

    def get_minimum_size(self, data):
        """Minimum width is the total width + margins, minimum height
        is the largest height."""
        width = 0
        min_height = 0
        for element in self.elements:
            size = element.get_minimum_size(data)
            min_height = max(min_height, size.y)
            width += size.x
        width += (len(self.elements)-1)*self.margin
        return datatypes.Point(width, min_height)

    def render(self, rect, data):
        """Displays the elements according to the align properties."""

        # Make sure we're aligned correctly
        if self.horizontal_align not in HorizontalLM._VALID_ALIGN_HORIZONTAL:
            raise ValueError('Horizontal align is not valid.')
        if self.vertical_align not in HorizontalLM._VALID_ALIGN_VERTICAL:
            raise ValueError('Vertical align is not valid.')

        # Work out the extra width we have to distribute
        extra_width = rect.w - self.get_minimum_size(data).x
        num_elements = len(self.elements)
        if num_elements == 0:
            return
        elif num_elements > 1:
            per_margin = 1.0 / float(num_elements-1)
        else:
            per_margin = 0.0
        per_element = 1.0 / float(num_elements)

        # Work out the starting x coordinate
        x = rect.x
        if self.horizontal_align == HorizontalLM.ALIGN_CENTER:
            x = rect.x + extra_width*0.5
        elif self.horizontal_align == HorizontalLM.ALIGN_RIGHT:
            x = rect.x + extra_width

        # Render each child element
        for element in self.elements:
            size = element.get_minimum_size(data)

            # Work out the y-coordinates
            if self.vertical_align == HorizontalLM.ALIGN_TOP:
                y = rect.top - size.y
                h = size.y
            elif self.vertical_align == HorizontalLM.ALIGN_MIDDLE:
                y = rect.middle - size.y*0.5
                h = size.y
            elif self.vertical_align == HorizontalLM.ALIGN_BOTTOM:
                y = rect.y
                h = size.y
            else:
                assert self.vertical_align == HorizontalLM.ALIGN_GROW
                y = rect.y
                h = rect.h

            # Work out the x-coordinates
            if self.horizontal_align in HorizontalLM._ALIGN_SIMPLE_SET:
                w = size.x
                next_x = x + size.x + self.margin
            elif self.horizontal_align == HorizontalLM.ALIGN_EQUAL_SPACING:
                w = size.x
                next_x = x + size.x + self.margin + extra_width*per_margin
            else:
                assert self.horizontal_align == HorizontalLM.ALIGN_EQUAL_GROWTH
                w = size.x + extra_width*per_element
                next_x = x + w + self.margin

            # Render and move on.
            element.render(datatypes.Rectangle(x, y, w, h), data)
            x = next_x


class EqualColumnsLM(root.GroupLayoutManager):
    """Arranges a set of elements into equally sized columns."""

    def __init__(self, margin=0, elements=[]):
        super(EqualColumnsLM, self).__init__(elements)
        self.margin = margin

    def get_minimum_size(self, data):
        """The minimum width is the number of columns multiplied by
        the widest element."""
        min_width = 0
        min_height = 0
        for element in self.elements:
            size = (
                datatypes.Point(0, 0) if element is None
                else element.get_minimum_size(data)
                )
            min_height = max(min_height, size.y)
            min_width = max(min_width, size.x)

        num_elements = len(self.elements)
        width = min_width * num_elements + self.margin * (num_elements-1)
        return datatypes.Point(width, min_height)

    def render(self, rect, data):
        """Draws the columns."""
        num_elements = len(self.elements)
        col_width = (rect.w-self.margin*(num_elements-1)) / float(num_elements)
        x = rect.x
        for element in self.elements:
            if element is not None:
                element.render(datatypes.Rectangle(
                        x, rect.y, col_width, rect.h
                        ), data)
            x += col_width + self.margin

class EqualRowsLM(root.GroupLayoutManager):
    """Arranges a set of elements into equally sized rows."""
    def __init__(self, margin=0, elements=[]):
        super(EqualRowsLM, self).__init__(elements)
        self.margin = margin

    def get_minimum_size(self, data):
        """The minimum height is the number of rows multiplied by the
        tallest row."""
        min_width = 0
        min_height = 0
        for element in self.elements:
            size = (
                datatypes.Point(0, 0) if element is None
                else element.get_minimum_size(data)
                )
            min_height = max(min_height, size.y)
            min_width = max(min_width, size.x)

        num_elements = len(self.elements)
        height = min_height * num_elements + self.margin * (num_elements-1)
        return datatypes.Point(min_width, height)

    def render(self, rect, data):
        num_elements = len(self.elements)
        row_height = \
            (rect.h-self.margin*(num_elements-1)) / float(num_elements)
        y = rect.y
        for element in reversed(self.elements):
            if element is not None:
                element.render(datatypes.Rectangle(
                        rect.x, y, rect.w, row_height
                        ), data)
            y += row_height + self.margin



