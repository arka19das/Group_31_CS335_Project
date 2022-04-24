struct p{
    int a;
    float s;
    // int arr[2];
}
// struct p foo(){
//     struct p x;
//     x.a=2;
//     x.p=2;
//     x.arr[0]=100;
//     x.arr[1]=200;
//     return x;
// }

int main(){
    // struct p z[2];
    // z[1].a=100;
    // print_int(z[1].a);
    // z = foo();
    // print_int(z.a);
    // print_int(z.arr[0]);
    // print_int(z.arr[1]);
    // print_float(z.p);

    int arr[2], i;
    for(i=0;i<2;i++){
        arr[i]=i;
        print_int(arr[i]);
    }
    // for(int i=0;i<2;i++){
    //     print_int(arr[i]);
    // }
    return 0;
}