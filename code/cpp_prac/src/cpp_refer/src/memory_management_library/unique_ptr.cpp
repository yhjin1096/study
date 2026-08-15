#include <cpp_refer/memory_management_library/memory_management_library.hpp>

//런타임 다형성을 위한 helper class 데모
struct B
{
    virtual ~B() = default;
    virtual void bar() {std::cout << "B::bar\n";}
};

struct D : B{
    D() {std::cout << "D::D\n";}
    ~D() {std::cout << "D::~D\n";}

    void bar() override {std::cout << "D::bar\n";}
};

std::unique_ptr<D> pass_through(std::unique_ptr<D> p)
{
    p->bar();
    return p;
}

//custom deleter
void close_file(std::FILE* fp){std::fclose(fp);}

struct List
{
    struct Node
    {
        int data;
        std::unique_ptr<Node> next;
    };
    std::unique_ptr<Node> head;
    ~List()
    {
        while(head)
        {
            auto next = std::move(head->next);
            head = std::move(next);
        }
    }
    void push(int data)
    {
        head = std::unique_ptr<Node>(new Node{data, std::move(head)});
    }
};

int main(int argc, char** argv)
{
    std::cout << "1) unique_ptr 소유권 데모" << std::endl;
    {
        std::unique_ptr<D> p = std::make_unique<D>();
        //p의 소유권을 q에게 이전
        //p는 nullptr
        std::unique_ptr<D> q = pass_through(std::move(p));
        assert(!p);
    }
    std::cout << "2) runtime 다형성(polymorphism) demo" << std::endl;
    {
        std::unique_ptr<B> p = std::make_unique<D>();
        p->bar();
    }
    std::cout << "3) Custom delter" << std::endl;
    std::ofstream("demo.txt") << "x";
    {
        std::unique_ptr<std::FILE, decltype(&close_file)> fp(std::fopen("demo.txt","r"), &close_file);
        if(fp)
            std::cout << char(std::fgetc(fp.get())) << std::endl;
    }
    std::cout << "4) lambda 표현 방식의 Custom deleter" << std::endl;
    try
    {
        std::unique_ptr<D, void(*)(D*)> p(new D, [](D* ptr){
            std::cout << "destroying from a custom deleter" << std::endl;
            delete ptr;
        });
        // D* ptr = new D;
        throw std::runtime_error(""); //p가 일반 포인터라면 아래에서 leak 발생
        // delete ptr;
    }
    catch(const std::exception& e)
    {
        std::cerr << "catch exception" << std::endl;
    }
    std::cout << "5) Array 형태의 unique_ptr" << std::endl;
    {
        std::unique_ptr<D[]> ptr(new D[3]);
    }
    std::cout << "6) linked list" << std::endl;
    {
        List wall;
        const int enough{1'000'000};
        for(int beer = 0; beer != enough; ++beer)
            wall.push(beer);
            
        std::cout.imbue(std::locale("en_US.UTF-8"));
        std::cout << enough << " bottles of beer on the wall...\n";
    }
    
    return 0;
}