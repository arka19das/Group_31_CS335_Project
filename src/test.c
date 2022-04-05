struct st
{

    int x[2];
    // struct st *next;
};
long *f(long long int *a)
{
    return a;
}
int main()
{

    short int **p;
    long double z;
    long long int x, y, z1;
    float x2 = 13.89;
    unsigned int x3 = 4;
    // z1 = ++(x + y);
    struct st s1, s2;
    s1.x[0] = 1;
    s2 = s1;
    z = z * z;
    s1.x[1] = 2;
    // printf("%d %d\n", s2.x[1], s1.x[1]);
    z1 = x * x3;
    z1 = x + y;
    z1 = x - y;
    z1 = x / y;
    z1 = x % y;
    z1 = x >= y;
    z1 = x <= y;
    z1 = x == y;
    z1 = x != y;
    z1 = x > y;
    z1 = x < y;
    z1 = x & y;
    z1 = x | y;
    z1 = x << y;
    z1 = x >> y;
    z1 = x ^ y;
    z1 = x && y;
    z1 = x || y;
    z1 = x ? y : z;

    x = (long long int)x2;
    p++;
    p--;
    ++p;
    --p;
    // z--;
    // z++;
    z = 16.0;
    // if (p == z)
    //     printf("1");
    // if (x2)
    //     printf("2");
    switch (x)
    {
    case 1:
        x2 = 0;
        // printf("2");
    }
    x = sizeof(int);
    y = sizeof(long double);
    x++;
    sizeof x2;
    return 0;
}