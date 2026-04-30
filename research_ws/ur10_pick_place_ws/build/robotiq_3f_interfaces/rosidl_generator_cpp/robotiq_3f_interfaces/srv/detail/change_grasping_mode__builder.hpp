// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:srv/ChangeGraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/srv/detail/change_grasping_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeGraspingMode_Request_mode
{
public:
  Init_ChangeGraspingMode_Request_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robotiq_3f_interfaces::srv::ChangeGraspingMode_Request mode(::robotiq_3f_interfaces::srv::ChangeGraspingMode_Request::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::srv::ChangeGraspingMode_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::srv::ChangeGraspingMode_Request>()
{
  return robotiq_3f_interfaces::srv::builder::Init_ChangeGraspingMode_Request_mode();
}

}  // namespace robotiq_3f_interfaces


namespace robotiq_3f_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeGraspingMode_Response_success
{
public:
  Init_ChangeGraspingMode_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robotiq_3f_interfaces::srv::ChangeGraspingMode_Response success(::robotiq_3f_interfaces::srv::ChangeGraspingMode_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::srv::ChangeGraspingMode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::srv::ChangeGraspingMode_Response>()
{
  return robotiq_3f_interfaces::srv::builder::Init_ChangeGraspingMode_Response_success();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__BUILDER_HPP_
