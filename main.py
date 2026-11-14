def fibonacci_rec(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci_rec(n - 1) + fibonacci_rec(n - 2)


def fibonacci_iter(n: int) -> int:
    arr = [1, 1]
    if n == 1 or n == 2:
        return 1
    else:
        for i in range(2, n):
            next_number = arr[i - 1] + arr[i - 2]
            arr.append(next_number)
    return arr[n - 1]


def fibonacci(n: int) -> int:
    if n == 1 or n == 2:
        return 1
    first_previous = 1
    second_previous = 1
    for i in range(2, n):
        next_number = first_previous + second_previous
        first_previous = second_previous
        second_previous = next_number
    return second_previous


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
