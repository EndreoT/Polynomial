import unittest
import random
from polynomial import Polynomial


test_polynomial_1 = Polynomial([(6, 13), (3, 11), (8, 10), (4, 9), (4, 8), (9, 7), (2, 6), (2, 5), (10, 1), (7, 0)])
# 6X^13 + 3X^11 + 8X^10 + 4X^9 + 4X^8 + 9X^7 + 2X^6 + 2X^5 + 10X + 7

test_polynomial_2 = Polynomial([(6, 13), (4, 12), (7, 11), (4, 6), (3, 2), (6, 0)])
# 6X^13 + 4X^12 + 7X^11 + 4X^6 + 3X^2 + 6


class TestPolynomial(unittest.TestCase):

    def setUp(self):
        self.poly_1 = test_polynomial_1
        self.poly_2 = test_polynomial_2

    def test_polynomial_init(self):
        array = [1, 0, 5, 1/3, 6, 4.4, 0, 0, 0]
        tuple_array = [(13, 0), (2, 5), (3, 6), (6, 5), (8, 5), (9, 1), (0, 34), (0, 2345)]
        incorrect_list = [0 for _ in range(25)]
        empty_list = []
        negative_powers = [(4, -6), (3, 5), (45, 124), (34, 0)]
        non_int_powers = [(3, 5.8), (4, 0), (45, 234), (5, 7)]
        incorrect_objects = [("4", 4), (5, 8), (234, 4)]
        more_incorrect_objects = ["3", 5, 3, 6, 3]

        poly = Polynomial(array)
        poly_str = "22/5X^5 + 6X^4 + 1/3X^3 + 5X^2 + 1"
        self.assertEqual(str(poly), poly_str)

        poly_array = [13, 9, 0, 0, 0, 16, 3]
        self.assertEqual(Polynomial(tuple_array).get_vector_repr(), poly_array)

        self.assertRaises(ValueError, Polynomial, incorrect_list)
        self.assertRaises(ValueError, Polynomial, empty_list)
        self.assertRaises(ValueError, Polynomial, negative_powers)
        self.assertRaises(ValueError, Polynomial, non_int_powers)
        self.assertRaises(ValueError, Polynomial, incorrect_objects)
        self.assertRaises(ValueError, Polynomial, more_incorrect_objects)

    def test_check_if_list_only_contains_zeroes(self):
        incorrect_list = [0 for _ in range(25)]
        self.assertEqual(Polynomial._check_if_list_only_contains_zeroes(incorrect_list), True)

    def test_check_if_tuple_contains_coefficients(self):
        incorrect_list = [(0, 4), (0, 345), (0, 18), (0, 46)]
        self.assertEqual(Polynomial._check_if_tuple_contains_coefficients(incorrect_list), False)

    def test_check_if_correctly_formatted_tuple(self):
        incorrectly_formatted_tuple_list = [(3, 4), 5, (4, 6), (234, 9), (3, 0)]
        self.assertEqual(Polynomial._check_if_correctly_formatted_tuple(incorrectly_formatted_tuple_list), False)

    def test_trim_array(self):
        array = [0, 3, 5, 0, 6, 0, 34, 0, 0, 0, 0, 0, 0]
        trimmed_array = [0, 3, 5, 0, 6, 0, 34]
        self.assertEqual(Polynomial._trim_array(array), trimmed_array)

    def test_collect_terms(self):
        array = [(1, 0), (4, 0), (3, 5), (2, 7), (27, 7), (6, 7), (2, 2), (5, 2)]
        final_vector = {(5, 0), (7, 2), (3, 5), (35, 7)}
        self.assertEqual(set(Polynomial._collect_terms(array)), final_vector)

    def test_add(self):
        result = self.poly_1 + self.poly_2
        target_array = [
            (13, 0), (10, 1), (3, 2), (2, 5), (6, 6), (9, 7),
            (4, 8), (4, 9), (8, 10), (10, 11), (4, 12), (12, 13)
            ]
        self.assertEqual(result, Polynomial(target_array))

    def test_subtract(self):
        result = self.poly_1 - self.poly_2
        target_array = [1, 10, -3, 0, 0, 2, -2, 9, 4, 4, 8, -4, -4]
        self.assertEqual(result, Polynomial(target_array))

    def test_multiplication(self):
        result = self.poly_1 * self.poly_2
        poly_target_str = '36X^26 + 24X^25 + 60X^24 + 60X^23 + 77X^22 + 96X^21 + 98X^20 + 100X^19 + 83X^18 + 34X^17 ' \
                          '+ 46X^16 + 34X^15 + 76X^14 + 163X^13 + 130X^12 + 87X^11 + 60X^10 + 51X^9 + 30X^8 + 100X^7 ' \
                          '+ 40X^6 + 12X^5 + 30X^3 + 21X^2 + 60X + 42'
        self.assertEqual(str(result), poly_target_str)

    def test_constant_multiplication(self):
        poly = Polynomial([3, 4, 2, 6, 0, 5, 0, 3, 2])
        result_target = [12, 16, 8, 24, 0, 20, 0, 12, 8]
        self.assertEqual(poly.constant_mul(4).get_vector_repr(), result_target)

    def test_get_degree(self):
        self.assertEqual(self.poly_1.get_degree(), 13)

    def test_create_random_polynomial(self):
        random.seed(3789)
        terms = 20
        poly1 = Polynomial.create_random_polynomial()
        poly2 = Polynomial.create_random_polynomial(terms)

        self.assertEqual(type(poly1), Polynomial)
        self.assertEqual(type(poly2), Polynomial)

        number_of_terms = len([i for i in poly2.get_vector_repr() if i])
        self.assertEqual(number_of_terms, terms)

    def test_polynomial_derivative(self):
        random.seed(9768)
        poly = Polynomial.create_random_polynomial()
        poly_str_deriv = '66X^10 + 60X^9 + 48X^7 + 70X^6 + 48X^5 + 15X^4 + 12X^3 + 8X + 2'
        self.assertEqual(str(poly.derive()), poly_str_deriv)

    def test_polynomial_integral(self):
        random.seed(9768)
        poly = Polynomial.create_random_polynomial()
        poly_str_integral = '1/2X^12 + 6/11X^11 + 2/3X^9 + 5/4X^8 + 8/7X^7 + 1/2X^6 + 3/5X^5 + 4/3X^3 + X^2 + 6X + 8'
        self.assertEqual(str(poly.integrate(8)), poly_str_integral)


if __name__ == "__main__":
    unittest.main()
