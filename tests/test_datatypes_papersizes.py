import unittest
from layout.datatypes.papersizes import *

class TestPaperSizes(unittest.TestCase):
    def _check(self, size, target):
        self.assertAlmostEqual(size[0], target[0])
        self.assertAlmostEqual(size[1], target[1])
                               
    def test_a_series(self):
        self._check(A4, (210*mm, 297*mm))
        self._check(A[4], (210*mm, 297*mm))
        self._check(A7, (74*mm, 105*mm))
        self._check(A10, (26*mm, 37*mm))
        self._check(A[-1], (1189*mm, 1682*mm))
    
class TestPapersizeFunctions(unittest.TestCase):
    def test_landscape(self):
        self.assertEqual(landscape((2,1)), (2,1))
        self.assertEqual(landscape((1,2)), (2,1))
        self.assertEqual(landscape((2,2)), (2,2))
        
    def test_portrait(self):
        self.assertEqual(portrait((2,1)), (1,2))
        self.assertEqual(portrait((1,2)), (1,2))
        self.assertEqual(portrait((2,2)), (2,2))
        
    def test_flip(self):
        self.assertEqual(flip((2,1)), (1,2))
        self.assertEqual(flip((1,2)), (2,1))
        self.assertEqual(flip((2,2)), (2,2))

    def test_small_square(self):
        self.assertEqual(small_square((2,1)), (1,1))
        self.assertEqual(small_square((3,3)), (3,3))
        
    def test_large_square(self):
        self.assertEqual(large_square((2,1)), (2,2))
        self.assertEqual(large_square((3,3)), (3,3))
        
    def test_is_landscape(self):
        assert not is_landscape((1,2))
        assert is_landscape((2,1))
        assert not is_landscape((2,2))

    def test_is_portrait(self):
        assert is_portrait((1,2))
        assert not is_portrait((2,1))
        assert not is_portrait((2,2))

    def test_is_square(self):
        assert not is_square((1,2))
        assert not is_square((2,1))
        assert is_square((2,2))
        
    def test_bleed(self):
        self.assertEqual(bleed((10, 10), 3), (16, 16))
        self.assertEqual(bleed((5, 5), 0), (5, 5))
        
class TextCalculateUp(unittest.TestCase):
    def test_type(self):
        result = calculate_up((10, 20), (3, 4), 0, 0, 0)
        self.assertEqual(result, (3, 5, False))
        self.assertEqual(type(result[0]), int)
        self.assertEqual(type(result[1]), int)
        self.assertEqual(type(result[2]), bool)
    
    def test_rotated(self):
        result = calculate_up((12, 18), (3, 4), 0, 0, 0)
        self.assertEqual(result, (3, 6, True))
        
    def test_bleed(self):
        result = calculate_up((12, 18), (1, 2), 1, 0, 0)
        self.assertEqual(result, (3, 6, True))

    def test_separation(self):
        result = calculate_up((11, 17), (2, 3), 0, 1, 0)
        self.assertEqual(result, (3, 6, True))
        
    def test_margin(self):
        result = calculate_up((14, 20), (3, 4), 0, 0, 1)
        self.assertEqual(result, (3, 6, True))
        
