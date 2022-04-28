// Struct Pointer

struct Human {
    float weight; 
    float height;
};

int main() {
    int height;
    int weight;
    float bmi;
    struct Human human;
    struct Human* pHuman;

    read_int(height);
    human.height = height;
    // pHuman.height = height // Error, since . cannot be used with pointer.

    read_int(weight);
    pHuman->weight = weight;
    // human->weight = weight // Error, since ->cannot be used with non-pointer

    bmi = (human.weight) / (pHuman->height * human.height);
    // getBMI(&human);
    print_float(bmi);

    return 0;
}
