// Switch: Is it a weekend?

void prints(char* str) {
    int i = 0; 
    while (str[i] != '\0') {
        print_char(str[i]);
        i++;
    }
    return;
}

int main() {
    int i;
    char* str;
    read_int(i);

    switch (i) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            print_int(0);
            break;
        case 6:
        case 0:
            print_int(1);
            break;
        default:
            print_int(-1);
    }
    return 0;
}

