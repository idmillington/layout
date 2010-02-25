import unittest
from layout.managers.directional import *
from layout.datatypes import *

class DummyElement(object):
    def __init__(self, size):
        self.size = size
    def get_minimum_size(self, data):
        return self.size
    def render(self, rect, data):
        self.rect = rect

class TestEqualColumnsLM(unittest.TestCase):
    def _create_lm(self, *sizes):
        return EqualColumnsLM(elements=[
                DummyElement(Point(*size)) for size in sizes
                ])

    def test_minimum_size(self):
        e = self._create_lm()
        self.assertEqual(e.get_minimum_size(None), Point(0,0))

        e = self._create_lm((1,2), (3,4))
        self.assertEqual(e.get_minimum_size(None), Point(6,4))

    def test_render(self):
        e = self._create_lm((1,2), (3,4))
        e.render(Rectangle(0, 0, 8, 5), None)
        self.assertEqual(e.elements[0].rect, Rectangle(0, 0, 4, 5))
        self.assertEqual(e.elements[1].rect, Rectangle(4, 0, 4, 5))

    def test_render_offset(self):
        e = self._create_lm((1,2), (3,4))
        e.render(Rectangle(5, 4, 8, 5), None)
        self.assertEqual(e.elements[0].rect, Rectangle(5, 4, 4, 5))
        self.assertEqual(e.elements[1].rect, Rectangle(9, 4, 4, 5))
        
    def test_empty_column(self):
        e = self._create_lm((1,2), (3,4))
        e.elements[1:1] = [None]
        self.assertEqual(e.get_minimum_size(None), Point(9,4))

        e.render(Rectangle(0, 0, 12, 5), None)
        self.assertEqual(e.elements[0].rect, Rectangle(0, 0, 4, 5))
        self.assertEqual(e.elements[2].rect, Rectangle(8, 0, 4, 5))

class TestEqualRowsLM(unittest.TestCase):
    def _create_lm(self, *sizes):
        return EqualRowsLM(elements=[
                DummyElement(Point(*size)) for size in sizes
                ])

    def test_minimum_size(self):
        e = self._create_lm()
        self.assertEqual(e.get_minimum_size(None), Point(0,0))

        e = self._create_lm((2,1), (4,3))
        self.assertEqual(e.get_minimum_size(None), Point(4,6))

    def test_render(self):
        e = self._create_lm((2,1), (4,3))
        e.render(Rectangle(0, 0, 5, 8), None)
        self.assertEqual(e.elements[0].rect, Rectangle(0, 4, 5, 4))
        self.assertEqual(e.elements[1].rect, Rectangle(0, 0, 5, 4))

    def test_render_offset(self):
        e = self._create_lm((2,1), (4,3))
        e.render(Rectangle(5, 4, 5, 8), None)
        self.assertEqual(e.elements[0].rect, Rectangle(5, 8, 5, 4))
        self.assertEqual(e.elements[1].rect, Rectangle(5, 4, 5, 4))
        
    def test_empty_column(self):
        e = self._create_lm((2,1), (4,3))
        e.elements[1:1] = [None]
        self.assertEqual(e.get_minimum_size(None), Point(4, 9))

        e.render(Rectangle(0, 0, 5, 12), None)
        self.assertEqual(e.elements[0].rect, Rectangle(0, 8, 5, 4))
        self.assertEqual(e.elements[2].rect, Rectangle(0, 0, 5, 4))
        
        
