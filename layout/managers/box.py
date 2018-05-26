from layout import datatypes
from . import root

_box_fields = ['top', 'right', 'bottom', 'left', 'center']

@root.add_fields('_elements', _box_fields)
class BoxLM(root.LayoutManager):
    """
    A layout manager in the style of Java's BoxLayout, with a central
    space that gobbles up as much size as possible and surrounding
    spaces that are at minimum size.
    """
    def __init__(self, margin=0,
                 top=None, right=None, bottom=None, left=None, center=None
                 ):
        """
        Arguments:

        ``margin``
            The gap to place between elements.

        ``top``
            The element to place at the top of the layout. This
            element will be at its minimum height, but may have extra
            width.

        ``right``
            The element to place at the right of the layout. This
            element will be at its minimum width, but may have extra
            height.

        ``bottom``
            The element to place at the bottom of the layout. This
            element will be at its minimum height, but may have extra
            width.

        ``left``
            The element to place at the left of the layout. This
            element will be at its minimum width, but may have extra
            height.

        ``center``
            The element to place in the center of the layout, this
            element may be stretched in both directions to fill all
            remaining room in the layout.

        Each of these arguments is placed in a data member with the
        same name, so the elements can later be overridden. If any
        element isn't provided, then that portion of the layout will
        be missed. Margins only apply between elements that have been
        given, they are not used for missed slots.

        If you have left/right elements and top/bottom elements, note
        that the algorithm lays out the contents so the top and bottom
        elements are at full-width, while the left and right elements
        extend from the bottom of the top element to the top of the
        bottom element. The left/right and top/bottom elements are
        therefore not treated in the same way -- top/bottom elements
        have priority:

            +-----------------------+
            |      Top Element      |
            +------+--------+-------+
            | Left | Center | Right |
            +------+--------+-------+
            |     Bottom Element    |
            +-----------------------+

        If you want to reverse this, you'll need to use
        two instances of this class inside one another: the outer one
        with the left/right elements set, and the inner one (in the
        'center' slot of the outer manager), with the top/bottom and
        center elements set.

        Outer :class:`BoxLM`:

            +------+-------------+-------+
            | Left | Inner BoxLM | Right |
            +------+-------------+-------+

        Inner :class:`BoxLM`:


            +----------+
            |   Top    |
            +----------+
            |  Center  |
            +----------+
            |  Bottom  |
            +----------+

        """
        super(BoxLM, self).__init__()
        self._elements = [None] * len(_box_fields)
        self.margin = margin
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.center = center

    def get_minimum_size(self, data):
        # Find the sizes for each component
        item_sizes = [
            (
                datatypes.Point(0, 0)
                if getattr(self, direction) is None
                else getattr(self, direction).get_minimum_size(data)
            ) for direction in _box_fields
        ]

        # Work out how many margins we'll be using
        w_margins = 0
        if self.right is not None: w_margins += self.margin
        if self.left is not None: w_margins += self.margin

        h_margins = 0
        if self.top is not None: h_margins += self.margin
        if self.bottom is not None: h_margins += self.margin

        # Work out the result
        min_width = max(
            item_sizes[0].x, item_sizes[2].x,
            item_sizes[1].x + item_sizes[4].x + item_sizes[3].x + w_margins
            )

        min_height = item_sizes[0].y + item_sizes[2].y + h_margins + max(
            item_sizes[1].y, item_sizes[4].y, item_sizes[3].y
            )
        return datatypes.Point(min_width, min_height)

    def render(self, rect, data):
        x, y, w, h = rect.get_data()

        if self.top is not None:
            size = self.top.get_minimum_size(data)
            self.top.render(datatypes.Rectangle(x,y+h-size.y,w,size.y), data)
            h -= size.y + self.margin
        if self.bottom is not None:
            size = self.bottom.get_minimum_size(data)
            self.bottom.render(datatypes.Rectangle(x, y, w, size.y), data)
            y += size.y + self.margin
            h -= size.y + self.margin
        if self.right is not None:
            size = self.right.get_minimum_size(data)
            self.right.render(datatypes.Rectangle(x+w-size.x,y,size.x,h), data)
            w -= size.x + self.margin
        if self.left is not None:
            size = self.left.get_minimum_size(data)
            self.left.render(datatypes.Rectangle(x, y, size.x, h), data)
            w -= size.x + self.margin
            x += size.x + self.margin
        if self.center is not None:
            self.center.render(datatypes.Rectangle(x, y, w, h), data)

