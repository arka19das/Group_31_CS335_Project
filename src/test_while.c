#include <stdio.h>
// struct t1
// {
//     int a;
//     struct t1 *next;
//     int b;
//     float d1;
//     // struct t1 *next;
// };

int func(int n) //(int a, struct t1 b, int c, int d, int e, int f)
{
    if (n<=2)
    {
        return 1;
    }
    return func(n-1)+func(n-2);
    // d++;
    
}
int main()
{
   
    int a=4;
    int b1=102;
    // c = c + (float *)1;
    // c = &(a);
    // a = *c;
    // *c = a; // ERROR
    // d = d + c1 + c1;
    // printf("%ld %ld", d, (float *)1);
    int b = func(a);

    return 0;
}