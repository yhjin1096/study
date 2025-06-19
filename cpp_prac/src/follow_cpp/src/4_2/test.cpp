#include <iostream>
#include "follow_cpp/4_2/MyConstants.hpp"

extern int a = 123;

void doSomething()
{
    // std::cout << "test.cpp doSomething" << std::endl;
    std::cout << "a = " << a << std::endl;

    std::cout << "-----test.cpp MyConstants-----" << std::endl;
    std::cout << "pi = " << MyConstants::pi << ", " << &MyConstants::pi << std::endl;
    std::cout << "avogadro = " << MyConstants::avogadro << ", " << &MyConstants::avogadro << std::endl;
    std::cout << "my_gravity = " << MyConstants::my_gravity << ", " << &MyConstants::my_gravity << std::endl;
}