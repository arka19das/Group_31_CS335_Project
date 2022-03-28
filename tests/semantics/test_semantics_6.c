int factorial(int n) {
    if (n == 0 || n == 1) {
        return n; 
    } else if (n < 0) {
        return -1; 
    } else {
        return n * factorial(n - 1);
    }
}


int main() { 
    if (factorial(5) == 120) {
        break; // Should throw error, as not in loop/switch
    }
}
