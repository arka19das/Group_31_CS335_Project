// Big Expressions and functions

int getk(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j) {
    int k=(a+b+c/5*124+d)*(f*(g*h+(f+g-d)/h)*e/3*4+d*c*b-a/h);
    return k;
}

int main() {
    int a,b,c,d,e,f,g,h,i,j,k,l;
    a=12,b=16,c=43,d=7,e=72,f=65,g=12,h=3,i=4,j=43;
    j*=((a*b+c)*d+e*f+g*h*(i*j))*(a*((b*d)/c)*j+i-(g^f^h));
    // k=(a+b+c/5*124+d)*(f*(g*h+(f+g-d)/h)*l/3*4+d*c*b-a/h);
    k = getk(a, b, c, d, e, f, g, h, i, j);
    print_int(j);
    print_char('\n');
    print_int(k);
    print_char('\n');

    return 0;
}
