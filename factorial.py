def factorialTR(n, result):
    if n == 1:
        return result
    return factorialTR(n - 1, result * n)

def factorial(n):
    return factorialTR(n, 1)

print(factorial(5))
