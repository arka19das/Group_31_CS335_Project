// checking multi dim array
struct st
{
    int a;
    int x;
};
int main()
{
    int s = 1;
    long a[4][5][6];
    long b;
    // b = &s;
    a[1][3] = &b;
    return 0;
}