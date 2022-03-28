void transpose(int** matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = i + 1; j < size; ++j) {
            matrix[i][j] = matrix[j][i];
        }
    }
}

int main() { 
    int **matrix;

    matrix[0][0] = 1;
    matrix[0][1] = 0;
    matrix[0][2] = 0;

    matrix[1][0] = 0;
    matrix[1][1] = 1;
    matrix[1][2] = 0;

    matrix[2][0] = 0;
    matrix[2][1] = 0;
    matrix[2][2] = 1;

    transpose(matrix, 3);
}
