cmake_minimum_required(VERSION 3.0.2)
project(pgo_toy_example)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/thirdparty/g2o/cmake_modules)

set(G2O_LIBS_DIRS ${PROJECT_SOURCE_DIR}/thirdparty/g2o/build/lib)
set(G2O_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/thirdparty/g2o)
find_package(g2o REQUIRED)

find_package(Eigen3 REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  std_msgs
  visualization_msgs
)

catkin_package(
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${EIGEN3_INCLUDE_DIR}
)

link_directories(${G2O_LIBS_DIRS})

set(G2O_LIBS
    g2o_core 
    g2o_types_sba 
    g2o_types_slam3d
    g2o_solver_csparse 
    g2o_stuff 
    g2o_csparse_extension
)

add_executable(pgo_toy_example
 src/pgo_toy_example_node.cpp
 src/pgo_toy_example.cpp)

 add_executable(pgo_additional_edge
 src/pgo_additional_edge_node.cpp
 src/pgo_additional_edge.cpp)

target_link_libraries(pgo_toy_example
  ${catkin_LIBRARIES}
  ${EIGEN3_LIBS}
  ${G2O_LIBS}
)

target_link_libraries(pgo_additional_edge
  ${catkin_LIBRARIES}
  ${EIGEN3_LIBS}
  ${G2O_LIBS}
)