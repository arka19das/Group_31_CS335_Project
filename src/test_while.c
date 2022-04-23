#include <stdio.h>
// struct t1
// {
//     int a;
//     struct t1 *next;
//     int b;
//     float d1;
//     // struct t1 *next;
// };

int func(int p) //(int a, struct t1 b, int c, int d, int e, int f)
{

    return p+1;
    // d++;
    
}
int main()
{
   
    int a=10;
    // c = c + (float *)1;
    // c = &(a);
    // a = *c;
    // *c = a; // ERROR
    // d = d + c1 + c1;
    // printf("%ld %ld", d, (float *)1);
    int b = func(a);

    return 0;
}