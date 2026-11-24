def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной ленты разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """

    n = len(matrix)
    a, b, c = _validate_matrix(matrix)

    def determinant(k: int) -> int:
        if k == 0:
            return 1
        if k == 1:
            return a

        return a * determinant(k - 1) - b * c * determinant(k - 2)

    return determinant(n)


def _check_element(
    matrix: list[list[int]], i: int, j: int, a: int, b: int, c: int
) -> None:
    if type(matrix[i][j]) is not int:
        raise Exception("элементы должны быть целыми")

    value = 0

    if i == j:
        value = a
    elif j == i + 1:
        value = b
    elif i == j + 1:
        value = c

    if matrix[i][j] != value:
        raise Exception("не трёхдиагональная матрица")


def _validate_matrix(matrix: list[list[int]]) -> tuple[int, int, int]:
    n = len(matrix)

    if n == 0:
        raise Exception("пустая матрица")

    for row in matrix:
        if len(row) != n:
            raise Exception("неквадратная матрица")

    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else 0
    c = matrix[1][0] if n > 1 else 0

    for i in range(n):
        for j in range(n):
            _check_element(matrix, i, j, a, b, c)

    return a, b, c


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
