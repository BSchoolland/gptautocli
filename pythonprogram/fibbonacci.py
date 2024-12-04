def print_fibonacci_sequence(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b
    print()

print_fibonacci_sequence(10)