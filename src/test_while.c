// // checking multi dim array

// arr[1][2][3][2];
// (((((0+1)*200+2)*300)+3)*400+2)*sizeof(int)
// arr[1]

// [100,200,300,400]

// [200*300*400*sizeof(datatype),300*400*sizeof(datatype),400*sizeof(datatype),sizeof(datatype)]
// struct st
// {
//     int a;
//     int x;
// };
// // if (s == s1)
// // {
// //     s = s1;
// //     return;
// // }
//     return 0;
// }
// int main()
// {
//     long s, s1;
//     s = s1;
//     // int x;
//     // x();
//     // c = b;
//     do
//     {
//         s++;
//         break;
//     } while (s);
//     x(s, s1);
//     // b = &s;
//     // c = !a[4];
//     // a[1][3] = &b;
//     return 0;
// }
// #include <stdio.h>
//     int main()
//     {
//         int arr[100][200][300];
//         int **x, *x1, arr1;
//         // int z;
//         // z=y;
//         // arr[1][3] = 1;
//         // x = **(arr + 2);
//         // x=*arr[1];
//         // *x = arr[1][1];
//         // x[1];//ERror
//         int y = 1;
//         (y) = 1;
//         x = (arr[1]); // Error we are alllowitn but gcc is not allowing
//         // (y + 1) = 1;
//         // instructions for this are not correctly generated
//         // printf("%ld %ld %ld\n", arr, (arr[1] + 1), x);
//         // y = 100;
//         // y = arr[1][2];
//         // y = sizeof(int) + sizeof arr[1][2];
//     }
int main()
{
    int *arr[100][200][300][400];
    // int **x = arr[100][200];
    // x++;
    int x, **y = arr[1][2][3];
    // y = arr[1][2][3];
    return 0;
}
// kjdjbfjkdfbjkf