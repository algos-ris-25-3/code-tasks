def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Итеративное вычисление определителя трёхдиагональной матрицы.
    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    n = len(matrix)

    # Проверка: квадратная матрица порядка >= 1
    if n < 1:
        raise Exception("Матрица должна быть порядка не меньше 1")
    for row in matrix:
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной")

    # Проверка: все элементы — целые числа
    for i in range(n):
        for j in range(n):
            if not isinstance(matrix[i][j], int):
                raise Exception("Все элементы должны быть целыми числами")

    # Определяем значения на диагоналях
    a = matrix[0][0]  # главная диагональ
    b = matrix[0][1] if n > 1 else 0  # наддиагональ
    c = matrix[1][0] if n > 1 else 0  # поддиагональ

    # Проверка: матрица действительно трёхдиагональная с постоянными значениями
    for i in range(n):
        for j in range(n):
            if i == j:
                # Главная диагональ
                if matrix[i][j] != a:
                    raise Exception("Непостоянное значение на главной диагонали")
            elif j == i + 1:
                # Наддиагональ
                if matrix[i][j] != b:
                    raise Exception("Непостоянное значение на наддиагонали")
            elif j == i - 1:
                # Поддиагональ
                if matrix[i][j] != c:
                    raise Exception("Непостоянное значение на поддиагонали")
            else:
                # Все остальные элементы должны быть нулями
                if matrix[i][j] != 0:
                    raise Exception("Матрица не является трёхдиагональной")

    # Итеративное вычисление определителя по рекуррентной формуле:
    # D_1 = a
    # D_2 = a^2 - b*c
    # D_k = a * D_{k-1} - b*c * D_{k-2}
    if n == 1:
        return a

    d_prev2 = a                    # D_1
    d_prev1 = a * a - b * c        # D_2

    if n == 2:
        return d_prev1

    for k in range(3, n + 1):
        d_curr = a * d_prev1 - b * c * d_prev2
        d_prev2 = d_prev1
        d_prev1 = d_curr

    return d_prev1

def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")

if __name__ == "__main__":
    main()
