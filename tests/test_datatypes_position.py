import unittest
from layout.datatypes.position import *

class TestRectangle(unittest.TestCase):
    def test_fields(self):
        r = Rectangle(1,2,3,4)
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 2)
        self.assertEqual(r.w, 3)
        self.assertEqual(r.h, 4)

    def test_slots(self):
        r = Rectangle(1,2,3,4)
        self.assertRaises(AttributeError, setattr, r, 'z', 2)

    def test_display(self):
        self.assertEqual(
            repr(Rectangle(1,2,3,4)),
            "Rectangle(1.000000, 2.000000, 3.000000, 4.000000)"
            )

    def test_get_data(self):
        self.assertEqual(Rectangle(1,2,3,4).get_data(), (1,2,3,4))

    def test_additional_fields(self):
        r = Rectangle(1,2,3,4)

        self.assertEqual(r.top, 6)
        self.assertEqual(r.bottom, 2)
        self.assertEqual(r.left, 1)
        self.assertEqual(r.right, 4)
        self.assertEqual(r.t, 6)
        self.assertEqual(r.b, 2)
        self.assertEqual(r.l, 1)
        self.assertEqual(r.r, 4)

        self.assertEqual(r.center, 2.5)
        self.assertEqual(r.middle, 4)
        self.assertEqual(r.c, 2.5)
        self.assertEqual(r.m, 4)

        self.assertEqual(r.top_left, Point(1, 6))
        self.assertEqual(r.left_top, Point(1, 6))
        self.assertEqual(r.tl, Point(1, 6))
        self.assertEqual(r.lt, Point(1, 6))
        self.assertEqual(r.bottom_left, Point(1, 2))
        self.assertEqual(r.bottom_right, Point(4, 2))
        self.assertEqual(r.top_right, Point(4, 6))
        self.assertEqual(r.center_middle, Point(2.5, 4))

    def test_equals(self):
        self.assertEqual(Rectangle(1,2,3,4), Rectangle(1.0, 2.0, 3.0, 4.0))
        self.assert_(Rectangle(1,2,3,4) != Rectangle(4,3,2,1))

