def validate_matrix(matrix):
    if not isinstance(matrix, list) or not matrix:
        raise ValueError("Матрица должна быть непустым списком строк")

    size = len(matrix)

    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("Строка матрицы должна быть списком")
        if len(row) != size:
            raise ValueError("Матрица должна быть квадратной")
        for value in row:
            if type(value) is not int:
                raise ValueError("Элементы матрицы должны быть целыми числами")


def determinant_rec(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    result = 0
    for column, value in enumerate(matrix[0]):
        submatrix = []
        for row in matrix[1:]:
            submatrix.append(row[:column] + row[column + 1 :])
        if column % 2 == 0:
            sign = 1 
        else:
            sign = -1
        result += sign * value * determinant_rec(submatrix)
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
