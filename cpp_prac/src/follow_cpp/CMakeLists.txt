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

add_executable(2_2 src/2_2/main.cpp)
add_executable(2_3 src/2_3/main.cpp)
add_executable(2_9 src/2_9/main.cpp)
add_executable(3_4 src/3_4/main.cpp)
add_executable(4_2 src/4_2/main.cpp)


# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )