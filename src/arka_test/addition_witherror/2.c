int main()
{
    int z = 5;
    int x = 5 ;
    {
        int x = 4 ;
        int z = 2 ;
        int y;
        z = x ;
    }
    x = z ;
    
}