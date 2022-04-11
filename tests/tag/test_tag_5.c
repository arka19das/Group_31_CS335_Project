struct p
{
    int a;
};
int main()
{

    int arr[10][20][30][50];
    int *x;
    x = *arr[1][100][4];
    return 0;
}
