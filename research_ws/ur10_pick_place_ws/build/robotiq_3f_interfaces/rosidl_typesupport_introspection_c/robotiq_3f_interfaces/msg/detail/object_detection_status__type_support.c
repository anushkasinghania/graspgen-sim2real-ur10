// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__rosidl_typesupport_introspection_c.h"
#include "robotiq_3f_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__functions.h"
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(message_memory);
}

void robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_fini_function(void * message_memory)
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_member_array[1] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(robotiq_3f_interfaces__msg__ObjectDetectionStatus, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_members = {
  "robotiq_3f_interfaces__msg",  // message namespace
  "ObjectDetectionStatus",  // message name
  1,  // number of fields
  sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus),
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_member_array,  // message members
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_type_support_handle = {
  0,
  &robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_robotiq_3f_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, robotiq_3f_interfaces, msg, ObjectDetectionStatus)() {
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_type_support_handle.typesupport_identifier) {
    robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &robotiq_3f_interfaces__msg__ObjectDetectionStatus__rosidl_typesupport_introspection_c__ObjectDetectionStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
