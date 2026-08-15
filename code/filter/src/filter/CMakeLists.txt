cmake_minimum_required(VERSION 3.0.2)
project(filter)

find_package(catkin REQUIRED COMPONENTS
  roscpp
)

find_package(OpenCV REQUIRED)

catkin_package(
  # INCLUDE_DIRS include
  # LIBRARIES filter ekf_mouse_tracking
  # CATKIN_DEPENDS roscpp
  # DEPENDS OpenCV
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(kf_mouse_tracking
  src/kalman_filter/kf_mouse_tracking.cpp
  src/kalman_filter/kf_mouse_tracking_example.cpp
)

target_link_libraries(kf_mouse_tracking
  ${catkin_LIBRARIES}
  ${OpenCV_LIBS}
)

add_executable(ekf_mouse_tracking
  src/extended_kalman_filter/ekf_mouse_tracking.cpp
  src/extended_kalman_filter/ekf_mouse_tracking_example.cpp
)

target_link_libraries(ekf_mouse_tracking
  ${catkin_LIBRARIES}
  ${OpenCV_LIBS}
)
