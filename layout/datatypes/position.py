import random
import math

class Point(object):
    """A single point in space, or a vector in 2D."""
    __slots__ = ('x', 'y')

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_data(self):
        """Returns the x, y coordinates as a 2-tuple."""
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, factor):
        if type(factor) not in (int, float, long):
            raise TypeError('unsupported operand for *')
        return Point(self.x*factor, self.y*factor)

    def __imul__(self, factor):
        if type(factor) not in (int, float, long):
            raise TypeError('unsupported operand for *')
        self.x *= factor
        self.y *= factor
        return self

    def __rmul__(self, factor):
        return self * factor

    def __div__(self, factor):
        factor = 1.0 / factor
        return Point(self.x*factor, self.y*factor)

    def __idiv__(self, factor):
        factor = 1.0 / factor
        self.x *= factor
        self.y *= factor
        return self

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __iter__(self):
        return iter([self.x, self.y])

    def get_component_product(self, other):
        """Returns the component product of this vector and the given
        other vector."""
        return Point(self.x * other.x, self.y * other.y)

    def update_component_product(self, other):
        """Updates this vector so that it is the component product of
        itself with the given other vector."""
        self.x *= other.x
        self.y *= other.y
        return self

    def get_normalized(self):
        """Returns the unit vector in the same direction as this vector."""
        magnitude = self.get_magnitude()
        if magnitude > 0:
            magnitude = 1.0 / magnitude
            return Point(self.x * magnitude, self.y * magnitude)
        else:
            return Point(0, 0)

    def normalize(self):
        """Makes this vector unit length, unless it is the zero
        vector, in which case it is left as is.."""
        magnitude = self.get_magnitude()
        if magnitude > 0:
            magnitude = 1.0 / magnitude
            self.x *= magnitude
            self.y *= magnitude

    def get_angle(self):
        """Returns the CCW angle from the positive X-axis (i.e. that
        returned from atan2."""
        return math.atan2(self.y, self.x)

    def get_right_normal(self):
        """Returns the right hand normal of this vector: the vector
        produced by rotating this vector about ninety degrees
        clockwise."""
        return Point(self.y, -self.x)

    def get_left_normal(self):
        """Returns the left hand normal of this vector: the vector
        produced by rotating this vector about ninety degrees
        anti-clockwise."""
        return Point(-self.y, self.x)

    def rotate(self, angle):
        """Rotates this vector through the given anti-clockwise angle
        in radians."""
        ca = math.cos(angle)
        sa = math.sin(angle)
        self.x, self.y = self.x*ca-self.y*sa, self.x*sa+self.y*ca

    def get_rotated(self, angle):
        """Returns the vector generated from this vector rotated by
        the given amount anti-clockwise."""
        ca = math.cos(angle)
        sa = math.sin(angle)
        return Point(self.x*ca-self.y*sa, self.x*sa+self.y*ca)

    def get_magnitude(self):
        """Returns the magnitude of this vector."""
        return math.sqrt(self.x*self.x + self.y*self.y)

    def get_magnitude_squared(self):
        """Returns the square of the magnitude of this vector."""
        return self.x*self.x + self.y*self.y

    def get_copy(self):
        """Returns a copy of this vector."""
        return Point(self.x, self.y)

    def get_x_mirror(self):
        """Returns a copy of this vector reflected in the x=0 axis."""
        return Point(-self.x, self.y)

    def get_y_mirror(self):
        """Returns a copy of this vector reflected in the y=0 axis."""
        return Point(self.x, -self.y)

    def get_scalar_product(self, other):
        """Returns the scalar product of this vector with the given
        other vector."""
        return self.x*other.x+self.y*other.y

    def get_angle_between(self, other):
        """Returns the smallest angle between this vector and the
        given other vector."""
        # The scalar product is the sum of the squares of the
        # magnitude times the cosine of the angle - so normalizing the
        # vectors first means the scalar product is just the cosine of
        # the angle.
        normself = self.get_normalized()
        normother = other.get_normalized()
        sp = normself.get_scalar_product(normother)
        return math.acos(sp)

    def update_minimum(self, other):
        """Updates this vector so its components are the lower of its
        current components and those of the given other value."""
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)

    def update_maximum(self, other):
        """Updates this vector so its components are the higher of its
        current components and those of the given other value."""
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)

    @staticmethod
    def get_random(min_pt, max_pt):
        """Returns a random vector in the given range."""
        result = Point(random.random(), random.random())
        result.update_component_product(max_pt - min_pt)
        result += min_pt
        return result

    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)

class _RectangleMetaclass(type):
    """Adds all combinations of directional properties to the rectangle, such
    as ``Rectangle.top_left``, ``Rectangle.left_top``, ``Rectangle.tl`` and
    ``Rectangle.center``."""
    def __init__(cls, name, base, dict):
        super(_RectangleMetaclass, cls).__init__(name, base, dict)

        xs = ('left', 'center', 'right')
        ys = ('bottom', 'middle', 'top')

        def _make_method(x, y):
            # Create the custom getter method
            def _get(self):
                return Point(getattr(self, x), getattr(self, y))

            # Set all combinations of lookup as properties
            setattr(cls, y[0]+x[0], property(_get))
            setattr(cls, "%s_%s" % (y, x), property(_get))
            setattr(cls, x[0]+y[0], property(_get))
            setattr(cls, "%s_%s" % (x, y), property(_get))

        for x in xs:
            for y in ys:
                _make_method(x, y)

        def _make_method(name, base, addition, amount):
            def _get(self):
                return getattr(self, base) + getattr(self, addition) * amount

            setattr(cls, name[0], property(_get))
            setattr(cls, name, property(_get))

        for i, (x, y) in enumerate(zip(xs, ys)):
            _make_method(x, 'x', 'w', i/2.0)
            _make_method(y, 'y', 'h', i/2.0)

class Rectangle(object):
    """A rectangle in two dimensional space.

    The data in this rectangle can be accessed in many different
    ways. It has data members of ``x``, ``y``, ``w``, and ``h``, and
    properties corresponding to all combinations of ``left`` (which
    equals ``x``), ``right``, ``top``, ``bottom`` (which equals
    ``y``), ``center`` (horizontal) and ``middle`` (vertical). Pair
    combinations (such as ``top_right``) return a :class:`Point`,
    while single values (such as ``center``) return a number. You can
    also abbreviate each of the properties using its initial letter.

    So to access the center point of the rectangle, for example, you
    use any of the properties:

    * ``Rectangle.cm``
    * ``Rectangle.mc``
    * ``Rectangle.center_middle``
    * ``Rectangle.middle_center``

    And to access just the right-hand coordinate, you can use:

    * ``Rectangle.right``
    * ``Rectangle.r``
    """
    __slots__ = ('x', 'y', 'w', 'h')
    __metaclass__ = _RectangleMetaclass

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __eq__(self, other):
        return (
            self.x == other.x and self.y == other.y and
            self.w == other.w and self.h == other.h
            )

    def __repr__(self):
        return "Rectangle(%f, %f, %f, %f)" % self.get_data()

    def get_data(self):
        """Returns the x, y, w, h, data as a tuple."""
        return self.x, self.y, self.w, self.h


