from fractions import Fraction
import random
from typing import Any, List, Tuple, Union


# TODO allow for multi-variable polynomials (ex 3X^2YZ^3)


class Polynomial:
    """Creates a polynomial object from a list of tuples, or from a list."""

    def __init__(self, array: List[Union[int, float, Tuple[Union[int, float], Union[int, float]]]]):
        """
        Args:
            Two different types: First, a list of either type int or float. Second, a list of tuples
                of length two, each representing an algebraic polynomial term. The first tuple element corresponds
                to the term's coefficient and is either an int or float. The second tuple element
                corresponds to the term's power and is must also be either an int or float.
        Examples:
            >>> poly = Polynomial([(2, 3), (5, -2), (.5, 1), (6, 3)])
            >>> str(poly)
            '8X^3 + 5X^2 + 2X'
            >>> poly.get_poly()
            [(8, 3), (5, -2), (1/2, 1)]
            >>> poly2 = Polynomial([4, 2, 0, 5, 0])
            >>> str(poly2)
            '5X^3 + 2X + 4'
            >>> poly2.get_poly()
            [(4, 0), (2, 1), (5, 3)]
        """
        if not array or array == [(0, 0)]:
            self._poly = [(0, 0)]
        elif self._check_if_correctly_formatted_tuple(array):
            if not self._check_if_tuple_contains_coefficients(array):
                raise ValueError("Incorrect tuple formatting: *******at least one non-zero coefficient needed.")
            processed_array = self._collect_terms(array)
            self._poly = self.sort_tuple_list(processed_array)
        else:
            result = self.array_contains_only_int_float(array)
            if result == -1:
                raise ValueError("Incorrect list formatting.")
            elif result == 0:
                self._poly = [(0, 0)]
            else:
                self._poly = self.vector_to_poly(array)

    def get_poly(self):
        return self._poly

    def set_poly(self, poly):
        self._poly = poly

    @staticmethod
    def _check_if_correctly_formatted_tuple(array: List[Tuple[Union[int, float], Union[int, float]]]) -> bool:
        """
        Determines if every tuple in the array is correctly formatted.

        >>> Polynomial._check_if_correctly_formatted_tuple([(2, 3), (-2, .3), (2.2, -34.8)])
        True
        """
        for element in array:
            if not (type(element) is tuple
                    and len(element) == 2
                    and type(element[0]) in {int, float}
                    and type(element[1]) in {int, float}):
                return False
        return True

    @staticmethod
    def _check_if_tuple_contains_coefficients(array: List[Tuple[Union[int, float], Union[int, float]]]) -> bool:
        """
        >>> Polynomial._check_if_tuple_contains_coefficients([(0, 3), (0, 5), (0, -5)])
        False
        """
        return any(i for i, j in array)

    @staticmethod
    def _collect_terms(input_array: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        """
        Collects and combines same powered terms of a list of tuples.

        Example:
        >>> array = [(1, 1), (2, 1), (3, 2), (8, 2)]
        >>> Polynomial._collect_terms(array)
        [(3, 1), (11, 2)]
        """
        term_dict = dict()
        for i, j in input_array:
            if i != 0:
                term_dict[j] = term_dict.get(j, 0) + i
        items = term_dict.items()
        return [(j, i) for i, j in items]

    @staticmethod
    def sort_tuple_list(array: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        """Sorts the tuple array by each term's power in O(nlog(n)) time."""
        sorted_poly = sorted(array, key=lambda x: x[1])
        return sorted_poly

    @staticmethod
    def array_contains_only_int_float(array: List[Any]) -> int:
        """
        Determines if array only contains integers or floats.

        >>> Polynomial.array_contains_only_int_float([2, 3.5, 8, -34.2])
        1
        >>> Polynomial.array_contains_only_int_float([2, "", -34.2])
        -1
        """
        zeroes = 0
        for i in array:
            if type(i) not in {int, float}:
                return -1
            if i == 0:
                zeroes += 1
        if zeroes == len(array):
            return 0
        return 1

    @staticmethod
    def vector_to_poly(array: List[Union[int, float]]) -> List[Tuple[Union[int, float], Union[int, float]]]:
        """
        Converst list to list of tuples.
        >>>Polynomial.vector_to_poly([0, 2, 4, -9])
        [(2, 1), (4, 2), (-9, 3)]
        """
        return [(array[i], i) for i in range(len(array)) if array[i] != 0]

    @classmethod
    def create_random_polynomial(cls, number_of_terms: int = None) -> "Polynomial":
        """Create a random Polynomial object with an optional fixed number of terms."""
        if number_of_terms:
            if 1 > number_of_terms > 20:
                raise ValueError("number_of_terms must be > 1 and <= 20")
            num_terms = number_of_terms
        else:
            num_terms = random.randint(1, 10)
        largest_possible_term = random.randint(num_terms, 20)
        array = []
        for i in random.sample(range(0, largest_possible_term), num_terms):
            array.append((random.randint(1, 10), i))
        return cls(array)

    @staticmethod
    def merge(array_1: List[Tuple[Union[int, float], Union[int, float]]],
              array_2: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        """Merges two sorted array of tuples into one sorted array of tuples in O(n) time."""
        index_1 = 0
        index_2 = 0
        output = []
        while index_1 < len(array_1) and index_2 < len(array_2):
            i, j = array_1[index_1]
            m, n = array_2[index_2]
            if j == n:
                if i + m != 0:
                    output.append((i + m, j))
                index_1 += 1
                index_2 += 1
            elif j < n:
                output.append((i, j))
                index_1 += 1
            else:
                output.append((m, n))
                index_2 += 1
        while index_2 < len(array_2):
            output.append(array_2[index_2])
            index_2 += 1
        while index_1 < len(array_1):
            output.append(array_1[index_1])
            index_1 += 1
        return output

    def _addition_helper(self, poly_vector: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        return self.merge(self.get_poly(), poly_vector)

    def add(self, other_poly: "Polynomial") -> None:
        """O(n + nlog(n)) time <- confirm"""
        terms = self._addition_helper(other_poly.get_poly())
        self.set_poly(terms)

    def __add__(self, other: "Polynomial") -> "Polynomial":
        terms = self._addition_helper(other.get_poly())
        return Polynomial(terms)

    def _subtraction_helper(self, poly_vector: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        neg_poly = [(-i, j) for i, j in poly_vector]
        return self.merge(self.get_poly(), neg_poly)

    def subtract(self, other: "Polynomial") -> None:
        terms = self._subtraction_helper(other.get_poly())
        self.set_poly(terms)

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        terms = self._subtraction_helper(other.get_poly())
        return Polynomial(terms)

    def _multiplication_helper(self, poly_vector: List[Tuple[Union[int, float], Union[int, float]]]) \
            -> List[Tuple[Union[int, float], Union[int, float]]]:
        output = []
        for i in range(len(self.get_poly())):
            for j in range(len(poly_vector)):
                output.append(
                    (self.get_poly()[i][0] * poly_vector[j][0],
                     self.get_poly()[i][1] + poly_vector[j][1])
                )
        return self.sort_tuple_list(self._collect_terms(output))

    def mul(self, other: "Polynomial") -> None:
        terms = self._multiplication_helper(other.get_poly())
        self.set_poly(terms)

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        terms = self._multiplication_helper(other.get_poly())
        return Polynomial(terms)

    def constant_mul(self, constant: Union[int, float]) -> None:
        terms = ([(constant * i, j) for i, j in self.get_poly()])
        self.set_poly(terms)

    @classmethod
    def get_derivative(cls, poly: "Polynomial") -> "Polynomial":
        if type(poly) is not Polynomial:
            raise TypeError("Must use a Polynomial object")
        derivative = [(i * j, j - 1) for i, j in poly.get_poly() if j != 0]
        return cls(derivative)

    def derive(self) -> None:
        derivative = [(i * j, j - 1) for i, j in self.get_poly() if j != 0]
        self.set_poly(derivative)

    @staticmethod
    def _integration_helper(poly: "Polynomial", constant: Union[int, float]) -> \
            List[Tuple[Union[int, float], Union[int, float]]]:
        integral = []
        for i, j in poly.get_poly():
            if j != -1:
                integral.append((i / (j + 1), j + 1))
            else:
                raise ValueError("Polynomial class does not support integration of forms a*X^-1")
        index = poly.next_highest_index_bin_search(integral, 0)
        integral.insert(index, (constant, 0))
        return integral

    @classmethod
    def get_integral(cls, poly: "Polynomial", constant: Union[int, float]) -> "Polynomial":
        if type(poly) is not Polynomial:
            raise TypeError("Must use a Polynomial object")
        integral = Polynomial._integration_helper(poly, constant)
        return cls(integral)

    def integrate(self, constant: Union[int, float]):
        integral = self._integration_helper(self, constant)
        self.set_poly(integral)

    def get_degree(self) -> int:
        """Return power of the term with the highest degree absolute value power."""
        first = self.get_poly()[-1][1]
        last = self.get_poly()[0][1]
        if abs(first) >= abs(last):
            return first
        return last

    @staticmethod
    def next_highest_index_bin_search(array: List[Tuple[Union[int, float], Union[int, float]]],
                                      target: Union[int, float]):
        """
        Returns index of next largest value of target in the array of tuples.
        >>> Polynomial.next_highest_index_bin_search([(1, -3), (-2, 1), (4, 2), (-6, 5)], 0)
        1
        """

        low = 0
        high = len(array) - 1
        while low < high:
            mid = (high + low) // 2
            if high - low == 1:
                if array[low][1] == target:
                    return low
                elif array[high][1] == target:
                    return high
                elif array[low][1] > target:
                    return low
                elif array[low][1] < target < array[high][1]:
                    return high
                else:
                    return high + 1
            elif array[mid][1] < target:
                low = mid
            else:
                high = mid

    def __len__(self):
        return len(self.get_poly())

    def __eq__(self, other: "Polynomial"):
        return self.get_poly() == other.get_poly()

    def __iter__(self):
        return iter(self.get_poly())

    def __getitem__(self, item):
        return self.get_poly()[item]

    def __str__(self):

        def to_frac(val):
            return str(Fraction(val).limit_denominator(100))

        def add_term(coeff, power):
            end_term = False
            if coeff >= 0:
                sign = " + "
            else:
                sign = " - "
            if power == 0:
                # Constant term
                end_term = sign + str(abs(coeff))
            elif power == 1:
                if coeff == 1:
                    output.append(sign + "X")
                else:
                    output.append(sign + str(abs(coeff)) + "X")
            else:
                if len(output) == 0:
                    if abs(coeff) == 1:
                        if sign == " - ":
                            output.append("-")
                        output.append("X^" + to_frac(power))
                    else:
                        if sign == " + ":
                            output.append(to_frac(abs(coeff)) + "X^" + to_frac(power))
                        else:
                            output.append(to_frac(coeff) + "X^" + to_frac(power))
                else:
                    if abs(coeff) == 1:
                        output.append(sign + "X^" + to_frac(power))
                    else:
                        output.append(sign + to_frac(abs(coeff)) + "X^" + to_frac(power))
            if end_term:
                output.append(end_term)

        output = []
        low = 0
        high = len(self.get_poly()) - 1
        terms = self.get_poly()
        while low <= high:
            if low == high:
                term = terms[low]
                add_term(term[0], term[1])
                break
            elif abs(terms[low][1]) > abs(terms[high][1]):
                term = terms[low]
                add_term(term[0], term[1])
                low += 1
            elif abs(terms[low][1]) < abs(terms[high][1]):
                term = terms[high]
                add_term(term[0], term[1])
                high -= 1
            else:
                first = terms[high]
                second = terms[low]
                add_term(first[0], first[1])
                add_term(second[0], second[1])
                low += 1
                high -= 1
        return "".join(output)
