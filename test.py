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

    def test_third_order_2(self):
        """Проверяет расчет определителя для симметричной матрицы 3x3"""
        matrix = [[3, 1, 0], [1, 3, 1], [0, 1, 3]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 21)

    def test_third_order_3(self):
        """Проверяет расчет определителя для матрицы 3x3 c одинаковыми числами"""
        matrix = [[10, 10, 0], [10, 10, 10], [0, 10, 10]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -1000)

    def test_fourth_order_2(self):
        """Проверяет расчет определителя для матрицы 4x4
        с нулевой главной диагональю"""
        matrix = [[0, 4, 0, 0], [2, 0, 4, 0], [0, 2, 0, 4], [0, 0, 2, 0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 64)

    def test_fourth_order_3(self):
        """Проверяет расчет определителя для матрицы 4x4
        с отрицательными соседними диагоналями"""
        matrix = [[3, -2, 0, 0], [-2, 3, -2, 0], [0, -2, 3, -2], [0, 0, -2, 3]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -11)

    def test_fifth_order(self):
        """Проверяет расчет определителя для матрицы 5x5"""
        matrix = [
            [3, 1, 0, 0, 0],
            [-4, 3, 1, 0, 0],
            [0, -4, 3, 1, 0],
            [0, 0, -4, 3, 1],
            [0, 0, 0, -4, 3],
        ]
        self.assertEqual(get_tridiagonal_determinant(matrix), 819)

    def test_fifth_order_2(self):
        """Проверяет расчет отрицательного определителя для матрицы 5x5"""
        matrix = [
            [-1, 3, 0, 0, 0],
            [2, -1, 3, 0, 0],
            [0, 2, -1, 3, 0],
            [0, 0, 2, -1, 3],
            [0, 0, 0, 2, -1],
        ]
        self.assertEqual(get_tridiagonal_determinant(matrix), -85)

    def test_fifth_order_3(self):
        """Проверяет расчет нулевого определителя для матрицы 5x5"""
        matrix = [
            [2, 2, 0, 0, 0],
            [2, 2, 2, 0, 0],
            [0, 2, 2, 2, 0],
            [0, 0, 2, 2, 2],
            [0, 0, 0, 2, 2],
        ]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)


if __name__ == "__main__":
    unittest.main()
