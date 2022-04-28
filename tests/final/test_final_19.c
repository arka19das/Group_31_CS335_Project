int main() {
    int* i; 
    int sum = 0;
    for (int i = 0; i < 10; ++i) {
        sum += i;
    }
    // sum += i;
    print_int(sum);
    return 0;
}
