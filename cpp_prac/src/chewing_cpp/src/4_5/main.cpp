#include "chewing_cpp/4_5/MyString.hpp"

int main(int argc, char** argv)
{
    {
        MyString str1("hello world");
        MyString str2(str1);
        str1.println();
        str2.println();
    }
    {
        // MyString str1("very very very long string");
        // str1.println();
        // str1.assign("short string");
        // str1.println(); // 결과는 short string이지만 실제는 short stringry long string
        // str1.assign("very long string");
        // str1.println();
    }
    {
        MyString str1("very very very long string");
        str1.reserve(30);

        std::cout << "Capacity : " << str1.capacity() << std::endl;
        std::cout << "String length : " << str1.length() << std::endl;
        str1.println();
    }
    {
        MyString str1("very long string");
        MyString str2("<some string inserted between>");
        str1.reserve(30);

        std::cout << "Capacity : " << str1.capacity() << std::endl;
        std::cout << "String length : " << str1.length() << std::endl;
        str1.println();

        str1.insert(5, str2);
        str1.println();
    }
    return 0;
}