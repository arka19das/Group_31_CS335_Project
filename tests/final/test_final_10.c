struct direction {
  int left, right;
};

int main() {
  struct direction x, *y;
  x.left = 100;
  x.right = 1;
  print_int(x.left);
  print_char('\n');
  print_int(x.right);
  print_char('\n');

  y = &x;
  y->right = 1000;
  y->left = 1;
  print_int(x.left);
  print_char('\n');
  print_int(x.right);
  print_char('\n');
  return 0;
}
