struct p{
    int a;
};
struct q{
    int a;
};

int foo(struct p x){
    return 0;
}


int main(){
    struct p a;
    struct q s;

    foo(s);
    return 0;
}