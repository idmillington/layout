# -*- coding: utf-8 -*-

"""Base class for output."""

import abc
import typing

Color = typing.Tuple[float, float, float]

class OutputTarget(metaclass=abc.ABCMeta):
    """
    To allow this package to work with various renderers, this defines
    an interface.
    """
    @abc.abstractmethod
    def _save_state(self) -> None:
        """Push current output settings on the stack."""
        pass

    @abc.abstractmethod
    def _restore_state(self) -> None:
        """Pop current output settings from the stack."""
        pass

    def __enter__(self):
        self._save_state()

    def __exit__(self, type, value, traceback):
        self._restore_state()

    @abc.abstractmethod
    def translate(self, x:float, y:float) -> None:
        """Translate the current rendering context."""
        pass

    @abc.abstractmethod
    def scale(self, x:float, y:float) -> None:
        """Scale the current rendering context."""
        pass

    @abc.abstractmethod
    def rotate(self, degrees:float) -> None:
        """Rotate the current rendering context."""
        pass

    @abc.abstractmethod
    def text_width(self, text:str, *, font_name:str, font_size:float) -> float:
        """The width of the given text string."""
        return 0

    @abc.abstractmethod
    def draw_text(self, text:str, x:float, y:float, *,
                  font_name:str, font_size:float, fill:Color) -> None:
        """Draws the given text at x,y."""
        pass

    @abc.abstractmethod
    def draw_line(
            self, x0:float, y0:float, x1:float, y1:float, *,
            stroke:Color,
            stroke_width:float=1,
            stroke_dash:typing.Sequence=None
            ) -> None:
        """Draws the given line."""
        pass

    @abc.abstractmethod
    def draw_rect(
            self, x:float, y:float, w:float, h:float, *,
            stroke:Color=None,
            stroke_width:float=1,
            stroke_dash:typing.Sequence=None,
            fill:Color=None
            ) -> None:
        """Draws the given rectangle."""
        pass

    @abc.abstractmethod
    def draw_image(
            self, img_filename:str, x:float, y:float, w:float, h:float
            ) -> None:
        """Draws the given image."""
        pass

    @abc.abstractmethod
    def draw_polygon(
            self,
            *pts,
            close_path:bool=True,
            stroke:Color=None,
            stroke_width:float=1,
            stroke_dash:typing.Sequence=None,
            fill:Color=None
            ) -> None:
        """Draws the given linear path."""
        pass

    @abc.abstractmethod
    def clip_rect(self, x:float, y:float, w:float, h:float) -> None:
        """Clip further output to this rect."""
        pass

    @abc.abstractmethod
    def end_page(self) -> None:
        """Complete the previous page and prepare to begin a new page."""
        pass
