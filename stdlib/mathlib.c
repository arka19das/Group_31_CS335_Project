int abs(int val) {
  if (val < 0) {
    return -val;
  }
  return val;
}

float fabs(float val) {
  if (val < 0) {
    return -val;
  }
  return val;
}

float exp(float x) {
  float sum = 1.0; // initialize sum of series
  for (int i = 30; i > 0; i--) {
    sum = 1.0 + x * sum / i;
  }
  return sum;
}

int pow(int x, int n) {
  int val = 1;
  for (int i = 1; i <= n; i++) {
    val *= x;
  }
  return val;
}

float fpow(float x, int n) {
  float val = 1.0;

  for (int i = 1; i <= n; i++) {
    val *= x;
  }
  return val;
}

float log(float n) {
  float num = (n - 1) / (n + 1);
  float cal;
  float sum = 0;
  int mul;
  int i = 1;
  for (; i <= 10; i++) {
    mul = 2 * i - 1;
    cal = fpow(num, mul);
    cal = cal / mul;
    sum = sum + cal;
  }
  sum = 2 * sum;
  return sum;
}

float log10(float x) { return log(x) / 2.303; }

float sqrt(int n) {
    float lo = 1;
    float hi = n;
    float mid;

    if (lo > hi) {
      mid = lo;
      lo = hi;
      hi = mid;
    }

    while (hi - lo >= 0.00001) {
        mid = (lo + hi) / 2;
        if (mid * mid - n > 0.00001) {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    return lo;
}
