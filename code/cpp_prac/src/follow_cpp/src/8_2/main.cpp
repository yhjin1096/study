#include <iostream>

class Date
{
    private: // access specifier
        int year_;
        int month_;
        int day_;
    
    public:
        void setDate(const int& year, const int& month, const int& day) // 접근 함수(access function)
        {
            year_ = year;
            month_ = month;
            day_ = day;
        }
        void setMonth(const int& month)
        {
            month_ = month;
        }
        const int& getDay()
        {
            return day_;
        }

        // private 멤버 변수에 접근이 가능하다!
        // -> 외부에서 접근 불가, 같은 class 내에서는 접근 가능
        void copyFrom(const Date& date)
        {
            year_ = date.year_;
            month_ = date.month_;
            day_ = date.day_;
        }
};

// // 다른 class에서는 private 멤버 변수에 접근 불가
// class Test
// {
//     public:
//         void printDate(const Date& date)
//         {
//             std::cout << date.year_ << " " << date.month_ << " " << date.day_ << std::endl;
//         }
// }

int main(int argc, char** argv)
{
    Date today; // Date의 instance 변수(객체)
    today.setDate(2025, 7, 14);
    today.setMonth(10);
    
    Date copy;
    copy.copyFrom(today);

    // Test test;
    // test.printDate(today);
    // test.printDate(copy);

    return 0;
}