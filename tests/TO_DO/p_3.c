int main()
{
    int *x , y ;
    x = &y ;
    x /= 5 ; // currently giving warning, should throw an error, not a major issue
    // x*=5;
    return 0 ;
}