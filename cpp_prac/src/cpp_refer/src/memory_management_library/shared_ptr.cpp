#include <cpp_refer/memory_management_library/memory_management_library.hpp>

struct Base
{
    Base() {std::cout << "Base::Base()" << std::endl;}
    ~Base() {std::cout << "Base::~Base()" << std::endl;}
};
struct Derived : public Base //public 상속은 is a 관계, Dervied는 Base이다.
{
    Derived() {std::cout << "Derived::Derived()" << std::endl;}
    ~Derived() {std::cout << "Derived::~Derived()" << std::endl;}
};
void print(auto rem, std::shared_ptr<Base> const& sp)
{
    std::cout << rem << "\n\tget() = " << sp.get() << ", use_count() = " << sp.use_count() << std::endl;
}
void thr(std::shared_ptr<Base> p, int idx)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(987));
    std::shared_ptr<Base> lp = p;
    {
        static std::mutex io_mutex;
        std::lock_guard<std::mutex> lk(io_mutex);
        print("local pointer in a thread:" + std::to_string(idx), lp);
    }
}
void firstExample()
{
    std::shared_ptr<Base> p = std::make_shared<Derived>();
    print("created ad shared Derived(as a pointer to Base)", p);
    
    std::thread t1{thr, p, 1}, t2{thr, p, 2}, t3{thr, p, 3};
    p.reset();
    
    print("Shared ownership between 3 threads and released ownership from main:", p);
    
    t1.join();
    t2.join();
    t3.join();
 
    std::cout << "All threads completed, the last one deleted Derived.\n";
}

struct MyObj
{
    MyObj() {std::cout << "MyObj()" << std::endl;}
    ~MyObj() {std::cout << "~MyObj()" << std::endl;}
};
struct Container : std::enable_shared_from_this<Container>
{
    std::shared_ptr<MyObj> memberObj;
    void CreateMember() { memberObj = std::make_shared<MyObj>();}
    std::shared_ptr<MyObj> GetAsMyObj()
    {
        //std::shared_ptr의 aliasing
        //std::shared_ptr<MyObj>{소유권을 공유한 포인터 - Container, 실제 가리킬 객체 - MyObj};
        //cppreference.com, std::shared_ptr->constructor의 aliasing 참고
        return std::shared_ptr<MyObj>(shared_from_this(), memberObj.get());
    }
};
#define COUT(str) std::cout << '\n' << str << '\n'
#define DEMO(...) std::cout << #__VA_ARGS__ << " = " << __VA_ARGS__ << '\n'
void secondExample()
{
    COUT("Creating shared container");
    std::shared_ptr<Container> cont = std::make_shared<Container>();
    DEMO(cont.use_count()); //1
    DEMO(cont->memberObj.use_count()); //0
 
    COUT("Creating member");
    cont->CreateMember(); //MyObj()
    DEMO(cont.use_count()); //1
    DEMO(cont->memberObj.use_count()); //1
 
    COUT("Creating another shared container");
    std::shared_ptr<Container> cont2 = cont;
    DEMO(cont.use_count()); //2
    DEMO(cont->memberObj.use_count()); //1
    DEMO(cont2.use_count()); //2
    DEMO(cont2->memberObj.use_count()); //1
 
    COUT("GetAsMyObj");
    std::shared_ptr<MyObj> myobj1 = cont->GetAsMyObj();
    DEMO(myobj1.use_count()); //3
    DEMO(cont.use_count()); //3
    DEMO(cont->memberObj.use_count()); //1
    DEMO(cont2.use_count()); //3
    DEMO(cont2->memberObj.use_count()); //1
 
    COUT("Copying alias obj");
    std::shared_ptr<MyObj> myobj2 = myobj1;
    DEMO(myobj1.use_count()); //4
    DEMO(myobj2.use_count()); //4
    DEMO(cont.use_count()); //4
    DEMO(cont->memberObj.use_count()); //1
    DEMO(cont2.use_count()); //4
    DEMO(cont2->memberObj.use_count()); //1
 
    COUT("Resetting cont2");
    cont2.reset();
    DEMO(myobj1.use_count()); //3
    DEMO(myobj2.use_count()); //3
    DEMO(cont.use_count()); //3
    DEMO(cont->memberObj.use_count()); //1
 
    COUT("Resetting myobj2");
    myobj2.reset(); //2
    DEMO(myobj1.use_count()); //2
    DEMO(cont.use_count()); //2
    DEMO(cont->memberObj.use_count()); //1
 
    COUT("Resetting cont");
    cont.reset();
    DEMO(myobj1.use_count()); //1
    DEMO(cont.use_count()); //0
}

int main(int argc, char** argv)
{
    // firstExample();
    secondExample();

    return 0;
}