from typing import List, Tuple, Union
import operator
import random
from fractions import Fraction


class Polynomial:
    """Creates a polynomial object from a list of tuples, or a list."""

    def __init__(self, array: List[
            Union[int, float, Fraction, Tuple[Union[int, float, Fraction], Union[int, Fraction]
            ]]]):
        """
        Args:
            Two different types: First, a list of either type int, float, or Fraction objects. Second, a list of tuples
                of length two, each representing an algebraic polynomial term. The first tuple element corresponds
                to the term's coefficient and is either an int, float or Fraction. The second tuple element
                corresponds to the term's power and must evaluate to a positive integer >= 0

        Examples:
            >>> poly = Polynomial([(2, 3), (5, 2), (2, 1), (6, 3)])
            >>> str(poly)
            '8X**3 + 5X**2 + 2X'
            >>> poly.get_vector_str()
            ['0', '2', '5', '8']
            >>> poly2 = Polynomial([4, 2, 0, 5, 0])
            >>>str(poly2)
            '5X**3 + 2X + 4'
            >>> poly2.get_vector_str()
            ['4', '2', '0', '5']
        """
        if not array:
            raise ValueError("Array must not be empty")

        if self._check_if_correctly_formatted_tuple(array):
            array = [(Fraction(i), int(j)) for i, j in array]
            if not self._check_if_tuple_contains_coefficients(array):
                raise ValueError("Incorrect formatting: at least one non-zero coefficient needed")
            array = self._collect_terms(array)
            max_dimension = max(j for i, j in array) + 1
            empty_array = [0] * max_dimension
            for i, j in array:
                empty_array[j] = i
            vector_repr = [Fraction(i).limit_denominator(100) for i in empty_array]
            self.vector_repr = self._trim_array(vector_repr)

        elif all(type(x) in {int, float, Fraction} for x in array):
            if self._check_if_list_only_contains_zeroes(array):
                raise ValueError("Array must contain at lease one non-zero int, float, or Fraction")
            vector_repr = self._trim_array(array)
            self.vector_repr = [Fraction(i).limit_denominator(100) for i in vector_repr]
        else:
            raise ValueError("Incorrect list formatting")

    @staticmethod
    def _check_if_correctly_formatted_tuple(
            array: List[Tuple[Union[int, float, Fraction], Union[int, Fraction]]]) -> bool:
        """Determines if every tuple in the array is correctly formatted"""
        for element in array:
            if not (type(element) is tuple
                    and len(element) == 2
                    and type(element[1]) in {int, Fraction}
                    and element[1] >= 0):
                return False
            try:
                if element[1].denominator != 1:
                    return False
            except AttributeError:
                pass
        return True

    @staticmethod
    def _check_if_tuple_contains_coefficients(array: List[Tuple[Fraction, int]]) -> bool:
        return any(i for i, j in array)

    @staticmethod
    def _check_if_list_only_contains_zeroes(array: List[Union[int, float, Fraction]]) -> bool:
        return all(1 if not e else 0 for e in array)

    @staticmethod
    def _trim_array(array: List[Fraction]) -> List[Fraction]:
        """Removes unnecessary higher order terms with zero value constants"""
        index = len(array) - 1
        while array[index] == 0:
            index -= 1
        return array[:index + 1]

    @staticmethod
    def _collect_terms(input_array: List[Tuple[Fraction, int]]) -> List[Tuple[Fraction, int]]:
        """Collects non-unique powered terms"""
        not_unique = set()
        possibly_unique = set()
        for i, j in input_array:
            if j not in possibly_unique:
                possibly_unique.add(j)
            else:
                not_unique.add(j)
        terms_for_collecting = dict()
        terms_not_for_collecting = []
        for i, j in input_array:
            if j in not_unique:
                terms_for_collecting[j] = terms_for_collecting.get(j, 0) + i
            else:
                terms_not_for_collecting.append((i, j))
        collected_terms = list(terms_for_collecting.items())
        collected_terms = [(j, i) for i, j in collected_terms]
        terms_not_for_collecting.extend(collected_terms)
        return terms_not_for_collecting

    @classmethod
    def create_random_polynomial(cls, number_of_terms: int = None) -> "Polynomial":
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

    def _operation_helper(self, other: "Polynomial", operation: operator) -> List[Union[int, float, Fraction]]:
        size_difference = abs(len(self) - len(other))
        if size_difference:
            vector_extension = [0] * size_difference
            smaller_vector = min([self, other], key=len).get_vector_repr()
            larger_vector = max([self, other], key=len).get_vector_repr()
            smaller_vector.extend(vector_extension)
            assert len(smaller_vector) == len(larger_vector)
            return [operation(i, j) for (i, j) in zip(smaller_vector, larger_vector)]
        assert len(self) == len(other)
        return [operation(i, j) for (i, j) in zip(self.get_vector_repr(), other.get_vector_repr())]

    def add(self, other: "Polynomial") -> "Polynomial":
        return Polynomial(self._operation_helper(other, operator.add))

    def __add__(self, other: "Polynomial") -> "Polynomial":
        return self.add(other)

    def subtract(self, other: "Polynomial") -> "Polynomial":
        return Polynomial(self._operation_helper(other, operator.sub))

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        return self.subtract(other)

    def mul(self, other: "Polynomial") -> "Polynomial":
        output = []
        for i in range(len(self.get_vector_repr())):
            for j in range(len(other.get_vector_repr())):
                output.append(
                    (self.vector_repr[i] * other.get_vector_repr()[j], i + j))
        return Polynomial(output)

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        return self.mul(other)

    def constant_mul(self, constant: int or float) -> "Polynomial":
        return Polynomial([constant * i for i in self.vector_repr])

    @classmethod
    def get_derivative(cls, poly: "Polynomial") -> "Polynomial":
        if type(poly) is not Polynomial:
            raise TypeError("Must use a Polynomial object")
        poly_vector = poly.get_vector_repr()[1:]
        derivative = [poly_vector[i] * (i + 1) for i in range(len(poly_vector))]
        return cls(derivative)

    def derivate(self) -> "Polynomial":
        return self.get_derivative(self)

    @classmethod
    def get_integral(cls, poly: "Polynomial", constant: int) -> "Polynomial":
        if type(poly) is not Polynomial:
            raise TypeError("Must use a Polynomial object")
        poly_vector = [0] + poly.get_vector_repr()
        integral = [poly_vector[i] / i if poly_vector[i] else 0 for i in range(len(poly_vector))]
        integral[0] = constant
        return cls(integral)

    def integrate(self, constant: int) -> "Polynomial":
        return self.get_integral(self, constant)

    def get_vector_repr(self) -> List[Union[Fraction]]:
        return self.vector_repr

    def get_vector_str(self) -> List[str]:
        """Human readable vector representation of the polynomial"""
        return [str(i.numerator) if i.denominator == 1 else str(i) for i in self.vector_repr]

    def get_degree(self) -> int:
        """Return order of highest degree term"""
        return len(self.vector_repr) - 1

    def __len__(self):
        return len(self.vector_repr)

    def __eq__(self, other: "Polynomial"):
        return self.get_vector_repr() == other.get_vector_repr()

    def __str__(self):
        output = []
        for i in range(len(self.get_vector_repr()) - 1, -1, -1):
            if self.vector_repr[i]:
                if not i:
                    output.append(str(self.get_vector_repr()[i]))
                elif i == 1:
                    if self.vector_repr[i] == 1:
                        output.append(str("X"))
                    else:
                        output.append(str(self.get_vector_repr()[i]) + "X")
                else:
                    if self.vector_repr[i] == 1:
                        output.append("X^" + str(i))
                    else:
                        output.append(str(self.get_vector_repr()[i]) + "X^" + str(i))
        return " + ".join(output)
