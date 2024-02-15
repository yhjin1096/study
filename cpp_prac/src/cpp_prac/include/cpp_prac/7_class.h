#ifndef __CAR_H__
#define __CAR_H__

#include "cpp_prac/header.h"

class Car
{
    public:
        void hello();
        void func();
    private:
        int test;
};

inline void Car::func()
{
    std::cout << "inline function은 class가 선언된 파일 내에서 선언되어야 합니다." << std::endl;
}

#endif