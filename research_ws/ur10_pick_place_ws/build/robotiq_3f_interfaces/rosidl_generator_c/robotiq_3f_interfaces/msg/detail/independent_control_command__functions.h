// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__FUNCTIONS_H_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "robotiq_3f_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.h"

/// Initialize msg/IndependentControlCommand message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * robotiq_3f_interfaces__msg__IndependentControlCommand
 * )) before or use
 * robotiq_3f_interfaces__msg__IndependentControlCommand__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__init(robotiq_3f_interfaces__msg__IndependentControlCommand * msg);

/// Finalize msg/IndependentControlCommand message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
void
robotiq_3f_interfaces__msg__IndependentControlCommand__fini(robotiq_3f_interfaces__msg__IndependentControlCommand * msg);

/// Create msg/IndependentControlCommand message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
robotiq_3f_interfaces__msg__IndependentControlCommand *
robotiq_3f_interfaces__msg__IndependentControlCommand__create();

/// Destroy msg/IndependentControlCommand message.
/**
 * It calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
void
robotiq_3f_interfaces__msg__IndependentControlCommand__destroy(robotiq_3f_interfaces__msg__IndependentControlCommand * msg);

/// Check for msg/IndependentControlCommand message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__are_equal(const robotiq_3f_interfaces__msg__IndependentControlCommand * lhs, const robotiq_3f_interfaces__msg__IndependentControlCommand * rhs);

/// Copy a msg/IndependentControlCommand message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__copy(
  const robotiq_3f_interfaces__msg__IndependentControlCommand * input,
  robotiq_3f_interfaces__msg__IndependentControlCommand * output);

/// Initialize array of msg/IndependentControlCommand messages.
/**
 * It allocates the memory for the number of elements and calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array, size_t size);

/// Finalize array of msg/IndependentControlCommand messages.
/**
 * It calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
void
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array);

/// Create array of msg/IndependentControlCommand messages.
/**
 * It allocates the memory for the array and calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence *
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__create(size_t size);

/// Destroy array of msg/IndependentControlCommand messages.
/**
 * It calls
 * robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
void
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__destroy(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array);

/// Check for msg/IndependentControlCommand message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__are_equal(const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * lhs, const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * rhs);

/// Copy an array of msg/IndependentControlCommand messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_robotiq_3f_interfaces
bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__copy(
  const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * input,
  robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__FUNCTIONS_H_
