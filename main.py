def _validate_matrix(matrix: list[list[int]]) -> None:
    if not isinstance(matrix, list):
        raise ValueError("Аргумент должен быть списком списков (матрицей).")

    n = len(matrix)
    if n == 0:
        raise ValueError("Матрица не может быть пустой (порядок должен быть >= 1).")

    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("Каждая строка матрицы должна быть списком.")
        if len(row) != n:
            raise ValueError("Матрица должна быть квадратной.")
        for elem in row:
            if not isinstance(elem, int):
                raise ValueError("Все элементы матрицы должны быть целыми числами.")


def _determinant_recursive(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 1:
        return matrix[0][0]

    determinant = 0

    for j in range(n):
        minor = []
        for i in range(1, n):
            minor_row = []
            for k in range(n):
                if k != j:
                    minor_row.append(matrix[i][k])
            minor.append(minor_row)
        sign = (-1) ** (0 + j)
        algebraic_complement = sign * _determinant_recursive(minor)
        determinant += matrix[0][j] * algebraic_complement
    return determinant


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    _validate_matrix(matrix)
    return _determinant_recursive(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
