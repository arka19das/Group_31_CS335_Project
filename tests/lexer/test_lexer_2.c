//Operation test
// Driver program to test above functions
int main(void)
{
    
    bool b1 = true;
    int assign = ((~(((1+2-5)/3)*1000)>>1))<<1)++;
    assign = (1ll&&2uL)?1:0;
    assign>>=1;
    assign<<=1;
    assign/=2;
    assign*=2;
    assign-=10;
    assign+=10;
    assign%=3;
    assign--;
    /*
        Bitwise
    */
    b1&=1;
    b1|=1;
    b1=b1^1;
    
    //Comparison
    if(0x1==020){ printf("Equal");} 
    else if(0x20>020u){ printf("Greater");}
    else if(0x20L<=020){ printf("Lesser");}
    else { printf("None");}


    return 0;
}