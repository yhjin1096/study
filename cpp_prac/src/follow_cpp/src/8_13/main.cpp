#include <iostream>

class A
{
    public:
        A()
        {
            std::cout << "constructor" << std::endl;
        }
        ~A()
        {
            std::cout << "destructor" << std::endl;
        }
        void print()
        {
            std::cout << "hello" << std::endl;
        }
};

int main(int argc, char* argv[])
{
    std::cout << "---------" << std::endl;
    A a;
    a.print();
    std::cout << "---------" << std::endl;

    // R value 처럼 작동
    // 주소 없이 임시 객체로 생성 후 삭제 됨
    std::cout << "---------" << std::endl;
    // std::cout << &A() << std::endl; // error: taking address of rvalue
    A().print();
    std::cout << "---------" << std::endl;
    A().print();
    std::cout << "---------" << std::endl;

    return 0;
}