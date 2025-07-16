#include <iostream>

// forward declaration
class B;

class A
{
    private:
        int m_value = 1;

        // doSomething 함수에 대해서만 접근 권한 주기
        friend void doSomething(A& a);
        friend void doSomething(A& a, B& b);
};

class B
{
    private:
        int m_value = 2;

        friend void doSomething(A& a, B& b);
};

void doSomething(A& a)
{
    // private 멤버 변수에 접근 불가 -> friend로 선언
    std::cout << a.m_value << std::endl;
}

// 2개의 class에 대한 멤버 변수 접근?
// A, B에 friend 선언하면 될 것 같지만, A의 경우 B가 선언 되기 전이라 B가 뭔지 모름
// -> 전방 선언으로 해결(forward declaration)
void doSomething(A& a, B& b)
{
    std::cout << a.m_value << " " << b.m_value << std::endl;
}

int main(int argc, char* argv[])
{
    A a;
    B b;
    doSomething(a);
    doSomething(a, b);

    return 0;
}