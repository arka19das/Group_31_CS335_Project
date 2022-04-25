// Structs and functions and functions on structs

struct Line {
    int x1;
    int x2;
    int y1;
    int y2;
};

float getSlope(struct Line line) {
    return (line.y2 - line.y1) / (line.x2 - line.x1);
}

int main() {
    float slope = 0;
    struct Line line;
    line.x1 = 0;
    line.y1 = 0; 
    line.x2 = 4;
    line.y2 = 8;
    slope = getSlope(line);
    print_float(slope);
    // currently error in print_float
    return 0;
}
