from profilehooks import profile


def fibonacci_rec(n: int) -> int:
    if n == 1:
        return 1
    if n == 2:
        return 1

    return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    numbers = [1, 1]

    for i in range(2, n):
        numbers.append(numbers[i - 1] + numbers[i - 2])

    return numbers[n - 1]


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


def main():
    n = 35
    print(f"Вычисление {n} числа Фибоначчи рекурсивно:")
    print(fibonacci_rec(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно:")
    print(fibonacci_iter(n))

    print(f"\nВычисление {n} числа Фибоначчи итеративно без использования массива:")
    print(fibonacci(n))


if __name__ == "__main__":
    main()
