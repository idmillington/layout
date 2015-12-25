from layout import datatypes
from . import root

class RecursionStopperLM(root.LayoutManager):
    """
    Because you can arrange the layout tree in any way you choose,
    it is possible to create circular loops in the tree which would
    lead to infinite loops in the code. Loops normally indicate that your
    code has a bug, but sometimes you do want the loop. In this case, adding
    this class somewhere in the loop prevents the loop from
    recursing more than a specified number of times.

    If the loop hasn't reached its maximum number of iterations, this
    class acts as if it isn't there: it passes all calls onto its child
    element. Otherwise it will act as if it were a zero sized element
    that has no visual effect.

    Note that this class uses the data object passed in to hold its
    recursion count, in particular in a field called 'recusion_stopper_count'.
    It cleans up after itself, so you shouldn't need to worry about clearing
    the value after you've run the layout (if you want to render again
    using the same data object, for example). But you shouldn't mess with
    that value yourself.
    """
    def __init__(self, recursion_limit=2, element=None):
        self.recursion_limit = recursion_limit
        self.element = element

    def _do_recursion(self, data, method_name, default_return, *args):
        # Make sure we've got our data
        if 'recursion_stopper_count' not in data:
            data['recursion_stopper_count'] = {}

        # Find our current count set and see if we've reached our limit
        counts = data['recursion_stopper_count']
        if self not in counts:
            counts[self] = 0
        if counts[self] >= self.recursion_limit:
            return default_return

        try:
            # Increment our count and recurse
            counts[self] += 1
            return getattr(self.element, method_name)(*args)
        finally:
            # Clean up regardless of what happened
            counts[self] -= 1

    def get_minimum_size(self, data):
        self._do_recursion(data, 'get_minimum_size', datatypes.Point(), data)

    def render(self, rect, data):
        self._do_recursion(data, 'render', None, rect, data)
