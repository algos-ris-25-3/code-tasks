def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной ленты разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    pass


def validate(matrix) -> None: 
    if not isinstance(matrix, list):
        raise TypeError("matrix must be list")
    if any(not isinstance(i, list) for i in matrix):
        raise TypeError('matrix must be list of list')
    if any(not isinstance(j, int) for i in matrix for j in i):
        raise TypeError('elements of matrix must be int')
    if any(len(i) != len(matrix) for i in matrix):
        raise ValueError("matrix must be square")
    if len(matrix) == 1: return None
    a, b, c = matrix[0][0], matrix[0][1], matrix[1][0]
    for y, row in enumerate(matrix):
        for x, col in enumerate(row):
            if y == x and a != col:
                raise ValueError(f'element with index ({y}; {x}) different than {a}')
            if y == x - 1 and b != col:
                raise ValueError(f'element with index ({y}; {x}) different than {b}')
            if y - 1 == x and c != col:
                raise ValueError(f'element with index ({y}; {x}) different than {c}')
            if col != 0 and (x < y - 1 or x > y + 1): 
                raise ValueError(f'element with index ({y}; {x}) different than 0')

validate([[1,2,0,0,0],[3,1,2,0,0],[0,3,1,2,0],[0,0,3,1,2],[0,0,0,3,1]])

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


# if __name__ == "__main__":
#     main()
