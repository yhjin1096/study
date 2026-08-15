#include "cpp_prac/header.h"
#include "cpp_prac/8_point.h"
#include "cpp_prac/8_rect.h"

int main()
{
    Point pos1;
    Point pos2;

    if(!pos1.InitMembers(-2, 4))
        std::cout << "초기화 실패" << std::endl;
    if(!pos1.InitMembers(2, 4))
        std::cout << "초기화 실패" << std::endl;

    if(!pos2.InitMembers(5, 9))
        std::cout << "초기화 실패" << std::endl;

    Rectangle rec;

    if(!rec.InitMembwers(pos2, pos1))
        std::cout << "직사각형 초기화 실패" << std::endl;
    if(!rec.InitMembwers(pos1, pos2))
        std::cout << "직사각형 초기화 실패" << std::endl;

    rec.ShowRecInfo();

    return 0;
}