// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "robotiq_3f_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.h"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _IndependentControlCommand__ros_msg_type = robotiq_3f_interfaces__msg__IndependentControlCommand;

static bool _IndependentControlCommand__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _IndependentControlCommand__ros_msg_type * ros_message = static_cast<const _IndependentControlCommand__ros_msg_type *>(untyped_ros_message);
  // Field name: finger_a_position
  {
    cdr << ros_message->finger_a_position;
  }

  // Field name: finger_b_position
  {
    cdr << ros_message->finger_b_position;
  }

  // Field name: finger_c_position
  {
    cdr << ros_message->finger_c_position;
  }

  // Field name: scissor_position
  {
    cdr << ros_message->scissor_position;
  }

  // Field name: finger_a_velocity
  {
    cdr << ros_message->finger_a_velocity;
  }

  // Field name: finger_b_velocity
  {
    cdr << ros_message->finger_b_velocity;
  }

  // Field name: finger_c_velocity
  {
    cdr << ros_message->finger_c_velocity;
  }

  // Field name: scissor_velocity
  {
    cdr << ros_message->scissor_velocity;
  }

  // Field name: finger_a_force
  {
    cdr << ros_message->finger_a_force;
  }

  // Field name: finger_b_force
  {
    cdr << ros_message->finger_b_force;
  }

  // Field name: finger_c_force
  {
    cdr << ros_message->finger_c_force;
  }

  // Field name: scissor_force
  {
    cdr << ros_message->scissor_force;
  }

  return true;
}

static bool _IndependentControlCommand__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _IndependentControlCommand__ros_msg_type * ros_message = static_cast<_IndependentControlCommand__ros_msg_type *>(untyped_ros_message);
  // Field name: finger_a_position
  {
    cdr >> ros_message->finger_a_position;
  }

  // Field name: finger_b_position
  {
    cdr >> ros_message->finger_b_position;
  }

  // Field name: finger_c_position
  {
    cdr >> ros_message->finger_c_position;
  }

  // Field name: scissor_position
  {
    cdr >> ros_message->scissor_position;
  }

  // Field name: finger_a_velocity
  {
    cdr >> ros_message->finger_a_velocity;
  }

  // Field name: finger_b_velocity
  {
    cdr >> ros_message->finger_b_velocity;
  }

  // Field name: finger_c_velocity
  {
    cdr >> ros_message->finger_c_velocity;
  }

  // Field name: scissor_velocity
  {
    cdr >> ros_message->scissor_velocity;
  }

  // Field name: finger_a_force
  {
    cdr >> ros_message->finger_a_force;
  }

  // Field name: finger_b_force
  {
    cdr >> ros_message->finger_b_force;
  }

  // Field name: finger_c_force
  {
    cdr >> ros_message->finger_c_force;
  }

  // Field name: scissor_force
  {
    cdr >> ros_message->scissor_force;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robotiq_3f_interfaces
size_t get_serialized_size_robotiq_3f_interfaces__msg__IndependentControlCommand(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _IndependentControlCommand__ros_msg_type * ros_message = static_cast<const _IndependentControlCommand__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name finger_a_position
  {
    size_t item_size = sizeof(ros_message->finger_a_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_b_position
  {
    size_t item_size = sizeof(ros_message->finger_b_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_c_position
  {
    size_t item_size = sizeof(ros_message->finger_c_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name scissor_position
  {
    size_t item_size = sizeof(ros_message->scissor_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_a_velocity
  {
    size_t item_size = sizeof(ros_message->finger_a_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_b_velocity
  {
    size_t item_size = sizeof(ros_message->finger_b_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_c_velocity
  {
    size_t item_size = sizeof(ros_message->finger_c_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name scissor_velocity
  {
    size_t item_size = sizeof(ros_message->scissor_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_a_force
  {
    size_t item_size = sizeof(ros_message->finger_a_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_b_force
  {
    size_t item_size = sizeof(ros_message->finger_b_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name finger_c_force
  {
    size_t item_size = sizeof(ros_message->finger_c_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name scissor_force
  {
    size_t item_size = sizeof(ros_message->scissor_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _IndependentControlCommand__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_robotiq_3f_interfaces__msg__IndependentControlCommand(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_robotiq_3f_interfaces
size_t max_serialized_size_robotiq_3f_interfaces__msg__IndependentControlCommand(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: finger_a_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_b_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_c_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: scissor_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_a_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_b_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_c_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: scissor_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_a_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_b_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: finger_c_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: scissor_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = robotiq_3f_interfaces__msg__IndependentControlCommand;
    is_plain =
      (
      offsetof(DataType, scissor_force) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _IndependentControlCommand__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_robotiq_3f_interfaces__msg__IndependentControlCommand(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_IndependentControlCommand = {
  "robotiq_3f_interfaces::msg",
  "IndependentControlCommand",
  _IndependentControlCommand__cdr_serialize,
  _IndependentControlCommand__cdr_deserialize,
  _IndependentControlCommand__get_serialized_size,
  _IndependentControlCommand__max_serialized_size
};

static rosidl_message_type_support_t _IndependentControlCommand__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_IndependentControlCommand,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, robotiq_3f_interfaces, msg, IndependentControlCommand)() {
  return &_IndependentControlCommand__type_support;
}

#if defined(__cplusplus)
}
#endif
