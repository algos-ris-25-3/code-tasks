import unittest

from main import get_tridiagonal_determinant


class TestTridiagonalDeterminant(unittest.TestCase):
    """Набор тестов для проверки функции вычисления определителя
    трёхдиагональной ленточной матрицы"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр значения None"""
        self.assertRaises(TypeError, get_tridiagonal_determinant, None)

    def test_empty_matrix(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр пустого списка"""
        self.assertRaises(ValueError, get_tridiagonal_determinant, [])

    def test_not_square_rectangle(self):
        """Проверяет, что функция выбрасывает исключение при передаче в
        параметр прямоугольной матрицы"""
        matrix = [[1, 2, 0, 0], [3, 1, 2, 0], [0, 3, 1, 2]]
        self.assertRaises(ValueError, get_tridiagonal_determinant, matrix)

    def test_not_tridiag_replace_zero(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        матрицы с ненулевым элементом вне трёх диагоналей"""
        matrix = [[1, 2, 0, 7], [3, 1, 2, 0], [0, 3, 1, 2], [0, 0, 3, 1]]
        self.assertRaises(ValueError, get_tridiagonal_determinant, matrix)

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

    def test_first_order_zero(self):
        """Проверяет нулевой определитель матрицы порядка 1."""
        matrix = [[0]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_second_order_zero(self):
        """Проверяет нулевой определитель матрицы порядка 2."""
        matrix = [[2, 1], [4, 2]]
        self.assertEqual(get_tridiagonal_determinant(matrix), 0)

    def test_second_order_negative(self):
        """Проверяет отрицательный определитель матрицы порядка 2."""
        matrix = [[-1, 2], [3, -1]]
        self.assertEqual(get_tridiagonal_determinant(matrix), -5)

    def test_invalid_matrix_type(self):
        """Отклоняет входные данные, которые не являются списком."""
        for matrix in (1, "matrix", ((1,),)):
            with self.subTest(matrix=matrix):
                with self.assertRaisesRegex(TypeError, "списком"):
                    get_tridiagonal_determinant(matrix)

    def test_invalid_row_type(self):
        """Отклоняет строки матрицы, которые не являются списками."""
        for row in (None, 1, "1", (1,)):
            with self.subTest(row=row):
                with self.assertRaisesRegex(TypeError, "Строка 0"):
                    get_tridiagonal_determinant([row])

    def test_ragged_matrix(self):
        """Отклоняет пустые строки и строки неодинаковой длины."""
        for matrix in ([[]], [[1, 2], [3]], [[1], [2, 3]]):
            with self.subTest(matrix=matrix):
                with self.assertRaisesRegex(ValueError, "не квадратная"):
                    get_tridiagonal_determinant(matrix)

    def test_non_integer_first_order(self):
        """Проверяет тип единственного элемента до возврата определителя."""
        for value in (1.5, 1.0, "text", None, True, 1j):
            with self.subTest(value=value):
                with self.assertRaisesRegex(TypeError, r"Элемент \[0\]\[0\]"):
                    get_tridiagonal_determinant([[value]])

    def test_non_integer_elements(self):
        """Отклоняет нецелые элементы на диагоналях и вне полосы."""
        matrices = (
            [[1, 0], [0, 1.0]],
            [[1, 0.0], [0, 1]],
            [[1, 0], [False, 1]],
            [[1, 0, 0.0], [0, 1, 0], [0, 0, 1]],
        )
        for matrix in matrices:
            with self.subTest(matrix=matrix):
                with self.assertRaisesRegex(TypeError, "целым числом"):
                    get_tridiagonal_determinant(matrix)

    def test_nonconstant_diagonals(self):
        """Отклоняет нарушение постоянства каждой из трёх диагоналей."""
        cases = (
            ([[1, 2, 0], [3, 9, 2], [0, 3, 1]], "главной"),
            ([[1, 2, 0], [3, 1, 9], [0, 3, 1]], "наддиагонали"),
            ([[1, 2, 0], [3, 1, 2], [0, 9, 1]], "поддиагонали"),
        )
        for matrix, location in cases:
            with self.subTest(location=location):
                with self.assertRaisesRegex(ValueError, location):
                    get_tridiagonal_determinant(matrix)

    def test_nonzero_below_band(self):
        """Отклоняет ненулевой элемент ниже трёх диагоналей."""
        matrix = [[1, 2, 0], [3, 1, 2], [9, 3, 1]]
        with self.assertRaisesRegex(ValueError, "вне трёх диагоналей"):
            get_tridiagonal_determinant(matrix)

    def test_first_order_negative(self):
        """Проверяет сохранение знака элемента матрицы порядка 1."""
        self.assertEqual(get_tridiagonal_determinant([[-7]]), -7)

    def test_zero_adjacent_diagonals(self):
        """Проверяет нулевые соседние диагонали и полностью нулевую матрицу."""
        cases = (
            ([[2, 0, 0], [3, 2, 0], [0, 3, 2]], 8),
            ([[2, 3, 0], [0, 2, 3], [0, 0, 2]], 8),
            ([[2, 0, 0], [0, 2, 0], [0, 0, 2]], 8),
            ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0),
        )
        for matrix, expected in cases:
            with self.subTest(matrix=matrix):
                self.assertEqual(get_tridiagonal_determinant(matrix), expected)


if __name__ == "__main__":
    unittest.main()
