#include <iostream>
#include <cstring>
class MyString
{
    private:
        char* string_content;
        int string_length;
        int memory_capacity;
    public:
        MyString(char c)
        {
            string_content = new char[1];
            string_content[0] = c;
            string_length = 1;
            memory_capacity = 1;
        }
        MyString(const char* str)
        {
            string_length = strlen(str);
            memory_capacity = string_length;
            string_content = new char[string_length];
            
            for(int i = 0; i != string_length; i++)
                string_content[i] = str[i];
        }
        MyString(const MyString& str) // 복사 생성자
        {
            string_length = str.string_length;
            memory_capacity = str.string_length;
            string_content = new char[string_length];
            
            for(int i = 0; i != string_length; i++)
                string_content[i] = str.string_content[i];
        }
        ~MyString() { delete[] string_content; }

        //class 멤버 변수 변경x -> const(상수) 함수
        int length() const { return string_length; }

        void print() const
        {
            for (int i = 0; i != string_length; i++)
                std::cout << string_content[i];
        }

        void println() const
        {
            for (int i = 0; i != string_length; i++)
                std::cout << string_content[i];
            std::cout << std::endl;
        }

        //assign 함수, = 연산과 동일
        MyString& assign(const MyString& str)
        {
            if(str.length() > memory_capacity)
            {
                delete[] string_content;
                string_content = new char[str.length()];
                memory_capacity = str.string_length;
            }

            for(int i = 0; i != string_length; i++)
                string_content[i] = str.string_content[i];
            
            string_length = str.length();

            return *this;
        }
        MyString& assign(const char* str)
        {
            int str_length = strlen(str);
            if (str_length > memory_capacity)
            {
                delete[] string_content;
                string_content = new char[str_length];
                memory_capacity = str_length;
            }
            for (int i = 0; i != str_length; i++)
                string_content[i] = str[i];
            
            string_length = str_length;
            
            return *this;
        }
        int capacity() { return memory_capacity; }
        void reserve(int size)
        {
            if(size > memory_capacity)
            {
                char* prev_string_content = string_content;
                string_content = new char[size];
                memory_capacity = size;
                for(int i = 0; i != string_length; i++)
                    string_content[i] = prev_string_content[i];
                
                // delete[] prev_string_content;
            }
        }
        char at(int i)
        {
            if(i >= string_length || i <0)
                return NULL;
            else
                return string_content[i];
        }
};

int main(int argc, char** argv)
{
    {
        MyString str1("hello world");
        MyString str2(str1);
        str1.println();
        str2.println();
    }
    {
        // MyString str1("very very very long string");
        // str1.println();
        // str1.assign("short string");
        // str1.println(); // 결과는 short string이지만 실제는 short stringry long string
        // str1.assign("very long string");
        // str1.println();
    }
    {
        MyString str1("very very very long string");
        str1.reserve(30);

        std::cout << "Capacity : " << str1.capacity() << std::endl;
        std::cout << "String length : " << str1.length() << std::endl;
        str1.println();
    }
    return 0;
}