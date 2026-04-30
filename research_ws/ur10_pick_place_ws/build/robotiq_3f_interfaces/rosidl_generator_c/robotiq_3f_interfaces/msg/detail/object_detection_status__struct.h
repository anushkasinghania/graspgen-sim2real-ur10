// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'MOVING'.
enum
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__MOVING = 0
};

/// Constant 'OBJECT_DETECTED_OPENING'.
enum
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__OBJECT_DETECTED_OPENING = 1
};

/// Constant 'OBJECT_DETECTED_CLOSING'.
enum
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__OBJECT_DETECTED_CLOSING = 2
};

/// Constant 'AT_REQUESTED_POSITION'.
enum
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__AT_REQUESTED_POSITION = 3
};

/// Struct defined in msg/ObjectDetectionStatus in the package robotiq_3f_interfaces.
/**
  * Reports whether an object has been gripped or not.
 */
typedef struct robotiq_3f_interfaces__msg__ObjectDetectionStatus
{
  int8_t status;
} robotiq_3f_interfaces__msg__ObjectDetectionStatus;

// Struct for a sequence of robotiq_3f_interfaces__msg__ObjectDetectionStatus.
typedef struct robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence
{
  robotiq_3f_interfaces__msg__ObjectDetectionStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_H_
