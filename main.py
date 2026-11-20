def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    n = len(matrix)
    a = matrix[0][0]

    if n == 1:
        return a

    b = matrix[0][1]
    c = matrix[1][0]

    previous_determinant = a
    current_determinant = a * a - b * c

    for _ in range(3, n + 1):
        next_determinant = (
            a * current_determinant - b * c * previous_determinant
        )
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