class TestPoint(unittest.TestCase):
    def test_display(self):
        self.assertEqual(
            repr(Point(2,3)),
            "Point(2.000000, 3.000000)"
            )

    def test_default(self):
        p = Point()
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 0)

    def test_slots(self):
        p = Point()
        self.assertRaises(AttributeError, setattr, p, 'z', 2)

    def test_fields(self):
        p = Point(2,3)
        self.assertEqual(p.x, 2)
        self.assertEqual(p.y, 3)

    def test_get_data(self):
        p = Point(2,3)
        self.assertEqual(p.get_data(), (2,3))

    def test_equals(self):
        self.assertEqual(Point(2,3), Point(2.0, 3.0))
        self.assert_(Point(2,3) != Point(3,2))

    def test_add(self):
        self.assertEqual(Point(2,3)+Point(1,2), Point(3,5))
        p1 = Point(2,3)
        p1 += Point(1,2)
        self.assertEqual(p1, Point(3,5))

    def test_subtract(self):
        self.assertEqual(Point(2,3)-Point(1,2), Point(1,1))
        p1 = Point(2,3)
        p1 -= Point(1,2)
        self.assertEqual(p1, Point(1,1))

    def test_negative(self):
        self.assertEqual(-Point(2,3), Point(-2, -3))
        self.assertEqual(Point(0,0), Point(0,0))

    def test_iterate(self):
        for test, value in zip(Point(2,3), (2,3)):
            self.assertEqual(test, value)

    def test_magnitudes(self):
        self.assertAlmostEqual(Point(4,3).get_magnitude(), 5)
        self.assertAlmostEqual(Point(4,3).get_magnitude_squared(), 25)

    def test_copy(self):
        p = Point(2,3)
        self.assertEqual(p.get_copy(), p)
        self.assertFalse(p.get_copy() is p)

    def test_multiply(self):
        self.assertEqual(Point(2,3) * 3, Point(6,9))

        p1 = Point(2,3)
        p1 *= 3
        self.assertEqual(p1, Point(6,9))

        self.assertEqual(3 * Point(2,3), Point(6,9))

        def fn():
            return Point(2,3) * Point(1,2)
        self.assertRaises(TypeError, fn)

        def fn():
            p = Point(2,3)
            p *= Point(1,2)
        self.assertRaises(TypeError, fn)

    def test_divide(self):
        self.assertEqual(Point(2,3) / 2.0, Point(1.0, 1.5))

        p1 = Point(2,3)
        p1 /= 2.0
        self.assertEqual(p1, Point(1.0, 1.5))

        def fn():
            return Point(2,3) / Point(1,2)
        self.assertRaises(TypeError, fn)

        def fn():
            return 2.0 / Point(2,3)
        self.assertRaises(TypeError, fn)

    def test_component_product(self):
        self.assertEqual(
            Point(2,3).get_component_product(Point(2,3)),
            Point(4,9)
            )
        self.assertEqual(
            Point(2,3).get_component_product(Point(2,0)),
            Point(4,0)
            )

    def test_normalized(self):
        p = Point(3, 4).get_normalized()
        self.assertAlmostEqual(p.x, 0.6)
        self.assertAlmostEqual(p.y, 0.8)

        self.assertEqual(Point(0,0).get_normalized(), Point(0,0))

    def test_get_angle(self):
        self.assertAlmostEqual(Point(1,0).get_angle(), 0.0)
        self.assertAlmostEqual(Point(0,1).get_angle(), math.pi * 0.5)
        self.assertAlmostEqual(Point(-1,0).get_angle(), math.pi)
        self.assertAlmostEqual(Point(0,-1).get_angle(), -math.pi * 0.5)

    def test_right_normal(self):
        self.assertEqual(Point(2,3).get_right_normal(), Point(3, -2))
        self.assertEqual(Point(0,0).get_right_normal(), Point(0, 0))

    def test_left_normal(self):
        self.assertEqual(Point(2,3).get_left_normal(), Point(-3, 2))
        self.assertEqual(Point(0,0).get_left_normal(), Point(0, 0))

    def test_rotate(self):
        p = Point(2,3).get_rotated(math.pi * 0.5)
        self.assertAlmostEqual(p.x, -3)
        self.assertAlmostEqual(p.y, 2)
        p = Point(2,3).get_rotated(math.pi * 0.5)
        self.assertAlmostEqual(p.x, -3)
        self.assertAlmostEqual(p.y, 2)

    def test_mirror(self):
        self.assertEqual(Point(2,3).get_x_mirror(), Point(-2, 3))
        self.assertEqual(Point(2,3).get_y_mirror(), Point(2, -3))
        self.assertEqual(Point(0,3).get_x_mirror(), Point(0, 3))
        self.assertEqual(Point(2,0).get_y_mirror(), Point(2, 0))

    def test_scalar_product(self):
        self.assertEqual(Point(2,3).get_scalar_product(Point(3,-2)), 0)
        self.assertEqual(Point(1,0).get_scalar_product(Point(-3,2)), -3)

    def test_angle(self):
        self.assertAlmostEqual(
            Point(2,3).get_angle_between(Point(3, -2)),
            math.pi * 0.5
            )
        self.assertAlmostEqual(
            Point(2,3).get_angle_between(Point(-3, 2)),
            math.pi * 0.5
            )
        self.assertAlmostEqual(
            Point(2,3).get_angle_between(Point(-2, -3)),
            math.pi
            )
        self.assertAlmostEqual(Point(2,3).get_angle_between(Point(2, 3)), 0)

    def test_min(self):
        p = Point(2,3)
        p = p.get_minimum(Point(3,2))
        self.assertEqual(p.x, 2)
        self.assertEqual(p.y, 2)
        p = p.get_minimum(Point(1,6))
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_max(self):
        p = Point(2,3)
        p = p.get_maximum(Point(3,2))
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 3)
        p = p.get_maximum(Point(1,6))
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 6)

    def test_random(self):
        for i in range(10):
            p = Point.get_random(Point(1,1), Point(4,4))
            self.assert_(1 <= p.x <= 4 and 1 <= p.y <= 4)


