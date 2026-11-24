def check_matrix(matrix):
    if not isinstance(matrix, list) or not matrix:
        raise Exception("Матрица должна быть непустой!")

    for row in matrix:
        if not isinstance(row, list) or len(row) != len(matrix):
            raise Exception("Матрица должна быть квадратной!")
        for value in row:
            if type(value) is not int:
                raise Exception("Элементы матрицы должны быть целыми числами!")


def check_tridiagonal_structure(matrix, a, b, c):
    n = len(matrix)
    for i in range(n):
        for j in range(max(0, i - 1)):
            if matrix[i][j] != 0:
                raise Exception("Матрица не является трёхдиагональной!")
        for j in range(i + 2, n):
            if matrix[i][j] != 0:
                raise Exception("Матрица не является трёхдиагональной!")
        if matrix[i][i] != a:
            raise Exception("Элементы главной диагонали должны быть одинаковыми!")
        if i < n - 1:
            if matrix[i][i + 1] != b:
                raise Exception("Элементы верхней диагонали должны быть одинаковыми!")
            if matrix[i + 1][i] != c:
                raise Exception("Элементы нижней диагонали должны быть одинаковыми")


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    check_matrix(matrix)

    n = len(matrix)
    a = matrix[0][0]

    if n == 1:
        return a

    b = matrix[0][1]
    c = matrix[1][0]

    check_tridiagonal_structure(matrix, a, b, c)

    bc = b * c
    det_prev = a
    det_curr = a * a - bc

    for _ in range(n - 2):
        det_next = a * det_curr - bc * det_prev
        det_prev = det_curr
        det_curr = det_next

    return det_curr


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
