// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__msg__IndependentControlCommand __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__msg__IndependentControlCommand __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IndependentControlCommand_
{
  using Type = IndependentControlCommand_<ContainerAllocator>;

  explicit IndependentControlCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->finger_a_position = 0.0;
      this->finger_b_position = 0.0;
      this->finger_c_position = 0.0;
      this->scissor_position = 0.0;
      this->finger_a_velocity = 0.0;
      this->finger_b_velocity = 0.0;
      this->finger_c_velocity = 0.0;
      this->scissor_velocity = 0.0;
      this->finger_a_force = 0.0;
      this->finger_b_force = 0.0;
      this->finger_c_force = 0.0;
      this->scissor_force = 0.0;
    }
  }

  explicit IndependentControlCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->finger_a_position = 0.0;
      this->finger_b_position = 0.0;
      this->finger_c_position = 0.0;
      this->scissor_position = 0.0;
      this->finger_a_velocity = 0.0;
      this->finger_b_velocity = 0.0;
      this->finger_c_velocity = 0.0;
      this->scissor_velocity = 0.0;
      this->finger_a_force = 0.0;
      this->finger_b_force = 0.0;
      this->finger_c_force = 0.0;
      this->scissor_force = 0.0;
    }
  }

  // field types and members
  using _finger_a_position_type =
    double;
  _finger_a_position_type finger_a_position;
  using _finger_b_position_type =
    double;
  _finger_b_position_type finger_b_position;
  using _finger_c_position_type =
    double;
  _finger_c_position_type finger_c_position;
  using _scissor_position_type =
    double;
  _scissor_position_type scissor_position;
  using _finger_a_velocity_type =
    double;
  _finger_a_velocity_type finger_a_velocity;
  using _finger_b_velocity_type =
    double;
  _finger_b_velocity_type finger_b_velocity;
  using _finger_c_velocity_type =
    double;
  _finger_c_velocity_type finger_c_velocity;
  using _scissor_velocity_type =
    double;
  _scissor_velocity_type scissor_velocity;
  using _finger_a_force_type =
    double;
  _finger_a_force_type finger_a_force;
  using _finger_b_force_type =
    double;
  _finger_b_force_type finger_b_force;
  using _finger_c_force_type =
    double;
  _finger_c_force_type finger_c_force;
  using _scissor_force_type =
    double;
  _scissor_force_type scissor_force;

  // setters for named parameter idiom
  Type & set__finger_a_position(
    const double & _arg)
  {
    this->finger_a_position = _arg;
    return *this;
  }
  Type & set__finger_b_position(
    const double & _arg)
  {
    this->finger_b_position = _arg;
    return *this;
  }
  Type & set__finger_c_position(
    const double & _arg)
  {
    this->finger_c_position = _arg;
    return *this;
  }
  Type & set__scissor_position(
    const double & _arg)
  {
    this->scissor_position = _arg;
    return *this;
  }
  Type & set__finger_a_velocity(
    const double & _arg)
  {
    this->finger_a_velocity = _arg;
    return *this;
  }
  Type & set__finger_b_velocity(
    const double & _arg)
  {
    this->finger_b_velocity = _arg;
    return *this;
  }
  Type & set__finger_c_velocity(
    const double & _arg)
  {
    this->finger_c_velocity = _arg;
    return *this;
  }
  Type & set__scissor_velocity(
    const double & _arg)
  {
    this->scissor_velocity = _arg;
    return *this;
  }
  Type & set__finger_a_force(
    const double & _arg)
  {
    this->finger_a_force = _arg;
    return *this;
  }
  Type & set__finger_b_force(
    const double & _arg)
  {
    this->finger_b_force = _arg;
    return *this;
  }
  Type & set__finger_c_force(
    const double & _arg)
  {
    this->finger_c_force = _arg;
    return *this;
  }
  Type & set__scissor_force(
    const double & _arg)
  {
    this->scissor_force = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__msg__IndependentControlCommand
    std::shared_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__msg__IndependentControlCommand
    std::shared_ptr<robotiq_3f_interfaces::msg::IndependentControlCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IndependentControlCommand_ & other) const
  {
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
    if (this->finger_a_velocity != other.finger_a_velocity) {
      return false;
    }
    if (this->finger_b_velocity != other.finger_b_velocity) {
      return false;
    }
    if (this->finger_c_velocity != other.finger_c_velocity) {
      return false;
    }
    if (this->scissor_velocity != other.scissor_velocity) {
      return false;
    }
    if (this->finger_a_force != other.finger_a_force) {
      return false;
    }
    if (this->finger_b_force != other.finger_b_force) {
      return false;
    }
    if (this->finger_c_force != other.finger_c_force) {
      return false;
    }
    if (this->scissor_force != other.scissor_force) {
      return false;
    }
    return true;
  }
  bool operator!=(const IndependentControlCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IndependentControlCommand_

// alias to use template instance with default allocator
using IndependentControlCommand =
  robotiq_3f_interfaces::msg::IndependentControlCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__INDEPENDENT_CONTROL_COMMAND__STRUCT_HPP_
