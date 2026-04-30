// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/msg/detail/status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace builder
{

class Init_Status_mode
{
public:
  explicit Init_Status_mode(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  ::robotiq_3f_interfaces::msg::Status mode(::robotiq_3f_interfaces::msg::Status::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_scissor_cmd_echo
{
public:
  explicit Init_Status_scissor_cmd_echo(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_mode scissor_cmd_echo(::robotiq_3f_interfaces::msg::Status::_scissor_cmd_echo_type arg)
  {
    msg_.scissor_cmd_echo = std::move(arg);
    return Init_Status_mode(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_c_cmd_echo
{
public:
  explicit Init_Status_finger_c_cmd_echo(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_scissor_cmd_echo finger_c_cmd_echo(::robotiq_3f_interfaces::msg::Status::_finger_c_cmd_echo_type arg)
  {
    msg_.finger_c_cmd_echo = std::move(arg);
    return Init_Status_scissor_cmd_echo(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_b_cmd_echo
{
public:
  explicit Init_Status_finger_b_cmd_echo(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_c_cmd_echo finger_b_cmd_echo(::robotiq_3f_interfaces::msg::Status::_finger_b_cmd_echo_type arg)
  {
    msg_.finger_b_cmd_echo = std::move(arg);
    return Init_Status_finger_c_cmd_echo(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_a_cmd_echo
{
public:
  explicit Init_Status_finger_a_cmd_echo(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_b_cmd_echo finger_a_cmd_echo(::robotiq_3f_interfaces::msg::Status::_finger_a_cmd_echo_type arg)
  {
    msg_.finger_a_cmd_echo = std::move(arg);
    return Init_Status_finger_b_cmd_echo(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_scissor_current
{
public:
  explicit Init_Status_scissor_current(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_a_cmd_echo scissor_current(::robotiq_3f_interfaces::msg::Status::_scissor_current_type arg)
  {
    msg_.scissor_current = std::move(arg);
    return Init_Status_finger_a_cmd_echo(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_c_current
{
public:
  explicit Init_Status_finger_c_current(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_scissor_current finger_c_current(::robotiq_3f_interfaces::msg::Status::_finger_c_current_type arg)
  {
    msg_.finger_c_current = std::move(arg);
    return Init_Status_scissor_current(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_b_current
{
public:
  explicit Init_Status_finger_b_current(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_c_current finger_b_current(::robotiq_3f_interfaces::msg::Status::_finger_b_current_type arg)
  {
    msg_.finger_b_current = std::move(arg);
    return Init_Status_finger_c_current(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_a_current
{
public:
  explicit Init_Status_finger_a_current(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_b_current finger_a_current(::robotiq_3f_interfaces::msg::Status::_finger_a_current_type arg)
  {
    msg_.finger_a_current = std::move(arg);
    return Init_Status_finger_b_current(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_scissor_position
{
public:
  explicit Init_Status_scissor_position(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_a_current scissor_position(::robotiq_3f_interfaces::msg::Status::_scissor_position_type arg)
  {
    msg_.scissor_position = std::move(arg);
    return Init_Status_finger_a_current(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_c_position
{
public:
  explicit Init_Status_finger_c_position(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_scissor_position finger_c_position(::robotiq_3f_interfaces::msg::Status::_finger_c_position_type arg)
  {
    msg_.finger_c_position = std::move(arg);
    return Init_Status_scissor_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_b_position
{
public:
  explicit Init_Status_finger_b_position(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_c_position finger_b_position(::robotiq_3f_interfaces::msg::Status::_finger_b_position_type arg)
  {
    msg_.finger_b_position = std::move(arg);
    return Init_Status_finger_c_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_a_position
{
public:
  explicit Init_Status_finger_a_position(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_b_position finger_a_position(::robotiq_3f_interfaces::msg::Status::_finger_a_position_type arg)
  {
    msg_.finger_a_position = std::move(arg);
    return Init_Status_finger_b_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_scissor_object_detection
{
public:
  explicit Init_Status_scissor_object_detection(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_a_position scissor_object_detection(::robotiq_3f_interfaces::msg::Status::_scissor_object_detection_type arg)
  {
    msg_.scissor_object_detection = std::move(arg);
    return Init_Status_finger_a_position(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_c_object_detection
{
public:
  explicit Init_Status_finger_c_object_detection(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_scissor_object_detection finger_c_object_detection(::robotiq_3f_interfaces::msg::Status::_finger_c_object_detection_type arg)
  {
    msg_.finger_c_object_detection = std::move(arg);
    return Init_Status_scissor_object_detection(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_b_object_detection
{
public:
  explicit Init_Status_finger_b_object_detection(::robotiq_3f_interfaces::msg::Status & msg)
  : msg_(msg)
  {}
  Init_Status_finger_c_object_detection finger_b_object_detection(::robotiq_3f_interfaces::msg::Status::_finger_b_object_detection_type arg)
  {
    msg_.finger_b_object_detection = std::move(arg);
    return Init_Status_finger_c_object_detection(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

class Init_Status_finger_a_object_detection
{
public:
  Init_Status_finger_a_object_detection()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Status_finger_b_object_detection finger_a_object_detection(::robotiq_3f_interfaces::msg::Status::_finger_a_object_detection_type arg)
  {
    msg_.finger_a_object_detection = std::move(arg);
    return Init_Status_finger_b_object_detection(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::Status msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::msg::Status>()
{
  return robotiq_3f_interfaces::msg::builder::Init_Status_finger_a_object_detection();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__BUILDER_HPP_
