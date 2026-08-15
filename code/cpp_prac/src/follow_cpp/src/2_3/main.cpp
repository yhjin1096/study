#include <iostream>

int main(int argc, char **argv)
{
    // fixed-width integers
    std::int8_t i8 = 1; // 1byte = 8bit
    std::int16_t i16 = 1; // 2byte = 16bit
    std::int32_t i32 = 1; // 4byte = 32bit
    std::int64_t i64 = 1; // 8byte = 64bit
    std::int_fast8_t i_fast8 = 1; // 1byte = 8bit
    std::int_fast16_t i_fast16 = 1; // 2byte = 16bit
    std::int_fast32_t i_fast32 = 1; // 4byte = 32bit
    std::int_fast64_t i_fast64 = 1; // 8byte = 64bit
    std::int_least8_t i_least8 = 1; // 1byte = 8bit
    std::int_least16_t i_least16 = 1; // 2byte = 16bit
    std::int_least32_t i_least32 = 1; // 4byte = 32bit
    std::int_least64_t i_least64 = 1; // 8byte = 64bit
    
    std::cout << "i8 = " << i8 << ", sizeof(i8) = " << sizeof(i8) << std::endl;
    std::cout << "i16 = " << i16 << ", sizeof(i16) = " << sizeof(i16) << std::endl;
    std::cout << "i32 = " << i32 << ", sizeof(i32) = " << sizeof(i32) << std::endl;
    std::cout << "i64 = " << i64 << ", sizeof(i64) = " << sizeof(i64) << std::endl;
    std::cout << "i_fast8 = " << i_fast8 << ", sizeof(i_fast8) = " << sizeof(i_fast8) << std::endl;
    std::cout << "i_fast16 = " << i_fast16 << ", sizeof(i_fast16) = " << sizeof(i_fast16) << std::endl;
    std::cout << "i_fast32 = " << i_fast32 << ", sizeof(i_fast32) = " << sizeof(i_fast32) << std::endl;
    std::cout << "i_fast64 = " << i_fast64 << ", sizeof(i_fast64) = " << sizeof(i_fast64) << std::endl;
    std::cout << "i_least8 = " << i_least8 << ", sizeof(i_least8) = " << sizeof(i_least8) << std::endl;
    std::cout << "i_least16 = " << i_least16 << ", sizeof(i_least16) = " << sizeof(i_least16) << std::endl;
    std::cout << "i_least32 = " << i_least32 << ", sizeof(i_least32) = " << sizeof(i_least32) << std::endl;
    std::cout << "i_least64 = " << i_least64 << ", sizeof(i_least64) = " << sizeof(i_least64) << std::endl;

    return 0;
}