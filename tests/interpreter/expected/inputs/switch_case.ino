int classify(int x) {
  switch (x) {
    case 1:
      return 10;
      break;
    case 2:
      return 20;
      break;
    default:
      return 0;
      break;
  }
}

int result = classify(1);
