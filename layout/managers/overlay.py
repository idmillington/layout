"""
Overlaying is the process of having more than one element in the same
space. In this module is a simple layout manager to achieve this, but
other layout managers may also provide this facility.  The
:class:`~layout.managers.grid.GridLM`, for example, allows you to
overlay many elements in each grid cell.
"""

from layout import datatypes
from . import root

class OverlayLM(root.GroupLayoutManager):
    """
    A layout manager that has any number of elements, all occupying the
    same area. The elements are drawn in strictly the same order
    that they are added to the manager, so early items form a back
    ground for later items.
    """
    def get_minimum_size(self, data):
        return self._get_smallest_dimensions(data)

    def render(self, rect, data):
        for element in self.elements:
            element.render(rect, data)
