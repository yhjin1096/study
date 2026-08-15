#include <iostream>

class Something
{
    private:
        static int value_;
        int value2_ = 2;
    public:
        static int getValue()
        {
            return value_;
            // 정적 멤버 함수는 this 불가
            // 정적 멤버 함수는 정적 멤버 변수만 접근 가능
            // return this->value_;
            // return this->value2_;
            // return value2_;
        }
        int temp()
        {
            // this는 특정 instance의 주소를 가리킴
            return this->value_ + this->value2_;
        }
};

int Something::value_ = 1;

int main(int argc, char* argv[])
{
    {
        // 특정 instance가 없어도 접근 가능
        // std::cout << Something::value_ << std::endl; // value_가 private, error
        // private이 되면 접근 불가 -> 정적 멤버 함수는 private이 되어도 접근 가능
        std::cout << Something::getValue() << std::endl;

        Something st1;
        // std::cout << st1.getValue() << " " << st1.value_ << std::endl; // value_가 private, error
        std::cout << st1.getValue() << std::endl;
        std::cout << st1.temp() << std::endl;

        // class 내 멤버 함수는 하나의 주소를 가리킨다.
        // 2개의 instance가 멤버 함수를 각각 호출하면 해당 함수의 주소를 찾아 실행시키며, 각자의 멤버 변수를 사용한다.
        // 이를 위해 사용되는 것이 this 포인터이다.
        
        // C++ forbids taking the address of a bound member function to form a pointer to member function
        // 바인딩된 멤버 함수의 주소를 멤버 함수 포인터로 만들 수 없다
        // 바인딩: 어떤 이름(함수, 변수 등)과 실제 메모리 상의 대상을 연결하는 것"
        // Something::*fptr는 멤버 함수 포인터, st1.temp는 st1이라는 instance에 바인딩 된 함수
        // &Something::temp는 어디에도 바인딩 되지 않음
        // int (Something::*fptr)() = &st1.temp; // error

        // non-static member function은 instance에 종속되어 있기 때문에 instance 선언 후 사용
        // 다른 instance에서 동일하게 호출 x, 내부적으로 this 포인터 사용
        int (Something::*fptr1)() = &Something::temp;
        Something st2;
        std::cout << (st2.*fptr1)() << std::endl; // st2의 this 포인터를 사용해서 temp 함수 호출

        // static member function, 특정 instance와 상관 없이 실행 시킬 수 있다.
        // int (Something::*fptr2)() = &Something::getValue; // error
        int (*fptr2)() = &Something::getValue;
        std::cout << fptr2() << std::endl;
    }


    return 0;
}