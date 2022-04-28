// Using Keywords for variables 
int binarySearch(int* arr, int n, int target) {
    int lo = 0;
    int hi = n; 
    int mid = -1; 
    while (lo < hi) {
        mid = (lo + hi) / 2; 
        if (arr[mid] == target) {
            break;
        } else {
            if (arr[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
    }
    return mid;
}

int main() {
    int num = 10; 
    int idx = -1;
    int arr[10];
    arr[0] = 4;
    arr[1] = 7;
    arr[2] = 10;
    arr[3] = 13;
    arr[4] = 16;
    arr[5] = 19;
    arr[6] = 20;
    arr[7] = 22;
    arr[8] = 25;
    arr[9] = 30;
    // int continue = 4; // Error: reserved keyword
    // idx = binarySearch(arr, num, 19);
    print_int(idx);
    return 0;


}
