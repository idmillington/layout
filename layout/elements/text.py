import layout.managers.root as root
import layout.datatypes as datatypes
import layout.managers.directional as directional

class TextBase(root.LayoutElement):
    """Base class of things that track their font, color and alignment."""

    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER = 2

    def __init__(self, font_name="Helvetica", font_size=11,
                 color=(0,0,0), align=ALIGN_LEFT):
        self.color = color
        self.font_name = font_name
        self.font_size = font_size
        self.align = align

class Paragraph(TextBase):
    """
    A paragraph of text that will be fit in the given width.

    Because this class has a specific width it does not scale to fit
    with the room it is given. It may therefore overlap surrounding
    content unless it is wrapped in a scaling layout manager.
    """
    def __init__(self, text, width, font_name='Helvetica',
                 font_size=11, color=(0,0,0),
                 leading=1.3, paragraph_indent=True):
        super(Paragraph, self).__init__(font_name, font_size, color)
        self.text = text
        self.width = width
        self.paragraph_indent = paragraph_indent
        self.leading = leading

    def _set_text(self, text):
        self._text = text
        # Clear calculated quantities
        self._layout = None
        self.height = 0
    def _get_text(self):
        return self._text
    text = property(_get_text, _set_text)

    def _do_layout(self, data):
        """
        Lays the text out into separate lines and calculates their
        total height.
        """
        c = data['output']
        word_space = c.text_width(
            ' ',
            font_name=self.font_name,
            font_size=self.font_size)

        # Arrange the text as words on lines
        self._layout = [[]]
        x = self.font_size if self.paragraph_indent else 0
        for word in self.text.split():
            ww = c.text_width(
                word,
                font_name=self.font_name,
                font_size=self.font_size)
            if x + ww > self.width:
                # Newline
                x = 0
                self._layout.append([])
            self._layout[-1].append(word)
            x += ww + word_space

        # Work out the height we need
        num_lines = len(self._layout)
        self.height = (
            num_lines * self.font_size +
            (num_lines-1)*(self.font_size * (self.leading - 1.0))
            )

    def get_minimum_size(self, data):
        if not self._layout:
            self._do_layout(data)
        return datatypes.Point(self.width, self.height)

    def render(self, rect, data):
        if not self._layout:
            self._do_layout(data)
        c = data['output']
        with c:
            y = rect.y + rect.h - self.font_size
            x = rect.x + (self.font_size if self.paragraph_indent else 0)
            for line in self._layout:
                c.draw_text(
                    ' '.join(line), x, y,
                    font_name=self.font_name,
                    font_size=self.font_size,
                    fill=self.color
                    )

                x = rect.x
                y -= self.font_size * self.leading


class TextLine(TextBase):
    """
    An unsplittable line of text formatted in a single font and size.
    """
    def __init__(self, text,
                 font_name="Helvetica", font_size=11,
                 color=(0,0,0), align=TextBase.ALIGN_LEFT):
        super(TextLine, self).__init__(font_name, font_size, color, align)
        self.text = text

    def get_minimum_size(self, data):
        c = data['output']
        width = c.text_width(
            self.text,
            font_name=self.font_name,
            font_size=self.font_size
            )
        return datatypes.Point(width, self.font_size)

    def render(self, rect, data):
        # Calculate the y coordinate including the descender (so we fit in
        # the box rather than resting on the bottom edge of it).
        y = rect.y + self.font_size*0.2

        # Draw the text at the appropriate alignment
        if self.align == TextLine.ALIGN_LEFT:
            x = rect.left
        else:
            align = 1 if self.align == TextLine.ALIGN_RIGHT else 0.5
            width = self.get_minimum_size(data).x
            x = rect.left + (rect.w - width) * align
        data['output'].draw_text(
            self.text, x, y,
            font_name=self.font_name,
            font_size=self.font_size,
            fill=self.color
            )

class TextBlock(TextBase):
    """
    A set of simple text lines. Each line in the list can be prepended
    with a + sign to make it bold.
    """
    def __init__(self, lines,
                 font_name="Helvetica", font_size=11,
                 color=(0,0,0), align=TextBase.ALIGN_LEFT, gap=5):
        super(TextBlock, self).__init__(font_name, font_size, color, align)
        self.gap = gap
        self.lines = lines

        self.vertical = directional.VerticalLM(
            gap,
            vertical_align = directional.VerticalLM.ALIGN_TOP
            )
        for text in self.lines:
            font_name = self.font_name
            if text and text[0] == '+':
                text = text[1:]
                font_name += '-Bold'
            self.vertical.add_element(TextLine(
                    text, font_name, self.font_size, self.color, self.align
                    ))

    def get_minimum_size(self, data):
        return self.vertical.get_minimum_size(data)

    def render(self, rect, data):
        return self.vertical.render(rect, data)


