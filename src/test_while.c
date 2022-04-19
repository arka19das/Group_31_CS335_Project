#include <stdio.h>
struct t1
{
    int a;
    struct t1 *next;
    int b;
    double d1;
    // struct t1 *next;
};

int func(int p,  int j, struct t1 d, int k) //(int a, struct t1 b, int c, int d, int e, int f)
{
    p+j+k;
    // d++;
    
}
int main()
{
    struct t1 d1;
    int a, x, b, *c, **d;
    int c1;
    // c = c + (float *)1;
    // c = &(a);
    // a = *c;
    // *c = a; // ERROR
    // d = d + c1 + c1;
    // printf("%ld %ld", d, (float *)1);
    func(a, x, d1, b);

    return 0;
}
