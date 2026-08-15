#include <iostream>
#include "follow_cpp/4_2/MyConstants.hpp"

// forward declaration
// void doSomething(); // extern 생략 가능
// 컴파일러가 어디에 정의가 되어있는지 자동으로 찾아준다.
// 링크 시점에서 경로 및 주소를 찾아 메모리에 할당하여 실행 파일을 만든다.
// 단, 여러 파일에 같은 이름의 함수가 있는 경우 multiple definition 에러 발생.
extern void doSomething();
extern int a;

int main(int argc, char **argv)
{
    doSomething();
    std::cout << "a = " << a << std::endl;

    // test.cpp에서 해당 const 변수들을 사용한 경우
    // 같은 namespace 내에 있는 변수를 참조 했지만 주소가 다르다.
    // -> 외부 참조를 할 때마다 복사본이 계속 만들어진다.

    // extern으로 헤더파일에서 정의만 하고, 소스파일에서 초기화 하는 경우 주소가 같아짐
    // 헤더파일에서 초기화까지 하면 에러 발생
    // -> 헤더 파일을 include 할 때마다 선언되기 때문에 multiple definition 에러 발생.
    std::cout << "-----main2.cpp MyConstants-----" << std::endl;
    std::cout << "pi = " << MyConstants::pi << ", " << &MyConstants::pi << std::endl;
    std::cout << "avogadro = " << MyConstants::avogadro << ", " << &MyConstants::avogadro << std::endl;
    std::cout << "my_gravity = " << MyConstants::my_gravity << ", " << &MyConstants::my_gravity << std::endl;
    
    return 0;
}