// Basics : Math Expressions

int main() {
  long i[8];
  unsigned long u[8];
  int sum;

  i[0] = 1;
  i[1] = -1;
  i[2] = -1L;
  i[3] = -1u;
  i[4] = -1l;
  i[5] = (1ll << 32) - 1 & 3;
  i[6] = (long)((1ull << 32) - 1) < 0;
  i[7] = -1u < 0;

  u[0] = 1;
  u[1] = -1;
  u[2] = -1l;
  u[3] = -1ull;
  u[4] = -1ll;
  u[5] = (1ll << 32) - 1 & 3;
  u[6] = (long)((1ll << 32) - 1) < 0;
  u[7] = -1u < 0;

  sum = 0;
  for (int j = 0; j < 8; ++j) {
    sum += i[j] * u[j];
  }

  return sum;
}
