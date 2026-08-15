#include <iostream>
#include <limits>
#include <array>
#include <vector>

void TestFunction()
{
    std::cout << "test function" << std::endl;
    std::cout << __func__ << std::endl; // log를 남기는 용도
}
int addNumbers(int num1, int num2)
{
    return num1+num2;
}
double addNumbers(double num1, double num2)
{
    return num1+num2;
}
class Demo
{
    public:
        int get(){return 5;}
};
int get(){return 10;}
namespace NS{ int get() {return 20;}}
struct CircleStruct
{
    int x, y;
    double radius;
};
class CircleCalss
{
    public:
        CircleCalss(int x, int y, double radius)
            : m_x {x}, m_y {y}, m_radius {radius}{}
    // private:
        int m_x, m_y;
        double m_radius;
};
void mysteryFunction(const std::string* someString)
{
    // *someString = "Test"; // error
}
class AirlineTicket
{
    public:
        void ChangeName() const
        {
            // name = "not yun"; //error
        }
    private:
        std::string name = "yun";
};

const int getArraySize() { return 32;};
constexpr int getArraySize2() { return 32;};

class MyClass
{
    public:
        MyClass(int& ref) : m_ref {ref}{};
    private:
        int& m_ref;
};
const std::string message{"Test"};
const std::string& foo(){return message;};


