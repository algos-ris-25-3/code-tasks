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

    def test_not_list_of_lists(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр списка содержащего не списки"""
        matrix = [0, 1, 2]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 3, 1, 2]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_not_square_more_rows(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы, где строк больше, чем столбцов"""
        matrix = [[1, 2, 0], [3, 1, 2], [0, 3, 1], [0, 0, 3]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_main_diagonal_unchanging(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с различающимися элементами на основной диагонали"""
        matrix = [[1, 2, 0, 0], [3, 2, 2, 0], [0, 3, 3, 2], [0, 0, 3, 4]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_upper_diagonal_unchanging(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с различающимися элементами на наддиагонали"""
        matrix = [[1, 2, 0, 0], [3, 1, 3, 0], [0, 3, 1, 4], [0, 0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_lower_diagonal_unchanging(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с различающимися элементами на поддиагонали"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 4, 1, 2], [0, 0, 5, 1]]
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

    def test_zero_matrix(self):
        """Проверяет расчет определителя для матрицы из нулей"""
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_one_diagonal_matrix(self):
        """Проверяет расчет определителя для матрицы с одной диагональю"""
        matrix = [[5, 0, 0], [0, 5, 0], [0, 0, 5]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 125)


if __name__ == "__main__":
    unittest.main()
