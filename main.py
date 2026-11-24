def validate(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise Exception("n должно быть целым числом не меньше 1")

def gray_code(n: int) -> list[list[int]]:
    """Рекурсивно строит полный n-разрядный код Грея зеркальным построением.

    :param n: число разрядов, целое не меньше 1.
        Логическое значение не является допустимой длиной
    :raises Exception: если n не является таким числом
    :return: список из 2**n слов в стандартной нумерации
    """
    validate(n)
    return create_gray_code(n)

def create_gray_code(n: int) -> list[list[int]]:
    if n == 1:
        return [[0], [1]]
    previous = create_gray_code(n - 1)
    left = [[0] + word for word in previous]
    right = [[1] + word for word in reversed(previous)]
    return left + right

def main():
    n = 3
    print(f"Код Грея, число разрядов {n}")
    for word in gray_code(n):
        print(word)


if __name__ == "__main__":
    main()
