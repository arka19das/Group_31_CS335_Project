long factorial(int n)  
{  
  if (n == 0)  
   { return 1;
   }  
  else  
  {
    return(n * factorial(n-1));
  }  
}  
   
void main()  
{  
  int number=1024;  
  long fact;  
   
  fact = factorial(number);    
  return 0;  
}  
