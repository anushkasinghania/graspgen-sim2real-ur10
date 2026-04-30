// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace builder
{

class Init_IndependentControlCommand_scissor_force
{
public:
  explicit Init_IndependentControlCommand_scissor_force(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  ::robotiq_3f_interfaces::msg::IndependentControlCommand scissor_force(::robotiq_3f_interfaces::msg::IndependentControlCommand::_scissor_force_type arg)
  {
    msg_.scissor_force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_c_force
{
public:
  explicit Init_IndependentControlCommand_finger_c_force(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_scissor_force finger_c_force(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_c_force_type arg)
  {
    msg_.finger_c_force = std::move(arg);
    return Init_IndependentControlCommand_scissor_force(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_b_force
{
public:
  explicit Init_IndependentControlCommand_finger_b_force(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_c_force finger_b_force(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_b_force_type arg)
  {
    msg_.finger_b_force = std::move(arg);
    return Init_IndependentControlCommand_finger_c_force(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_a_force
{
public:
  explicit Init_IndependentControlCommand_finger_a_force(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_b_force finger_a_force(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_a_force_type arg)
  {
    msg_.finger_a_force = std::move(arg);
    return Init_IndependentControlCommand_finger_b_force(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_scissor_velocity
{
public:
  explicit Init_IndependentControlCommand_scissor_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_a_force scissor_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand::_scissor_velocity_type arg)
  {
    msg_.scissor_velocity = std::move(arg);
    return Init_IndependentControlCommand_finger_a_force(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_c_velocity
{
public:
  explicit Init_IndependentControlCommand_finger_c_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_scissor_velocity finger_c_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_c_velocity_type arg)
  {
    msg_.finger_c_velocity = std::move(arg);
    return Init_IndependentControlCommand_scissor_velocity(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_b_velocity
{
public:
  explicit Init_IndependentControlCommand_finger_b_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_c_velocity finger_b_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_b_velocity_type arg)
  {
    msg_.finger_b_velocity = std::move(arg);
    return Init_IndependentControlCommand_finger_c_velocity(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_a_velocity
{
public:
  explicit Init_IndependentControlCommand_finger_a_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_b_velocity finger_a_velocity(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_a_velocity_type arg)
  {
    msg_.finger_a_velocity = std::move(arg);
    return Init_IndependentControlCommand_finger_b_velocity(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_scissor_position
{
public:
  explicit Init_IndependentControlCommand_scissor_position(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_a_velocity scissor_position(::robotiq_3f_interfaces::msg::IndependentControlCommand::_scissor_position_type arg)
  {
    msg_.scissor_position = std::move(arg);
    return Init_IndependentControlCommand_finger_a_velocity(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_c_position
{
public:
  explicit Init_IndependentControlCommand_finger_c_position(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_scissor_position finger_c_position(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_c_position_type arg)
  {
    msg_.finger_c_position = std::move(arg);
    return Init_IndependentControlCommand_scissor_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_b_position
{
public:
  explicit Init_IndependentControlCommand_finger_b_position(::robotiq_3f_interfaces::msg::IndependentControlCommand & msg)
  : msg_(msg)
  {}
  Init_IndependentControlCommand_finger_c_position finger_b_position(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_b_position_type arg)
  {
    msg_.finger_b_position = std::move(arg);
    return Init_IndependentControlCommand_finger_c_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

class Init_IndependentControlCommand_finger_a_position
{
public:
  Init_IndependentControlCommand_finger_a_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IndependentControlCommand_finger_b_position finger_a_position(::robotiq_3f_interfaces::msg::IndependentControlCommand::_finger_a_position_type arg)
  {
    msg_.finger_a_position = std::move(arg);
    return Init_IndependentControlCommand_finger_b_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::IndependentControlCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::msg::IndependentControlCommand>()
{
  return robotiq_3f_interfaces::msg::builder::Init_IndependentControlCommand_finger_a_position();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__BUILDER_HPP_
