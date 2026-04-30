// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_3f_interfaces:msg/SimpleControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__TRAITS_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_3f_interfaces/msg/detail/simple_control_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_3f_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const SimpleControlCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: position
  {
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << ", ";
  }

  // member: force
  {
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SimpleControlCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position: ";
    rosidl_generator_traits::value_to_yaml(msg.position, out);
    out << "\n";
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << "\n";
  }

  // member: force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force: ";
    rosidl_generator_traits::value_to_yaml(msg.force, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SimpleControlCommand & msg, bool use_flow_style = false)
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
  const robotiq_3f_interfaces::msg::SimpleControlCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_3f_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_3f_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_3f_interfaces::msg::SimpleControlCommand & msg)
{
  return robotiq_3f_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_3f_interfaces::msg::SimpleControlCommand>()
{
  return "robotiq_3f_interfaces::msg::SimpleControlCommand";
}

template<>
inline const char * name<robotiq_3f_interfaces::msg::SimpleControlCommand>()
{
  return "robotiq_3f_interfaces/msg/SimpleControlCommand";
}

template<>
struct has_fixed_size<robotiq_3f_interfaces::msg::SimpleControlCommand>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_3f_interfaces::msg::SimpleControlCommand>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_3f_interfaces::msg::SimpleControlCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__TRAITS_HPP_
