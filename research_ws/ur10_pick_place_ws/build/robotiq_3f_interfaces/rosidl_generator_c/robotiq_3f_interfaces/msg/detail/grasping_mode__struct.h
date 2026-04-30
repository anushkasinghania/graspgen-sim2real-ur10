// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:msg/GraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'BASIC'.
enum
{
  robotiq_3f_interfaces__msg__GraspingMode__BASIC = 0
};

/// Constant 'PINCH'.
enum
{
  robotiq_3f_interfaces__msg__GraspingMode__PINCH = 1
};

/// Constant 'WIDE'.
enum
{
  robotiq_3f_interfaces__msg__GraspingMode__WIDE = 2
};

/// Constant 'SCISSOR'.
enum
{
  robotiq_3f_interfaces__msg__GraspingMode__SCISSOR = 3
};

/// Struct defined in msg/GraspingMode in the package robotiq_3f_interfaces.
typedef struct robotiq_3f_interfaces__msg__GraspingMode
{
  int8_t mode;
} robotiq_3f_interfaces__msg__GraspingMode;

// Struct for a sequence of robotiq_3f_interfaces__msg__GraspingMode.
typedef struct robotiq_3f_interfaces__msg__GraspingMode__Sequence
{
  robotiq_3f_interfaces__msg__GraspingMode * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__msg__GraspingMode__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_H_
