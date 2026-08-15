#include "cpp_prac/8_rect.h"

bool Rectangle::InitMembwers(const Point &ul, const Point &lr)
{
    //ul은 const 참조자이기 때문에
    //GetX() 함수가 const 함수가 아니라면 error 발생
    
    if (ul.GetX() > lr.GetX() || ul.GetY() > lr.GetY())
    {
        return false;
    }

    upLeft = ul;
    lowRight = lr;
    return true;
}
void Rectangle::ShowRecInfo() const
{
    std::cout << "좌상단: " << upLeft.GetX() << "," << upLeft.GetY() << std::endl;
    std::cout << "우하단: " << lowRight.GetX() << "," << lowRight.GetY() << std::endl;
    // upLeft.ShowTest();
}