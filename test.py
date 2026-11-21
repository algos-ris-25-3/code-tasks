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

    def test_zero_matrix_1x1(self):
        """Определитель [0] равен 0"""
        self.assertEqual(get_tridiagonal_determinant([[0]]), 0)

    def test_zero_matrix_3x3(self):
        """Нулевая матрица — определитель 0"""
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_identity_3x3(self):
        """Единичная матрица — определитель 1"""
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 1)

    def test_negative_diagonal(self):
        """Отрицательные элементы на диагоналях"""
        matrix = [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -1)

    def test_only_main_diagonal(self):
        """b =c = 0: определитель =a^n"""
        matrix = [[2, 0, 0], [0, 2, 0], [0, 0, 2]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 8)

    def test_fifth_order(self):
        matrix = [
            [1, 2, 0, 0, 0],
            [3, 1, 2, 0, 0],
            [0, 3, 1, 2, 0],
            [0, 0, 3, 1, 2],
            [0, 0, 0, 3, 1],
        ]
        self.assertEqual(get_tridiagonal_determinant(matrix), 85)

    def test_bool_in_matrix(self):
        """bool не должен быть принят за int"""
        matrix = [[True, 0, 0], [0, True, 0], [0, 0, True]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_non_constant_main_diagonal(self):
        """Разные значения на главной диагонали"""
        matrix = [[1, 2, 0], [3, 4, 5], [0, 6, 7]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_non_constant_upper_diagonal(self):
        """Разные значения на наддиагонали"""
        matrix = [[1, 2, 0], [3, 1, 4], [0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_non_constant_lower_diagonal(self):
        """Разные значения на поддиагонали"""
        matrix = [[1, 2, 0], [3, 1, 2], [0, 4, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)

    def test_nonzero_far_corner(self):
        """Ненулевой элемент в правом верхнем углу"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 3, 1, 2], [9, 0, 3, 1]]
        self.assertRaises(Exception, get_tridiagonal_determinant, matrix)


if __name__ == "__main__":
    unittest.main()
