#include <stdio.h>
struct t2{
    int a;
    int b;

};
struct t1
{
    int a;
    struct t2 d;
    int b;
    // float d1;
    // struct t1 *next;
};

// int func(int n) //(int a, struct t1 b, int c, int d, int e, int f)
// {
//     int sum=0;
//     do{
//         sum += n;
//         n++;
//         print_int(sum);
//     }while(sum<80);
//     // d++;
//     return sum;
    
// }
int func(int *x)
{
    *x=3;
    
    return 0;
}
int main()
{
   

//    int a1=100;
    // struct t1 a;
    // float a1=3;
    // a.a=2;
    // b.d1=3;
    // print_int(a.a);
    // a=b;
    // a.a=2;
    // a.d.a=1; /nested struct wrong
    int *x,y=1000,z=3,arr[10];
    // arr[19][1]=18737346;
    // arr[19]+1;
    arr[0]=2;
    x=arr;
    // *x=300;
    print_int(*x);
    // func(a);
    return 0;
}