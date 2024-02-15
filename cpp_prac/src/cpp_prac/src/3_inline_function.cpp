#include "cpp_prac/header.h"

// macro function
// 장점: 속도, 자료형에 구애받지 않음
// 단점: 복잡한 함수 정의 힘듦 -> inline 함수
#define SQUARE(x) (x * x)

// inline function
inline int square(int x)
{
    return x * x;
}

inline int square(double x) // return이 int 형으로 고정됨 -> template function, 나중에 다룸
{
    return x * x;
}

int main()
{
    std::cout << SQUARE(3) << std::endl;
    std::cout << SQUARE(3.3) << std::endl;

    std::cout << square(3) << std::endl;
    std::cout << square(3.3) << std::endl;
    return 0;
}