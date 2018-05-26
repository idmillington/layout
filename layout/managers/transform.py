import math
from layout import datatypes
from . import root

class RotateLM(root.LayoutManager):
    """
    A layout manager that holds one element and rotates it by the
    given number of right angles.

    The right angle value given can't be fractional, it must be an
    integer. Convenience constants are provided in this class for code
    readability.
    """
    #: No rotation
    NORMAL = 0

    #: No rotation
    ANGLE_0 = 0

    #: Rotates 90 degrees counter-clockwise so the X-axis points up.
    X_UP = 1

    #: Rotates 90 degrees counter-clockwise
    ANGLE_90 = 1

    #: Rotates 180 degrees.
    UPSIDE_DOWN = 2

    #: Rotates 180 degrees.
    ANGLE_180 = 2

    #: Rotates 90 degrees clockwise, so the X-axis points down.
    X_DOWN = 3

    #: Rotates 90 decrees clockwise, or 270 degrees clockwise.
    ANGLE_270 = 3

    def __init__(self, angle, element=None):
        super(RotateLM, self).__init__()
        self.element = element
        self.angle = angle

    def get_minimum_size(self, data):
        """Returns the rotated minimum size."""
        size = self.element.get_minimum_size(data)
        if self.angle in (RotateLM.NORMAL, RotateLM.UPSIDE_DOWN):
            return size
        else:
            return datatypes.Point(size.y, size.x)

    def render(self, rect, data):
        # Use an if statement - it is much easier.
        x, y, w, h = rect.get_data()
        c = data['output']

        with c:
            if self.angle == RotateLM.NORMAL:
                self.element.render(rect, data)
            else:
                c.translate(*rect.cm)
                c.rotate(self.angle * 90)

                if self.angle == RotateLM.ANGLE_180:
                    self.element.render(
                        datatypes.Rectangle(-w*0.5, -h*0.5, w, h), data
                        )
                else:
                    assert (self.angle in (RotateLM.ANGLE_90, RotateLM.ANGLE_270))
                    self.element.render(
                        datatypes.Rectangle(-h*0.5, -w*0.5, h, w), data
                        )

class AnyRotationLM(root.LayoutManager):
    """
    A layout manager that allows its child element to be rotated to
    any angle. The rotated element is always given space that is of
    the same aspect ratio as the minimum size it requested, even if
    extra space is available.

    This class implements a different algorithm that is much less
    efficient than :class:`RotateLM` for right angles. Use
    :class:`RotateLM` if you are rotating through a multiple of
    PI/2. Because of the aspect ratio feature of this algorithm, the
    results of this class with a right-angle rotation will also differ
    from that of :class:`RotateLM`.
    """
    def __init__(self, angle, element=None):
        """
        Arguments:

        ``angle``
            The angle to rotate, given in radians.
        """
        super(AnyRotationLM, self).__init__()
        self.angle = angle
        self.element = element

    def get_minimum_size(self, data):
        """Finds the minimum size of its child element as a
        rectangle. Then works out the minimum size needed to fit that
        rectangle when rotated. This can dramatically overstate the
        actual size needed to fit the rotated element if the original
        element is not rectangular."""
        return self._calculate_ms_from_base(
            self.element.get_minimum_size(data)
            )

    def _calculate_ms_from_base(self, size):
        """Calculates the rotated minimum size from the given base minimum
        size."""
        hw = size.x * 0.5
        hh = size.y * 0.5

        a = datatypes.Point(hw, hh).get_rotated(self.angle)
        b = datatypes.Point(-hw, hh).get_rotated(self.angle)
        c = datatypes.Point(hw, -hh).get_rotated(self.angle)
        d = datatypes.Point(-hw, -hh).get_rotated(self.angle)

        minp = a.get_minimum(b).get_minimum(c).get_minimum(d)
        maxp = a.get_maximum(b).get_maximum(c).get_maximum(d)
        return maxp - minp

    def render(self, rect, data):
        # Find the biggest rectangle of our original aspect ratio,
        # that we can fit in the given rectangle at our target angle.

        # First find the upscale we got going from our element to our
        # rotated minimum size.
        base_ms = self.element.get_minimum_size(data)
        rotated_ms = self._calculate_ms_from_base(base_ms)

        # Find the scale of the rect we're given and the limiting scale
        scale_x = rect.w / rotated_ms.x if rotated_ms.x > 0 else 999999999.0
        scale_y = rect.h / rotated_ms.y if rotated_ms.y > 0 else 999999999.0
        scale = min(scale_x, scale_y)

        # Transform the base size by this scale
        hw = base_ms.x * 0.5 * scale
        hh = base_ms.y * 0.5 * scale

        # Thats the space we give to our child element.
        center = rect.center_middle
        c = data['output']
        with c:
            c.translate(center.x, center.y)
            c.rotate(self.angle / math.pi * 180.0)
            self.element.render(datatypes.Rectangle(-hw, -hh, hw*2.0, hh*2.0), data)

class FixedScaleLM(root.LayoutManager):
    """
    A layout manager that scales its one element by a fixed amount.
    """
    def __init__(self, scale=1.0, element=None):
        super(FixedScaleLM, self).__init__()
        self.scale = scale
        self.element = element

    def get_minimum_size(self, data):
        child_size = self.element.get_minimum_size(data)
        return datatypes.Point(
            child_size.x*self.scale, child_size.y*self.scale
            )

    def render(self, rect, data):
        scale = self.scale
        c = data['output']
        with c:
            c.translate(rect.x, rect.y)
            c.scale(scale, scale)
            self.element.render(
                datatypes.Rectangle(0, 0, rect.x/scale, rect.y/scale),
                data
                )

class ScaleLM(root.LayoutManager):
    """
    A layout manager that holds one element, and scales it down with
    isotropic scaling if it is too large to fit.
    """
    def __init__(self, element=None):
        super(ScaleLM, self).__init__()
        self.element = element

    def get_minimum_size(self, data):
        return self.element.get_minimum_size(data)

    def render(self, rect, data):
        size = self.element.get_minimum_size(data)

        # The object is too big, work out the minimum scaling
        scale = min(
            1,
            float(rect.w) / float(size.x),
            float(rect.h) / float(size.y)
            )
        extra_width = rect.w - size.x * scale
        extra_height = rect.h - size.y * scale

        # Apply the scaling and render the output.
        c = data['output']
        with c:
            c.translate(rect.x+extra_width*0.5, rect.y+extra_height*0.5)
            if scale < 1.0:
                c.scale(scale, scale)
            self.element.render(datatypes.Rectangle(0, 0, size.x, size.y), data)

class FlexScaleLM(root.LayoutManager):
    """
    A layout manager that holds one element, and scales it down with
    anisotropic scaling, if it is too large to fit. Unlike the regular
    :class:`ScaleLM`, this class gives the scaled object any
    additional room it has to fit, rather than preserving its aspect
    ratio.
    """
    def __init__(self, element=None):
        super(FlexScaleLM, self).__init__()
        self.element = element

    def get_minimum_size(self, data):
        return self.element.get_minimum_size(data)

    def render(self, rect, data):
        size = self.element.get_minimum_size(data)
        if size.x > rect.w or size.y > rect.h:
            # The object is too big, work out the minimum scaling
            scale = min(
                float(rect.w) / float(size.x),
                float(rect.h) / float(size.y)
                )

            # Apply the scaling and render the output.
            c = data['output']
            with c:
                c.translate(rect.x, rect.y)
                c.scale(scale, scale)
                self.element.render(datatypes.Rectangle(
                        0, 0, rect.w / scale, rect.h / scale
                        ), data)
        else:
            self.element.render(rect, data)
