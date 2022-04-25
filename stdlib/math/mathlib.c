int abs(int val){
	if(val < 0)
		{return -val;}
	return val;
}

float abs(float val){
	if(val < 0)
		{return -val;}
	return val;
}
float exp(float x){
	float sum = 1.0; // initialize sum of series
    for (int i=30; i > 0; i--) {
        sum = 1.0 + x * sum / i;
    }
 
    return sum;
}


float log(float n)
{
    float num = (n - 1) / (n + 1);
    float cal;
    float sum = 0;
    int mul;
    int i = 1;
    for (; i <= 10; i++) {
        mul = 2*i - 1;
        cal = pow(num, mul);
        cal = cal / mul;
        sum = sum + cal;
    }
    sum = 2 * sum;
    return sum;
}
  

float log10(float x)
{
    return log(x)/2.303;
}
int pow(int x, int n) {
    int val = 1;
    for (int i=1 ; i <= n; i++)
    {
        val *= x;
    }
    return val;
}

float pow(float x, int n){
	float val = 1.0; 
    
    for (int i=1; i <= n; i++)
    {
        val *= x;
    }
    return val;
}
