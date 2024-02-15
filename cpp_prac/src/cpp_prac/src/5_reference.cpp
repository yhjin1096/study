#include "cpp_prac/header.h"

void swap(int &ref1, int &ref2)
{
    int tmp;
    tmp = ref1;
    ref1 = ref2;
    ref2 = tmp;
}

int main()
{
    // num2는 num1을 참조하는 reference
    // 10을 저장한 메모리에 접근할 수 있는 변수 이름이 2개인 것임
    int num1 = 10;
    // 이때 &은 주소연산자가 아닌 참조연산자
    // 이미 선언된 변수에 사용하면 주소연산자, 선언시 사용하면 참조연산자 
    int &num2 = num1; 
    int &num3 = num2;

    std::cout << num1++ << std::endl;
    std::cout << num2++ << std::endl;
    std::cout << num1 << "," << num2 << std::endl;
    std::cout << num3 << std::endl;
    
    ////////////////////////////

    int val1 = 10;
    int val2 = 20;
    swap(val1, val2);
    std::cout << val1 << ", " << val2 << std::endl;

    return 0;
}