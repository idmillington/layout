import random
import math
from layout import datatypes
from . import root

class _JitterBase(root.LayoutManager):
    def _render_jittered(
        self, rectangle, data, angle_jitter, x_jitter, y_jitter
        ):
        c = data['output']
        with c:
            c.translate(rectangle.center, rectangle.middle)
            c.translate(x_jitter, y_jitter)
            c.rotate(angle_jitter * 180.0 / math.pi)
            self.element.render(
                datatypes.Rectangle(
                    -rectangle.w*0.5, -rectangle.h*0.5,
                    rectangle.w, rectangle.h
                    ), data
                )

class JitterLM(_JitterBase):
    """
    Displays its managed element slightly offset from its reserved space.

    The layout manager reserves the minimum space needed for its child
    element, but when it comes to draw the element, it draws it offset
    from its natural position, and slightly at an angle. The jitter
    parameters are given to the layout manager when it is constructed.

    See :class:`RandomJitterLM` for a manager that randomizes the
    jitter applied.
    """
    def __init__(self, angle_jitter=0.1, x_jitter=5.0, y_jitter=5.0,
                 element=None):
        super(JitterLM, self).__init__()
        self.element = element
        self.angle_jitter = angle_jitter
        self.x_jitter = x_jitter
        self.y_jitter = y_jitter

    def get_minimum_size(self, data):
        return self.element.get_minimum_size(data)

    def render(self, rectangle, data):
        self._render_jittered(
            rectangle, data, self.angle_jitter, self.x_jitter, self.y_jitter
            )

class UnstableRandomJitterLM(_JitterBase):
    """
    A random jitter layout manager that does rerandomize its offsets
    each time it is called to render. Rendering the tree twice, therefore,
    may lead to different results.
    """
    def __init__(
        self,
        max_angle_jitter=0.1, max_x_jitter=5.0, max_y_jitter=5.0,
        element=None
        ):
        self.max_angle_jitter = max_angle_jitter
        self.max_x_jitter = max_x_jitter
        self.max_y_jitter = max_y_jitter
        self.element = element

    def get_minimum_size(self, data):
        return self.element.get_minimum_size(data)

    def render(self, rect, data):
        self._render_jittered(
            rect, data,
            (random.random()-random.random())*self.max_angle_jitter,
            (random.random()-random.random())*self.max_x_jitter,
            (random.random()-random.random())*self.max_y_jitter
            )

class RandomJitterLM(JitterLM):
    """
    A Jitter layout manager that chooses a random jitter binomially
    distributed around 0, and with half-size equal to the given
    parameters.

    Note this layout manager does not randomize
    its offset each time it is called on to draw its content, only when
    it is constructed. The jitter is therefore consistent for the lifetime
    of an instance of this class.
    """
    def __init__(
        self,
        max_angle_jitter=0.1, max_x_jitter=5.0, max_y_jitter=5.0,
        element=None
        ):
        super(RandomJitterLM, self).__init__(
            (random.random()-random.random())*max_angle_jitter,
            (random.random()-random.random())*max_x_jitter,
            (random.random()-random.random())*max_y_jitter,
            element
            )



