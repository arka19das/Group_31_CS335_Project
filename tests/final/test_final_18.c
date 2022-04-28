// Struct Pointer

struct Human {
    int height;
    int weight; 
};

int main() {
    int height;
    int weight;
    float bmi;
    struct Human h;
    struct Human* human;
    human = &h;

    read_int(height);
    human->height = height;

    read_int(weight);
    human->weight = weight;

    bmi = (human->weight) / (human->height * human->height);
    print_float(bmi);

    return 0;
}
