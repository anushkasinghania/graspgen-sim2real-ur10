// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:msg/SimpleControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/msg/detail/simple_control_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace builder
{

class Init_SimpleControlCommand_force
{
public:
  explicit Init_SimpleControlCommand_force(::robotiq_3f_interfaces::msg::SimpleControlCommand & msg)
  : msg_(msg)
  {}
  ::robotiq_3f_interfaces::msg::SimpleControlCommand force(::robotiq_3f_interfaces::msg::SimpleControlCommand::_force_type arg)
  {
    msg_.force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::SimpleControlCommand msg_;
};

class Init_SimpleControlCommand_velocity
{
public:
  explicit Init_SimpleControlCommand_velocity(::robotiq_3f_interfaces::msg::SimpleControlCommand & msg)
  : msg_(msg)
  {}
  Init_SimpleControlCommand_force velocity(::robotiq_3f_interfaces::msg::SimpleControlCommand::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_SimpleControlCommand_force(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::SimpleControlCommand msg_;
};

class Init_SimpleControlCommand_position
{
public:
  Init_SimpleControlCommand_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SimpleControlCommand_velocity position(::robotiq_3f_interfaces::msg::SimpleControlCommand::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_SimpleControlCommand_velocity(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::SimpleControlCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::msg::SimpleControlCommand>()
{
  return robotiq_3f_interfaces::msg::builder::Init_SimpleControlCommand_position();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__BUILDER_HPP_
