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
    int sum=0;
    do{
        sum += n;
        n++;
        print_int(sum);
    }while(sum<80);
    // d++;
    return sum;
    
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