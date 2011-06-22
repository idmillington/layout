import unittest
from layout.datatypes.parse_dimensions import *

class TestParseDimension(unittest.TestCase):
    def test_dimensionless(self):
        self.assertEqual(parse_dimension('1'), 1)
        self.assertEqual(parse_dimension('14'), 14)
        self.assertEqual(parse_dimension('2.5'), 2.5)
        self.assertEqual(parse_dimension('.25'), 0.25)
        self.assertEqual(parse_dimension('2.'), 2.0)
        self.assertEqual(parse_dimension('-16'), -16)

    def test_points(self):
        self.assertEqual(parse_dimension('1pt'), 1)
        self.assertEqual(parse_dimension('1 pt'), 1)
        self.assertEqual(parse_dimension('1pts'), 1)
        self.assertEqual(parse_dimension('1 pts'), 1)
        self.assertEqual(parse_dimension('1point'), 1)
        self.assertEqual(parse_dimension('1 point'), 1)
        self.assertEqual(parse_dimension('1points'), 1)
        self.assertEqual(parse_dimension('1 points'), 1)

    def test_inches(self):
        self.assertEqual(parse_dimension('1in'), 72)
        self.assertEqual(parse_dimension('1inch'), 72)
        self.assertEqual(parse_dimension('1inches'), 72)
        self.assertEqual(parse_dimension('1 in'), 72)
        self.assertEqual(parse_dimension('1"'), 72)
        self.assertEqual(parse_dimension('1.25"'), 90.0)

    def test_mm(self):
        self.assertEqual(parse_dimension('1mm'), 2.8346456692913389)
        self.assertEqual(parse_dimension('1 mm'), 2.8346456692913389)
        self.assertEqual(parse_dimension('1.25mm'), 3.5433070866141736)

    def test_cm(self):
        self.assertEqual(parse_dimension('1cm'), 28.346456692913385)
        self.assertEqual(parse_dimension('1 cm'), 28.346456692913385)
        self.assertEqual(parse_dimension('1.25cm'), 35.433070866141733)

class TestParseDimensions(unittest.TestCase):
    def test_separators(self):
        self.assertEqual(parse_dimensions('1x2'), (1, 2))
        self.assertEqual(parse_dimensions('1inx2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in x 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in x2in'), (72, 144))
        self.assertEqual(parse_dimensions('1inx 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in, 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in,2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in; 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in;2in'), (72, 144))
        self.assertEqual(parse_dimensions('1in-2in'), (72, 144))

    def test_positional_inferrence(self):
        self.assertEqual(parse_dimensions('1in, 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1, 2in'), (72, 144))
        self.assertEqual(parse_dimensions('1, 2'), (1, 2))
        self.assertEqual(parse_dimensions('1in, 2, 3in'), (72, 2, 216))
        self.assertEqual(parse_dimensions('1, 2, 3in'), (72, 144, 216))

