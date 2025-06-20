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


# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )