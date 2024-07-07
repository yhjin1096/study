#include <iostream>

int change_val(int &p)
{
    std::cout << &p << std::endl;
    p = 3;
    return 0;
}

int& function() {
    int a = 2;
    return a;
}

int function1() {
    int a = 2;
    std::cout << &a << std::endl;
    return a;
}

int& function2(int& a) {
    a = 2;
    return a;
}

int main(int argc, char** argv)
{
    {
        int a = 3;
        int& another_a = a;
    }
    {
        // int& another_a; //error, 선언시 참조할 변수 명시해야함
    }
    {
        int a = 10;

        int* p = &a;
        int& another_a = a;

        int b = 3;
        another_a = b; // another_a가 가리키는 놈에게 b를 대입, 주소 변화 x
        p = &b;

        std::cout << &a << "," << &b << "," << &another_a << "," << p << std::endl;
        std::cout << another_a << std::endl;
    }
    {// 함수 인자로 reference를 사용했을 때 메모리에 존재한다. -> 주소 값이 다른가 확인 -> 같다.
        int num = 5;
        std::cout << &num << std::endl;
        change_val(num);
        std::cout << num << std::endl;
    }
    {
        // 상수 값 즉, 리터럴은 참조 불가, 4는 메모리 주소 없음
        // int &ref = 4;
        
        // 상수 참조자로 선언하면 가능, const가 변경할 수 없는 상수로 만들어주기 때문
        // ref는 메모리 주소 없음, 4는 상수 값으로 데이터 영역에 저장
        const int &ref = 4;
        int a = ref;
        std::cout << a << "," << ref << std::endl;
    }
    {
        // a가 사라졌기 때문에 reference만 남음 -> 에러, Dangling
        // int b = function();
        // b = 3;
        // std::cout << b << std::endl;

        // 메모리 사용하는 경우
        // function1은 scope를 벗어나는 지역변수를 return
        // b는 이런 상태에서 값을 저장하기 위해 메모리 사용
        const int& b = function1();
        std::cout << &b << std::endl;
        std::cout << b << std::endl;

        // 주소 값 복사 한 번으로 전달이 끝
        // 주소 전달을 위해 메모리가 사용된다.
        int a = 10;
        int c = function2(a);
        std::cout << c << std::endl;
    }
    return 0;
}