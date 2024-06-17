#include <iostream>

int main(int argc, char** argv)
{
    // memory leak
    // while(1)
    // {
    //     int* ptr = new int;
    // }

    // 기본적인 new, delete 사용
    {
        int tmp = 10;
        int* ptr = &tmp; // strack에 저장된 tmp 주소를 가리킴
        std::cout << tmp << "," << *ptr << std::endl;
        // delete ptr; // delete 불가
        // std::cout << tmp << "," << *ptr << std::endl;
    }
    {
        int tmp = 10;
        int* ptr = new int;
        *ptr = 7; // free store에 7이 저장, 그 주소를 가리킴
        std::cout << tmp << "," << *ptr << std::endl;
        delete ptr;
        std::cout << tmp << "," << *ptr << std::endl;
    }
    {
        int* ptr {nullptr};
        if(ptr)
            std::cout << "메모리 할당 성공 " << ptr << std::endl;
        else
            std::cout << "nullptr " << ptr << std::endl;
    }
    
    // 메모리 할당에 실패한 경우 예외처리
    {
        // new를 사용할 때마다 해줘야하는 단점
        try
        {
            int* ptr = new int[100000000000000];
        }
        catch(std::bad_alloc &exception)
        {
            std::cout << "exception: " << exception.what() << std::endl;
            std::abort(); // 비정상 종료를 의미
        }
    }
    {
        int* ptr = new(std::nothrow) int[100000000000000];
        if(ptr)
            std::cout << "done" << std::endl;
        else
            std::cout << "error" << std::endl;
        delete ptr;
    }
    
    return 0;
}