// Matrix Determinant

int main() {
    int matrix[3][3];
    int det = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            matrix[i][j] = i * i + j;
        }
    }


    for (int i = 0; i < 3; ++i) {
        int curr = matrix[i][0];
        int prod;
        if (i % 2 == 1) {
            curr = -curr;
        }
        prod = matrix[(i + 1) % 3][1] * matrix[(i + 2) % 3][2];
        prod -= matrix[(i + 2) % 3][1] * matrix[(i + 1) % 3][2];
        curr *= prod; 
        det += curr;
    }

    print_int(det);

    return 0;
}

