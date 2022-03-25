int
foo(int x[100])
{
	// int y[100];
	// int *p;
	
	// y[0] = 2000;
	
	// if(x[0] != 1000)
	// {
	// 	return 1;
	// }
	
	// p = x;
	
	// if(p[0] != 1000)
	// {
	// 	return 2;
	// }
	
	// p = y;
	
	// if(p[0] != 2000)
	// {
	// 	return 3;
	// }
	
	if(sizeof(x) != sizeof(void*))
	{
		return 4;
	}
	
	// if(sizeof(y) <= sizeof(x))
	// {
	// 	return 5;
	// }
	
	return 0;
}



int
main()
{
    long i;
	unsigned long u;
	int x[100];
	
	// i = 1;
	// i = -1;
	// i = -1L;
	// i = -1u;
	// i = -1l;
	// i = (1ll << 32) - 1 & 3;
	// i = (long) ((1ull << 32) - 1) < 0;
	// i = -1u < 0;

	// u = 1;
	// u = -1;
	// u = -1l;
	// u = -1ull;
	// u = -1ll;
	// u = (1ll << 32) - 1 & 3;
	// u = (long) ((1ll << 32) - 1) < 0;
	// u = -1u < 0;
	
	// int x[100];
	// x[0] = 1000;

	return foo(x);
}