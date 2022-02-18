void Array_sort(int *array , int n)
{ 
    // declare some local variables
    int i=0 , j=0 , temp=0;

    for(i=0 ; i<n ; i++)
    {
        for(j=0 ; j<n-1 ; j++)
        {
            if(array[j]>array[j+1])
            {
                temp        = array[j];
                array[j]    = array[j+1];
                array[j+1]  = temp;
            }
        }
    }
}
float Find_median(int array[] , int n)
{
    float median=0;
    
    // if number of elements are even
    if(n%2 == 0)
    {
        median = (array[(n-1)/2] + array[n/2])/2.0;
    }
    // if number of elements are odd
    else
    {
        median = array[n/2];
    }
    
    return median;
}
int main()
{
    int arr[] = {11,9,8,5,3,1,1,6,10,5,3,1,2};
    int i=0, sum=0;
    int n = sizeof(arr)/sizeof(arr[0]);
    while (i<n)
    {
        i++;
        sum += i;
    }
    Array_sort(arr,n);
    float f =Find_median(arr,n);
    return 0;
}
