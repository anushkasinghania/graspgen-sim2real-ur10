// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:msg/SimpleControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/SimpleControlCommand in the package robotiq_3f_interfaces.
typedef struct robotiq_3f_interfaces__msg__SimpleControlCommand
{
  double position;
  double velocity;
  double force;
} robotiq_3f_interfaces__msg__SimpleControlCommand;

// Struct for a sequence of robotiq_3f_interfaces__msg__SimpleControlCommand.
typedef struct robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence
{
  robotiq_3f_interfaces__msg__SimpleControlCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_H_
