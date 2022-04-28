// Sort in quick time

int partition( int * data, int low, int high ) {
	int i,j,p,t;
	p = data[high];
	i = low - 1;
	for ( j = low; j <= high - 1; j++ ) {
		if ( data[j] < p ) {
			i++;
			t = data[i];
			data[i] = data[j];
			data[j] = t;
		}
		
	}
	t = data[i+1];
	data[i+1] = data[high];
	data[high] = t;
	return i + 1;
}

void quickSort (int * data, int low, int high) {
    int i, j, p, t;
	if ( low >= high ) 
    {
        return;
    }
	p = partition( data, low, high);

	quickSort( data, low, p-1);
	quickSort( data, p+1, high);
    return;
}
int main() {
	int i;
	int j;
	int k;
    int sz = 5;
	int a[5];
	j = 31;
	for ( i = 0; i < sz; i++) 
	{ 
        int x;
        read_int(x);    
		a[i] = x;
		print_int(a[i]);
		print_char(' ');
	}
	print_char('\n');

	quickSort(a,0,sz);
	for ( i = 0; i < sz; i++) 
	{ 
		print_int(a[i]);
		print_char(' ');
	}
	print_char('\n');
	return 0;
}
