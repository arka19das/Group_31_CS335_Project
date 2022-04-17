#include <stdio.h>
struct t1
{
    int a;
    int b;
    // struct t1 *next;
};
// char *strchr(char *str, char ch)
// {
//     char *temp = 0; // NULL
//     int i = 0;
//     char ch1 = '\\';
//     printf("%c 1\n", ch1);
//     while (*(str + i) != '\0')
//     {
//         if (*(str + i) == ch)
//         {
//             temp = str + i;
//         }
//         i++;
//     }
//     return temp;
// }
int func(int p, long int j, int k) //(int a, struct t1 b, int c, int d, int e, int f)
{
    p++;
    j++;
    k++;
}
int main()
{
    // float a, b;
    // struct t1 t2;
    // int **x, y;
    // char ch = 'n';
    // // printf("%c\n", ch);
    // int *p;
    // // a = 0;
    // // a = a + b;
    // y = **x;
    // (unsigned long long int)a;

    // func(t2, p); //(a, t2, a, b, a, b);
    int *c, a, b;
    func(a, a, b);
    return 0;
}
