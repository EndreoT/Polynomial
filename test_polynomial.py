import unittest
import random
from polynomial import Polynomial


test_polynomial_1 = Polynomial([(6.3, -13.2), (3, -11), (8, 6), (4, 9), (-4, 8), (9, 9), (2, 6), (2, 5.6), (10, 1), (-7, 0)])
# 63/10X^-66/5 + 3X^-11 + 13X^9 - 4X^8 + 10X^6 + 2X^28/5 + 10X - 7

test_polynomial_2 = Polynomial([(1, 11.1), (-6, 13), (7, 11.1),  (6, 0), (4, 6), (3, -2), (4, 12)])
# -6X^13 + 4X^12 + 8X^111/10 + 4X^6 + 3X^-2 + 6# -6X^13 + 4X^12 + 8X^111/10 + 4X^6 + 3X^-2 + 6


class TestPolynomial(unittest.TestCase):

    def setUp(self):
        self.poly_1 = test_polynomial_1
        self.poly_2 = test_polynomial_2

    def test_polynomial_init(self):
        tuple_array = [(4, -6), (3, 5), (45, 2.3), (-34, 0), (3, 5.8), (4, 0)]
        array = [1, 0, 5, 1/3, 6, 4.4, 0, 0, 0]
        list_array = [13, 9, 0, 0, 0, 16, 3]
        tuple_equivalent = [(13, 0), (2, 5), (3, 6), (6, 5), (8, 5), (9, 1), (0, 34), (0, 2345)]
        list_of_zeroes = [0 for _ in range(25)]
        zero_tuple_array = [(0, 0)]
        empty_list = []
        incorrect_objects = [("4", 4), (5, 8), (234, 4)]
        more_incorrect_objects = ["3", 5, 3, 6, 3]

        poly = Polynomial(tuple_array)
        poly_str = "4X^-6 + 3X^29/5 + 3X^5 + 45X^23/10 - 30"
        self.assertEqual(str(poly), poly_str)

        poly_from_array = Polynomial(array)
        poly_from_array_str = "22/5X^5 + 6X^4 + 1/3X^3 + 5X^2 + 1"
        self.assertEqual(str(poly_from_array), poly_from_array_str)

        self.assertEqual(Polynomial(tuple_equivalent).get_poly(), Polynomial(list_array).get_poly())

        self.assertEqual(Polynomial(list_of_zeroes).get_poly(), [(0, 0)])
        self.assertEqual(Polynomial(zero_tuple_array).get_poly(), [(0, 0)])
        self.assertEqual(Polynomial(empty_list).get_poly(), [(0, 0)])
        self.assertRaises(ValueError, Polynomial, incorrect_objects)
        self.assertRaises(ValueError, Polynomial, more_incorrect_objects)

    def test_check_if_tuple_contains_coefficients(self):
        incorrect_list = [(0, 4), (0, 345), (0, 18), (0, 46)]
        self.assertEqual(Polynomial._check_if_tuple_contains_coefficients(incorrect_list), False)

    def test_check_if_correctly_formatted_tuple_true(self):
        incorrectly_formatted_tuple_list = [(3, 4), (4, 6), (234, 9), (3, 0)]
        self.assertEqual(Polynomial._check_if_correctly_formatted_tuple(incorrectly_formatted_tuple_list), True)

    def test_check_if_correctly_formatted_tuple_false(self):
        incorrectly_formatted_tuple_list = [(3, 4), 5, (4, 6), (234, 9), (3, 0)]
        self.assertEqual(Polynomial._check_if_correctly_formatted_tuple(incorrectly_formatted_tuple_list), False)

    def test_collect_terms(self):
        array = [(1, 0), (4, 0), (3, 5), (2, 7), (27, 7), (6, 7), (2, 2), (5, 2)]
        final_vector = {(5, 0), (7, 2), (3, 5), (35, 7)}
        self.assertEqual(set(Polynomial._collect_terms(array)), final_vector)

    def test_sort_tuple_list(self):
        array = [
            (6.3, -13.2), (3, -11), (14, 6), (4, 9),
            (-4, 8), (9, 9), (2, 5.6), (10, 1), (-1, 0),
            (1, 11.1), (-6, 13), (7, 11.1), (3, -2), (4, 12)
        ]
        target = [
            (6.3, -13.2), (3, -11), (3, -2), (-1, 0),
            (10, 1), (2, 5.6), (14, 6), (-4, 8), (4, 9),
            (9, 9), (1, 11.1), (7, 11.1), (4, 12), (-6, 13)
        ]
        self.assertEqual(Polynomial.sort_tuple_list(array), target)

    def test_array_contains_only_int_float(self):
        right_array = [3, -5, 3.4, 23/7, 654.345, -345.6]
        wrong_array = ["a", 3, 5/3, 3.5]
        self.assertEqual(Polynomial.array_contains_only_int_float(right_array), 1)
        self.assertEqual(Polynomial.array_contains_only_int_float(wrong_array), -1)

    def test_add(self):
        addition = self.poly_1 + self.poly_2
        target_array = [
            (6.3, -13.2), (3, -11), (14, 6), (4, 9),
            (-4, 8), (9, 9), (2, 5.6), (10, 1), (-1, 0),
            (1, 11.1), (-6, 13), (7, 11.1), (3, -2), (4, 12)
        ]
        self.assertEqual(addition.get_poly(), Polynomial(target_array).get_poly())

    def test_subtract(self):
        subtraction = self.poly_1 - self.poly_2
        target_array = [
            (6.3, -13.2), (3, -11), (-3, -2), (-13, 0),
            (10, 1), (2, 5.6), (6, 6), (-4, 8),
            (13, 9), (-8, 11.1), (-4, 12), (6, 13)]

        self.assertEqual(subtraction.get_poly(), Polynomial(target_array).get_poly())

    def test_multiplication(self):
        poly_1 = Polynomial([(-3, 4), (5, -3), (5, 1)])  # -3X^4 + 5X^-3 + 5X
        poly_2 = Polynomial([(7, 2), (-3, -8), (6, 0)])  # 7X^2 -3X^-8 + 6
        mul = poly_1 * poly_2
        poly_target_str = "-15X^-11 - 15X^-7 - 21X^6 - 18X^4 + 9X^-4 + 35X^3 + 30X^-3 + 30X + 35X^-1"
        self.assertEqual(str(mul), poly_target_str)

    def test_constant_multiplication(self):
        poly = Polynomial([(3, 0), (4, -1), (-2, 9), (6, -8)])
        result_target = "-4X^9 + 12X^-8 + 8X^-1 + 6"
        poly.constant_mul(2)
        self.assertEqual(str(poly), result_target)

    def test_get_degree(self):
        self.assertEqual(self.poly_1.get_degree(), -13.2)

    def test_create_random_polynomial(self):
        random.seed(3789)
        terms = 20
        poly1 = Polynomial.create_random_polynomial()
        poly2 = Polynomial.create_random_polynomial(terms)

        self.assertEqual(type(poly1), Polynomial)
        self.assertEqual(type(poly2), Polynomial)

        number_of_terms = len(poly2)
        self.assertEqual(number_of_terms, terms)

    def test_polynomial_derivative(self):
        poly = Polynomial([(66/11, 11), (60/-8, -8), (48/8, 8), (-10, 7), (8, 6), (-5, -3), (3, 4), (4, 2), (2, 1)])
        poly.derive()
        poly_str_deriv = '66X^10 + 60X^-9 + 48X^7 - 70X^6 + 48X^5 + 15X^-4 + 12X^3 + 8X + 2'
        self.assertEqual(str(poly), poly_str_deriv)

    def test_polynomial_integral(self):
        poly = Polynomial([(6, 11), (-6, -12), (6, 10), (-10, -9), (8, 6), (-3, 5), (3, 4), (6, 0)])
        integral = Polynomial.get_integral(poly, 8)
        poly.integrate(8)
        poly_str_integral = '1/2X^12 + 6/11X^11 + 6/11X^-11 + 5/4X^-8 + 8/7X^7 - 1/2X^6 + 3/5X^5 + 6.0X + 8'
        self.assertEqual(str(integral), poly_str_integral)
        self.assertEqual(str(poly), poly_str_integral)

    def test_next_highest_index_bin_search(self):
        index = Polynomial.next_highest_index_bin_search([(1, -3), (-2, 1), (4, 2), (-6, 5)], 0)
        self.assertEqual(index, 1)

    def test_polynomial_string_representation(self):
        poly = Polynomial([(1, -3), (-2, 1), (4, 2), (-6, 5), (3, 0), (-1, 1)])
        self.assertEqual(str(poly), "-6X^5 + X^-3 + 4X^2 - 3X + 3")


if __name__ == "__main__":
    unittest.main()
