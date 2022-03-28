int main() { 
    char* str = "Hello World!"; 
    int sum = 0;
    for (int str = 0; str < 9; ++str) {
        sum += str;
    }
    sum += str; // Throws error, since str is char* in outer scope
    return 0;
}
