#include "cpp_prac/header.h"
// c에서 동적할당을 담당하는 malloc, free를
// c++에서는 new, delete를 사용한다.

char * makestr(int len)
{
    char * str = new char[len];
    return str;
}

class Simple
{
    public:
        Simple()
        {
            std::cout << "I'm simple constructor!" << std::endl;
        }
        int tmp = 10;
};

int main()
{
    char * str = makestr(20);
    strcpy(str, "i am so happy");
    std::cout << str << std::endl;
    delete []str; // 배열로 동적 할당된 변수 메모리 비우기
    std::cout << str << std::endl;

    ////////////////////////////

    Simple sp1;
    Simple *sp2 = new Simple();
    std::cout << sp1.tmp << "," << sp2->tmp << std::endl;
    return 0;
}