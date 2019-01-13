cmake_minimum_required(VERSION 2.8.3)
project(la_madriguera)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  message_generation
)
## Generate messages in the 'msg' folder
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )

## Generate services in the 'srv' folder
add_service_files(
   FILES
   SetTemperature.srv
   GetTemperature.srv
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES csuro_comms_cpp
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs message_runtime
#  DEPENDS system_lib
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)


add_executable(temp_controller_node src/temp_controller.cpp)
target_link_libraries(temp_controller_node ${catkin_LIBRARIES})
