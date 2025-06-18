#include <iostream>

int main(int argc, char **argv)
{
    // constexpr: 컴파일 타임에 값이 결정되는 상수
    constexpr int my_const(123);

    int number;
    std::cin >> number;

    // const: 런타임에 값이 결정되는 상수
    const int my_const_var(number);
    
    // error, 런타임에 값이 결정되는 상수는 constexpr로 선언할 수 없다.
    // constexpr int my_const_var_2(number);

    std::cout << "my_const_var = " << my_const_var << std::endl;

    return 0;
}