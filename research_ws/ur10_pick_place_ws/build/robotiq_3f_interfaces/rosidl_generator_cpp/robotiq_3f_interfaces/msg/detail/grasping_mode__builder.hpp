// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:msg/GraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace builder
{

class Init_GraspingMode_mode
{
public:
  Init_GraspingMode_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robotiq_3f_interfaces::msg::GraspingMode mode(::robotiq_3f_interfaces::msg::GraspingMode::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::GraspingMode msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::msg::GraspingMode>()
{
  return robotiq_3f_interfaces::msg::builder::Init_GraspingMode_mode();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__BUILDER_HPP_
