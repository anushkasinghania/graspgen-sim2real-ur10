// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `finger_a_object_detection`
// Member `finger_b_object_detection`
// Member `finger_c_object_detection`
// Member `scissor_object_detection`
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__functions.h"
// Member `mode`
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__functions.h"

bool
robotiq_3f_interfaces__msg__Status__init(robotiq_3f_interfaces__msg__Status * msg)
{
  if (!msg) {
    return false;
  }
  // finger_a_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&msg->finger_a_object_detection)) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
    return false;
  }
  // finger_b_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&msg->finger_b_object_detection)) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
    return false;
  }
  // finger_c_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&msg->finger_c_object_detection)) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
    return false;
  }
  // scissor_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&msg->scissor_object_detection)) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
    return false;
  }
  // finger_a_position
  // finger_b_position
  // finger_c_position
  // scissor_position
  // finger_a_current
  // finger_b_current
  // finger_c_current
  // scissor_current
  // finger_a_cmd_echo
  // finger_b_cmd_echo
  // finger_c_cmd_echo
  // scissor_cmd_echo
  // mode
  if (!robotiq_3f_interfaces__msg__GraspingMode__init(&msg->mode)) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
    return false;
  }
  return true;
}

void
robotiq_3f_interfaces__msg__Status__fini(robotiq_3f_interfaces__msg__Status * msg)
{
  if (!msg) {
    return;
  }
  // finger_a_object_detection
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&msg->finger_a_object_detection);
  // finger_b_object_detection
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&msg->finger_b_object_detection);
  // finger_c_object_detection
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&msg->finger_c_object_detection);
  // scissor_object_detection
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&msg->scissor_object_detection);
  // finger_a_position
  // finger_b_position
  // finger_c_position
  // scissor_position
  // finger_a_current
  // finger_b_current
  // finger_c_current
  // scissor_current
  // finger_a_cmd_echo
  // finger_b_cmd_echo
  // finger_c_cmd_echo
  // scissor_cmd_echo
  // mode
  robotiq_3f_interfaces__msg__GraspingMode__fini(&msg->mode);
}

