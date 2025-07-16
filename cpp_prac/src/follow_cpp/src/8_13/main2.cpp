#include <iostream>

class Cents
{
    private:
        int m_cents;
    public:
        Cents(int cents)
        {
            m_cents = cents;
        }
        int getCents() const
        {
            return m_cents;
        }
};

// const로 선언하지 않으면 erro 발생한다.
// error: cannot bind non-const lvalue reference of type ‘Cents&’ to an rvalue of type ‘Cents’
Cents add(const Cents& c1, const Cents& c2)
{
    return Cents(c1.getCents() + c2.getCents());
}

int main(int argc, char* argv[])
{
    std::cout << add(Cents(6), Cents(8)).getCents() << std::endl;
    std::cout << int(6) + int(8) << std::endl;

    return 0;
}