int main(int argc, char** argv)
{
    // 71p 숫자 경계값
    // #include <limits>
    std::cout << "71p 숫자 경계값" << std::endl;
    std::cout << std::numeric_limits<int>::min() << std::endl;
    std::cout << std::numeric_limits<int>::max() << std::endl;

    // zero initializer
    // = -> copy initializer
    // {} -> uniform initializer
    // pointer는 null로 초기화
    // 장점: int num {4.5};의 경우 축소 변환(narrowing conversions)이 필요 -> 프로그램 실행 안됨(오류 발생)
    std::cout << "initializer" << std::endl;
    int zero_initializer {};
    int uniform_initializer {10};
    std::cout << zero_initializer << "," << uniform_initializer << std::endl;

    // 72p cast(동적 형변환)
    // 변수 타입 변경 3가지 방법
    std::cout << "cast(동적 형변환)" << std::endl;
    float myFloat = 3.54;
    int i1 = (int)myFloat; // 피해야할 방식
    int i2 = int(myFloat); // 거의 사용하지 않음
    int i3 = static_cast<int>(myFloat); // 가장 명시적, 권장하는 방식
    std::cout << i1 << "," << i2 << "," << i3 << std::endl;

    // 91p 현재 함수 이름
    std::cout << "현재 함수 이름" << std::endl;
    TestFunction();

    // 함수 오버로딩
    // 함수 이름은 같지만 매개변수 구성은 다른 함수
    // __func__ 로 구분 불가
    std::cout << "함수 오버로딩" << std::endl;
    std::cout << addNumbers(1, 2) << std::endl;
    std::cout << addNumbers(1.1, 2.1) << std::endl;

    // 98p std::array, 정적 배열
    std::cout << "std::array, 정적 배열" << std::endl;
    std::array<int, 3> arr = {0,  9,  8};
    std::cout << arr.size() << std::endl;
    std::cout << arr[0] << "," << arr[1] << "," << arr[2] << std::endl;

    // 99p std::vector, 동적 배열
    std::cout << "std::vector, 동적 배열" << std::endl;
    std::vector<int> myVector = {0,1,2};
    myVector.push_back(3);

    // 100p, std::pair
    std::cout << "100p, std::pair" << std::endl;
    std::pair<double, int> myPair = {1.23, 5};
    std::cout << myPair.first << "," << myPair.second << std::endl;

    // 101p, std::optional //c++17

    // 102p, 구조적 바인딩(structed binding)
    std::cout << "102p, 구조적 바인딩(structed binding)" << std::endl;
    auto [theDouble, theInt] {myPair};
    std::cout << theDouble << "," << theInt << std::endl;

    // 105p 범위 기반 for문
    // 모든 원소에 대한 복제본 출력
    // 단점: 반복 배열의 접근 index가 없다, 모든 배열을 처음부터 끝까지 탐색해야한다.
    // 반복문 속도 비교: https://blog.naver.com/PostView.naver?blogId=remocon33&logNo=221701119330
    std::cout << "범위 기반 for문" << std::endl;
    std::array<int, 4> arr2 {1, 2, 3, 4};
    for(int i : arr2) {std::cout << i << std::endl;}
    std::vector<int> vec(3, -1);
    for(int i : vec) {std::cout << i << std::endl;} //복사
    for(auto& i : vec) {std::cout << i << std::endl;} //레퍼런스, 원본
    for(const auto& i : vec) {std::cout << i << std::endl;} //원본 수정 불가

    // p112 scope
    std::cout << "scope" << std::endl;
    Demo d;
    std::cout << d.get() << std::endl;
    std::cout << NS::get() << std::endl; // ::은 scope 지정 연산자
    std::cout << ::get() << std::endl;
    std::cout << get() << std::endl; // global scope

    // p115 균일 초기화(초기화 방식 통일)
    std::cout << "균일 초기화(초기화 방식 통일)" << std::endl;
    // 이전 방식
    CircleStruct myCircle1 = {10, 10, 2.5};
    CircleCalss myCircle2(10, 10, 2.5);
    // 현재 방식
    CircleStruct myCircle3 {10, 10, 2.5};
    CircleCalss myCircle4 {10, 10, 2.5};
    std::cout << myCircle1.x << "," << myCircle2.m_x << "," << myCircle3.x << "," << myCircle4.m_x << std::endl;

    // p119~
    // pointer, stack, free store
    // pointer의 null 값은 nullptr, NULL은 0과 같다
    std::cout << "pointer, stack, free store" << std::endl;
    int* myIntPointer = new int;
    int* myIntArrPointer = {new int[8]};
    delete myIntPointer;
    delete[] myIntArrPointer;

    // p124~ const의 다양한 용도
    std::cout << "const의 다양한 용도" << std::endl;
    // const 상수
        // c++에서 const는 상수로도 쓰인다(c에서 #define의 역할)
        // const는 바로 왼쪽에 나온 대상에 적용된다고 보면 된다.
            // const pointer
            const int* ip; // ip가 가리키는 값 변경 불가 == int const* ip
            int* const ip2 {nullptr}; // pointer 변수 자체 변경 불가 -> 초기화 반드시 해야함 -> int* const ip2 {new int[10]};
            int const* const ip3 {nullptr}; // 가리키는 값, 포인터 자체 변경 불가 == const int* const ip3 {nullptr};
            ip = new int[10];
            // ip2 = new int[10]; // error
            // ip[4] = 5; // error
            // ip2[4] = 5;
            
            // const 매개변수
            // 비 const 변수를 const 변수로 캐스트할 수 있다.
            std::string myString {"The string"};
            // mysteryFunction(&myString);

    // p128 const 메서드
    std::cout << "const 메서드" << std::endl;
        // class의 데이터 멤버를 수정할 수 없다.
        // class AirlineTicket 참고

    // p132 레퍼런스 변수
    std::cout << "레퍼런스 변수" << std::endl;
    // 변수 타입 뒤에 & 연산자, 원본 변수에 대한 포인터로 취급
    // xRef는 x에 대한 별명(alias)이다.
    // 값은 변경 가능하지만 가리키는 변수를 변경할 수는 없다.
    int x{3}, y{4};
    int& xRef{x}; // 초기화 필수

        // const 레퍼런스
        const int& yRef{y};
        // yRef = 5; // error
        y = 5;
        // 이름 없는 값 -> 레퍼런스 X, const 값 -> 레퍼런스 O
        // int& unnamedRef1{5}; //error
        const int& unnamedRef2{5};

        // pointer 레퍼런스
        int* intP{nullptr};
        int*& ptrRef{intP};
        ptrRef = new int;
        *ptrRef = 5;
        std::cout << *intP << "," << *ptrRef << std::endl;

        // p136 레퍼런스 데이터 멤버
        std::cout << "레퍼런스 데이터 멤버" << std::endl;
        // 레퍼런스는 가리키는 대상이 되는 변수 없이 존재할 수 없다. -> class내의 레퍼런스 멤버 변수는 반드시 생성자 초기자에서 초기화해야 한다.
        // MyClass 참고

        // 레퍼런스 매개변수
        // 효율: 객체 복사 과정이 없어 효율적, 지원: ㄱ밧 전달 방식을 허용하지 않는 클래스가 있다.

    // p149 타입 앨리어스(type alias)
    std::cout << "타입 앨리어스(type alias)" << std::endl;
    // typedef와 동일한 역할
    using IntPtr = int*;
    IntPtr p1; // == int* p1;

    // p151 타입 추론(type inference)
    std::cout << "타입 추론(type inference)" << std::endl;
    // 표현식의 타입을 컴파일러가 스스로 알아내는 기능, auto, decltype
        // auto: 컴파일시 타입을 자동으로 추론할 변수 앞에 붙인다.
        // auto는 const와 레퍼런스를 지운다. -> 지정을 따로 해줘야한다.
        auto x2 {123};
        auto f1{foo()}; // const, 레퍼런스 지워짐
        const auto& f2{foo()}; 

        // decltype: 인수로 전달한 표현식의 타입을 알아낸다.
        // const, 레퍼런스를 지우지 않는다.
        decltype(x2) y2{456};
        decltype(foo()) f3{foo()};

    // p172~

    return 0;
}