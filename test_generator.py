import unittest
from fractions import Fraction
from unittest.mock import Mock

from main import (
    build_conditions,
    evaluate_formula,
    find_diagonal_pair,
    format_conditions,
    generate_conditions,
    is_simple_coefficient,
    iter_matrix_candidates,
    validate_bounds,
)


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


class TestEvaluateFormula(unittest.TestCase):
    """Проверки вычисления коэффициентов формулы."""

    def test_distinct_roots_positive(self):
        """Разные положительные корни дают целые коэффициенты."""
        candidate = {"a": 5, "b": -3, "c": -2, "root1": 2, "root2": 3}
        result = evaluate_formula(candidate)
        self.assertEqual(result["root_type"], "distinct")
        self.assertEqual(result["coefficients"]["A1"], Fraction(-2))
        self.assertEqual(result["coefficients"]["A2"], Fraction(3))

    def test_double_root(self):
        """Двойной корень даёт целые коэффициенты."""
        candidate = {"a": 8, "b": 2, "c": 8, "root1": 4, "root2": 4}
        result = evaluate_formula(candidate)
        self.assertEqual(result["root_type"], "double")
        self.assertEqual(result["coefficients"]["A"], Fraction(1))
        self.assertEqual(result["coefficients"]["B"], Fraction(1))

    def test_negative_roots(self):
        """Отрицательные корни корректно обрабатываются."""
        candidate = {"a": -5, "b": 2, "c": 3, "root1": -3, "root2": -2}
        result = evaluate_formula(candidate)
        self.assertEqual(result["root_type"], "distinct")
        self.assertEqual(result["coefficients"]["A1"], Fraction(3))
        self.assertEqual(result["coefficients"]["A2"], Fraction(-2))

    def test_complex_coefficients_rejected(self):
        """Сложные коэффициенты отклоняются (возврат None)."""
        candidate = {"a": 14, "b": 1, "c": 13, "root1": 1, "root2": 13}
        result = evaluate_formula(candidate)
        self.assertIsNone(result)

    def test_zero_main_diagonal(self):
        """Нулевая главная диагональ и противоположные корни."""
        candidate = {"a": 0, "b": -3, "c": 3, "root1": -3, "root2": 3}
        result = evaluate_formula(candidate)
        self.assertEqual(result["root_type"], "distinct")
        self.assertEqual(result["coefficients"]["A1"], Fraction(1, 2))
        self.assertEqual(result["coefficients"]["A2"], Fraction(1, 2))

    def test_negative_double_root(self):
        """Отрицательный двойной корень."""
        candidate = {"a": -4, "b": -2, "c": -2, "root1": -2, "root2": -2}
        result = evaluate_formula(candidate)
        self.assertEqual(result["root_type"], "double")
        self.assertEqual(result["coefficients"]["A"], Fraction(1))
        self.assertEqual(result["coefficients"]["B"], Fraction(1))

    def test_numerator_is_allowed(self):
        """Числитель допустим (граничное значение)."""
        self.assertTrue(is_simple_coefficient(Fraction(20, 1)))
        self.assertTrue(is_simple_coefficient(Fraction(-20, 3)))
        self.assertTrue(is_simple_coefficient(Fraction(20, 7)))

    def test_numerator_is_rejected(self):
        """Числитель недопустим (выходит за границу)."""
        self.assertFalse(is_simple_coefficient(Fraction(21, 1)))
        self.assertFalse(is_simple_coefficient(Fraction(-21, 2)))
        self.assertFalse(is_simple_coefficient(Fraction(21, 10)))

    def test_denominator_is_allowed(self):
        """Знаменатель допустим (граничное значение)."""
        self.assertTrue(is_simple_coefficient(Fraction(1, 10)))
        self.assertTrue(is_simple_coefficient(Fraction(19, 10)))
        self.assertTrue(is_simple_coefficient(Fraction(-20, 10)))

    def test_denominator_is_rejected(self):
        """Знаменатель недопустим (выходит за границу)."""
        self.assertFalse(is_simple_coefficient(Fraction(1, 11)))
        self.assertFalse(is_simple_coefficient(Fraction(20, 11)))
        self.assertFalse(is_simple_coefficient(Fraction(-5, 11)))

    def test_fraction_simplification(self):
        """Проверяет автоматическое сокращение дробей."""
        candidate = {"a": 7, "b": 2, "c": 5, "root1": 2, "root2": 5}
        result = evaluate_formula(candidate)
        self.assertIsNotNone(result)
        self.assertEqual(result["coefficients"]["A1"], Fraction(-2, 3))
        self.assertEqual(result["coefficients"]["A2"], Fraction(5, 3))
        self.assertEqual(result["coefficients"]["A1"].denominator, 3)
        self.assertEqual(result["coefficients"]["A2"].denominator, 3)

    def test_negative_coefficients(self):
        """Проверяет корректную работу с отрицательными коэффициентами."""
        candidate = {"a": -5, "b": 2, "c": 3, "root1": -3, "root2": -2}
        result = evaluate_formula(candidate)
        self.assertIsNotNone(result)
        self.assertEqual(result["coefficients"]["A2"], Fraction(-2))

    def test_recurrent(self):
        """Сравнение явной формулы с рекуррентным вычислением."""
        candidate = {"a": 7, "b": 2, "c": 5, "root1": 2, "root2": 5}

        # Коэффициенты для явной формулы
        formula_res = evaluate_formula(candidate)
        self.assertIsNotNone(formula_res)
        coeffs = formula_res["coefficients"]
        A1, A2 = coeffs["A1"], coeffs["A2"]
        l1, l2 = Fraction(2), Fraction(5)

        a, b, c = candidate["a"], candidate["b"], candidate["c"]
        bc = b * c
        d_prev = a
        d_curr = a * a - bc

        for n in range(1, 7):
            if n == 1:
                recurrent_val = d_prev
            elif n == 2:
                recurrent_val = d_curr
            else:
                next_val = a * d_curr - bc * d_prev
                d_prev, d_curr = d_curr, next_val
                recurrent_val = next_val

            # Значение по явной формуле
            explicit_val = A1 * (l1**n) + A2 * (l2**n)
            self.assertEqual(
                explicit_val,
                Fraction(recurrent_val),
                f"Несовпадение при n={n}: Явная={explicit_val}, "
                f"Рекуррент={recurrent_val}",
            )

    def test_negative_double_root_recurrent(self):
        """Сравнивает формулу двойного корня -2 с рекуррентным вычислением."""
        candidate = {"a": -4, "b": -2, "c": -2, "root1": -2, "root2": -2}
        formula = evaluate_formula(candidate)
        self.assertIsNotNone(formula)
        self.assertEqual(formula["root_type"], "double")
        coefficients = formula["coefficients"]
        previous_determinant = -4
        current_determinant = 12

        for order in range(1, 7):
            if order == 1:
                recurrent_determinant = previous_determinant
            elif order == 2:
                recurrent_determinant = current_determinant
            else:
                recurrent_determinant = (
                    -4 * current_determinant - 4 * previous_determinant
                )
                previous_determinant = current_determinant
                current_determinant = recurrent_determinant
            explicit_determinant = (coefficients["A"] * order + coefficients["B"]) * (
                -2
            ) ** order
            with self.subTest(order=order):
                self.assertEqual(explicit_determinant, recurrent_determinant)

    def test_integration_with_generator(self):
        """Совместный вызов генератора с evaluate_formula."""
        result = generate_conditions(2, 3, evaluate_formula)

        self.assertIn("a", result)
        self.assertIn("root_type", result)
        self.assertIn("coefficients", result)

        self.assertEqual(result["root1"], 2)
        self.assertEqual(result["root2"], 2)
        self.assertEqual(result["root_type"], "double")

        self.assertEqual(result["coefficients"]["A"], Fraction(1))
        self.assertEqual(result["coefficients"]["B"], Fraction(1))


