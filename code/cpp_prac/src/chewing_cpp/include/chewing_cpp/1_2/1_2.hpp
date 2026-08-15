#include <iostream>
namespace {
int only_in_this_file = 0;
void OnlyInThisFile() {std::cout << only_in_this_file << std::endl;}
}