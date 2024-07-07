#include <iostream>
#include <cstring>
class string
{
    char *str;
    int len;

    public:
    
        string(char c, int n)
        {// 문자 c 가 n 개 있는 문자열로 정의
            str = new char[n+1];
            for(int i = 0; i < n; i++)
            {
                str[i] = static_cast<char>(i+97);
            }
            len = 10;
        } ; 
        string(const char *s) 
        {
            // s는 원본 pointer 변수의 복사본, 같은 주소를 가리키므로 const가 아니면 값은 변경 가능
            // 원본 pointer가 가리키는 주소는 변경 불가
            len = 0;

            while(*s)
            {
                len++;
                s++;
                // std::cout <<static_cast<void*>(&s[0]) << std::endl; // const라 cast 안됨
                printf("%p\n", &s[0]);
                std::cout << s << std::endl;
            }
            s-=len;

            str = new char[len];
            strcpy(str, s);
        };
        string(const string &s);
        ~string(){};

        char* get_string(){return str;}
        void add_string(const string &s)
        {
            // str 뒤에 s 를 붙인다.
            char* tmp = new char(len + s.len);
            strcpy(tmp, str);
            for(int i = len; i < len+s.len; i++)
            {
                tmp[i] = s.str[i - len];
            }
        }   
        void copy_string(const string &s);  // str 에 s 를 복사한다.
        int strlen(){return len;}                       // 문자열 길이 리턴
};

int main(int argc, char** argv)
{
    string str('c', 10);
    string str2(str.get_string());
    str.add_string(str2.get_string());


    // char* str = new char[10];
    // std::cout << static_cast<void*>(&str[0]) << std::endl;
    // printf("%p\n", &str[0]);

    return 0;
}