cmake_minimum_required(VERSION 3.0.2)
project(rand_walker)
find_package(catkin REQUIRED COMPONENTS
    message_generation
    geometry_msgs
    #rw_msgs
    roscpp
    std_msgs
)

add_message_files(
    FILES
    BumperEvent.msg
    CliffEvent.msg
    Led.msg
    WheelDropEvent.msg
    )

generate_messages(
    DEPENDENCIES
    std_msgs
    )

catkin_package(INCLUDE_DIRS include
    LIBRARIES rand_walker
    CATKIN_DEPENDS 
        message_runtime
        geometry_msgs
        #rw_msgs
        roscpp
        std_msgs
)

include_directories(include
    ${catkin_INCLUDE_DIRS})

add_executable(rand_walker_controller src/rand_walker_controller.cpp)
target_link_libraries(rand_walker_controller ${catkin_LIBRARIES})
