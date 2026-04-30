// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__rosidl_typesupport_introspection_c.h"
#include "robotiq_3f_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__functions.h"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robotiq_3f_interfaces__msg__IndependentControlCommand__init(message_memory);
}

void robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_fini_function(void * message_memory)
{
  robotiq_3f_interfaces__msg__IndependentControlCommand__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_member_array[12] = {
  {
    "finger_a_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_a_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_b_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_b_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_c_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_c_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scissor_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, scissor_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_a_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_a_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_b_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_b_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_c_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_c_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scissor_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, scissor_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_a_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_a_force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_b_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_b_force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "finger_c_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, finger_c_force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scissor_force",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__IndependentControlCommand, scissor_force),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_members = {
  "robotiq_3f_interfaces__msg",  // message namespace
  "IndependentControlCommand",  // message name
  12,  // number of fields
  sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand),
  robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_member_array,  // message members
  robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_init_function,  // function to initialize message memory (memory has to be allocated)
  robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_type_support_handle = {
  0,
  &robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robotiq_3f_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robotiq_3f_interfaces, msg, IndependentControlCommand)() {
  if (!robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_type_support_handle.typesupport_identifier) {
    robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &robotiq_3f_interfaces__msg__IndependentControlCommand__rosidl_typesupport_introspection_c__IndependentControlCommand_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
