// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice
#include "robotiq_3f_interfaces/msg/detail/status__rosidl_typesupport_fastrtps_cpp.hpp"
#include "robotiq_3f_interfaces/msg/detail/status__struct.hpp"

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
bool cdr_serialize(
  const robotiq_3f_interfaces::msg::ObjectDetectionStatus &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  robotiq_3f_interfaces::msg::ObjectDetectionStatus &);
size_t get_serialized_size(
  const robotiq_3f_interfaces::msg::ObjectDetectionStatus &,
  size_t current_alignment);
size_t
max_serialized_size_ObjectDetectionStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace robotiq_3f_interfaces

// functions for robotiq_3f_interfaces::msg::ObjectDetectionStatus already declared above

// functions for robotiq_3f_interfaces::msg::ObjectDetectionStatus already declared above

// functions for robotiq_3f_interfaces::msg::ObjectDetectionStatus already declared above

namespace robotiq_3f_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const robotiq_3f_interfaces::msg::GraspingMode &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  robotiq_3f_interfaces::msg::GraspingMode &);
size_t get_serialized_size(
  const robotiq_3f_interfaces::msg::GraspingMode &,
  size_t current_alignment);
size_t
max_serialized_size_GraspingMode(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace robotiq_3f_interfaces


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
cdr_serialize(
  const robotiq_3f_interfaces::msg::Status & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: finger_a_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.finger_a_object_detection,
    cdr);
  // Member: finger_b_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.finger_b_object_detection,
    cdr);
  // Member: finger_c_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.finger_c_object_detection,
    cdr);
  // Member: scissor_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.scissor_object_detection,
    cdr);
  // Member: finger_a_position
  cdr << ros_message.finger_a_position;
  // Member: finger_b_position
  cdr << ros_message.finger_b_position;
  // Member: finger_c_position
  cdr << ros_message.finger_c_position;
  // Member: scissor_position
  cdr << ros_message.scissor_position;
  // Member: finger_a_current
  cdr << ros_message.finger_a_current;
  // Member: finger_b_current
  cdr << ros_message.finger_b_current;
  // Member: finger_c_current
  cdr << ros_message.finger_c_current;
  // Member: scissor_current
  cdr << ros_message.scissor_current;
  // Member: finger_a_cmd_echo
  cdr << ros_message.finger_a_cmd_echo;
  // Member: finger_b_cmd_echo
  cdr << ros_message.finger_b_cmd_echo;
  // Member: finger_c_cmd_echo
  cdr << ros_message.finger_c_cmd_echo;
  // Member: scissor_cmd_echo
  cdr << ros_message.scissor_cmd_echo;
  // Member: mode
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.mode,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  robotiq_3f_interfaces::msg::Status & ros_message)
{
  // Member: finger_a_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.finger_a_object_detection);

  // Member: finger_b_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.finger_b_object_detection);

  // Member: finger_c_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.finger_c_object_detection);

  // Member: scissor_object_detection
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.scissor_object_detection);

  // Member: finger_a_position
  cdr >> ros_message.finger_a_position;

  // Member: finger_b_position
  cdr >> ros_message.finger_b_position;

  // Member: finger_c_position
  cdr >> ros_message.finger_c_position;

  // Member: scissor_position
  cdr >> ros_message.scissor_position;

  // Member: finger_a_current
  cdr >> ros_message.finger_a_current;

  // Member: finger_b_current
  cdr >> ros_message.finger_b_current;

  // Member: finger_c_current
  cdr >> ros_message.finger_c_current;

  // Member: scissor_current
  cdr >> ros_message.scissor_current;

  // Member: finger_a_cmd_echo
  cdr >> ros_message.finger_a_cmd_echo;

  // Member: finger_b_cmd_echo
  cdr >> ros_message.finger_b_cmd_echo;

  // Member: finger_c_cmd_echo
  cdr >> ros_message.finger_c_cmd_echo;

  // Member: scissor_cmd_echo
  cdr >> ros_message.scissor_cmd_echo;

  // Member: mode
  robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.mode);

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
get_serialized_size(
  const robotiq_3f_interfaces::msg::Status & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: finger_a_object_detection

  current_alignment +=
    robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.finger_a_object_detection, current_alignment);
  // Member: finger_b_object_detection

  current_alignment +=
    robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.finger_b_object_detection, current_alignment);
  // Member: finger_c_object_detection

  current_alignment +=
    robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.finger_c_object_detection, current_alignment);
  // Member: scissor_object_detection

  current_alignment +=
    robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.scissor_object_detection, current_alignment);
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
  // Member: finger_a_current
  {
    size_t item_size = sizeof(ros_message.finger_a_current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_b_current
  {
    size_t item_size = sizeof(ros_message.finger_b_current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_c_current
  {
    size_t item_size = sizeof(ros_message.finger_c_current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: scissor_current
  {
    size_t item_size = sizeof(ros_message.scissor_current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_a_cmd_echo
  {
    size_t item_size = sizeof(ros_message.finger_a_cmd_echo);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_b_cmd_echo
  {
    size_t item_size = sizeof(ros_message.finger_b_cmd_echo);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: finger_c_cmd_echo
  {
    size_t item_size = sizeof(ros_message.finger_c_cmd_echo);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: scissor_cmd_echo
  {
    size_t item_size = sizeof(ros_message.scissor_cmd_echo);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: mode

  current_alignment +=
    robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.mode, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_robotiq_3f_interfaces
max_serialized_size_Status(
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


  // Member: finger_a_object_detection
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectDetectionStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: finger_b_object_detection
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectDetectionStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: finger_c_object_detection
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectDetectionStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: scissor_object_detection
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_ObjectDetectionStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: finger_a_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_b_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_c_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: scissor_position
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_a_current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_b_current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_c_current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: scissor_current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_a_cmd_echo
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_b_cmd_echo
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: finger_c_cmd_echo
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: scissor_cmd_echo
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: mode
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_GraspingMode(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = robotiq_3f_interfaces::msg::Status;
    is_plain =
      (
      offsetof(DataType, mode) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _Status__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const robotiq_3f_interfaces::msg::Status *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Status__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<robotiq_3f_interfaces::msg::Status *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Status__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const robotiq_3f_interfaces::msg::Status *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Status__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Status(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Status__callbacks = {
  "robotiq_3f_interfaces::msg",
  "Status",
  _Status__cdr_serialize,
  _Status__cdr_deserialize,
  _Status__get_serialized_size,
  _Status__max_serialized_size
};

static rosidl_message_type_support_t _Status__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Status__callbacks,
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
get_message_type_support_handle<robotiq_3f_interfaces::msg::Status>()
{
  return &robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::_Status__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, robotiq_3f_interfaces, msg, Status)() {
  return &robotiq_3f_interfaces::msg::typesupport_fastrtps_cpp::_Status__handle;
}

#ifdef __cplusplus
}
#endif
