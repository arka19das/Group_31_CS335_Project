// Intentional Compile TIme Evaluation + Array Size type

int main() {
    int arr1[3];
    int arr2['a'];
    int arr3['a' + 3];

    float f = 2; 
    int n = 4;
    // arr3[f] = 1; // Error cannot use float
    // int arr4[f]; // Error: Variable length does not work
    // int arr5[-4]; // Negative dimension not possible
    // int arr6['a' + 4.0]; // Float type expression not possible.
    // int arr7[n]; // Error: Variable length does not work


    return 0;
}
