#include "cpp_prac/header.h"

// 함수 이름은 같으나 매개변수(input parameter)로 구분된다.
// 함수 선언시 func(int val)은 input parameter
// 함수 사용시 func(3)은 argument

void func(void)
{
    std::cout << "void" << std::endl;
}

void func(int val)
{
    std::cout << "int: " << val << std::endl;
}

void func(char c)
{
    std::cout << "char: " << c << std::endl;
}

int main()
{
    func();
    func(3);
    func('q');
    
    return 0;
}