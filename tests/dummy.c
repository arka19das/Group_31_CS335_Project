struct complex {
  int imag;
  float real;
};

struct number {
  struct complex comp;
  int integer;
} ;

int main() {
  int a=1, b, c;
  
  struct number num1;
  // initialize complex variables
  num1.comp.imag = 11;
//   num1.comp.real = 5.25;
//   num2.comp.imag = -22;
//   num2.comp.real = -5.25;
//   //initialize number variable
//   num1.integer = 6;
//   num2.integer = 10;

  return 0;
}
