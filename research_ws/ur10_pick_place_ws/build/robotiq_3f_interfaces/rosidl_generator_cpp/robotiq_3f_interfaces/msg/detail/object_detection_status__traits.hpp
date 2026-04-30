// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__TRAITS_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_3f_interfaces/msg/detail/object_detection_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_3f_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ObjectDetectionStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ObjectDetectionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ObjectDetectionStatus & msg, bool use_flow_style = false)
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
  const robotiq_3f_interfaces::msg::ObjectDetectionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_3f_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_3f_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_3f_interfaces::msg::ObjectDetectionStatus & msg)
{
  return robotiq_3f_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_3f_interfaces::msg::ObjectDetectionStatus>()
{
  return "robotiq_3f_interfaces::msg::ObjectDetectionStatus";
}

template<>
inline const char * name<robotiq_3f_interfaces::msg::ObjectDetectionStatus>()
{
  return "robotiq_3f_interfaces/msg/ObjectDetectionStatus";
}

template<>
struct has_fixed_size<robotiq_3f_interfaces::msg::ObjectDetectionStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_3f_interfaces::msg::ObjectDetectionStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_3f_interfaces::msg::ObjectDetectionStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__TRAITS_HPP_
