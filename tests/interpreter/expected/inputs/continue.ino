int count_odds(int a) {
    int result = 0;
    for (int i = 1; i <= a; i++) {
        if (i % 2 == 0) continue;
        result++;
    }
    return result;
}

int count_odds_while(int a) {
    int result = 0;
    int i = 1;
    while (i <= a) {
        if (i % 2 == 0) {
            i++;
            continue;
        }
        i++;
        result++;
    }
    return result;
}

int odds = count_odds(6);
int odds_while = count_odds_while(6);

>>>>>

INT odds = 3
INT odds_while = 3
