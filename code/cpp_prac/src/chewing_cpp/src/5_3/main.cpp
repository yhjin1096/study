#include "chewing_cpp/5_3/5_3.hpp"

int main(int argc, char** argv)
{
    {
        int** arr;
        arr = new int*[3];
        for(int i = 0; i < 3; i++)
            arr[i] = new int[5];
    }
    return 0;
}