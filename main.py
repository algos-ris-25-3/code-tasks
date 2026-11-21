def _validate_diagonals(matrix: list[list[int]]) -> None:
    """Проверяет постоянство трёх диагоналей и нули вне них.

    :param matrix: квадратная целочисленная матрица порядка не меньше 2
    :raises ValueError: если элемент нарушает структуру матрицы
    """
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            offset = j - i
            if offset == 0:
                expected = a
                location = "на главной диагонали"
            elif offset == 1:
                expected = b
                location = "на наддиагонали"
            elif offset == -1:
                expected = c
                location = "на поддиагонали"
            else:
                expected = 0
                location = "вне трёх диагоналей"
            if value != expected:
                raise ValueError(
                    f"Элемент [{i}][{j}] {location} равен {value}, "
                    f"ожидалось {expected}."
                )


def _validate_tridiagonal_matrix(matrix: list[list[int]]) -> None:
    """Проверяет типы, размеры и трёхдиагональную структуру матрицы.

    :param matrix: проверяемая матрица; логические элементы не допускаются
    :raises TypeError: если матрица или строка не является списком либо
        элемент не является целым числом
    :raises ValueError: если матрица пуста, не квадратная либо нарушает
        постоянство трёх диагоналей или содержит ненулевой элемент вне них
    """
    if not isinstance(matrix, list):
        raise TypeError("Матрица должна быть списком строк-списков.")
    if not matrix:
        raise ValueError("Матрица пуста: требуется порядок не меньше 1.")

    n = len(matrix)
    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise TypeError(f"Строка {i} должна быть списком.")
        if len(row) != n:
            raise ValueError(
                f"Матрица не квадратная: строка {i} содержит {len(row)} "
                f"элементов, ожидалось {n}."
            )
        for j, value in enumerate(row):
            if type(value) is not int:
                raise TypeError(
                    f"Элемент [{i}][{j}] должен быть целым числом, "
                    f"получен {type(value).__name__}."
                )

    if n > 1:
        _validate_diagonals(matrix)


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises TypeError: если матрица или строка не является списком либо
        элемент не является целым числом; логические элементы не допускаются
    :raises ValueError: если матрица пуста, не квадратная либо нарушает
        постоянство трёх диагоналей или содержит ненулевой элемент вне них
    :return: значение определителя
    """
    _validate_tridiagonal_matrix(matrix)
    n = len(matrix)
    a = matrix[0][0]

    if n == 1:
        return a

    b = matrix[0][1]
    c = matrix[1][0]

    previous_determinant = a
    current_determinant = a * a - b * c

    for _ in range(3, n + 1):
        next_determinant = a * current_determinant - b * c * previous_determinant
        previous_determinant = current_determinant
        current_determinant = next_determinant

    return current_determinant


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
