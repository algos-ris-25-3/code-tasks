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

    def test_type_of_lists(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        списка с не списками возвращает исключение"""
        matrix = [[1, 2, 0], (3, 1, 2), [0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_type_of_elements_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с не интовыми элементами возвращает исключение"""
        matrix = [[1, 2, "0", 0], [3, 1, 2, 0], [0, 3, 1, 2]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_elements_on_main_diagonal_not_equal(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы где на главной диагонали отлично хоть одно значение
          элементами возвращает исключение"""
        matrix = [
            [6, 53, 0, 0, 0],
            [-4, 6, 53, 0, 0],
            [0, -4, 6, 53, 0],
            [0, 0, -4, 4, 53],
            [0, 0, 0, -4, 6],
        ]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_elements_on_second_diagonal_not_equal(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы где на главной диагонали отлично хоть одно значение
        элементами возвращает исключение"""
        matrix1 = [
            [6, 35, 0, 0, 0],
            [-4, 6, 53, 0, 0],
            [0, -4, 6, 53, 0],
            [0, 0, -4, 6, 53],
            [0, 0, 0, -4, 6],
        ]
        matrix2 = [
            [6, 53, 0, 0, 0],
            [-4, 6, 53, 0, 0],
            [0, -4, 6, 53, 0],
            [0, 0, 4, 6, 53],
            [0, 0, 0, -4, 6],
        ]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix1)
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix2)

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


if __name__ == "__main__":
    unittest.main()
