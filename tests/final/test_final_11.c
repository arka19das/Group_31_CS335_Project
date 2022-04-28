void swap(int *p1, int *p2) {
  int tmp = *p1;
  *p1 = *p2;
  *p2 = tmp;
  return;
}

int main() {
  int a = 3;
  int b = 4;
  print_int(a);
  print_char(' ');
  print_int(b);
  print_char('\n');

  swap(&a, &b);
  print_int(a);
  print_char(' ');
  print_int(b);
  print_char('\n');
  return 0;
}
