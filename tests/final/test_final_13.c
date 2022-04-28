int square(int a) {
    return a * a;
}

int main() {
    int n = square(4);
    // int n = square(4, 5); // Error: wrong arguments count
    print_int(n);
    return 0;
}
