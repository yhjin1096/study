#include <iostream>
#include <typeinfo>
#include <iomanip>

int main(int argc, char** argv)
{
    // 암시적 형 변환 - 컴파일러가 자동으로 변환
    {
        int a = 123.0;
        std::cout << typeid(a).name() << std::endl;
    }
    
    // numeric promotion
    // 작은 것을 큰 것으로
    {
        // 4 byte float to 8 byte double
        float a = 1.0f;
        double d = a;
        std::cout << typeid(d).name() << std::endl;
    }
    
    std::cout << "--------------------------------" << std::endl;

    // numeric conversion
    // 큰 것을 작은 것으로
    {
        short s = 2;

        int i = 300;
        char c = i; // 범위 넘어감

        double d = 0.123456789;
        float f = d;

        std::cout << static_cast<int>(c) << std::endl;

        std::cout << std::setprecision(12);
        std::cout << d << std::endl;
        std::cout << f << std::endl;

        std::cout << "--------------------------------" << std::endl;
        // 형변환 우선 순위
        // int < unsigned int < long < unsigned long < long long < unsigned long long < float < double < long double
        std::cout << 5u - 10 << std::endl;
        std::cout << 5u - 10u << std::endl;
    }

    return 0;
}