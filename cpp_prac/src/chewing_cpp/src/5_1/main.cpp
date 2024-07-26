#include "chewing_cpp/4_5/MyString.hpp"
#include "chewing_cpp/5_1/complex.hpp"

int main(int argc, char** argv)
{
    {
        MyString str1("a word");
        MyString str2("sentence");
        MyString str3("sentence");

        if (str1 == str2)
            std::cout << "str1 와 str2 같다." << std::endl;
        else
            std::cout << "st1 와 str2 는 다르다." << std::endl;

        if (str2 == str3)
            std::cout << "str2 와 str3 는 같다." << std::endl;
        else
            std::cout << "st2 와 str3 는 다르다" << std::endl;
    }
    {
        Complex a(1.0, 2.0);
        Complex b(3.0, -2.0);

        Complex c = a * b;

        c.println();
    }
    {
        // 주석 풀기 Complex& Complex::operator+(const Complex& c)

        // Complex b(3.0, -2.0);
        // Complex c(1.0, 2.0);
        // Complex a = b + c + b;
        // a.println();
    }
    {
        Complex a(1.0, 2.0);
        Complex b(3.0, -2.0);
        Complex c(0.0, 0.0);
        c = a * b + a / b + a + b;
        c.println();
    }
    {
        Complex a(1.0, 2.0);
        Complex b(3.0, -2.0);
        a += b;
        a.println();
        b.println();
    }
    {
        Complex a(0, 0);
        a = a + "-1.1 + i3.923";
        a.println();
    }
    {
        Complex a(0, 0);
        a = a + "-1.1 + i3.923";
        a.println();
        a = a - "1.2 -i1.823";
        a.println();
        a = a * "2.3+i22";
        a.println();
        a = a / "-12+i55";
        a.println();
    }
    return 0;
}