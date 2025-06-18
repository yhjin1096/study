#include <iostream>
#include <bitset>

int main(int argc, char **argv)
{
    // comma operator
    int x = 3;
    int y = 10;
    int z = (++x, ++y);
    // ++x; ++y; z = y 와 같다.
    std::cout << "x = " << x << ", y = " << y << ", z = " << z << std::endl;

    int a = 3;
    int b = 10;
    int c = (a++, b++, a+b);
    std::cout << "a = " << a << ", b = " << b << ", c = " << c << std::endl;

    // conditional operator
    // if문과 다르게 const로 선언할 수 있다.
    // if문은 scope가 존재하기 때문, if문 이후 결과를 return 하는 함수를 작성하면 가능하다.
    bool onSale = true;
    const int price = (onSale == true) ? 10 : 100;
    /*
    if (onSale == true)
        price = 10;
    else
        price = 100;
    */
    std::cout << "price = " << price << std::endl;

    int tmp = 5;
    // 에러 발생, ?: 연산자보다 << 연산자의 우선순위가 높다.
    // std::cout << (tmp % 2 == 0) ? "even" : "odd" << std::endl;
    
    return 0;
}