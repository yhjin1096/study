#include "chewing_cpp/4_4/4_4.hpp"

void create_marine() {
    Marine marine3(10, 10, 4);
    // marine3.show_status();
    Marine::show_total_marine();
};

int main(int argc, char** argv)
{
    Marine marine1(2, 3, 5);
    marine1.show_status();
    // Marine::show_total_marine();
    
    Marine marine2(3, 5, 10);
    marine2.show_status();
    // Marine::show_total_marine();

    // create_marine();

    std::cout << std::endl << "마린 1 이 마린 2 를 두 번 공격! " << std::endl;
    marine2.be_attacked(marine1.attack()).be_attacked(marine1.attack());

    marine1.show_status();
    marine2.show_status();

    return 0;
}