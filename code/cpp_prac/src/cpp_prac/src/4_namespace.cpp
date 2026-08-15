#include "cpp_prac/header.h"

namespace first_name
{
    void hello()
    {
        std::cout << "first namespace" << std::endl;
    }
}

namespace second_name
{
    void hello()
    {
        std::cout << "second namespace" << std::endl;
    }
}

namespace third_name
{
    void hello();
}
void third_name::hello()
{
    std::cout << "third namespace" << std::endl;
}

int main()
{
    first_name::hello();
    second_name::hello();
    third_name::hello();

    return 0;
}