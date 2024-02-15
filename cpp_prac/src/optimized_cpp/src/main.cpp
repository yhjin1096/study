#include <iostream>
#include <time.h>
#include <math.h>

int main()
{
    clock_t start, end;
    double time_result;

    double x = 3.5, y = 2.3, angle = M_PI;
    double x1, y1;
    
    start = clock();

    for (int i = 0; i < 30000; i++)
    {
        
        x1 = x * cos(angle) - y * sin(angle);
        y1 = x * cos(angle) + y * sin(angle);
    }

    end = clock();
    time_result = (double)(end - start);
    printf("(%lf, %lf) -> (%lf, %lf), %lfms \n", x, y, x1, y1, time_result);

//-----------------------------------------------------//

    start = clock();

    const double Cos = cos(angle);
    const double Sin = sin(angle);

    for (int i = 0; i < 30000; i++)
    {   
        x1 = x * Cos - y * Sin;
        y1 = x * Cos + y * Sin;
    }

    end = clock();
    time_result = (double)(end - start);
    printf("(%lf, %lf) -> (%lf, %lf), %lfms \n", x, y, x1, y1, time_result);

    return 0;
}