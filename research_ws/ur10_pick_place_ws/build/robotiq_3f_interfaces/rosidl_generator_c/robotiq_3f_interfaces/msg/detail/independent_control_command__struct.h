// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/IndependentControlCommand in the package robotiq_3f_interfaces.
typedef struct robotiq_3f_interfaces__msg__IndependentControlCommand
{
  double finger_a_position;
  double finger_b_position;
  double finger_c_position;
  double scissor_position;
  double finger_a_velocity;
  double finger_b_velocity;
  double finger_c_velocity;
  double scissor_velocity;
  double finger_a_force;
  double finger_b_force;
  double finger_c_force;
  double scissor_force;
} robotiq_3f_interfaces__msg__IndependentControlCommand;

// Struct for a sequence of robotiq_3f_interfaces__msg__IndependentControlCommand.
typedef struct robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence
{
  robotiq_3f_interfaces__msg__IndependentControlCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_H_
