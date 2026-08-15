#include <iostream>

int main()
{
    // const는 자기 왼쪽에 있는 값을 상수로 만든다.
    // 맨 앞은 예외
    {
        int value = 10;
        const int* ptr = &value; // 가리키는 값을 const로
        // -> 동일하다: int const* ptr = &value;
        std::cout << "value: " << value << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;
        
        // *ptr = 20; // 컴파일 에러
        value = 20;
        std::cout << "value: " << value << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;

        int value2 = 30;
        ptr = &value2;
        std::cout << "value2: " << value2 << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;
    }
    std::cout << "--------------------------------" << std::endl;
    {
        int value = 5;
        int *const ptr = &value; // 포인터 자체를 const로(주소값 변경 불가)
        std::cout << "value: " << value << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;

        *ptr = 10;
        std::cout << "value: " << value << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;

        int value2 = 15;
        // ptr = &value2; // 컴파일 에러
        std::cout << "value2: " << value2 << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;
    }
    std::cout << "--------------------------------" << std::endl;
    {
        int value = 5;
        // const int *const ptr; // 컴파일 에러, 초기화 필수
        const int *const ptr = &value; // 포인터 자체와 가리키는 값 모두 const
        std::cout << "value: " << value << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;

        // *ptr = 10; // 컴파일 에러
        int value2 = 10;
        // ptr = &value2; // 컴파일 에러
        std::cout << "value2: " << value2 << std::endl;
        std::cout << "ptr: " << ptr << std::endl;
        std::cout << "*ptr: " << *ptr << std::endl;
    }
    
    return 0;
}