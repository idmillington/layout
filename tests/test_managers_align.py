import unittest
from layout.managers.align import *
from layout.datatypes import *

class DummyElement(object):
    def __init__(self, size):
        self.size = size
    def get_minimum_size(self, data):
        return self.size
    def render(self, rect, data):
        self.rect = rect

class TestAlignLM(unittest.TestCase):
    def test_minimum_size(self):
        a = AlignLM(element=DummyElement(Point(2,1)))
        self.assertEquals(a.get_minimum_size(None), Point(2,1))

    def test_explicit_minimum_size(self):
        a = AlignLM(3, 2, element=DummyElement(Point(5, 4)))
        self.assertEquals(a.get_minimum_size(None), Point(5,4))

        a = AlignLM(5, 4, element=DummyElement(Point(3, 2)))
        self.assertEquals(a.get_minimum_size(None), Point(5,4))

    def test_render(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(0, 2, 2, 1))

    def test_render_offset(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(element=e)
        a.render(Rectangle(5, 4, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(5, 6, 2, 1))
        
    def test_render_center(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(horizontal_align=AlignLM.ALIGN_CENTER, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(1, 2, 2, 1))

    def test_render_right(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(horizontal_align=AlignLM.ALIGN_RIGHT, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(2, 2, 2, 1))

    def test_render_middle(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(vertical_align=AlignLM.ALIGN_MIDDLE, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(0, 1, 2, 1))

    def test_render_bottom(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(vertical_align=AlignLM.ALIGN_BOTTOM, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(0, 0, 2, 1))
        
    def test_render_grow_x(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(horizontal_align=AlignLM.GROW_X, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(0, 2, 4, 1))

    def test_render_grow_y(self):
        e = DummyElement(Point(2,1))
        a = AlignLM(vertical_align=AlignLM.GROW_Y, element=e)
        a.render(Rectangle(0, 0, 4, 3), None)
        self.assertEquals(e.rect, Rectangle(0, 0, 2, 3))
