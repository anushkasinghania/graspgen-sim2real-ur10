// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:srv/ChangeGraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'mode'
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.h"

/// Struct defined in srv/ChangeGraspingMode in the package robotiq_3f_interfaces.
typedef struct robotiq_3f_interfaces__srv__ChangeGraspingMode_Request
{
  robotiq_3f_interfaces__msg__GraspingMode mode;
} robotiq_3f_interfaces__srv__ChangeGraspingMode_Request;

// Struct for a sequence of robotiq_3f_interfaces__srv__ChangeGraspingMode_Request.
typedef struct robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence
{
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/ChangeGraspingMode in the package robotiq_3f_interfaces.
typedef struct robotiq_3f_interfaces__srv__ChangeGraspingMode_Response
{
  bool success;
} robotiq_3f_interfaces__srv__ChangeGraspingMode_Response;

// Struct for a sequence of robotiq_3f_interfaces__srv__ChangeGraspingMode_Response.
typedef struct robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence
{
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_H_
