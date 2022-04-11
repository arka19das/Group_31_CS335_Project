struct p
{
    int a;
};
int main()
{
    int a;
    struct p p1;

    int b;
    int c;
    int arr[2][2];

    a = 1;
    b = 1;

    arr[1][1] = 1;
    switch (arr[1][1])
    {
    case 'a':
        for (int i = 0; i < 100; i++)
        {
            int j;
            if (i == j)
            {
                arr[1][0] = 1;
            }
            else
            {
                break;
            }
        }
    case 96:
        for (int i = 0; i < 100; i++)
        {
            int j;
            if (i == j)
            {
                continue;
            }
            else
            {
                break;
            }
        }
    default:
        break;
    }
    return 0;
}