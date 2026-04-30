// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__rosidl_typesupport_fastrtps_cpp.hpp"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace robotiq_3f_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
cdr_serialize(
  const robotiq_3f_interfaces::msg::IndependentControlCommand & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: finger_a_position
  cdr << ros_message.finger_a_position;
  // Member: finger_b_position
  cdr << ros_message.finger_b_position;
  // Member: finger_c_position
  cdr << ros_message.finger_c_position;
  // Member: scissor_position
  cdr << ros_message.scissor_position;
  // Member: finger_a_velocity
  cdr << ros_message.finger_a_velocity;
  // Member: finger_b_velocity
  cdr << ros_message.finger_b_velocity;
  // Member: finger_c_velocity
  cdr << ros_message.finger_c_velocity;
  // Member: scissor_velocity
  cdr << ros_message.scissor_velocity;
  // Member: finger_a_force
  cdr << ros_message.finger_a_force;
  // Member: finger_b_force
  cdr << ros_message.finger_b_force;
  // Member: finger_c_force
  cdr << ros_message.finger_c_force;
  // Member: scissor_force
  cdr << ros_message.scissor_force;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_3f_interfaces::msg::IndependentControlCommand & ros_message)
{
  // Member: finger_a_position
  cdr >> ros_message.finger_a_position;

  // Member: finger_b_position
  cdr >> ros_message.finger_b_position;

  // Member: finger_c_position
  cdr >> ros_message.finger_c_position;

  // Member: scissor_position
  cdr >> ros_message.scissor_position;

  // Member: finger_a_velocity
  cdr >> ros_message.finger_a_velocity;

  // Member: finger_b_velocity
  cdr >> ros_message.finger_b_velocity;

  // Member: finger_c_velocity
  cdr >> ros_message.finger_c_velocity;

  // Member: scissor_velocity
  cdr >> ros_message.scissor_velocity;

  // Member: finger_a_force
  cdr >> ros_message.finger_a_force;

  // Member: finger_b_force
  cdr >> ros_message.finger_b_force;

  // Member: finger_c_force
  cdr >> ros_message.finger_c_force;

  // Member: scissor_force
  cdr >> ros_message.scissor_force;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
get_serialized_size(
  const robotiq_3f_interfaces::msg::IndependentControlCommand & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: finger_a_position
  {
    size_t item_size = sizeof(ros_message.finger_a_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_b_position
  {
    size_t item_size = sizeof(ros_message.finger_b_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_c_position
  {
    size_t item_size = sizeof(ros_message.finger_c_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: scissor_position
  {
    size_t item_size = sizeof(ros_message.scissor_position);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_a_velocity
  {
    size_t item_size = sizeof(ros_message.finger_a_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_b_velocity
  {
    size_t item_size = sizeof(ros_message.finger_b_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_c_velocity
  {
    size_t item_size = sizeof(ros_message.finger_c_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: scissor_velocity
  {
    size_t item_size = sizeof(ros_message.scissor_velocity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_a_force
  {
    size_t item_size = sizeof(ros_message.finger_a_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_b_force
  {
    size_t item_size = sizeof(ros_message.finger_b_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_c_force
  {
    size_t item_size = sizeof(ros_message.finger_c_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: scissor_force
  {
    size_t item_size = sizeof(ros_message.scissor_force);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
max_serialized_size_IndependentControlCommand(
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


  // Member: finger_a_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_b_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_c_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: scissor_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_a_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_b_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_c_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: scissor_velocity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_a_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_b_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: finger_c_force
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: scissor_force
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
    using DataType = robotiq_3f_interfaces::msg::IndependentControlCommand;
    is_plain =
      (
      offsetof(DataType, scissor_force) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _IndependentControlCommand__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robotiq_3f_interfaces::msg::IndependentControlCommand *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _IndependentControlCommand__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robotiq_3f_interfaces::msg::IndependentControlCommand *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _IndependentControlCommand__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robotiq_3f_interfaces::msg::IndependentControlCommand *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _IndependentControlCommand__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_IndependentControlCommand(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _IndependentControlCommand__callbacks = {
  "robotiq_3f_interfaces::msg",
  "IndependentControlCommand",
  _IndependentControlCommand__cdr_serialize,
  _IndependentControlCommand__cdr_deserialize,
  _IndependentControlCommand__get_serialized_size,
  _IndependentControlCommand__max_serialized_size
};

static rosidl_message_type_support_t _IndependentControlCommand__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_IndependentControlCommand__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace robotiq_3f_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_robotiq_3f_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<robotiq_3f_interfaces::msg::IndependentControlCommand>()
{
  return &robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::_IndependentControlCommand__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_3f_interfaces, msg, IndependentControlCommand)() {
  return &robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::_IndependentControlCommand__handle;
}

#ifdef __cplusplus
}
#endif
