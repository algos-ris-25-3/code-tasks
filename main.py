def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной ленты разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    a, b, c = validate_matrix(matrix)
    n = len(matrix)

    def determinant(order: int) -> int:
        if order == 1:
            return a
        if order == 2:
            return a ** 2 - c * b
        return a * determinant(order - 1) - b * c * determinant(order - 2)

    return determinant(n)

def validate_matrix(matrix) -> tuple[int, int, int]:
    if not isinstance(matrix, list):
        raise Exception("Матрица должна быть списком")

    n = len(matrix)
    if n == 0:
        raise Exception("Порядок матрицы должен быть не меньше 1")

    if any(not isinstance(s, list) for s in matrix):
        raise Exception("Матрица должна быть списком из списков")

    if any(len(row) != n for row in matrix):
        raise Exception("Матрица должна быть квадратной")

    a = matrix[0][0]

    if n == 1:
        return a, 0, 0

    b = matrix[0][1]
    c = matrix[1][0]

    for i in range(n):
        for j in range(n):
            if i == j and matrix[i][j] != a:
                raise Exception("Элементы на основной диагонали должны быть одинаковыми")
            elif i + 1 == j and matrix[i][j] != b:
                raise Exception("Элементы на наддиагонали должны быть одинаковыми")
            elif i - 1 == j and matrix[i][j] != c:
                raise Exception("Элементы на поддиагонали должны быть одинаковыми")
            elif abs(i - j) > 1 and matrix[i][j] != 0:
                raise Exception("Элементы вне диагоналей должны быть равны 0")

    return a, b, c

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
