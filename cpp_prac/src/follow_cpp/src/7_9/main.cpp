#include <iostream>
#include <array>
#include <functional>

int func()
{
    return 5;
}

int goo()
{
    return 9;
}

int func2(int a)
{
    return a;
}

bool isEven(const int& number)
{
    return number % 2 == 0;
}

bool isOdd(const int& number)
{
    return number % 2 == 1;
}

void printNumbers(const std::array<int, 10>& my_array, bool print_even)
{
    for(auto element : my_array)
    {
        if(print_even && element % 2 == 0)
        {
            std::cout << element << " ";
        }
        else if(!print_even && element % 2 == 1)
        {
            std::cout << element << " ";
        }
    }
    std::cout << std::endl;
}

void printNumbers(const std::array<int, 10>& my_array, bool (*check_func)(const int&))
{
    for(auto element : my_array)
    {
        if(check_func(element) == true)
        {
            std::cout << element << " ";
        }
    }
    std::cout << std::endl;
}

void printNumbers(const std::array<int, 10>& my_array, std::function<bool(const int&)> check_func)
{
    for(auto element : my_array)
    {
        if(check_func(element) == true)
        {
            std::cout << element << " ";
        }
    }
    std::cout << std::endl;
}

int main()
{
    {
        // 함수 포인터
        std::cout << func << std::endl; // 함수 포인터가 bool로 변환됨
        std::cout << (void*)func << std::endl; // void*로 캐스팅

        // std::cout << sizeof(func) << std::endl;
        // 함수의 메모리 크기를 알려면 sizeof(함수명)이 아닌 sizeof(함수포인터)를 사용해야 합니다.
        // 함수 포인터는 함수의 주소를 저장하는 변수이므로 시스템에 따라 4바이트 또는 8바이트가 됩니다.
        std::cout << "시스템 아키텍처: " << sizeof(void*) << "bytes" << std::endl;
        std::cout << "함수 포인터의 크기: " << sizeof(&func) << " bytes" << std::endl;
        
        // 함수 포인터 선언
        int (*func_ptr)() = func;
        int (*goo_ptr)() = goo;
        int (*func_ptr2)(int) = func2;
        std::cout << func_ptr() << std::endl;
        std::cout << goo_ptr() << std::endl;
        std::cout << func_ptr2(10) << std::endl;
        std::cout << (void*)func_ptr << std::endl;
        std::cout << (void*)goo_ptr << std::endl;
        std::cout << (void*)func_ptr2 << std::endl;

        func_ptr = goo_ptr;
        std::cout << func_ptr() << std::endl;
        std::cout << (void*)func_ptr << std::endl;
    }

    {
        std::array<int, 10> my_array = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        printNumbers(my_array, true);
        printNumbers(my_array, false);
        printNumbers(my_array, isEven);
        printNumbers(my_array, isOdd);
    }

    {
        std::array<int, 10> my_array = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        std::function<bool(const int&)> func_ptr = isEven;
        printNumbers(my_array, func_ptr);
    }
    return 0;
}