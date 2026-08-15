#include <iostream>

int add (int a, int b)
{
    return a + b;
}

int main()
{
    // Implicit Type Conversion 을 따른다.
    // 서로 다른 타입의 연산 → 더 넓은 타입으로 변환
    // bool → char → short → int → long → long long → float → double → long double
    auto a = 1 + 2.0; // double
    auto b = 1.0f + 2.0; // double
    auto d = 1L + 2;       // long (long + int)
    auto e = 1u + 2;       // unsigned int (unsigned int + int)
    
    auto result = add(1, 2);
}