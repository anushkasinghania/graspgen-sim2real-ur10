// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__TRAITS_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_3f_interfaces/msg/detail/status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'finger_a_object_detection'
// Member 'finger_b_object_detection'
// Member 'finger_c_object_detection'
// Member 'scissor_object_detection'
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__traits.hpp"
// Member 'mode'
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__traits.hpp"

namespace robotiq_3f_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Status & msg,
  std::ostream & out)
{
  out << "{";
  // member: finger_a_object_detection
  {
    out << "finger_a_object_detection: ";
    to_flow_style_yaml(msg.finger_a_object_detection, out);
    out << ", ";
  }

  // member: finger_b_object_detection
  {
    out << "finger_b_object_detection: ";
    to_flow_style_yaml(msg.finger_b_object_detection, out);
    out << ", ";
  }

  // member: finger_c_object_detection
  {
    out << "finger_c_object_detection: ";
    to_flow_style_yaml(msg.finger_c_object_detection, out);
    out << ", ";
  }

  // member: scissor_object_detection
  {
    out << "scissor_object_detection: ";
    to_flow_style_yaml(msg.scissor_object_detection, out);
    out << ", ";
  }

  // member: finger_a_position
  {
    out << "finger_a_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_position, out);
    out << ", ";
  }

  // member: finger_b_position
  {
    out << "finger_b_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_position, out);
    out << ", ";
  }

  // member: finger_c_position
  {
    out << "finger_c_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_position, out);
    out << ", ";
  }

  // member: scissor_position
  {
    out << "scissor_position: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_position, out);
    out << ", ";
  }

  // member: finger_a_current
  {
    out << "finger_a_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_current, out);
    out << ", ";
  }

  // member: finger_b_current
  {
    out << "finger_b_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_current, out);
    out << ", ";
  }

  // member: finger_c_current
  {
    out << "finger_c_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_current, out);
    out << ", ";
  }

  // member: scissor_current
  {
    out << "scissor_current: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_current, out);
    out << ", ";
  }

  // member: finger_a_cmd_echo
  {
    out << "finger_a_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_cmd_echo, out);
    out << ", ";
  }

  // member: finger_b_cmd_echo
  {
    out << "finger_b_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_cmd_echo, out);
    out << ", ";
  }

  // member: finger_c_cmd_echo
  {
    out << "finger_c_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_cmd_echo, out);
    out << ", ";
  }

  // member: scissor_cmd_echo
  {
    out << "scissor_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_cmd_echo, out);
    out << ", ";
  }

  // member: mode
  {
    out << "mode: ";
    to_flow_style_yaml(msg.mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Status & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: finger_a_object_detection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_object_detection:\n";
    to_block_style_yaml(msg.finger_a_object_detection, out, indentation + 2);
  }

  // member: finger_b_object_detection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_object_detection:\n";
    to_block_style_yaml(msg.finger_b_object_detection, out, indentation + 2);
  }

  // member: finger_c_object_detection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_object_detection:\n";
    to_block_style_yaml(msg.finger_c_object_detection, out, indentation + 2);
  }

  // member: scissor_object_detection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_object_detection:\n";
    to_block_style_yaml(msg.scissor_object_detection, out, indentation + 2);
  }

  // member: finger_a_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_position, out);
    out << "\n";
  }

  // member: finger_b_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_position, out);
    out << "\n";
  }

  // member: finger_c_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_position: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_position, out);
    out << "\n";
  }

  // member: scissor_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_position: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_position, out);
    out << "\n";
  }

  // member: finger_a_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_current, out);
    out << "\n";
  }

  // member: finger_b_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_current, out);
    out << "\n";
  }

  // member: finger_c_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_current: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_current, out);
    out << "\n";
  }

  // member: scissor_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_current: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_current, out);
    out << "\n";
  }

  // member: finger_a_cmd_echo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_cmd_echo, out);
    out << "\n";
  }

  // member: finger_b_cmd_echo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_cmd_echo, out);
    out << "\n";
  }

  // member: finger_c_cmd_echo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_cmd_echo, out);
    out << "\n";
  }

  // member: scissor_cmd_echo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_cmd_echo: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_cmd_echo, out);
    out << "\n";
  }

  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode:\n";
    to_block_style_yaml(msg.mode, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Status & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace robotiq_3f_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use robotiq_3f_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const robotiq_3f_interfaces::msg::Status & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_3f_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_3f_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_3f_interfaces::msg::Status & msg)
{
  return robotiq_3f_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_3f_interfaces::msg::Status>()
{
  return "robotiq_3f_interfaces::msg::Status";
}

template<>
inline const char * name<robotiq_3f_interfaces::msg::Status>()
{
  return "robotiq_3f_interfaces/msg/Status";
}

template<>
struct has_fixed_size<robotiq_3f_interfaces::msg::Status>
  : std::integral_constant<bool, has_fixed_size<robotiq_3f_interfaces::msg::GraspingMode>::value && has_fixed_size<robotiq_3f_interfaces::msg::ObjectDetectionStatus>::value> {};

template<>
struct has_bounded_size<robotiq_3f_interfaces::msg::Status>
  : std::integral_constant<bool, has_bounded_size<robotiq_3f_interfaces::msg::GraspingMode>::value && has_bounded_size<robotiq_3f_interfaces::msg::ObjectDetectionStatus>::value> {};

template<>
struct is_message<robotiq_3f_interfaces::msg::Status>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__TRAITS_HPP_
