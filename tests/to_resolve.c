struct node{
    int data ;
    struct node* next ;
};

int main(){
    struct node n, *p; // should give error
    // struct node* p;
    n.data = 1;
    n->next = p;
    return 0;
}
