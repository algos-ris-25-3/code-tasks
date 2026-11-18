def validate_matrix(matrix):
    if type(matrix) is not list:
        raise ValueError("Матрица должна быть списком")

    if not matrix:
        raise ValueError("Матрица не может быть пустой")

    for row in matrix:
        if type(row) is not list:
            raise ValueError("Каждая строка матрицы должна быть списком")

        if len(row) != len(matrix):
            raise ValueError("Матрица должна быть квадратной")

        for value in row:
            if type(value) is not int:
                raise ValueError("Элементы матрицы должны быть целыми числами")


def determinant_rec(matrix):

    if len(matrix) == 1:
        return matrix[0][0]

    result = 0

    for j in range(len(matrix)):
        minor = []

        for row in matrix[1:]:
            new_row = []

            for i in range(len(row)):
                if i != j:
                    new_row.append(row[i])

            minor.append(new_row)

        result += (-1) ** j * matrix[0][j] * determinant_rec(minor)

    return result


def calculate_determinant(matrix: list[list[int]]) -> int:
    """Вычисляет определитель разложением по строке.

    :param matrix: квадратная целочисленная матрица порядка не меньше 1
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    validate_matrix(matrix)
    return determinant_rec(matrix)


def main():
    matrix = [[1, 2], [3, 4]]
    print("Матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {calculate_determinant(matrix)}")


if __name__ == "__main__":
    main()
