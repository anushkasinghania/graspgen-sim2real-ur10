// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'finger_a_object_detection'
// Member 'finger_b_object_detection'
// Member 'finger_c_object_detection'
// Member 'scissor_object_detection'
#include "robotiq_3f_interfaces/msg/detail/object_detection_status__struct.hpp"
// Member 'mode'
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__msg__Status __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__msg__Status __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Status_
{
  using Type = Status_<ContainerAllocator>;

  explicit Status_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : finger_a_object_detection(_init),
    finger_b_object_detection(_init),
    finger_c_object_detection(_init),
    scissor_object_detection(_init),
    mode(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->finger_a_position = 0;
      this->finger_b_position = 0;
      this->finger_c_position = 0;
      this->scissor_position = 0;
      this->finger_a_current = 0;
      this->finger_b_current = 0;
      this->finger_c_current = 0;
      this->scissor_current = 0;
      this->finger_a_cmd_echo = 0;
      this->finger_b_cmd_echo = 0;
      this->finger_c_cmd_echo = 0;
      this->scissor_cmd_echo = 0;
    }
  }

  explicit Status_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : finger_a_object_detection(_alloc, _init),
    finger_b_object_detection(_alloc, _init),
    finger_c_object_detection(_alloc, _init),
    scissor_object_detection(_alloc, _init),
    mode(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->finger_a_position = 0;
      this->finger_b_position = 0;
      this->finger_c_position = 0;
      this->scissor_position = 0;
      this->finger_a_current = 0;
      this->finger_b_current = 0;
      this->finger_c_current = 0;
      this->scissor_current = 0;
      this->finger_a_cmd_echo = 0;
      this->finger_b_cmd_echo = 0;
      this->finger_c_cmd_echo = 0;
      this->scissor_cmd_echo = 0;
    }
  }

  // field types and members
  using _finger_a_object_detection_type =
    robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>;
  _finger_a_object_detection_type finger_a_object_detection;
  using _finger_b_object_detection_type =
    robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>;
  _finger_b_object_detection_type finger_b_object_detection;
  using _finger_c_object_detection_type =
    robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>;
  _finger_c_object_detection_type finger_c_object_detection;
  using _scissor_object_detection_type =
    robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>;
  _scissor_object_detection_type scissor_object_detection;
  using _finger_a_position_type =
    uint8_t;
  _finger_a_position_type finger_a_position;
  using _finger_b_position_type =
    uint8_t;
  _finger_b_position_type finger_b_position;
  using _finger_c_position_type =
    uint8_t;
  _finger_c_position_type finger_c_position;
  using _scissor_position_type =
    uint8_t;
  _scissor_position_type scissor_position;
  using _finger_a_current_type =
    uint8_t;
  _finger_a_current_type finger_a_current;
  using _finger_b_current_type =
    uint8_t;
  _finger_b_current_type finger_b_current;
  using _finger_c_current_type =
    uint8_t;
  _finger_c_current_type finger_c_current;
  using _scissor_current_type =
    uint8_t;
  _scissor_current_type scissor_current;
  using _finger_a_cmd_echo_type =
    uint8_t;
  _finger_a_cmd_echo_type finger_a_cmd_echo;
  using _finger_b_cmd_echo_type =
    uint8_t;
  _finger_b_cmd_echo_type finger_b_cmd_echo;
  using _finger_c_cmd_echo_type =
    uint8_t;
  _finger_c_cmd_echo_type finger_c_cmd_echo;
  using _scissor_cmd_echo_type =
    uint8_t;
  _scissor_cmd_echo_type scissor_cmd_echo;
  using _mode_type =
    robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>;
  _mode_type mode;

  // setters for named parameter idiom
  Type & set__finger_a_object_detection(
    const robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> & _arg)
  {
    this->finger_a_object_detection = _arg;
    return *this;
  }
  Type & set__finger_b_object_detection(
    const robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> & _arg)
  {
    this->finger_b_object_detection = _arg;
    return *this;
  }
  Type & set__finger_c_object_detection(
    const robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> & _arg)
  {
    this->finger_c_object_detection = _arg;
    return *this;
  }
  Type & set__scissor_object_detection(
    const robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> & _arg)
  {
    this->scissor_object_detection = _arg;
    return *this;
  }
  Type & set__finger_a_position(
    const uint8_t & _arg)
  {
    this->finger_a_position = _arg;
    return *this;
  }
  Type & set__finger_b_position(
    const uint8_t & _arg)
  {
    this->finger_b_position = _arg;
    return *this;
  }
  Type & set__finger_c_position(
    const uint8_t & _arg)
  {
    this->finger_c_position = _arg;
    return *this;
  }
  Type & set__scissor_position(
    const uint8_t & _arg)
  {
    this->scissor_position = _arg;
    return *this;
  }
  Type & set__finger_a_current(
    const uint8_t & _arg)
  {
    this->finger_a_current = _arg;
    return *this;
  }
  Type & set__finger_b_current(
    const uint8_t & _arg)
  {
    this->finger_b_current = _arg;
    return *this;
  }
  Type & set__finger_c_current(
    const uint8_t & _arg)
  {
    this->finger_c_current = _arg;
    return *this;
  }
  Type & set__scissor_current(
    const uint8_t & _arg)
  {
    this->scissor_current = _arg;
    return *this;
  }
  Type & set__finger_a_cmd_echo(
    const uint8_t & _arg)
  {
    this->finger_a_cmd_echo = _arg;
    return *this;
  }
  Type & set__finger_b_cmd_echo(
    const uint8_t & _arg)
  {
    this->finger_b_cmd_echo = _arg;
    return *this;
  }
  Type & set__finger_c_cmd_echo(
    const uint8_t & _arg)
  {
    this->finger_c_cmd_echo = _arg;
    return *this;
  }
  Type & set__scissor_cmd_echo(
    const uint8_t & _arg)
  {
    this->scissor_cmd_echo = _arg;
    return *this;
  }
  Type & set__mode(
    const robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> & _arg)
  {
    this->mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::msg::Status_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::msg::Status_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::Status_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::Status_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__msg__Status
    std::shared_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__msg__Status
    std::shared_ptr<robotiq_3f_interfaces::msg::Status_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Status_ & other) const
  {
    if (this->finger_a_object_detection != other.finger_a_object_detection) {
      return false;
    }
    if (this->finger_b_object_detection != other.finger_b_object_detection) {
      return false;
    }
    if (this->finger_c_object_detection != other.finger_c_object_detection) {
      return false;
    }
    if (this->scissor_object_detection != other.scissor_object_detection) {
      return false;
    }
    if (this->finger_a_position != other.finger_a_position) {
      return false;
    }
    if (this->finger_b_position != other.finger_b_position) {
      return false;
    }
    if (this->finger_c_position != other.finger_c_position) {
      return false;
    }
    if (this->scissor_position != other.scissor_position) {
      return false;
    }
    if (this->finger_a_current != other.finger_a_current) {
      return false;
    }
    if (this->finger_b_current != other.finger_b_current) {
      return false;
    }
    if (this->finger_c_current != other.finger_c_current) {
      return false;
    }
    if (this->scissor_current != other.scissor_current) {
      return false;
    }
    if (this->finger_a_cmd_echo != other.finger_a_cmd_echo) {
      return false;
    }
    if (this->finger_b_cmd_echo != other.finger_b_cmd_echo) {
      return false;
    }
    if (this->finger_c_cmd_echo != other.finger_c_cmd_echo) {
      return false;
    }
    if (this->scissor_cmd_echo != other.scissor_cmd_echo) {
      return false;
    }
    if (this->mode != other.mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const Status_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Status_

// alias to use template instance with default allocator
using Status =
  robotiq_3f_interfaces::msg::Status_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__STATUS__STRUCT_HPP_
