// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:msg/SimpleControlCommand.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__msg__SimpleControlCommand __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__msg__SimpleControlCommand __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SimpleControlCommand_
{
  using Type = SimpleControlCommand_<ContainerAllocator>;

  explicit SimpleControlCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->position = 0.0;
      this->velocity = 0.0;
      this->force = 0.0;
    }
  }

  explicit SimpleControlCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->position = 0.0;
      this->velocity = 0.0;
      this->force = 0.0;
    }
  }

  // field types and members
  using _position_type =
    double;
  _position_type position;
  using _velocity_type =
    double;
  _velocity_type velocity;
  using _force_type =
    double;
  _force_type force;

  // setters for named parameter idiom
  Type & set__position(
    const double & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__velocity(
    const double & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__force(
    const double & _arg)
  {
    this->force = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__msg__SimpleControlCommand
    std::shared_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__msg__SimpleControlCommand
    std::shared_ptr<robotiq_3f_interfaces::msg::SimpleControlCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SimpleControlCommand_ & other) const
  {
    if (this->position != other.position) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->force != other.force) {
      return false;
    }
    return true;
  }
  bool operator!=(const SimpleControlCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SimpleControlCommand_

// alias to use template instance with default allocator
using SimpleControlCommand =
  robotiq_3f_interfaces::msg::SimpleControlCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__SIMPLE_CONTROL_COMMAND__STRUCT_HPP_
