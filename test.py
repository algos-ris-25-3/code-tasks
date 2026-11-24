import unittest

from main import get_tridiagonal_determinant


class TestTridiagonalDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    трёхдиагональной ленточной матрицы"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения None"""
        self.assertRaises(Exception, get_tridiagonal_determinant, None)

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(Exception, get_tridiagonal_determinant, [])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 3, 1, 2]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_not_tridiag_replace_zero(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с ненулевым элементом вне трёх диагоналей"""
        matrix = [[1, 2, 0, 7], [3, 1, 2, 0], [0, 3, 1, 2], [0, 0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_first_order(self):
        """Проверяет расчет определителя для матрицы порядка 1"""
        matrix = [[1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 1)

    def test_second_order(self):
        """Проверяет расчет определителя для матрицы порядка 2"""
        matrix = [[1, 2], [2, 1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -3)

    def test_third_order(self):
        """Проверяет расчет определителя для матрицы порядка 3"""
        matrix = [[1, -2, 0], [-4, 1, -2], [0, -4, 1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -15)

    def test_fourth_order(self):
        """Проверяет расчет определителя для матрицы порядка 4"""
        matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 421)

    def test_not_list_matrix(self):
        """Проверяет, что функция выбрасывает исключение,
        если матрица не является списком."""
        matrix = ((1, 2), (3, 1))
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_non_list_row(self):
        """Проверяет, что функция выбрасывает исключение,
        если строка матрицы не является списком."""
        matrix = [[1, 2], (3, 1)]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_unequal_row_lengths(self):
        """Проверяет, что функция выбрасывает исключение для строк различной длины."""
        matrix = [[1, 2], [3]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_non_integer_element(self):
        """Проверяет, что функция выбрасывает исключение
        для нецелочисленных элементов."""
        matrix = [[1, 2], [3, 1.5]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_boolean_element(self):
        """Проверяет, что функция выбрасывает исключение для логического значения."""
        matrix = [[True]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_inconsistent_main_diagonal(self):
        """Проверяет, что функция выбрасывает исключение при вычислении
        определителя матрицы с разными значениями на главной диагонали."""
        matrix = [[1, 2, 0], [3, 7, 2], [0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_inconsistent_upper_diagonal(self):
        """Проверяет, что функция выбрасывает исключение при вычислении
        определителя матрицы с разными значениями на верхней диагонали."""
        matrix = [[1, 2, 0], [3, 1, 7], [0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_inconsistent_lower_diagonal(self):
        """Проверяет, что функция выбрасывает исключение при вычислении
        определителя матрицы с разными значениями на нижней диагонали."""
        matrix = [[1, 2, 0], [3, 1, 2], [0, 7, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_first_order_zero(self):
        """Проверяет расчет определителя матрицы порядка 1 с нулём."""
        matrix = [[0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_first_order_negative(self):
        """Проверяет расчет определителя матрицы порядка 1 с отрицательным элементом."""
        matrix = [[-50]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -50)

    def test_all_zero(self):
        """Проверяет расчет определителя нулевой матрицы."""
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_zero_off_diagonals(self):
        """Проверяет расчет матрицы с нулевыми соседними диагоналями."""
        matrix = [[3, 0, 0], [0, 3, 0], [0, 0, 3]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 27)


if __name__ == "__main__":
    unittest.main()
