//https://modoocode.com/189
#include <iostream>
int& foo(int& i){return i;};
int foobar(int j){return j;};

class X
{
    private:
        int id;
    public:
        X& X::operator=(const X& rhs) //복사 대입 연산자
        {
            this->id = rhs.id;
            return *this;
        };
};

int main(int argc, char** argv)
{
    {
        int i = 42;
        std::cout << i << std::endl;

        i = 43;            // ok, i 는 좌측값, 43은 우측값
        std::cout << i << std::endl;

        int* p = &i;       //&i 를 쓸 수 있다.
        std::cout << *p << std::endl;

        foo(i) = 42;        // ok, foo() 는 좌측값
        int* p1 = &foo(i);  // ok, &foo() 를 할 수 있다.
        std::cout << *p1 << std::endl;
        //////////////////////
        int j = 0;
        std::cout << j << std::endl;

        j = foobar(j);         // ok. foobar() 는 우측값이다
        std::cout << j << std::endl;

        // int* p2 = &foobar(j);  // error. 우측값의 주소는 참조할 수 없다.    
        j = 42;               // 42 는 우측값이다.
    }
    
    //TODO 12 끝낸 후 다시 보기

    return 0;
}