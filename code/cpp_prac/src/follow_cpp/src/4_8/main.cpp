#include <iostream>

enum Color
{
    RED,
    GREEN,
    BLUE
};

enum Fruit
{
    APPLE,
    BANANA,
    ORANGE
};

enum class Color2
{
    RED,
    GREEN,
    BLUE
};

enum class Fruit2
{
    APPLE,
    BANANA,
    ORANGE
};

int main()
{
    Color color = RED;
    Fruit fruit = APPLE;
    if(color == fruit)
    {
        std::cout << color << "==" << fruit << std::endl;
    }

    Color2 color2 = Color2::RED;
    Fruit2 fruit2 = Fruit2::APPLE;
    // if(color2 == fruit2) // 컴파일 에러
}