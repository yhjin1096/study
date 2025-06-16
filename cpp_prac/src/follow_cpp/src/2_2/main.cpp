#include <iostream>
#include <limits>
#include <cmath>

int main(int argc, char **argv)
{
  {
    int i = 1; // copy initialization
    int i2(1); // direct initialization
    int i3{1}; // uniform initialization
    // int i4{3.15}; // error
  }

  short s = 1; // 2byte
  int i = 1; // 4byte
  long l = 1; // 4byte
  long long ll = 1; // 8byte

  std::cout << "short s = " << s << std::endl;
  std::cout << "int i = " << i << std::endl;
  std::cout << "long l = " << l << std::endl;
  std::cout << "long long ll = " << ll << std::endl;

  std::cout << "sizeof(short) = " << sizeof(s) << std::endl;
  std::cout << "sizeof(int) = " << sizeof(i) << std::endl;
  std::cout << "sizeof(long) = " << sizeof(l) << std::endl;
  std::cout << "sizeof(long long) = " << sizeof(ll) << std::endl;

  std::cout << std::pow(2, sizeof(short) * 8 - 1) - 1 << std::endl; // 부호 비트 제외, 0 제외
  std::cout << std::numeric_limits<short>::min() << std::endl;
  std::cout << std::numeric_limits<short>::max() << std::endl;
  std::cout << std::pow(2, sizeof(int) * 8 - 1) - 1 << std::endl;
  std::cout << std::numeric_limits<int>::min() << std::endl;
  std::cout << std::numeric_limits<int>::max() << std::endl;
  std::cout << std::pow(2, sizeof(long) * 8 - 1) - 1 << std::endl;
  std::cout << std::numeric_limits<long>::min() << std::endl;
  std::cout << std::numeric_limits<long>::max() << std::endl;
  std::cout << std::pow(2, sizeof(long long) * 8 - 1) - 1 << std::endl;
  std::cout << std::numeric_limits<long long>::min() << std::endl;
  std::cout << std::numeric_limits<long long>::max() << std::endl;

  unsigned int ui = -1;
  std::cout << "unsigned int ui = " << ui << std::endl;

  return 0;
}