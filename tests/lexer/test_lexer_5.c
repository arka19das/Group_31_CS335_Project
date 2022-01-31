// Example modified from https://www.w3schools.com/cpp/cpp_classes.asp
class Vehicle {
    public {
        char *type;
    }
}

class Car <- public Vehicle {
    public {
        char *brand;
        int year;
    };
    private {
        short internal_part1;
    }
};

int main(int argc, char **argv) {
    Car newcar1;
    printf("Class Test");
    return 1;
}