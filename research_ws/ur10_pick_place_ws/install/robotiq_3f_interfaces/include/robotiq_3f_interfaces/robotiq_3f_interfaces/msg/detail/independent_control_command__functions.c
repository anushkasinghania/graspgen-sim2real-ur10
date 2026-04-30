// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
robotiq_3f_interfaces__msg__IndependentControlCommand__init(robotiq_3f_interfaces__msg__IndependentControlCommand * msg)
{
  if (!msg) {
    return false;
  }
  // finger_a_position
  // finger_b_position
  // finger_c_position
  // scissor_position
  // finger_a_velocity
  // finger_b_velocity
  // finger_c_velocity
  // scissor_velocity
  // finger_a_force
  // finger_b_force
  // finger_c_force
  // scissor_force
  return true;
}

void
robotiq_3f_interfaces__msg__IndependentControlCommand__fini(robotiq_3f_interfaces__msg__IndependentControlCommand * msg)
{
  if (!msg) {
    return;
  }
  // finger_a_position
  // finger_b_position
  // finger_c_position
  // scissor_position
  // finger_a_velocity
  // finger_b_velocity
  // finger_c_velocity
  // scissor_velocity
  // finger_a_force
  // finger_b_force
  // finger_c_force
  // scissor_force
}

bool
robotiq_3f_interfaces__msg__IndependentControlCommand__are_equal(const robotiq_3f_interfaces__msg__IndependentControlCommand * lhs, const robotiq_3f_interfaces__msg__IndependentControlCommand * rhs)
{
  if (!lhs || !rhs) {
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
  // finger_a_velocity
  if (lhs->finger_a_velocity != rhs->finger_a_velocity) {
    return false;
  }
  // finger_b_velocity
  if (lhs->finger_b_velocity != rhs->finger_b_velocity) {
    return false;
  }
  // finger_c_velocity
  if (lhs->finger_c_velocity != rhs->finger_c_velocity) {
    return false;
  }
  // scissor_velocity
  if (lhs->scissor_velocity != rhs->scissor_velocity) {
    return false;
  }
  // finger_a_force
  if (lhs->finger_a_force != rhs->finger_a_force) {
    return false;
  }
  // finger_b_force
  if (lhs->finger_b_force != rhs->finger_b_force) {
    return false;
  }
  // finger_c_force
  if (lhs->finger_c_force != rhs->finger_c_force) {
    return false;
  }
  // scissor_force
  if (lhs->scissor_force != rhs->scissor_force) {
    return false;
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__IndependentControlCommand__copy(
  const robotiq_3f_interfaces__msg__IndependentControlCommand * input,
  robotiq_3f_interfaces__msg__IndependentControlCommand * output)
{
  if (!input || !output) {
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
  // finger_a_velocity
  output->finger_a_velocity = input->finger_a_velocity;
  // finger_b_velocity
  output->finger_b_velocity = input->finger_b_velocity;
  // finger_c_velocity
  output->finger_c_velocity = input->finger_c_velocity;
  // scissor_velocity
  output->scissor_velocity = input->scissor_velocity;
  // finger_a_force
  output->finger_a_force = input->finger_a_force;
  // finger_b_force
  output->finger_b_force = input->finger_b_force;
  // finger_c_force
  output->finger_c_force = input->finger_c_force;
  // scissor_force
  output->scissor_force = input->scissor_force;
  return true;
}

robotiq_3f_interfaces__msg__IndependentControlCommand *
robotiq_3f_interfaces__msg__IndependentControlCommand__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__IndependentControlCommand * msg = (robotiq_3f_interfaces__msg__IndependentControlCommand *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand));
  bool success = robotiq_3f_interfaces__msg__IndependentControlCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
robotiq_3f_interfaces__msg__IndependentControlCommand__destroy(robotiq_3f_interfaces__msg__IndependentControlCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    robotiq_3f_interfaces__msg__IndependentControlCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__IndependentControlCommand * data = NULL;

  if (size) {
    data = (robotiq_3f_interfaces__msg__IndependentControlCommand *)allocator.zero_allocate(size, sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = robotiq_3f_interfaces__msg__IndependentControlCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        robotiq_3f_interfaces__msg__IndependentControlCommand__fini(&data[i - 1]);
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
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array)
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
      robotiq_3f_interfaces__msg__IndependentControlCommand__fini(&array->data[i]);
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

robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence *
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array = (robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence *)allocator.allocate(sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__destroy(robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__are_equal(const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * lhs, const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!robotiq_3f_interfaces__msg__IndependentControlCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__copy(
  const robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * input,
  robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(robotiq_3f_interfaces__msg__IndependentControlCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    robotiq_3f_interfaces__msg__IndependentControlCommand * data =
      (robotiq_3f_interfaces__msg__IndependentControlCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!robotiq_3f_interfaces__msg__IndependentControlCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          robotiq_3f_interfaces__msg__IndependentControlCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!robotiq_3f_interfaces__msg__IndependentControlCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
