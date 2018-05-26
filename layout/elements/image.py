import layout.managers.root as root
import layout.datatypes as datatypes

try:
    import Image as PIL
except ImportError:
    import warnings
    warnings.warn(
        "Python Imaging Library not found - you will not be able "
        "to use image elements.",
        ImportWarning
        )

class Image(root.LayoutElement):
    """Represents an image to be displayed at a fixed aspect ratio."""

    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER = 2

    ALIGN_TOP = 10
    ALIGN_MIDDLE = 11
    ALIGN_BOTTOM = 12

    def __init__(self, filename, min_width,
                 fixed_size = False,
                 horizontal_align=ALIGN_LEFT,
                 vertical_align=ALIGN_TOP):

        self.filename = filename
        self.image_size = PIL.open(filename).size
        self.ratio = float(self.image_size[1]) / float(self.image_size[0])
        self.min_width = min_width
        self.fixed_size = fixed_size
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

    def get_minimum_size(self, data):
        height = self.min_width * self.ratio
        return datatypes.Point(self.min_width, height)

    def render(self, rect, data):
        if self.fixed_size:
            width = self.min_width
            height = self.min_width * self.ratio
        else:
            # Check for which way round we're scaling.
            if (float(rect.h) / float(rect.w)) > self.ratio:
                # The space is taller than the image
                width = rect.w
                height = width * self.ratio
            else:
                # The space is wider than the image
                height = rect.h
                width = height / self.ratio

        # Check for extra space
        extra_width = rect.w - width
        extra_height = rect.h - height
        x = rect.x
        y = rect.y

        if self.horizontal_align == Image.ALIGN_CENTER:
            x += extra_width * 0.5
        elif self.horizontal_align == Image.ALIGN_RIGHT:
            x += extra_width

        if self.vertical_align == Image.ALIGN_MIDDLE:
            y += extra_height * 0.5
        elif self.vertical_align == Image.ALIGN_TOP:
            y += extra_height

        # Draw the image
        data['output'].draw_image(self.filename, x, y, width, height)

