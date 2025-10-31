int max_of_three(int a, int b, int c) {
  if (a > b && a > c) {
    return a;
  } else if (b > c) {
    return b;
  } else {
    return c;
  }
}

int first  = max_of_three(8, 7, 3);
int second = max_of_three(5, 7, 3);
int third  = max_of_three(5, 7, 9);
