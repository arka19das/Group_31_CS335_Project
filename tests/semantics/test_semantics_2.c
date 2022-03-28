// Recursion

int choose_calls = 0;

int choose(int n, int k) {
  ++choose_calls;
  if (n == k || k == 0) {
    return 1;
  } else {
    return choose(n - 1, k - 1) + choose(n - 1, k);
  }
}

int main() {
  int ans[8] = { 1, 10, 45, 120, 210, 252, 210, 120, 45, 10 };

  for (int i = 0; i < 8; i++) {
    if (choose(10, i) != ans[i]) {
      return -1;
    }
  }
  return 0;
}
