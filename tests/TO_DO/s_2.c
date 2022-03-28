// struct Point
// {
//    int x, y;
// };
 
// int main()
// {   

//    struct Point p1 = {};
// //    struct Point p1;
//    return 0;
//}

int main() {
struct Point {
  int sum;
  int arr[10];
  double f;  
};

  struct Point p = { 1, {1}, 2.0};
  int x;
//   p.f = 0.1;
  return p.sum;
}