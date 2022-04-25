// 1D array

int main() {
    int arr[10];
    for (int i = 0; i < 10; ++i) {
        arr[i] = i * i;
    }

    for (int i = 0; i < 10; ++i) {
        print_int(arr[i]);
        print_char('\n');
    }

    return 0;
}