class TestValidateBounds(unittest.TestCase):
    """Проверки типов и порядка границ диапазона."""

    def test_valid_range(self):
        """Принимает целые границы в правильном порядке."""
        self.assertEqual(validate_bounds(-5, 5), (-5, 5))

    def test_equal_bounds(self):
        """Принимает диапазон из одного целого числа."""
        self.assertEqual(validate_bounds(4, 4), (4, 4))

    def test_reversed_bounds(self):
        """Отклоняет нижнюю границу больше верхней."""
        with self.assertRaisesRegex(ValueError, "не должна превышать"):
            validate_bounds(5, 3)

    def test_non_integer_bounds(self):
        """Отклоняет границы нецелочисленных типов."""
        for bounds in ((3.0, 5), ("3", 5), (None, 5), (Fraction(3), 5)):
            with (
                self.subTest(bounds=bounds),
                self.assertRaisesRegex(TypeError, "целыми числами"),
            ):
                validate_bounds(*bounds)

    def test_bool_bounds(self):
        """Отклоняет логические значения в обеих позициях."""
        for bounds in ((True, 5), (0, False)):
            with (
                self.subTest(bounds=bounds),
                self.assertRaisesRegex(TypeError, "целыми числами"),
            ):
                validate_bounds(*bounds)


class TestBuildConditions(unittest.TestCase):
    """Проверки публичного вызова генератора условий."""

    def test_equal_bounds_double_root(self):
        """Возвращает полный набор для двойного корня 4."""
        self.assertEqual(
            build_conditions(4, 4),
            {
                "a": 8,
                "b": -4,
                "c": -4,
                "root1": 4,
                "root2": 4,
                "root_type": "double",
                "coefficients": {"A": Fraction(1), "B": Fraction(1)},
            },
        )

    def test_negative_range(self):
        """Подбирает параметры в полностью отрицательном диапазоне."""
        conditions = build_conditions(-5, -2)
        self.assertEqual(conditions["root1"], -5)
        self.assertEqual(conditions["root2"], -5)
        self.assertEqual(conditions["root_type"], "double")
        self.assertEqual(conditions["a"], -10)
        self.assertEqual(conditions["b"] * conditions["c"], 25)

    def test_range_containing_zero(self):
        """Находит ненулевой корень в диапазоне с нулём."""
        conditions = build_conditions(-1, 1)
        self.assertEqual(conditions["root1"], -1)
        self.assertEqual(conditions["root_type"], "double")

    def test_positive_range(self):
        """Подбирает первый допустимый корень положительного диапазона."""
        conditions = build_conditions(2, 3)
        self.assertEqual(conditions["root1"], 2)
        self.assertEqual(conditions["root2"], 2)
        self.assertEqual(conditions["a"], 4)

    def test_zero_only_range(self):
        """Сообщает, что для диапазона из одного нуля условий нет."""
        with self.assertRaisesRegex(ValueError, "нет набора"):
            build_conditions(0, 0)

    def test_reversed_bounds(self):
        """Сообщает об обратном порядке границ до подбора условий."""
        with self.assertRaisesRegex(ValueError, "не должна превышать"):
            build_conditions(5, 3)

    def test_non_integer_bounds(self):
        """Отклоняет дробную границу при вызове генератора."""
        with self.assertRaisesRegex(TypeError, "целыми числами"):
            build_conditions(2.5, 6)

    def test_outside_limits(self):
        """Сообщает об отсутствии набора для слишком больших корней."""
        with self.assertRaisesRegex(ValueError, "нет набора"):
            build_conditions(10**12, 10**12 + 5)

    def test_repeatable(self):
        """Возвращает одинаковый результат для одинаковых границ."""
        self.assertEqual(build_conditions(2, 3), build_conditions(2, 3))

    def test_vieta_identities(self):
        """Проверяет формулы Виета и ненулевые соседние диагонали."""
        conditions = build_conditions(4, 4)
        root1, root2 = conditions["root1"], conditions["root2"]
        self.assertEqual(conditions["a"], root1 + root2)
        self.assertEqual(conditions["b"] * conditions["c"], root1 * root2)
        self.assertNotEqual(conditions["b"], 0)
        self.assertNotEqual(conditions["c"], 0)

    def test_distinct_roots_through_generator(self):
        """Находит разные корни и точные коэффициенты."""
        conditions = build_conditions(-25, -9)
        self.assertEqual(conditions["a"], -20)
        self.assertEqual(conditions["root1"], -11)
        self.assertEqual(conditions["root2"], -9)
        self.assertEqual(conditions["root_type"], "distinct")
        self.assertEqual(conditions["coefficients"]["A1"], Fraction(11, 2))
        self.assertEqual(conditions["coefficients"]["A2"], Fraction(-9, 2))


