// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__BUILDER_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "robotiq_3f_interfaces/msg/detail/object_detection_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace robotiq_3f_interfaces
{

namespace msg
{

namespace builder
{

class Init_ObjectDetectionStatus_status
{
public:
  Init_ObjectDetectionStatus_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::robotiq_3f_interfaces::msg::ObjectDetectionStatus status(::robotiq_3f_interfaces::msg::ObjectDetectionStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::robotiq_3f_interfaces::msg::ObjectDetectionStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::robotiq_3f_interfaces::msg::ObjectDetectionStatus>()
{
  return robotiq_3f_interfaces::msg::builder::Init_ObjectDetectionStatus_status();
}

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__BUILDER_HPP_
