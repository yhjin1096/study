cmake_minimum_required(VERSION 3.0.2)
project(local_ba_g2o)

add_definitions(-DPROJECT_SOURCE_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}\")

set(tinycolormap_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/thirdparty/tinycolormap/include)

find_package(g2o REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)
find_package(PCL 1.8 REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  sensor_msgs
  pcl_ros
  pcl_conversions
  tf2_ros
  geometry_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES local_ba_g2o
#  CATKIN_DEPENDS roscpp sensor_msgs pcl_ros pcl_conversions tf2_ros geometry_msgs
#  DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${G2O_INCLUDE_DIR}
  ${EIGEN3_INCLUDE_DIR}
  ${OpenCV_INCLUDE_DIRS}
  ${tinycolormap_INCLUDE_DIR}
  ${PCL_INCLUDE_DIRS}
)

link_directories(${G2O_LIBS_DIRS})

set(G2O_LIBS
    g2o_core 
    g2o_types_sba 
    g2o_types_slam3d
    g2o_solver_csparse 
    g2o_solver_dense
    g2o_solver_eigen
    g2o_stuff 
    g2o_csparse_extension
    g2o_solver_cholmod
)

add_executable(${PROJECT_NAME}_node src/main.cpp)

target_link_libraries(${PROJECT_NAME}_node
  ${catkin_LIBRARIES}
  ${G2O_LIBS}
  ${EIGEN3_LIBS}
  ${OpenCV_LIBS}
  ${PCL_LIBRARIES}
)