class TestFormatConditions(unittest.TestCase):
    """Проверки текстового представления результата."""

    def test_double_root_display(self):
        """Выводит параметры, корень и формулу для двойного корня."""
        text = format_conditions(build_conditions(4, 4))
        self.assertIn("a = 8, b = -4, c = -4", text)
        self.assertIn("Корни: 4 и 4", text)
        self.assertIn("двойной корень", text)
        self.assertIn("Dn = (A·n + B)·λ^n", text)
        self.assertIn("Коэффициенты: A = 1, B = 1", text)

    def test_distinct_root_display(self):
        """Выводит формулу для разных корней и точные дроби."""
        conditions = {
            "a": 0,
            "b": -3,
            "c": 3,
            "root1": -3,
            "root2": 3,
            "root_type": "distinct",
            "coefficients": {"A1": Fraction(1, 2), "A2": Fraction(1, 2)},
        }
        text = format_conditions(conditions)
        self.assertIn("разные корни", text)
        self.assertIn("Dn = A1·λ1^n + A2·λ2^n", text)
        self.assertIn("A1 = 1/2, A2 = 1/2", text)

    def test_distinct_output_from_generator(self):
        """Форматирует результат генератора с разными корнями."""
        text = format_conditions(build_conditions(-25, -9))
        self.assertIn("разные корни", text)
        self.assertIn("A1 = 11/2", text)
        self.assertIn("A2 = -9/2", text)

    def test_negative_fraction_display(self):
        """Сохраняет знак и точную запись дробного коэффициента."""
        conditions = {
            "a": 7,
            "b": 2,
            "c": 5,
            "root1": 2,
            "root2": 5,
            "root_type": "distinct",
            "coefficients": {"A1": Fraction(-2, 3), "A2": Fraction(5, 3)},
        }
        text = format_conditions(conditions)
        self.assertIn("A1 = -2/3", text)
        self.assertIn("A2 = 5/3", text)


if __name__ == "__main__":
    unittest.main()
