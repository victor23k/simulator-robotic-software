int factorial(int n) {
    int i = 1;
    int fact = 1;
    do {
        fact *= i;
        i++;
    } while (i <= n);
    return fact;
}

int five_factorial = factorial(5);

>>>>>>

INT five_factorial = 120
