cmake_minimum_required(VERSION 3.0.2)
project(cpp_refer)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

catkin_package(
 INCLUDE_DIRS include
 LIBRARIES cpp_refer
 CATKIN_DEPENDS roscpp
 DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(unique_ptr
              src//memory_management_library/unique_ptr.cpp)

add_executable(shared_ptr
              src//memory_management_library/shared_ptr.cpp)

add_executable(weak_ptr
              src//memory_management_library/weak_ptr.cpp)

link_libraries(
  ${catkin_LIBRARIES}
)

target_link_libraries(shared_ptr
  ${catkin_LIBRARIES}
  pthread
)