#include <iostream>

int main(int argc, char **argv)
{
    // void my_void; // void는 메모리 차지하지 않아 선언 불가
    int i = 123;
    float f = 123.456f;
    double d = 123.456;

    // 포인터의 크기는 모두 같다(8byte)
    // 때문에 void 포인터로 모든 타입을 가리킬 수 있다.
    void *my_void;
    
    my_void = &i;
    std::cout << "my_void = " << my_void << std::endl;
    
    my_void = &f;
    std::cout << "my_void = " << my_void << std::endl;

    my_void = &d;
    std::cout << "my_void = " << my_void << std::endl;

    float *my_float = &f;
    double *my_double = &d;

    // 포인터의 크기는 모두 같다(8byte)
    // 8byte인 이유는 시스템 아키텍처가 64bit 이기 때문이다.
    // 시스템 아키텍처가 32bit 이면 4byte이다.
    // 이를 확인하려면 void*의 크기를 확인하면 된다. sizeof(void*)
    std::cout << "sizeof(my_void) = " << sizeof(my_void) << std::endl;
    std::cout << "sizeof(my_float) = " << sizeof(my_float) << std::endl;
    std::cout << "sizeof(my_double) = " << sizeof(my_double) << std::endl;
    
    std::cout << "sizeof(i) = " << sizeof(i) << std::endl;
    std::cout << "sizeof(f) = " << sizeof(f) << std::endl;
    std::cout << "sizeof(d) = " << sizeof(d) << std::endl;
    
    return 0;
}