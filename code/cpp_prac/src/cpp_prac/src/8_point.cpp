#include "cpp_prac/8_point.h"

bool Point::InitMembers(int xpos, int ypos)
{
    if(xpos < 0 || ypos < 0)
        return false;
    
    x = xpos;
    y = ypos;

    return true;
}
int Point::GetX() const
{
    // 8_point.cpp: In member function ‘int Point::GetX() const’:
    // 8_point.cpp:15:7: error: assignment of member ‘Point::x’ in read-only object
    // x = 10;
    return x;
}
int Point::GetY() const
{
    return y;
}
bool Point::SetX(int xpos)
{
    if(xpos < 0 || xpos > 100)
        return false;

    x = xpos;
    return true;
}
bool Point::SetY(int ypos)
{
    if(ypos < 0 || ypos > 100)
        return false;

    y = ypos;
    return true;
}
void Point::ShowTest()
{
    std::cout << "Point::ShowTest()" << std::endl;
}