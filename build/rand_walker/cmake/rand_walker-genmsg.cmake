# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "rand_walker: 4 messages, 0 services")

set(MSG_I_FLAGS "-Irand_walker:/home/artur/UM/inesctec/random_walker/src/rand_walker/msg;-Istd_msgs:/nix/store/p2np8nj9zs5dj23pxljlbv98256lb2v4-ros-env/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(rand_walker_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_custom_target(_rand_walker_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rand_walker" "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" ""
)

get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_custom_target(_rand_walker_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rand_walker" "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" ""
)

get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_custom_target(_rand_walker_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rand_walker" "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" ""
)

get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_custom_target(_rand_walker_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "rand_walker" "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
)
_generate_msg_cpp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
)
_generate_msg_cpp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
)
_generate_msg_cpp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
)

### Generating Services

### Generating Module File
_generate_module_cpp(rand_walker
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(rand_walker_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(rand_walker_generate_messages rand_walker_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_cpp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_cpp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_cpp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_cpp _rand_walker_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rand_walker_gencpp)
add_dependencies(rand_walker_gencpp rand_walker_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rand_walker_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
)
_generate_msg_eus(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
)
_generate_msg_eus(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
)
_generate_msg_eus(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
)

### Generating Services

### Generating Module File
_generate_module_eus(rand_walker
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(rand_walker_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(rand_walker_generate_messages rand_walker_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_eus _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_eus _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_eus _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_eus _rand_walker_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rand_walker_geneus)
add_dependencies(rand_walker_geneus rand_walker_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rand_walker_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
)
_generate_msg_lisp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
)
_generate_msg_lisp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
)
_generate_msg_lisp(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
)

### Generating Services

### Generating Module File
_generate_module_lisp(rand_walker
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(rand_walker_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(rand_walker_generate_messages rand_walker_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_lisp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_lisp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_lisp _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_lisp _rand_walker_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rand_walker_genlisp)
add_dependencies(rand_walker_genlisp rand_walker_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rand_walker_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
)
_generate_msg_nodejs(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
)
_generate_msg_nodejs(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
)
_generate_msg_nodejs(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
)

### Generating Services

### Generating Module File
_generate_module_nodejs(rand_walker
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(rand_walker_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(rand_walker_generate_messages rand_walker_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_nodejs _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_nodejs _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_nodejs _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_nodejs _rand_walker_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rand_walker_gennodejs)
add_dependencies(rand_walker_gennodejs rand_walker_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rand_walker_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
)
_generate_msg_py(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
)
_generate_msg_py(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
)
_generate_msg_py(rand_walker
  "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
)

### Generating Services

### Generating Module File
_generate_module_py(rand_walker
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(rand_walker_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(rand_walker_generate_messages rand_walker_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/CliffEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_py _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/WheelDropEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_py _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/BumperEvent.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_py _rand_walker_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/artur/UM/inesctec/random_walker/src/rand_walker/msg/Led.msg" NAME_WE)
add_dependencies(rand_walker_generate_messages_py _rand_walker_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(rand_walker_genpy)
add_dependencies(rand_walker_genpy rand_walker_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS rand_walker_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/rand_walker
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(rand_walker_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/rand_walker
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(rand_walker_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/rand_walker
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(rand_walker_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/rand_walker
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(rand_walker_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker)
  install(CODE "execute_process(COMMAND \"/nix/store/9j34pp0ajq2hzb3hi7zv0l3bpszm4n43-python-2.7.18/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/rand_walker
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(rand_walker_generate_messages_py std_msgs_generate_messages_py)
endif()
