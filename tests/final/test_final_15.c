// Intentional: Break in Loops

int main() {
    int i = 10;
    int j = 2;

    for (; ; j += 3) {
        if (j >= i) {
            break;
        }
        print_int(j);
        print_char(' ');
    }

    // print_int(j);

    switch (j) {
        case 12: 
            {
                print_int(144);
                break;
            }
        case 11: 
            {
                print_int(121);
                break;
            }
        case 10: 
            {
                print_int(100);
                break;
            }
    }

    if (j < 12) {
        // break; // Error: compilation error, since break not in switch/for
    }

    return 0;
}
