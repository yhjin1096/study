#include <cpp_refer/memory_management_library/memory_management_library.hpp>

std::weak_ptr<int> gw;

void observe()
{
    std::cout << "gw.use_count() == " << gw.use_count() << "; ";
    
    if(std::shared_ptr<int> spt = gw.lock())
        std::cout << "*spt == " << *spt << '\n';
    else
        std::cout << "gw is expired\n";
}

int main(int argc, char** argv)
{
    {
        auto sp = std::make_shared<int>(42);
        gw = sp;
        observe();
    }// scope 벗어나 해제
    observe();

    return 0;
}