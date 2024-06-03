#include <iostream>
#include <professional_cpp/ch1/ch1_Employee.hpp>

using namespace Records;

int main(int argv, char** argc)
{
    std::cout << "Testing the Employee class." << std::endl;
    Employee emp{"Jane", "Doe"};
    emp.setFirstName("John");
    emp.setLastName("Doe");
    emp.setEmployeeNumber(71);
    emp.setSalary(50000);
    emp.promote();
    emp.promote(50);
    emp.hire();
    emp.display();
    return 0;
}