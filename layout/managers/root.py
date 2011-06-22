from layout import datatypes

class LayoutElement(object):
    """
    A layout element has size data and can be asked to draw itself.
    """
    def get_minimum_size(self, data):
        """How small can the element be? Should return a Point."""
        return datatypes.Point(0, 0)

    def render(self, rectangle, data):
        """Asks the element to render itself."""
        pass

class LayoutManager(LayoutElement):
    """
    Layout managers position and size content to fit some container,
    based on some algorithm. This class is an empty subclass used for
    clearer naming when used as a parent class.
    """

class SpecificFieldsLMMetaclass(type):
    """
    A meta-class that creates layout managers with a set of named
    fields.
    """
    def __init__(cls, name, bases, dict):
        """Creates a new class with a set of fields defined by its
        _fields and _store_name class properties."""
        super(SpecificFieldsLMMetaclass, cls).__init__(name, bases, dict)

        field_names = cls._fields
        store_name = cls._store_name

        def _add(index, name):
            def _set_dir(self, value): getattr(self, store_name)[index] = value
            def _get_dir(self): return getattr(self, store_name)[index]
            setattr(cls, name, property(_get_dir, _set_dir))

        for index, field_name in enumerate(field_names):
            _add(index, field_name)

class GroupLayoutManager(LayoutManager):
    """
    A base class for layout managers that can have any number of
    elements.
    """
    def __init__(self, elements=[]):
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
