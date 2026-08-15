#include <iostream>
#include <cstring>

class A
{
    private:
        void private_func() {std::cout << private_num << std::endl;}
        int private_num;

        // B 는 A 의 친구!
        friend class B;
        // func 은 A 의 친구!
        friend void func();
};

class B
{
    public:
        B()
        {
            A a;
            a.private_num = 3;
            a.private_func();
        }
};
void func() {
  A a;
  a.private_num = 2;
  a.private_func();
}

class Complex {
 private:
  double real, img;

  double get_number(const char* str, int from, int to) const;

 public:
  Complex(double real, double img) : real(real), img(img) {}
  Complex(const Complex& c) { real = c.real, img = c.img; }
  Complex(const char* str);

//   Complex operator+(const Complex& c) const;
  Complex& operator=(const Complex& c);

  // 나머지 연산자 함수들은 생략 :)

  void println() {
    std::cout << "( " << real << " , " << img << " ) " << std::endl;
  }

  // 이제 이 함수는 Complex 의 private 멤버 변수들에 접근할 수 있습니다.
  friend Complex operator+(const Complex& a, const Complex& b);
  friend std::ostream& operator<<(std::ostream& os, const Complex&c);
};

Complex operator+(const Complex& a, const Complex& b) {
  Complex temp(a.real + b.real, a.img + b.img);
  return temp;
}

std::ostream& operator<<(std::ostream& os, const Complex&c)
{
   os << "( " << c.real << " , " << c.img << " ) ";
   return os;
}

Complex::Complex(const char* str) {
  // 입력 받은 문자열을 분석하여 real 부분과 img 부분을 찾아야 한다.
  // 문자열의 꼴은 다음과 같습니다 "[부호](실수부)(부호)i(허수부)"
  // 이 때 맨 앞의 부호는 생략 가능합니다. (생략시 + 라 가정)

  int begin = 0, end = strlen(str);
  img = 0.0;
  real = 0.0;

  // 먼저 가장 기준이 되는 'i' 의 위치를 찾는다.
  int pos_i = -1;
  for (int i = 0; i != end; i++) {
    if (str[i] == 'i') {
      pos_i = i;
      break;
    }
  }

  // 만일 'i' 가 없다면 이 수는 실수 뿐이다.
  if (pos_i == -1) {
    real = get_number(str, begin, end - 1);
    return;
  }

  // 만일 'i' 가 있다면,  실수부와 허수부를 나누어서 처리하면 된다.
  real = get_number(str, begin, pos_i - 1);
  img = get_number(str, pos_i + 1, end - 1);

  if (pos_i >= 1 && str[pos_i - 1] == '-') img *= -1.0;
}
double Complex::get_number(const char* str, int from, int to) const {
  bool minus = false;
  if (from > to) return 0;

  if (str[from] == '-') minus = true;
  if (str[from] == '-' || str[from] == '+') from++;

  double num = 0.0;
  double decimal = 1.0;

  bool integer_part = true;
  for (int i = from; i <= to; i++) {
    if (isdigit(str[i]) && integer_part) {
      num *= 10.0;
      num += (str[i] - '0');
    } else if (str[i] == '.')
      integer_part = false;
    else if (isdigit(str[i]) && !integer_part) {
      decimal /= 10.0;
      num += ((str[i] - '0') * decimal);
    } else
      break;  // 그 이외의 이상한 문자들이 올 경우
  }

  if (minus) num *= -1.0;

  return num;
}

// Complex Complex::operator+(const Complex& c) const {
//   Complex temp(real + c.real, img + c.img);
//   return temp;
// }

Complex& Complex::operator=(const Complex& c) {
  real = c.real;
  img = c.img;
  return *this;
}

///////////////////////////////////////////////////////////////////////

#include <iostream>
#include <cstring>

class MyString {
  char* string_content;  // 문자열 데이터를 가리키는 포인터
  int string_length;     // 문자열 길이

  int memory_capacity;  // 현재 할당된 용량

 public:
  // 문자 하나로 생성
  MyString(char c);

  // 문자열로 부터 생성
  MyString(const char* str);

  // 복사 생성자
  MyString(const MyString& str);

  ~MyString();

  int length();

  void print() const;
  void println() const;

  char& operator[](const int index);
};

char& MyString::operator[](const int index){
  return string_content[index];
}

MyString::MyString(char c) {
  string_content = new char[1];
  string_content[0] = c;
  memory_capacity = 1;
  string_length = 1;
}
MyString::MyString(const char* str) {
  string_length = strlen(str);
  memory_capacity = string_length;
  string_content = new char[string_length];

  for (int i = 0; i != string_length; i++) string_content[i] = str[i];
}
MyString::MyString(const MyString& str) {
  string_length = str.string_length;
  string_content = new char[string_length];

  for (int i = 0; i != string_length; i++)
    string_content[i] = str.string_content[i];
}
MyString::~MyString() { delete[] string_content; }
int MyString::length() { return string_length; }
void MyString::print() const {
  for (int i = 0; i != string_length; i++) {
    std::cout << string_content[i];
  }
}
void MyString::println() const {
  for (int i = 0; i != string_length; i++) {
    std::cout << string_content[i];
  }
  std::cout << std::endl;
}
///////////////////////////////////////////////
class Int
{
	int data;
	public:
		Int(int data) : data(data) {}
		Int(const Int&  i) : data(i.data) {}

    operator int(){return data;}
};

class Test {
  int x;

 public:
  Test(int x) : x(x) {}
  Test(const Test& t) : x(t.x) {}

  Test& operator++() {
    x++;
    std::cout << "전위 증감 연산자" << std::endl;
    return *this;
  }

  // 전위 증감과 후위 증감에 차이를 두기 위해 후위 증감의 경우 인자로 int 를
  // 받지만 실제로는 아무것도 전달되지 않는다.
  Test operator++(int t) {
    Test temp(*this);
    x++;
    std::cout << "후위 증감 연산자" << std::endl;
    return temp;
  }

  int get_x() const {
    return x;
  }
};

void func(const Test& t) {
  std::cout << "x : " << t.get_x() << std::endl;
}