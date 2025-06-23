#include <iostream>

int main()
{
    int i = 10;
    float f = 3.0f;
    // 타입이 없는 포인터
    // 메모리 주소만 가리키고, 어떤 데이터 타입이 들어잇는지 알 수 없음
    void* ptr = nullptr; 

    ptr = &i;
    ptr = &f;

    std::cout << &f << ", " << ptr << std::endl;
    // std::cout << *ptr << std::endl; // 컴파일 에러
    std::cout << *static_cast<float*>(ptr) << std::endl; // float 포인터로 변환 후 내용 출력
}