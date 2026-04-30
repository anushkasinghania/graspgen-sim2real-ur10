// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__TRAITS_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace robotiq_3f_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const IndependentControlCommand & msg,
  std::ostream & out)
{
  out << "{";
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

  // member: finger_a_velocity
  {
    out << "finger_a_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_velocity, out);
    out << ", ";
  }

  // member: finger_b_velocity
  {
    out << "finger_b_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_velocity, out);
    out << ", ";
  }

  // member: finger_c_velocity
  {
    out << "finger_c_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_velocity, out);
    out << ", ";
  }

  // member: scissor_velocity
  {
    out << "scissor_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_velocity, out);
    out << ", ";
  }

  // member: finger_a_force
  {
    out << "finger_a_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_force, out);
    out << ", ";
  }

  // member: finger_b_force
  {
    out << "finger_b_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_force, out);
    out << ", ";
  }

  // member: finger_c_force
  {
    out << "finger_c_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_force, out);
    out << ", ";
  }

  // member: scissor_force
  {
    out << "scissor_force: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_force, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IndependentControlCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
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

  // member: finger_a_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_velocity, out);
    out << "\n";
  }

  // member: finger_b_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_velocity, out);
    out << "\n";
  }

  // member: finger_c_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_velocity, out);
    out << "\n";
  }

  // member: scissor_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_velocity, out);
    out << "\n";
  }

  // member: finger_a_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_a_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_a_force, out);
    out << "\n";
  }

  // member: finger_b_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_b_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_b_force, out);
    out << "\n";
  }

  // member: finger_c_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finger_c_force: ";
    rosidl_generator_traits::value_to_yaml(msg.finger_c_force, out);
    out << "\n";
  }

  // member: scissor_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scissor_force: ";
    rosidl_generator_traits::value_to_yaml(msg.scissor_force, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IndependentControlCommand & msg, bool use_flow_style = false)
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
  const robotiq_3f_interfaces::msg::IndependentControlCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  robotiq_3f_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use robotiq_3f_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
{
  return robotiq_3f_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<robotiq_3f_interfaces::msg::IndependentControlCommand>()
{
  return "robotiq_3f_interfaces::msg::IndependentControlCommand";
}

template<>
inline const char * name<robotiq_3f_interfaces::msg::IndependentControlCommand>()
{
  return "robotiq_3f_interfaces/msg/IndependentControlCommand";
}

template<>
struct has_fixed_size<robotiq_3f_interfaces::msg::IndependentControlCommand>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<robotiq_3f_interfaces::msg::IndependentControlCommand>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<robotiq_3f_interfaces::msg::IndependentControlCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__TRAITS_HPP_
