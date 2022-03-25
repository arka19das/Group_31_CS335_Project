int main()
{
    int *x ;
    int y ;
    //char y should not through an error
    x = & y ; // should not throw a warning
    return 0 ;   
}