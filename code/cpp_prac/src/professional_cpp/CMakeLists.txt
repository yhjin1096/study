cmake_minimum_required(VERSION 3.0.2)
project(professional_cpp)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES professional_cpp
 CATKIN_DEPENDS roscpp
 DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(${PROJECT_NAME}_node
              src//ch1/ch1.cpp)
add_executable(employee_test
              src/ch1/ch1_Employee.cpp
              src/ch1/ch1_EmployeeTest.cpp)

add_executable(1_memory
              src/ch7/1_memory.cpp)
add_executable(2_smart_pointer
              src/ch7/2_smart_pointer.cpp)

link_libraries(
  ${catkin_LIBRARIES}
)