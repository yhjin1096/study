cmake_minimum_required(VERSION 3.0.2)
project(chewing_cpp)

set(CMAKE_BUILD_TYPE Debug)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES chewing_cpp
 CATKIN_DEPENDS roscpp
 DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(1_2 src/1_2/main.cpp)
add_executable(2_1 src/2_1/main.cpp)

add_executable(4_3
               src/4_3/4_3.cpp
               src/4_3/main.cpp)
add_executable(4_3_mission
              src/4_3/mission.cpp)

add_executable(4_4
              src/4_4/main.cpp
              src/4_4/4_4.cpp)
add_executable(4_4_stub
              src/4_4/stub.cpp)

add_executable(4_5
              src/4_5/main.cpp)

add_executable(4_6
              src/4_6/main.cpp)
         
add_executable(5_1
              src/5_1/main.cpp)
           
add_executable(5_2
               src/5_2/main.cpp)
link_libraries(
  ${catkin_LIBRARIES}
)