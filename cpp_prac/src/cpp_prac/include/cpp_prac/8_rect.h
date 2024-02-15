#ifndef __RECT_H_
#define __RECT_H_

#include "header.h"
#include "cpp_prac/8_point.h"

class Rectangle
{
    private:
        Point upLeft;
        Point lowRight;
    
    public:
        bool InitMembwers(const Point &ul, const Point &lr);
        void ShowRecInfo() const;
};

#endif