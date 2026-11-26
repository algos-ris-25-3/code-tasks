from collections.abc import Callable, Iterator
from fractions import Fraction
from typing import Literal, TypedDict

DIAGONAL_LIMIT = 20


class MatrixParameters(TypedDict):
    """Параметры диагоналей и упорядоченные целые корни."""

    a: int
    b: int
    c: int
    root1: int
    root2: int


class FormulaParameters(TypedDict):
    """Тип формулы и её точные коэффициенты, рассчитанные частью Арины."""

    root_type: Literal["distinct", "double"]
    coefficients: dict[str, Fraction]


class GeneratedConditions(MatrixParameters, FormulaParameters):
    """Полный набор условий для ручного вычисления определителя."""


def find_diagonal_pair(product: int) -> tuple[int, int] | None:
    """Подбирает ненулевые целые b и c с заданным произведением.

    Модули множителей не превышают DIAGONAL_LIMIT. Выбирается пара
    с минимальным max(abs(b), abs(c)), при равенстве — с меньшим b.

    :param product: целое произведение соседних диагоналей
    :return: пара (b, c) либо None, если допустимых множителей нет
    """
    best_pair = None
    best_size = DIAGONAL_LIMIT + 1
    for upper_diagonal in range(-DIAGONAL_LIMIT, DIAGONAL_LIMIT + 1):
        if upper_diagonal == 0 or product % upper_diagonal != 0:
            continue
        lower_diagonal = product // upper_diagonal
        if not 1 <= abs(lower_diagonal) <= DIAGONAL_LIMIT:
            continue
        pair_size = max(abs(upper_diagonal), abs(lower_diagonal))
        if pair_size < best_size:
            best_pair = upper_diagonal, lower_diagonal
            best_size = pair_size
    return best_pair


def iter_matrix_candidates(
    lower_bound: int, upper_bound: int
) -> Iterator[MatrixParameters]:
    """Выдаёт допустимые параметры матрицы в порядке возрастания корней.

    Границы заранее проверены частью Вики: это целые числа,
    lower_bound <= upper_bound. Обе границы включены. Корни ненулевые,
    root1 <= root2; совпадение допускается. Модули диагоналей не больше 20.
    Для каждой пары корней выдаётся одна предпочтительная пара b, c.

    :param lower_bound: проверенная нижняя граница корней
    :param upper_bound: проверенная верхняя граница корней
    :return: итератор кандидатов, пустой при отсутствии вариантов
    """
    # |root1 * root2| = |bc| <= 400; ненулевой целый корень по модулю >= 1.
    root_limit = DIAGONAL_LIMIT**2
    first_root = max(lower_bound, -root_limit)
    last_root = min(upper_bound, root_limit)
    for root1 in range(first_root, last_root + 1):
        if root1 == 0:
            continue
        for root2 in range(root1, last_root + 1):
            if root2 == 0:
                continue
            main_diagonal = root1 + root2
            if abs(main_diagonal) > DIAGONAL_LIMIT:
                continue
            diagonal_pair = find_diagonal_pair(root1 * root2)
            if diagonal_pair is None:
                continue
            upper_diagonal, lower_diagonal = diagonal_pair
            yield MatrixParameters(
                a=main_diagonal,
                b=upper_diagonal,
                c=lower_diagonal,
                root1=root1,
                root2=root2,
            )


def generate_conditions(
    lower_bound: int,
    upper_bound: int,
    evaluate_formula: Callable[[MatrixParameters], FormulaParameters | None],
) -> GeneratedConditions:
    """Возвращает первый набор, принятый расчётом коэффициентов Арины.

    Границы предварительно проверяются частью Вики. evaluate_formula
    получает кандидата и возвращает тип формулы и точные коэффициенты,
    если они проходят ограничения простоты, иначе None. Для разных
    корней используются ключи A1, A2, для двойного корня — A, B.
    Ошибки самой функции расчёта передаются вызывающей стороне.

    :param lower_bound: проверенная нижняя граница корней включительно
    :param upper_bound: проверенная верхняя граница корней включительно
    :param evaluate_formula: расчёт и проверка коэффициентов части Арины
    :raises ValueError: если ни один кандидат не удовлетворяет ограничениям
    :return: параметры матрицы, корни, тип формулы и её коэффициенты
    """
    for candidate in iter_matrix_candidates(lower_bound, upper_bound):
        formula = evaluate_formula(candidate.copy())
        if formula is not None:
            return GeneratedConditions(**candidate, **formula)
    raise ValueError(
        "В заданном диапазоне нет набора, удовлетворяющего ограничениям генератора."
    )
