#include <iostream>
#include <typeinfo>

int main()
{
    // 기본 타입 테스트
    auto a = 1 + 2;
    auto b = 1 + 2.0;
    auto c = 1.0f + 2.0;
    auto d = 1L + 2;
    auto e = 1u + 2;
    
    // 나눗셈 테스트
    auto f = 5 / 2;
    auto g = 5.0 / 2;
    auto h = 5 / 2.0;
    
    // 부호 테스트
    auto i = 1u + 1;
    auto j = -1 + 1u;
    
    // 출력
    std::cout << "a = " << a << " (type: " << typeid(a).name() << ")" << std::endl;
    std::cout << "b = " << b << " (type: " << typeid(b).name() << ")" << std::endl;
    std::cout << "c = " << c << " (type: " << typeid(c).name() << ")" << std::endl;
    std::cout << "d = " << d << " (type: " << typeid(d).name() << ")" << std::endl;
    std::cout << "e = " << e << " (type: " << typeid(e).name() << ")" << std::endl;
    std::cout << "f = " << f << " (type: " << typeid(f).name() << ")" << std::endl;
    std::cout << "g = " << g << " (type: " << typeid(g).name() << ")" << std::endl;
    std::cout << "h = " << h << " (type: " << typeid(h).name() << ")" << std::endl;
    std::cout << "i = " << i << " (type: " << typeid(i).name() << ")" << std::endl;
    std::cout << "j = " << j << " (type: " << typeid(j).name() << ")" << std::endl;
    
    return 0;
} 