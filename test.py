import unittest

from main import calculate_determinant
from matrix_generator import generate_matrix_and_det


def require_generator(test_case):
    sample = generate_matrix_and_det(1)
    if sample is None:
        test_case.skipTest("Generator is not implemented")
    return sample


class TestDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    целочисленной квадратной матрицы"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения None"""
        self.assertRaises(Exception, calculate_determinant, None)

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(Exception, calculate_determinant, [])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [-4, 3, 5, -6]]
        self.assertRaises(Exception, calculate_determinant, matrix)

    def test_first_order(self):
        """Проверяет расчет определителя для матрицы порядка 1"""
        matrix = [[1]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_second_order(self):
        """Проверяет расчет определителя для матрицы порядка 2"""
        matrix = [[1, 2], [3, 4]]
        self.assertEqual(calculate_determinant(matrix), -2)

    def test_third_order(self):
        """Проверяет расчет определителя для матрицы порядка 3"""
        matrix = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[3, -3, -5, 8], [-3, 2, 4, -6], [2, -5, -7, 5], [-4, 3, 5, -6]]
        self.assertEqual(calculate_determinant(matrix), 18)

    def test_generator(self):
        """Проверяет генератор матриц с известным определителем"""
        require_generator(self)
        for order in range(1, 11):
            with self.subTest(order=order):
                test_case = generate_matrix_and_det(order)
                self.assertEqual(len(test_case.matrix), order)
                for row in test_case.matrix:
                    self.assertEqual(len(row), order)
                self.assertEqual(
                    calculate_determinant(test_case.matrix), test_case.det
                )
    def test_not_list(self):
        self.assertRaises(ValueError, calculate_determinant, 123)

    def test_row_not_list(self):
        matrix = [[1, 2], 3]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_empty_row(self):
        matrix = [[]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_short_row(self):
        matrix = [[1, 2], [3]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_long_row(self):
        matrix = [[1, 2], [3, 4, 5]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_more_rows_than_columns(self):
        matrix = [[1], [2]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_tuple_matrix(self):
        matrix = ((1, 2), (3, 4))
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_tuple_row(self):
        matrix = [[1, 2], (3, 4)]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_float_element(self):
        matrix = [[1, 2], [3, 4.5]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_string_element(self):
        matrix = [[1, 2], [3, "4"]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_boolean_element(self):
        matrix = [[True, 2], [3, 4]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_false_element(self):
        matrix = [[False]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_none_element(self):
        matrix = [[None]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_nan(self):
        self.assertRaises(ValueError, calculate_determinant, float("nan"))

    def test_nan_element(self):
        matrix = [[float("nan")]]
        self.assertRaises(ValueError, calculate_determinant, matrix)

    def test_first_order_negative(self):
        matrix = [[-7]]
        self.assertEqual(calculate_determinant(matrix), -7)

    def test_first_order_zero(self):
        matrix = [[0]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_zero_matrix(self):
        matrix = [[0, 0], [0, 0]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_identity_matrix(self):
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(calculate_determinant(matrix), 1)

    def test_triangular_matrix(self):
        matrix = [[2, 3, 4], [0, 5, 6], [0, 0, 7]]
        self.assertEqual(calculate_determinant(matrix), 70)
    def test_lower_triangular_matrix(self):
        matrix = [[1, 0, 0], [2, -3, 0], [4, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), -18)

    def test_equal_rows(self):
        matrix = [[1, 2, 3], [1, 2, 3], [4, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_equal_columns(self):
        matrix = [[1, 2, 1], [3, 4, 3], [5, 6, 5]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_zero_first_row(self):
        matrix = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_dependent_rows(self):
        matrix = [[1, 2, 3], [2, 4, 6], [0, 1, 0]]
        self.assertEqual(calculate_determinant(matrix), 0)

    def test_third_order_nonzero(self):
        matrix = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]
        self.assertEqual(calculate_determinant(matrix), 22)

    def test_large_elements(self):
        matrix = [[10**20, 0], [0, 10**20]]
        self.assertEqual(calculate_determinant(matrix), 10**40)

    def test_matrix_unchanged(self):
        matrix = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]
        original = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]

        calculate_determinant(matrix)

        self.assertEqual(matrix, original)


if __name__ == "__main__":
    unittest.main()
