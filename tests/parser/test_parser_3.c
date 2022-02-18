
struct complex {
  int imag;
  float real;
};

struct number {
  struct complex comp;
  int integer;
} num1, num2, num3;

int main() {

  // initialize complex variables
  num1.comp.imag = 11;
  num1.comp.real = 5.25;
  num2.comp.imag = -22;
  num2.comp.real = -5.25;
  // initialize number variable
  num1.integer = 6;
  num2.inetger = 10;
  char operation = '/';
  int a=1,b=2,c;
  switch(operation)
    {
        case '+':
            c=a+b;
            break;

        case '-':
            c=a-b;
            break;

        case '*':
            c=a*b;
            break;

        case '/':
            c=a/b;
            break;

        default:
            ;
    }
  int x = num1==num2?1:0;
  return 0;
}
