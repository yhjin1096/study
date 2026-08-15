#include <iostream>
#include <memory>

class Simple
{
    public:
        Simple(){std::cout << "Simple()" << std::endl;};
        Simple(int a, int b){std::cout << "Simple() " << a+b << std::endl;};
        ~Simple(){std::cout << "~Simple()" << std::endl;};

        int num;
        void go(){std::cout << "go" << std::endl;};
        void go(int a){if(a==3) throw a;}
        void setNum(int a) {num = a;}
        void printNum(){std::cout << num << std::endl;}
    private:
};

void processData(Simple* simple)
{
    simple->num = 5;
}
int* my_alloc(int value){return new int {value};}
void my_free(int* p){delete p;}

void useResource(std::weak_ptr<Simple>& weakSimple)
{
    auto resource { weakSimple.lock() };
    if (resource) {
        std::cout << "Resource still alive." << std::endl;
    } else {
        std::cout << "Resource has been freed!" << std::endl;
    }
}


int main(int argc, char** argv)
{
    // unique_ptr 생성
    {
        Simple* sc = new Simple();
        delete sc;
    }
    {
        try{
             Simple* sc = new Simple();
             sc->go(3);
             delete sc; // 해제 안됨
        }
        catch(int exc)
        {
            std::cout << "exception 발생 " << exc << std::endl;
        }
    }
    {
        std::unique_ptr<Simple> ptr = std::make_unique<Simple>();
        ptr->go();
        (*ptr).go();
    }
    {
        std::unique_ptr<Simple> ptr {std::make_unique<Simple>()};
    }
    {
        std::unique_ptr<Simple> ptr = std::make_unique<Simple>(1, 3);
    }
    std::cout << "-------------------" << std::endl;
    // unique_ptr 사용
    {
        std::unique_ptr<Simple> ptr {std::make_unique<Simple>()};
        std::cout << ptr.get() << std::endl;
        ptr.get()->setNum(1);
        
        ptr->printNum();
        processData(ptr.get()); // 내부 포인터는 복사 가능
        ptr->printNum();
    }
    {
        std::unique_ptr<Simple> ptr {std::make_unique<Simple>()};
        ptr.reset(); // 내부 포인터 해제, ~Simple()
        ptr.reset(new Simple(1,6)); // 내부 포인터 헤제 후 재할당
    }
    {
        std::unique_ptr<Simple> mySimpleSmartPtr { std::make_unique<Simple>() };
        mySimpleSmartPtr->setNum(10);
        std::cout << mySimpleSmartPtr.get() << std::endl;
        std::cout << mySimpleSmartPtr->num << std::endl;

        Simple* simple {mySimpleSmartPtr.release()};
        std::cout << mySimpleSmartPtr.get() << std::endl;
        std::cout << simple << std::endl;
        std::cout << simple->num << std::endl;

        delete simple;
        std::cout << simple << std::endl;
        
        simple = nullptr;
        std::cout << simple << std::endl;
    }
    {
        std::unique_ptr<int[]> mySimpleSmartPtr { std::make_unique<int[]>(10) };
        mySimpleSmartPtr[2] = 123;
        std::cout << mySimpleSmartPtr[0] << "," << mySimpleSmartPtr[1] << "," << mySimpleSmartPtr[2] << std::endl;
    }
    {
        // <int, decltype(&my_free)> -> <내부 포인터 타입, 사용자 정의 삭제자 타입>
        // decltype(&my_free)는 void (*)(int*) 타입을 반환
        // my_free는 pointer가 삭제될 때 실행되는 함수
        std::unique_ptr<int, decltype(&my_free)> myIntSmartPtr(my_alloc(42), my_free);
    }
    std::cout << "-------------------" << std::endl;
    // shared_ptr
    {
        Simple* mySimple {new Simple()}; // 생성
        std::shared_ptr<Simple> smartPtr1 {mySimple}; // 스코프 벗어나 삭제
        // std::shared_ptr<Simple> smartPtr2 {mySimple}; // 스코프 벗어나 삭제, 에러
    }
    {
        std::shared_ptr<Simple> ptr {std::make_shared<Simple>()};
        ptr->setNum(10);
        
        std::cout << ptr.use_count() << std::endl;

        //std::shared_ptr<int> aliasing {std::shared_ptr<int>{ptr, &ptr->num}};
        //std::shared_ptr<int> aliasing {소유권을 공유한 포인터, 실제 가리킬 객체};
        std::shared_ptr<int> aliasing {ptr, &ptr->num};

        std::cout << ptr.use_count() << std::endl;
        std::cout << aliasing.use_count() << std::endl;
        
        ptr->printNum();
        std::cout << *aliasing.get() << std::endl;
    }
    std::cout << "-------------------" << std::endl;
    // weak_ptr
    {
        std::shared_ptr<Simple> sharedSimple {std::make_shared<Simple>()};
        std::weak_ptr<Simple> weakSimple {sharedSimple};

        useResource(weakSimple);
        sharedSimple.reset();
        useResource(weakSimple);
    }
    return 0;
}