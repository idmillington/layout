from layout import datatypes
from . import root

@root.add_fields('_margins', ['top', 'right', 'bottom', 'left'])
class MarginsLM(root.LayoutManager):
    """
    A layout manager that has only one element, surrounded by the given
    absolute margins.
    """
    def __init__(self, top=0, right=0, bottom=0, left=0, element=None):
        self._margins = [top, right, bottom, left]
        self.element = element

    def get_minimum_size(self, data):
        size = self.element.get_minimum_size(data)
        return datatypes.Point(
            size.x + self.right + self.left,
            size.y + self.top + self.bottom
            )

    def render(self, rect, data):
        self.element.render(datatypes.Rectangle(
            rect.x + self.left, rect.y + self.bottom,
            rect.w - self.left - self.right,
            rect.h - self.bottom - self.top
            ), data)

@root.add_fields('_margins', ['top', 'right', 'bottom', 'left'])
class ProportionalMarginsLM(root.LayoutManager):
    """
    A layout manager that has only one element, surrounded by the given
    margins that are proportional to total size of this manager.

    For example, if we specify that the left margin is at 0.2 and the right
    margin is at 0.4, then the child element will be 0.4 times the width
    of this manager.

    Pairs of margins (left & right or top & bottom) must sum to at least zero,
    and strictly less than 1.
    """
    def __init__(self, top=0, right=0, bottom=0, left=0, element=None):
        self._margins = [top, right, bottom, left]
        self.element = element

    def get_minimum_size(self, data):

        # Work out what proportion of the total the child takes up.
        assert 0 <= top+bottom < 1.0, "Top and bottom margins are invalid."
        assert 0 <= left+right < 1.0, "Left and right margins are invalid."
        width_scale = 1.0 - left - right
        height_scale = 1.0 - top - bottom

        # We divide the child element's size by these values.
        size = self.element.get_minimum_size(data)
        return datatypes.Point(
            size.x / width_scale,
            size.y / height_scale
            )

    def render(self, rect, data):
        self.element.render(datatypes.Rectangle(
            rect.x + rect.w * self.left,
            rect.y + rect.h * self.bottom,
            rect.w * (1.0 - self.left - self.right),
            rect.h * (1.0 - self.bottom - self.top)
            ), data)

_NINETH = 1.0 / 9.0
class VanDeGraafCanonLM(ProportionalMarginsLM):
    """
    Wraps its child element in margins calculated according to the
    Van de Graaf page construction canon.

    Using this canon the proportions of the child
    element are the same as the proportions of this manager. The standard
    de Graaf proportions are based on geometrical construction, here we
    perform the calculation, by dividing the page into ninths (the original
    canon would also do this, if drawn precisely, obviously we don't allow
    for the innacuracies in drawing which would have been common in medieval
    manuscripts).

    Using this approach the child element gets two thirds of both the
    height and the width of the parent element.
    """
    def __init__(self, recto=True, element=None):
        if recto:
            super(VanDeGraafCanonLM, self).__init__(
                _NINETH, _NINETH, 2.0*_NINETH, 2.0*_NINETH, element
                )
        else:
            super(VanDeGraafCanonLM, self).__init__(
                _NINETH, 2.0*_NINETH, 2.0*_NINETH, _NINETH, element
                )

@root.add_fields('_margins', ['top', 'right', 'bottom', 'left', 'width', 'height'])
class PaddedMarginsLM(root.LayoutManager):
    """
    A layout manager that surrounds its single element by margins
    that grow with the available space. The margins grow with the available
    space in the given proportions. If the proportions for a pair of margins
    don't add up to 1.0, then any additional proportion will be given to the
    element to make it grow.

    Using this layout manager with the correct proportions, you can
    duplicate the behavior of the
    :class:`layout.managers.align.AlignLM`. This class provides more
    flexibility, however.
    """
    def __init__(self, top=0.5, right=0.5, bottom=0.5, left=0.5, element=None):
        assert (top+bottom <= 1.0)
        assert (left+right <= 1.0)

        self._margins = [
            top, right, bottom, left, 1.0-left-right, 1.0-top-bottom
            ]
        self.element = element

    def get_minimum_size(self, data):
        """Our minimum size is simply our element's minimum size."""
        return self.element.get_minimum_size(data)

    def render(self, rect, data):
        if self.element is None: return

        size = self.element.get_minimum_size(data)
        extra_width = max(0, rect.w - size.x)
        extra_height = max(0, rect.h - size.y)

        self.element.render(datatypes.Rectangle(
                rect.x + self._margins[3]*extra_width,
                rect.y + self._margins[2]*extra_height,
                rect.w - extra_width,
                rect.h - extra_height
                ), data)

