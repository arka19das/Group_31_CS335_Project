/* Switch test
Recursion */
int f1(int n){
    printf("In f1");
    return fact(n);
}

int fact(int n){
    if (n==0){
        return 1;
    }
    else{
        return n*fact(n-1);
    }
}
 
int main(){
    int i1 = f1(2);
    if(i1==3){
        double d1 = 1.222e12;
        i1++;
        goto iff;
    }

    iff:
    printf("%d\n",i1);

    long i2;
    switch (i1){
        case 1:
            i2=1;
            break;
        case 2:
            i2=5; 
        default:
            i2 = ++i1;
            break;
    }
    return 0;
}