#include <iostream>

void doSomething()
{
    static int a = 1;
    int b = 1;
    static int c;
    ++a;
    ++b;
    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "c = " << c << std::endl;
    std::cout << "address of a = " << &a << std::endl;
    std::cout << "address of b = " << &b << std::endl;
    std::cout << "address of c = " << &c << std::endl;
}

int value = 123;

int main(int argc, char **argv)
{
    std::cout << "value = " << value << std::endl;
    
    int value = 1;

    std::cout << "value = " << value << std::endl;

    // 전역 연산자, :: 를 사용하면 전역 변수를 사용할 수 있다.
    std::cout << "::value = " << ::value << std::endl;

    // static 변수
    // 왜 이런 결과가? 전역변수랑은 뭐가 다르지?
    // static의 의미: 변수 a가 OS로부터 받은 메모리가 static 하다는 의미다.
    // 초기화 최초 한 번만 한다. -> 결국 초기화가 필수다. -> 초기화 따로 안하면 0으로 초기화
    doSomething(); // a = 2
    doSomething(); // a = 3
    doSomething(); // a = 4

    return 0;
}