// 1D array

int func(int* arr, int n) {
    for (int i = 0; i < n; ++i) {
        print_int(arr[i]);
    }
    return 0;
}

int main() {
    int arr[5];
    int x;
    for (int i = 0; i < 5; ++i) {
        arr[i] = i * i;
    }
    func(arr, 2);

    // for (int i = 0; i < 10; ++i) {
    //     print_int(arr[i]);
    //     print_char('\n');
    // }

    return 0;
}
