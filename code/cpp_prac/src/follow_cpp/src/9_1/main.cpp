#include <iostream>

/* 산술연산자 없는 버전*/
/*
class Cents
{
    private:
        int m_cents;
    public:
        Cents(int cents = 0)
        {
            m_cents = cents;
        }
        int getCents() const
        {
            return m_cents;
        }
        int& getCents()
        {
            return m_cents;
        }
};

void add(const Cents& c1, const Cents& c2, Cents& c_out)
{
    c_out.getCents() = c1.getCents() + c2.getCents();
}

int main(int argc, char* argv[])
{
    Cents cents1(6);
    Cents cents2(8);
    Cents sum;

    add(cents1, cents2, sum);
    std::cout << sum.getCents() << std::endl;

    return 0;
}
*/

class Cents
{
    private:
        int m_cents;
    public:
        Cents(int cents = 0)
        {
            m_cents = cents;
        }
        int getCents() const
        {
            return m_cents;
        }
        int& getCents()
        {
            return m_cents;
        }
        Cents operator+(const Cents& c2) const
        {
            return Cents(this->m_cents + c2.m_cents);
        }
};

int main(int argc, char* argv[])
{
    Cents cents1(6);
    Cents cents2(8);

    std::cout << (cents1 + cents2 + Cents(10)).getCents() << std::endl;

    return 0;
}