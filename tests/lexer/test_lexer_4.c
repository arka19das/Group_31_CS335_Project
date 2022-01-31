// Loops ans Struct test
struct Node { 
	int data; 
	struct Node* next; 
}; 

int main(){
    int i = 0, n = 10;
    int sum = 0;
    for (i = 0; i< n&&i*i<=1000; i++){
        sum += i;
        // /**/ for
    }
    i--;
    i/=2;
    while (i>0){
        i--;
        /* // while*/ sum -= i;
    }
    do{
        i--;
        sum *= i;
        // do while
    } while (i>1||sum*sum>100);

    struct Node* head;
    struct Node* temp;
    head = (struct Node*)malloc(sizeof(struct Node));
    for(int j=0;i<5;i++){
        temp = (struct Node*)malloc(sizeof(struct Node));
        temp->data = j;
        head->next = temp;
        head = head->next;
    }
    return 0;
}