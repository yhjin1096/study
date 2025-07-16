#include <iostream>

class Something
{
    public:
        // static member variable은 초기화 불가능
        // static member variable은 헤더에서 선언 불가, 소스 파일에서 선언 가능
        // 해당 class에 속하는 모든 객체가 접근 가능한 변수 -> 주소 미리 할당
        static int value_;
        // constexpr -> 컴파일 타임에 값이 결정되어야함 -> static 이여도 초기화 가능
        static constexpr int value2_ = 10;
};

// 초기화는 class 외부에서 1번만 해야한다.
int Something::value_ = 1;
// int Something::value_ = 13;

int main(int argc, char* argv[])
{
    // instance 선언 전에 이미 메모리 할당됨
    // 특정 instance가 없어도 접근 가능
    std::cout << &Something::value_ << " " << Something::value_ << std::endl;
    std::cout << &Something::value2_ << " " << Something::value2_ << std::endl;

    Something st1;
    Something st2;

    st1.value_ = 2;
    std::cout << &st1.value_ << " " << st1.value_ << std::endl;
    std::cout << &st2.value_ << " " << st2.value_ << std::endl;

    return 0;
}