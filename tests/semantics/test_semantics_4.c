// Pointers

int main() {
  // Equivalence of pointer and array
  int arr[10]; 
  int val = 123456; 
  int* ptr = &arr[0]; 
  char* cptr;

  if (ptr != arr) {
    return -1;
  } 

  for (int i = 0; i < 10; ++i) {
    *ptr = i;
    ptr++;
  }

  for (int i = 0; i < 10; ++i) {
    if (arr[i] != i) {return -1;}
  }

  // Using pointers to change specific bytes of int
  ptr = &val;
  cptr = (char*)ptr;
  cptr++; 
  *cptr = 78; 


  return 0;
}
