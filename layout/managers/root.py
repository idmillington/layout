from layout import datatypes
import typing
import abc

class LayoutElement(abc.ABC):
    """
    A layout element has size data and can be asked to draw itself.
    """
    @abc.abstractmethod
    def get_minimum_size(self, data) -> datatypes.Point:
        """How small can the element be? Should return a Point."""
        return datatypes.Point(0, 0)

    @abc.abstractmethod
    def render(self, rectangle:datatypes.Rectangle, data) -> None:
        """Asks the element to render itself."""
        pass

class LayoutManager(LayoutElement):
    """
    Layout managers position and size content to fit some container,
    based on some algorithm. This class is an empty subclass used for
    clearer naming when used as a parent class.
    """

def add_fields(store_name, field_names):
    """
    A class-decorator that creates layout managers with a set of named
    fields.
    """
    def decorate(cls):
        def _add(index, name):
            def _set_dir(self, value): getattr(self, store_name)[index] = value
            def _get_dir(self): return getattr(self, store_name)[index]
            setattr(cls, name, property(_get_dir, _set_dir))

        for index, field_name in enumerate(field_names):
            _add(index, field_name)

        return cls

    return decorate

class GroupLayoutManager(LayoutManager):
    """
    A base class for layout managers that can have any number of
    elements.
    """
    def __init__(self, elements:typing.Sequence[LayoutElement]=[]) -> None:
        self.elements = elements[:]

    def add_element(self, element):
        self.elements.append(element)

    def _get_smallest_dimensions(self, data):
        """A utility method to return the minimum size needed to fit
        all the elements in."""
        min_width = 0
        min_height = 0
        for element in self.elements:
            if not element: continue
            size = element.get_minimum_size(data)
            min_width = max(min_width, size.x)
            min_height = max(min_height, size.y)
        return datatypes.Point(min_width, min_height)
