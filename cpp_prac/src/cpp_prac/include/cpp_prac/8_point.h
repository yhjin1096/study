#ifndef __POINT_H_
#define __POINT_H_
#include "header.h"

class Point
{
    // 정보 은닉(information hiding): 외부로부터 class 멤버에 접근하는 방법에 제한이 있도록 설계하는 것, private, const화
    
    // private: class의 다른 멤버들만 접근할 수 있다. -> 외부에서 접근 불가
private:
    int x;
    int y;

public:
    bool InitMembers(int xpos, int ypos);
    
    //const 함수
    //멤버 변수에 저장된 값을 변경하지 않겠다는 선언 -> 8_point.cpp의 GetX함수 볼 것
    //const 함수 내에서는 const가 아닌 함수의 호출이 제한된다. -> 8_rect.cpp의 ShowRecInfo 볼 것
    int GetX() const;
    int GetY() const;

    bool SetX(int xpos);
    bool SetY(int ypos);
    void ShowTest();
};

#endif