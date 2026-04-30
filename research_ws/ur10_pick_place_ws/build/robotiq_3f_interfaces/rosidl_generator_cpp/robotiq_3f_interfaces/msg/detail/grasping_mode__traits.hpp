// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_3f_interfaces:msg/GraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__TRAITS_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_3f_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const GraspingMode & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GraspingMode & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GraspingMode & msg, bool use_flow_style = false)
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
  const robotiq_3f_interfaces::msg::GraspingMode & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_3f_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_3f_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_3f_interfaces::msg::GraspingMode & msg)
{
  return robotiq_3f_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_3f_interfaces::msg::GraspingMode>()
{
  return "robotiq_3f_interfaces::msg::GraspingMode";
}

template<>
inline const char * name<robotiq_3f_interfaces::msg::GraspingMode>()
{
  return "robotiq_3f_interfaces/msg/GraspingMode";
}

template<>
struct has_fixed_size<robotiq_3f_interfaces::msg::GraspingMode>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_3f_interfaces::msg::GraspingMode>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_3f_interfaces::msg::GraspingMode>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__TRAITS_HPP_
