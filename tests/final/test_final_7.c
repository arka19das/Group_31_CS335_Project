// Recursion

struct Point {
    int x; 
    int y;
};

struct Point getCentroid(struct Point p1, 
                         struct Point p2, 
                         struct Point p3) {
    struct Point c; 
    c.x = (p1.x + p2.x + p3.x) / 3;
    c.y = (p1.y + p2.y + p3.y) / 3;
    return c;
}

int main() {
    struct Point p1, p2, p3, c;
    p1.x = 2;
    p2.x = 3;
    p3.x = 4;
    p1.y = 5;
    p2.y = 6;
    p3.y = 7;
    c = getCentroid(p1, p2, p3);
    print_int(c.x);
    print_char('\n');
    print_int(c.y);
    print_char('\n');
    return 0;
}