bool
robotiq_3f_interfaces__msg__Status__are_equal(const robotiq_3f_interfaces__msg__Status * lhs, const robotiq_3f_interfaces__msg__Status * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // finger_a_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(
      &(lhs->finger_a_object_detection), &(rhs->finger_a_object_detection)))
  {
    return false;
  }
  // finger_b_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(
      &(lhs->finger_b_object_detection), &(rhs->finger_b_object_detection)))
  {
    return false;
  }
  // finger_c_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(
      &(lhs->finger_c_object_detection), &(rhs->finger_c_object_detection)))
  {
    return false;
  }
  // scissor_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(
      &(lhs->scissor_object_detection), &(rhs->scissor_object_detection)))
  {
    return false;
  }
  // finger_a_position
  if (lhs->finger_a_position != rhs->finger_a_position) {
    return false;
  }
  // finger_b_position
  if (lhs->finger_b_position != rhs->finger_b_position) {
    return false;
  }
  // finger_c_position
  if (lhs->finger_c_position != rhs->finger_c_position) {
    return false;
  }
  // scissor_position
  if (lhs->scissor_position != rhs->scissor_position) {
    return false;
  }
  // finger_a_current
  if (lhs->finger_a_current != rhs->finger_a_current) {
    return false;
  }
  // finger_b_current
  if (lhs->finger_b_current != rhs->finger_b_current) {
    return false;
  }
  // finger_c_current
  if (lhs->finger_c_current != rhs->finger_c_current) {
    return false;
  }
  // scissor_current
  if (lhs->scissor_current != rhs->scissor_current) {
    return false;
  }
  // finger_a_cmd_echo
  if (lhs->finger_a_cmd_echo != rhs->finger_a_cmd_echo) {
    return false;
  }
  // finger_b_cmd_echo
  if (lhs->finger_b_cmd_echo != rhs->finger_b_cmd_echo) {
    return false;
  }
  // finger_c_cmd_echo
  if (lhs->finger_c_cmd_echo != rhs->finger_c_cmd_echo) {
    return false;
  }
  // scissor_cmd_echo
  if (lhs->scissor_cmd_echo != rhs->scissor_cmd_echo) {
    return false;
  }
  // mode
  if (!robotiq_3f_interfaces__msg__GraspingMode__are_equal(
      &(lhs->mode), &(rhs->mode)))
  {
    return false;
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__Status__copy(
  const robotiq_3f_interfaces__msg__Status * input,
  robotiq_3f_interfaces__msg__Status * output)
{
  if (!input || !output) {
    return false;
  }
  // finger_a_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
      &(input->finger_a_object_detection), &(output->finger_a_object_detection)))
  {
    return false;
  }
  // finger_b_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
      &(input->finger_b_object_detection), &(output->finger_b_object_detection)))
  {
    return false;
  }
  // finger_c_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
      &(input->finger_c_object_detection), &(output->finger_c_object_detection)))
  {
    return false;
  }
  // scissor_object_detection
  if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
      &(input->scissor_object_detection), &(output->scissor_object_detection)))
  {
    return false;
  }
  // finger_a_position
  output->finger_a_position = input->finger_a_position;
  // finger_b_position
  output->finger_b_position = input->finger_b_position;
  // finger_c_position
  output->finger_c_position = input->finger_c_position;
  // scissor_position
  output->scissor_position = input->scissor_position;
  // finger_a_current
  output->finger_a_current = input->finger_a_current;
  // finger_b_current
  output->finger_b_current = input->finger_b_current;
  // finger_c_current
  output->finger_c_current = input->finger_c_current;
  // scissor_current
  output->scissor_current = input->scissor_current;
  // finger_a_cmd_echo
  output->finger_a_cmd_echo = input->finger_a_cmd_echo;
  // finger_b_cmd_echo
  output->finger_b_cmd_echo = input->finger_b_cmd_echo;
  // finger_c_cmd_echo
  output->finger_c_cmd_echo = input->finger_c_cmd_echo;
  // scissor_cmd_echo
  output->scissor_cmd_echo = input->scissor_cmd_echo;
  // mode
  if (!robotiq_3f_interfaces__msg__GraspingMode__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  return true;
}

robotiq_3f_interfaces__msg__Status *
robotiq_3f_interfaces__msg__Status__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__Status * msg = (robotiq_3f_interfaces__msg__Status *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__Status), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_3f_interfaces__msg__Status));
  bool success = robotiq_3f_interfaces__msg__Status__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_3f_interfaces__msg__Status__destroy(robotiq_3f_interfaces__msg__Status * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_3f_interfaces__msg__Status__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_3f_interfaces__msg__Status__Sequence__init(robotiq_3f_interfaces__msg__Status__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__Status * data = NULL;

  if (size) {
    data = (robotiq_3f_interfaces__msg__Status *)allocator.zero_allocate(size, sizeof(robotiq_3f_interfaces__msg__Status), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_3f_interfaces__msg__Status__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_3f_interfaces__msg__Status__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
robotiq_3f_interfaces__msg__Status__Sequence__fini(robotiq_3f_interfaces__msg__Status__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      robotiq_3f_interfaces__msg__Status__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

robotiq_3f_interfaces__msg__Status__Sequence *
robotiq_3f_interfaces__msg__Status__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__Status__Sequence * array = (robotiq_3f_interfaces__msg__Status__Sequence *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__Status__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_3f_interfaces__msg__Status__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_3f_interfaces__msg__Status__Sequence__destroy(robotiq_3f_interfaces__msg__Status__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_3f_interfaces__msg__Status__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_3f_interfaces__msg__Status__Sequence__are_equal(const robotiq_3f_interfaces__msg__Status__Sequence * lhs, const robotiq_3f_interfaces__msg__Status__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_3f_interfaces__msg__Status__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__Status__Sequence__copy(
  const robotiq_3f_interfaces__msg__Status__Sequence * input,
  robotiq_3f_interfaces__msg__Status__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_3f_interfaces__msg__Status);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_3f_interfaces__msg__Status * data =
      (robotiq_3f_interfaces__msg__Status *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_3f_interfaces__msg__Status__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_3f_interfaces__msg__Status__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_3f_interfaces__msg__Status__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
