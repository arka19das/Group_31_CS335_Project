// Intentional: Struct operators not defined 

struct Point {
    int x;
    int y;
};

int main() {
    struct Point p1;
    struct Point p2;

    p1.x = 10;
    p1.y = 15;
    p2.x = 20;
    p2.y = 25;

    // p1 += p2; // Error: += not defined for struct Point

    return 0;
}