class TestVerticalLM(unittest.TestCase):
    def _create_lm(self, *sizes):
        return VerticalLM(elements=[
                DummyElement(Point(*size)) for size in sizes
                ])
    
    def test_minimum_size(self):
        v = self._create_lm()
        self.assertEqual(v.get_minimum_size(None), Point(0,0))

        v = self._create_lm((1,2), (3,4))
        self.assertEqual(v.get_minimum_size(None), Point(3,6))

        v.horizontal_align = VerticalLM.ALIGN_LEFT
        self.assertEqual(v.get_minimum_size(None), Point(3,6))

        v.margin = 2
        self.assertEqual(v.get_minimum_size(None), Point(3,8))

    def test_render_minimum_size(self):
        v = self._create_lm((1,2), (3,4))
        v.render(Rectangle(0, 0, 3, 6), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 4, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_offset(self):
        v = self._create_lm((1,2), (3,4))
        v.render(Rectangle(5, 4, 3, 6), None)
        self.assertEqual(v.elements[0].rect, Rectangle(5, 8, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(5, 4, 3, 4))

    def test_render_h_align_left(self):
        v = self._create_lm((1,2), (3,4))
        v.horizontal_align = VerticalLM.ALIGN_LEFT
        v.render(Rectangle(0, 0, 3, 6), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 4, 1, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_h_align_right(self):
        v = self._create_lm((1,2), (3,4))
        v.horizontal_align = VerticalLM.ALIGN_RIGHT
        v.render(Rectangle(0, 0, 3, 6), None)
        self.assertEqual(v.elements[0].rect, Rectangle(2, 4, 1, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_h_align_center(self):
        v = self._create_lm((1,2), (3,4))
        v.horizontal_align = VerticalLM.ALIGN_CENTER
        v.render(Rectangle(0, 0, 3, 6), None)
        self.assertEqual(v.elements[0].rect, Rectangle(1, 4, 1, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_grow(self):
        v = self._create_lm((1,2), (3,4))
        v.render(Rectangle(0, 0, 4, 8), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 5, 4, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 4, 5))

    def test_render_v_align_top(self):
        v = self._create_lm((1,2), (3,4))
        v.vertical_align = VerticalLM.ALIGN_TOP
        v.render(Rectangle(0, 0, 3, 8), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 6, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 2, 3, 4))

    def test_render_v_align_bottom(self):
        v = self._create_lm((1,2), (3,4))
        v.vertical_align = VerticalLM.ALIGN_BOTTOM
        v.render(Rectangle(0, 0, 3, 8), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 4, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_v_align_middle(self):
        v = self._create_lm((1,2), (3,4))
        v.vertical_align = VerticalLM.ALIGN_MIDDLE
        v.render(Rectangle(0, 0, 3, 8), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 5, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 1, 3, 4))

    def test_render_v_align_equal_spacing(self):
        v = self._create_lm((1,2), (3,4))
        v.vertical_align = VerticalLM.ALIGN_EQUAL_SPACING
        v.render(Rectangle(0, 0, 3, 8), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 6, 3, 2))
        self.assertEqual(v.elements[1].rect, Rectangle(0, 0, 3, 4))

    def test_render_wrong_aligns(self):
        v = self._create_lm((1,2), (3,4))
        v.vertical_align = VerticalLM.ALIGN_CENTER
        self.assertRaises(ValueError, v.render, Rectangle(0,0,4,8), None)
        v.vertical_align = VerticalLM.ALIGN_TOP
        v.horizontal_align = VerticalLM.ALIGN_MIDDLE
        self.assertRaises(ValueError, v.render, Rectangle(0,0,4,8), None)
        
    def test_render_degenerate(self):
        self._create_lm().render(Rectangle(0,0,2,2), None)

        v = self._create_lm((1,2))
        v.render(Rectangle(0,0,4,4), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 4, 4))


class TestHorizontalLM(unittest.TestCase):
    def _create_lm(self, *sizes):
        return HorizontalLM(elements=[
                DummyElement(Point(*size)) for size in sizes
                ])
    
    def test_minimum_size(self):
        v = self._create_lm()
        self.assertEqual(v.get_minimum_size(None), Point(0,0))

        v = self._create_lm((1,2), (3,4))
        self.assertEqual(v.get_minimum_size(None), Point(4,4))

        v.vertical_align = HorizontalLM.ALIGN_TOP
        self.assertEqual(v.get_minimum_size(None), Point(4,4))

        v.margin = 2
        self.assertEqual(v.get_minimum_size(None), Point(6,4))

    def test_render_minimum_size(self):
        v = self._create_lm((2,1), (4,3))
        v.render(Rectangle(0, 0, 6, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(2, 0, 4, 3))

    def test_render_offset(self):
        v = self._create_lm((2,1), (4,3))
        v.render(Rectangle(5, 4, 6, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(5, 4, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(7, 4, 4, 3))
        
    def test_render_v_align_bottom(self):
        v = self._create_lm((2,1), (4,3))
        v.vertical_align = HorizontalLM.ALIGN_BOTTOM
        v.render(Rectangle(0, 0, 6, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 2, 1))
        self.assertEqual(v.elements[1].rect, Rectangle(2, 0, 4, 3))

    def test_render_v_align_top(self):
        v = self._create_lm((2,1), (4,3))
        v.vertical_align = HorizontalLM.ALIGN_TOP
        v.render(Rectangle(0, 0, 6, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 2, 2, 1))
        self.assertEqual(v.elements[1].rect, Rectangle(2, 0, 4, 3))

    def test_render_v_align_middle(self):
        v = self._create_lm((2,1), (4,3))
        v.vertical_align = HorizontalLM.ALIGN_MIDDLE
        v.render(Rectangle(0, 0, 6, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 1, 2, 1))
        self.assertEqual(v.elements[1].rect, Rectangle(2, 0, 4, 3))

    def test_render_grow(self):
        v = self._create_lm((2,1), (4,3))
        v.render(Rectangle(0, 0, 8, 4), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 3, 4))
        self.assertEqual(v.elements[1].rect, Rectangle(3, 0, 5, 4))

    def test_render_h_align_left(self):
        v = self._create_lm((2,1), (4,3))
        v.horizontal_align = HorizontalLM.ALIGN_LEFT
        v.render(Rectangle(0, 0, 8, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(2, 0, 4, 3))

    def test_render_h_align_right(self):
        v = self._create_lm((2,1), (4,3))
        v.horizontal_align = HorizontalLM.ALIGN_RIGHT
        v.render(Rectangle(0, 0, 8, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(2, 0, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(4, 0, 4, 3))

    def test_render_h_align_center(self):
        v = self._create_lm((2,1), (4,3))
        v.horizontal_align = HorizontalLM.ALIGN_CENTER
        v.render(Rectangle(0, 0, 8, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(1, 0, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(3, 0, 4, 3))

    def test_render_h_align_equal_spacing(self):
        v = self._create_lm((2,1), (4,3))
        v.horizontal_align = HorizontalLM.ALIGN_EQUAL_SPACING
        v.render(Rectangle(0, 0, 8, 3), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 2, 3))
        self.assertEqual(v.elements[1].rect, Rectangle(4, 0, 4, 3))

    def test_render_wrong_aligns(self):
        v = self._create_lm((2,1), (4,3))
        v.vertical_align = HorizontalLM.ALIGN_CENTER
        self.assertRaises(ValueError, v.render, Rectangle(0,0,8,4), None)
        v.vertical_align = HorizontalLM.ALIGN_TOP
        v.horizontal_align = HorizontalLM.ALIGN_MIDDLE
        self.assertRaises(ValueError, v.render, Rectangle(0,0,8,4), None)
        
    def test_render_degenerate(self):
        self._create_lm().render(Rectangle(0,0,2,2), None)

        v = self._create_lm((1,2))
        v.render(Rectangle(0,0,4,4), None)
        self.assertEqual(v.elements[0].rect, Rectangle(0, 0, 4, 4))
