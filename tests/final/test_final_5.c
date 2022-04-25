// Ifffff

int main(){  
    int i;
    read_int(i);
    // i=1000;
    if (i<100)
    {
        if(i<50)
        {
            if(i==0)
            {
                print_int(1);
            }
            else
            {
                print_int(2);
            }
        }
        else
        {
            print_int(3);
        }
    }
    else{
        if(i<200)
        {
            print_int(4);
        }
        else{
            if(i<300)
            {
                print_int(5);
            }
            else
            {
                print_int(6);
            }
        }
    }
    print_char('\n');
    return 0;
}

