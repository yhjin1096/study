#include <iostream>

inline int min(int a, int b)
{
    return a<b ? a : b;
}

int main()
{
    // 1. 함수 호출
    // 2. 지역변수 a, b 생성
    // 3. argument 값 복사 후 전달
    // 4. 두 값 비교 후 작은 값 반환
    // 5. 반환된 값을 출력
    // -> 이런 작은 함수가 많이 호출되는 경우 1~3번 과정이 4번 과정보다 오래 걸리는 경우가 있음
    // -> inline 함수를 사용하면 컴파일 시 함수 호출 부분에 함수 본문을 그대로 삽입하여 오버헤드를 줄일 수 있음
    std::cout << min(1,2) << std::endl;
    std::cout << min(3,2) << std::endl;

    // inline 함수 사용시 컴파일러는 아래와 같이 최적화 함
    // 컴파일러가 최적화하기 좋은 함수라고 하면 최적화 한다.
    // 최신 컴파일러는 inline으로 최적화하지 않아도 자동으로 최적화 한다.
    std::cout << (1<2 ? 1 : 2) << std::endl;
    std::cout << (3<2 ? 3 : 2) << std::endl;

    return 0;
}