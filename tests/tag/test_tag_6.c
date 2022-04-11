struct p
{
    int a;
    char b;
    char arr[41];
};
int main()
{
    struct p p1;

    int arr[10][20][30][50];
    int x;
    x = *arr[1][100][4];
    x = p1.a;
    x = p1.arr[1];

    return 0;
}
