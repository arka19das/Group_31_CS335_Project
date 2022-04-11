struct p
{
    int a;
};
int main()
{
    int a, m, n;
    struct p p1;

    int b;
    int c;
    int arr[2][2];

    a = 1;
    b = 1;

    arr[1][1] = 1;
    for (int i = 0; i < n; i++)
    {
        int j = 0;
        while (j < m)
        {
            a++;
            do
            {
                b++;
            } while (b < a);
        }
    }
    return 0;
}
