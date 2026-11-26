import unittest
from fractions import Fraction
from unittest.mock import Mock

from main import find_diagonal_pair, generate_conditions, iter_matrix_candidates


class TestDiagonalPair(unittest.TestCase):
    """Проверки подбора соседних диагоналей по произведению."""

    def test_balanced_pair(self):
        """Выбирается пара с наименьшим максимальным модулем."""
        self.assertEqual(find_diagonal_pair(12), (-4, -3))

    def test_negative_product(self):
        """Отрицательное произведение даёт множители разных знаков."""
        self.assertEqual(find_diagonal_pair(-12), (-4, 3))

    def test_limit_included(self):
        """Модуль диагонали 20 входит в допустимые значения."""
        self.assertEqual(find_diagonal_pair(400), (-20, -20))

    def test_no_pair(self):
        """Нулевое произведение и неподходящие множители отклоняются."""
        for product in (0, 23, 401):
            with self.subTest(product=product):
                self.assertIsNone(find_diagonal_pair(product))


class TestMatrixCandidates(unittest.TestCase):
    """Проверки корней, границ и допустимости параметров матрицы."""

    def test_root_pairs(self):
        """Включены обе границы, разные и двойные корни без перестановок."""
        candidates = list(iter_matrix_candidates(2, 3))
        self.assertEqual(
            [(item["root1"], item["root2"]) for item in candidates],
            [(2, 2), (2, 3), (3, 3)],
        )

    def test_zero_main_diagonal(self):
        """Противоположные корни допускают нулевую главную диагональ."""
        self.assertIn(
            {"a": 0, "b": -3, "c": 3, "root1": -3, "root2": 3},
            list(iter_matrix_candidates(-3, 3)),
        )

    def test_negative_double_root(self):
        """Одинаковые отрицательные границы дают двойной корень."""
        self.assertEqual(
            list(iter_matrix_candidates(-2, -2)),
            [{"a": -4, "b": -2, "c": -2, "root1": -2, "root2": -2}],
        )

    def test_candidate_properties(self):
        """Небольшая выборка удовлетворяет Виету и ограничениям диагоналей."""
        for candidate in iter_matrix_candidates(-3, 3):
            with self.subTest(candidate=candidate):
                a, b, c = (candidate[key] for key in ("a", "b", "c"))
                root1, root2 = candidate["root1"], candidate["root2"]
                self.assertTrue(-3 <= root1 <= root2 <= 3)
                self.assertNotEqual(root1, 0)
                self.assertNotEqual(root2, 0)
                self.assertEqual(a, root1 + root2)
                self.assertEqual(b * c, root1 * root2)
                self.assertLessEqual(abs(a), 20)
                self.assertTrue(1 <= abs(b) <= 20)
                self.assertTrue(1 <= abs(c) <= 20)

    def test_no_candidates(self):
        """Проверенные диапазоны могут не содержать допустимых параметров."""
        for bounds in ((0, 0), (11, 12), (10**12, 10**12 + 10)):
            with self.subTest(bounds=bounds):
                self.assertEqual(list(iter_matrix_candidates(*bounds)), [])


class TestConditionsSelection(unittest.TestCase):
    """Проверки взаимодействия с внешним расчётом коэффициентов."""

    def test_rejected_candidate_is_skipped(self):
        """Поиск продолжается после отказа и возвращает принятый набор."""
        formula = {
            "root_type": "distinct",
            "coefficients": {"A1": Fraction(-2), "A2": Fraction(3)},
        }
        evaluate_formula = Mock(side_effect=[None, formula])
        result = generate_conditions(2, 3, evaluate_formula)
        self.assertEqual(
            result,
            {"a": 5, "b": -3, "c": -2, "root1": 2, "root2": 3, **formula},
        )
        self.assertEqual(evaluate_formula.call_count, 2)

    def test_repeatable_double_root(self):
        """Одинаковый ввод и расчёт дают одинаковый результат."""
        formula = {
            "root_type": "double",
            "coefficients": {"A": Fraction(1), "B": Fraction(1)},
        }
        first = generate_conditions(4, 4, Mock(return_value=formula))
        second = generate_conditions(4, 4, Mock(return_value=formula))
        self.assertEqual(first, second)
        self.assertEqual(first["root_type"], "double")
        self.assertEqual(first["coefficients"], formula["coefficients"])

    def test_all_candidates_rejected(self):
        """Отказ для всех кандидатов заканчивается понятным исключением."""
        with self.assertRaisesRegex(ValueError, "нет набора"):
            generate_conditions(2, 3, Mock(return_value=None))

    def test_no_candidates_does_not_call_formula(self):
        """При отсутствии корней расчёт коэффициентов не вызывается."""
        evaluate_formula = Mock()
        with self.assertRaisesRegex(ValueError, "нет набора"):
            generate_conditions(0, 0, evaluate_formula)
        evaluate_formula.assert_not_called()

    def test_formula_error_propagates(self):
        """Ошибка расчёта не маскируется сообщением об отсутствии набора."""
        with self.assertRaisesRegex(RuntimeError, "Ошибка расчёта"):
            generate_conditions(2, 3, Mock(side_effect=RuntimeError("Ошибка расчёта")))


if __name__ == "__main__":
    unittest.main()
