// Switch: Is it a weekend?
int main() {
    int i;
    read_int(i);

    switch (i) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            {
                print_int(0);
                break;
            }
        case 6:
        case 0:
            {
                print_int(1);
                break;
            }
        default:
            {
                print_int(-1);
            }
    }
    return 0;
}

