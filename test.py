import unittest

from main import gray_code


def find_grey_by_index(i: int, n: int) -> list[int]:
    expected_number = i ^ (i >> 1)
    expected_bits = format(expected_number, f"0{n}b")
    return list(map(int, expected_bits))


class TestGrayCode(unittest.TestCase):
    """Набор тестов для проверки рекурсивной генерации кода Грея"""

    def test_none(self):
        """Проверяет, что функция выбрасывает исключение при передаче
        значения None"""
        self.assertRaises(Exception, gray_code, None)

    def test_zero_length(self):
        """Проверяет, что функция выбрасывает исключение при нулевой длине"""
        self.assertRaises(Exception, gray_code, 0)

    def test_negative_length(self):
        self.assertRaises(Exception, gray_code, -1)

    def test_bool_true(self):
        self.assertRaises(Exception, gray_code, True)

    def test_bool_false(self):
        self.assertRaises(Exception, gray_code, False)

    def test_float_length(self):
        self.assertRaises(Exception, gray_code, 2.5)

    def test_string_length(self):
        self.assertRaises(Exception, gray_code, "abc")

    def test_one_bit(self):
        """Проверяет код длины 1"""
        self.assertEqual(gray_code(1), [[0], [1]])

    def test_two_bits(self):
        """Проверяет код длины 2"""
        self.assertEqual(gray_code(2), [[0, 0], [0, 1], [1, 1], [1, 0]])

    def test_three_bits(self):
        """Проверяет стандартную нумерацию для длины 3"""
        expected = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
            [1, 0, 1],
            [1, 0, 0],
        ]
        self.assertEqual(gray_code(3), expected)

    def test_reflected_order(self):
        for n in range(1, 6):
            numbers = gray_code(n)
            self.assertEqual(len(numbers), 2**n)
            for i, number in enumerate(numbers):
                expected_number = find_grey_by_index(i, n)
                self.assertEqual(number, expected_number)

    def test_return_type_is_list_of_lists(self):
        result = gray_code(3)
        self.assertIsInstance(result, list)
        for number in result:
            self.assertIsInstance(number, list)

    def test_length_of_result(self):
        self.assertEqual(len(gray_code(5)), 2**5)

    def test_code_length(self):
        for number in gray_code(6):
            self.assertEqual(len(number), 6)


if __name__ == "__main__":
    unittest.main()
