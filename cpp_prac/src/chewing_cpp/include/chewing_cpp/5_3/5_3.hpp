#include <iostream>

class Array
{
    private:
        const int dim; // 몇 차원 배열?
        int* size; // size[0]*size[1]*...*size[dim-1]의 크기, [숫자]는 레벨

        struct Address
        {
            int level; 
            void* next; // dim-1 레벨은 int를 가리키고, 그 외의 레벨은 다음 Address 배열을 가리킨다.
        };

        Address* top;
    public:
        Array(int dim, int* array_size) : dim(dim)
        {
            size = new int[dim];
            for(int i = 0; i < dim; i++)
            {
                size[i] = array_size[i];
            }
        }
};