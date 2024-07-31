#include "chewing_cpp/5_2/5_2.hpp"

int main(int argc, char** argv)
{
    {
        func();
        B b;
    }
    {
        Complex a(0, 0);
        a = "-1.1 + i3.923" + a;
        a.println();
    }
    {
        Complex a(0, 0);
        a = "-1.1 + i3.923" + a;

        a = a + a;
        a.println();
    }
    {
        Complex a(0, 0);
        a = "-1.1 + i3.923" + a;
        a = a + a;

        Complex b(1, 2);
        b = a + b;

        b.println();
    }
    {
        Complex a(0, 0);
        a = "-1.1 + i3.923" + a;
        std::cout << "a 의 값은 : " << a << " 이다. " << std::endl;
    }
    {
        MyString str("abcdef");
        str[3] = 'c';

        str.println();
    }
    {
        Int x = 3;
        std::cout << x << std::endl;
        int a = x+4;
        std::cout << a << std::endl;
        x = a * 2 + x + 4;
        std::cout << x << std::endl;
    }
    {
        Test t(3);

        func(++t); // 4
        func(t++); // 4 가 출력됨
        std::cout << "x : " << t.get_x() << std::endl;
    }
    return 0;
}