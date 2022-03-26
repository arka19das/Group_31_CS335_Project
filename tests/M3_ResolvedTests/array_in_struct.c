struct point{
    int p1 , p2 ;
    int a[10] ;
};

void foo(int a){

}
int main(){
    struct point arr[10] ;
    arr[0].p1 = 10;
    foo(arr[0].p1);
    //int b;
    // foo(b);
}