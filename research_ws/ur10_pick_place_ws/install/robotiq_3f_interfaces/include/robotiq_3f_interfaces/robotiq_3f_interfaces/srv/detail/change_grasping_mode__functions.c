// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_3f_interfaces:srv/ChangeGraspingMode.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/srv/detail/change_grasping_mode__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `mode`
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__functions.h"

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * msg)
{
  if (!msg) {
    return false;
  }
  // mode
  if (!robotiq_3f_interfaces__msg__GraspingMode__init(&msg->mode)) {
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(msg);
    return false;
  }
  return true;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * msg)
{
  if (!msg) {
    return;
  }
  // mode
  robotiq_3f_interfaces__msg__GraspingMode__fini(&msg->mode);
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__are_equal(const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * lhs, const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * rhs)
{
  if (!lhs || !rhs) {
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
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__copy(
  const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * input,
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // mode
  if (!robotiq_3f_interfaces__msg__GraspingMode__copy(
      &(input->mode), &(output->mode)))
  {
    return false;
  }
  return true;
}

robotiq_3f_interfaces__srv__ChangeGraspingMode_Request *
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * msg = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Request *)allocator.allocate(sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request));
  bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__destroy(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__init(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * data = NULL;

  if (size) {
    data = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Request *)allocator.zero_allocate(size, sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(&data[i - 1]);
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
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__fini(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * array)
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
      robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(&array->data[i]);
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

robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence *
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * array = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence *)allocator.allocate(sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__destroy(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__are_equal(const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * lhs, const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__copy(
  const robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * input,
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Request * data =
      (robotiq_3f_interfaces__srv__ChangeGraspingMode_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__fini(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__are_equal(const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * lhs, const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  return true;
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__copy(
  const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * input,
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  return true;
}

robotiq_3f_interfaces__srv__ChangeGraspingMode_Response *
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * msg = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Response *)allocator.allocate(sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response));
  bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__destroy(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__init(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * data = NULL;

  if (size) {
    data = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Response *)allocator.zero_allocate(size, sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__fini(&data[i - 1]);
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
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__fini(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * array)
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
      robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__fini(&array->data[i]);
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

robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence *
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * array = (robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence *)allocator.allocate(sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__destroy(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__are_equal(const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * lhs, const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__copy(
  const robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * input,
  robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_3f_interfaces__srv__ChangeGraspingMode_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_3f_interfaces__srv__ChangeGraspingMode_Response * data =
      (robotiq_3f_interfaces__srv__ChangeGraspingMode_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
