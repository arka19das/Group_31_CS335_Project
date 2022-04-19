
// #include<stdio.h>
// int j=0;
int foo(int a){
    return 0;
}
int main(){
    // foo(1);
    int *p,a;
    p=&1;
    p=&(1);
    p=&(a+1);
    p=&a;
    return 0;
}