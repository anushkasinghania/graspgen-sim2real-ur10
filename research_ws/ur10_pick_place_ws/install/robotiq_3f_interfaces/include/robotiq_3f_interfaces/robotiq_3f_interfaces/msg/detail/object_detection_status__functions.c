// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(robotiq_3f_interfaces__msg__ObjectDetectionStatus * msg)
{
  if (!msg) {
    return false;
  }
  // status
  return true;
}

void
robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(robotiq_3f_interfaces__msg__ObjectDetectionStatus * msg)
{
  if (!msg) {
    return;
  }
  // status
}

bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(const robotiq_3f_interfaces__msg__ObjectDetectionStatus * lhs, const robotiq_3f_interfaces__msg__ObjectDetectionStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
  const robotiq_3f_interfaces__msg__ObjectDetectionStatus * input,
  robotiq_3f_interfaces__msg__ObjectDetectionStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  return true;
}

robotiq_3f_interfaces__msg__ObjectDetectionStatus *
robotiq_3f_interfaces__msg__ObjectDetectionStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__ObjectDetectionStatus * msg = (robotiq_3f_interfaces__msg__ObjectDetectionStatus *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus));
  bool success = robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_3f_interfaces__msg__ObjectDetectionStatus__destroy(robotiq_3f_interfaces__msg__ObjectDetectionStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__init(robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__ObjectDetectionStatus * data = NULL;

  if (size) {
    data = (robotiq_3f_interfaces__msg__ObjectDetectionStatus *)allocator.zero_allocate(size, sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&data[i - 1]);
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
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__fini(robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * array)
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
      robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&array->data[i]);
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

robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence *
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * array = (robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__destroy(robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__are_equal(const robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * lhs, const robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__copy(
  const robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * input,
  robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_3f_interfaces__msg__ObjectDetectionStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_3f_interfaces__msg__ObjectDetectionStatus * data =
      (robotiq_3f_interfaces__msg__ObjectDetectionStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_3f_interfaces__msg__ObjectDetectionStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_3f_interfaces__msg__ObjectDetectionStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
