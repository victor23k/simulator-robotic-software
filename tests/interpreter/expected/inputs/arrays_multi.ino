int a[3][3] = {
  {1, 2, 3},
  {4, 5, 6},
  {7, 8, 9},
};

int identity[3][3] = {
  {1, 0, 0},
  {0, 1, 0},
  {0, 0, 1},
};

int result[3][3] = {
  {0, 0, 0},
  {0, 0, 0},
  {0, 0, 0},
};

for (int i = 0; i < 3; i++) {
  for (int j = 0; j < 3; j++) {
    for (int k = 0; k < 3; k++) {
      result[i][j] += a[i][k] * identity[k][j];
    }
  }
}

int one = a[0][0];
int two = a[0][1];
int three = a[0][2];
int four = a[1][0];
int five = a[1][1];
int six = a[1][2];
int seven = a[2][0];
int eight = a[2][1];
int nine = a[2][2];

>>>>>

INT one = 1
INT two = 2
INT three = 3
INT four = 4
INT five = 5
INT six = 6
INT seven = 7
INT eight = 8
INT nine = 9
