// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'finger_a_object_detection'
// Member 'finger_b_object_detection'
// Member 'finger_c_object_detection'
// Member 'scissor_object_detection'
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__struct.h"
// Member 'mode'
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.h"

/// Struct defined in msg/Status in the package robotiq_3f_interfaces.
/**
  * Reports whether an object has been gripped or not.
 */
typedef struct robotiq_3f_interfaces__msg__Status
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus finger_a_object_detection;
  robotiq_3f_interfaces__msg__ObjectDetectionStatus finger_b_object_detection;
  robotiq_3f_interfaces__msg__ObjectDetectionStatus finger_c_object_detection;
  robotiq_3f_interfaces__msg__ObjectDetectionStatus scissor_object_detection;
  /// Actuator states
  uint8_t finger_a_position;
  uint8_t finger_b_position;
  uint8_t finger_c_position;
  uint8_t scissor_position;
  uint8_t finger_a_current;
  uint8_t finger_b_current;
  uint8_t finger_c_current;
  uint8_t scissor_current;
  uint8_t finger_a_cmd_echo;
  uint8_t finger_b_cmd_echo;
  uint8_t finger_c_cmd_echo;
  uint8_t scissor_cmd_echo;
  robotiq_3f_interfaces__msg__GraspingMode mode;
} robotiq_3f_interfaces__msg__Status;

// Struct for a sequence of robotiq_3f_interfaces__msg__Status.
typedef struct robotiq_3f_interfaces__msg__Status__Sequence
{
  robotiq_3f_interfaces__msg__Status * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__msg__Status__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_H_
