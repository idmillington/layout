import unittest
from layout.datatypes import *
from layout.managers.box import *

class DummyElement(object):
    def __init__(self, size):
        self.size = size
    def get_minimum_size(self, data):
        return self.size
    def render(self, rect, data):
        self.rect = rect

class BoxLMTest(unittest.TestCase):
    def test_center_minimum_size(self):
        b = BoxLM()
        b.center = DummyElement(Point(3,4))
        self.assertEqual(b.get_minimum_size(None), Point(3,4))

    def test_vertical_minimum_size(self):
        b = BoxLM()
        b.top = DummyElement(Point(4,2))
        b.center = DummyElement(Point(3,4))
        b.bottom = DummyElement(Point(5,1))
        self.assertEqual(b.get_minimum_size(None), Point(5,7))

    def test_horizontal_minimum_size(self):
        b = BoxLM()
        b.left = DummyElement(Point(2,4))
        b.center = DummyElement(Point(3,4))
        b.right = DummyElement(Point(1,5))
        self.assertEqual(b.get_minimum_size(None), Point(6,5))
        
    def test_margin_minimum_size(self):
        b = BoxLM()
        b.top = DummyElement(Point(4,2))
        b.center = DummyElement(Point(3,4))
        b.bottom = DummyElement(Point(5,1))
        b.margin = 1
        self.assertEqual(b.get_minimum_size(None), Point(5,9))

    def test_all_minimum_size(self):
        b = BoxLM()
        b.left = DummyElement(Point(2,5))
        b.top = DummyElement(Point(4,2))
        b.center = DummyElement(Point(3,4))
        b.bottom = DummyElement(Point(5,1))
        b.right = DummyElement(Point(2,4))
        b.margin = 1
        self.assertEqual(b.get_minimum_size(None), Point(9,10))
        
    
        
