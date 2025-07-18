cmake_minimum_required(VERSION 3.0.2)
project(follow_cpp)

set(CMAKE_CXX_STANDARD 17)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES follow_cpp
#  CATKIN_DEPENDS roscpp
#  DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(follow_2_2 src/2_2/main.cpp) # integers
add_executable(follow_2_3 src/2_3/main.cpp) # fixed-width integers, 멀티 플랫폼 개발시 자주 사용
add_executable(follow_2_4 src/2_4/main.cpp) # void pointer
add_executable(follow_2_9 src/2_9/main.cpp) # 심볼릭 상수(const)

add_executable(follow_3_4 src/3_4/main.cpp) # 쉼표 연산자, 삼항 연산자

add_executable(follow_4_2 src/4_2/main.cpp) # static variable - internal linkage
add_executable(follow_4_2_2 src/4_2/main2.cpp # global variable - external linkage
                            src/4_2/test.cpp
                            src/4_2/MyConstraint.cpp)
add_executable(follow_4_4 src/4_4/main.cpp) # auto
add_executable(follow_4_5 src/4_5/main.cpp) # 형변환
add_executable(follow_4_8 src/4_8/main.cpp) # enum class

add_executable(follow_6_13 src/6_13/main.cpp) # 포인터와 const
add_executable(follow_6_18 src/6_18/main.cpp) # void pointer

add_executable(follow_7_6 src/7_6/main.cpp) # inline 함수
add_executable(follow_7_9 src/7_9/main.cpp) # 함수 포인터

add_executable(follow_8_2 src/8_2/main.cpp) # 캡슐화(encapsulation), 접근 지정자(access specifier), 접근 함수(access function)
add_executable(follow_8_10 src/8_10/main.cpp) # 정적 멤버 변수
add_executable(follow_8_11 src/8_11/main.cpp) # 정적 멤버 함수
add_executable(follow_8_12 src/8_12/main.cpp) # 친구 함수와 클래스 friend
add_executable(follow_8_12_2 src/8_12/main2.cpp) # 친구 함수와 클래스 friend
add_executable(follow_8_13 src/8_13/main.cpp) # 익명 객체
add_executable(follow_8_13_2 src/8_13/main2.cpp) # 익명 객체

add_executable(follow_9_1 src/9_1/main.cpp) # 산술 연산자 오버로딩

# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )