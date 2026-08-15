#include "chewing_cpp/4_5/MyString.hpp"

void DoSomethingWithString(MyString s)
{
  // Do something...
  s.println();
};

class A {
    private:
        mutable int data_;

    public:
        A(int data) : data_(data) {}
        void DoSomething(int x) const {
            data_ = x;  // 가능!
        }

    void PrintData() const { std::cout << "data: " << data_ << std::endl; }
};

int main(int argc, char** argv)
{
    {
        MyString s(3);
    }
    {
        DoSomethingWithString(MyString("abc"));
        DoSomethingWithString("abc"); //암시적 변환(implicit conversion)
    }
    {
        //암시적 변환 막기 - explicit
        DoSomethingWithString(MyString('c'));
        // DoSomethingWithString('c');
    }
    {
        MyString s(5);
        // MyString ss = 5;
    }
    ///////////////////////////////////////////////////
    {
        A a(10);
        a.PrintData();
        a.DoSomething(3);
        a.PrintData();
    }
    return 0;
}