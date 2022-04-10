struct p{
    int a;
};
struct p p1;
int a;
int main(){
    int b;
    int c;
    a=1;
    b=1;
    
    int arr[2][2];
    arr[1][1]=1;
    switch(arr[1][1])
    {
        case 'a': for(int i=0;i<100;i++)
        {
            int j;
            if(i==j)
            {
                arr[1][0]=1;
            }
            else 
            {
                break;
            }
        }
    default:break;
    }
    return 0;
}