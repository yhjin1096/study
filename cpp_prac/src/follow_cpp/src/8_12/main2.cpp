#include <iostream>

// forward declaration
class A;

class B
{
    private:
        int m_value = 2;

    public:
        void doSomething(A& a);
};

class A
{
    private:
        int m_value = 1;
        // class 전체에 접근 권한이 주어짐 -> B의 모든 멤버 함수들이 접근 가능
        // friend class B;
        // B 내의 특정 함수에 대해서만 접근 권한 주기
        friend void B::doSomething(A& a);
};

// declaration 문제 때문에 여기서 선언
void B::doSomething(A& a)
{
    std::cout << a.m_value << std::endl;
}

int main(int argc, char* argv[])
{
    A a;
    B b;
    b.doSomething(a);

    return 0;
}