// struct + multiple functions

struct Point {
	int x; 
	int y; 
}

struct Rectangle {
	struct Point *topRight; 
	struct Point *botLeft; 
}

long xdist(struct Rectangle* rect) {
	return (rect->topRight->x - rect->botLeft->x);
} 

long ydist(struct Rectangle* rect) {
	return (rect->topRight->y - rect->botLeft->y);
} 

long area(struct Rectangle* rect) {
	return xdist(rect) * ydist(rect);
}

int main() {
	struct Point *p1; 
	struct Point *p2;
	struct Rectangle *rect; 
	long a;
	p1->x = 0; 
	p1->y = 0; 
	p2->x = 30; 
	p2->y = 30; 
	rect->topRight = p2; 
	rect->botLeft = p1; 
	a = area(rect);
	return a != 900;
}

