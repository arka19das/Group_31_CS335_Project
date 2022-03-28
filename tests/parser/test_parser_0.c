struct Point {
  int x;
  int y;
};

int x(struct Point *p) { return p->x * p->y; }

int main() {
  struct Point *p;
  p->x = 2;
  p->y = 3;
  return x(p);
}
