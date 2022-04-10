// // checking multi dim array
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
// int x(int y, int z3)
// {
//     int z;
//     if (z > 0)
//     {
//         int y;
//     }
//     if (z < 0)
//     {
//         if (z < 0)
//         {
//             int z1;
//         }
//         else
//         {
//             int z2;
//         }
//     }

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
int main()
{
    int arr[2][2];
    int *x, y;
    arr[1][3] = 1;
    x = *(arr + 1);
    x = arr[1]; // instructions for this are not correctly generated

    y = 100;
    y = arr[1][2];
    y = sizeof(int) + sizeof arr[1][2];
}