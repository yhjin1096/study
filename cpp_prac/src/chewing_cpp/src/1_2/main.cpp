#include "chewing_cpp/1_2/1_2.hpp"

// namespace {
// int only_in_this_file = 0;
// void OnlyInThisFile() {std::cout << only_in_this_file << std::endl;}
// }

int main(int argc, char** argv)
{
    only_in_this_file = 3;
    OnlyInThisFile();
    return 0;
}