// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:msg/GraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__msg__GraspingMode __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__msg__GraspingMode __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct GraspingMode_
{
  using Type = GraspingMode_<ContainerAllocator>;

  explicit GraspingMode_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = 0;
    }
  }

  explicit GraspingMode_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode = 0;
    }
  }

  // field types and members
  using _mode_type =
    int8_t;
  _mode_type mode;

  // setters for named parameter idiom
  Type & set__mode(
    const int8_t & _arg)
  {
    this->mode = _arg;
    return *this;
  }

  // constant declarations
  static constexpr int8_t BASIC =
    0;
  static constexpr int8_t PINCH =
    1;
  static constexpr int8_t WIDE =
    2;
  static constexpr int8_t SCISSOR =
    3;

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__msg__GraspingMode
    std::shared_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__msg__GraspingMode
    std::shared_ptr<robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GraspingMode_ & other) const
  {
    if (this->mode != other.mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const GraspingMode_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GraspingMode_

// alias to use template instance with default allocator
using GraspingMode =
  robotiq_3f_interfaces::msg::GraspingMode_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t GraspingMode_<ContainerAllocator>::BASIC;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t GraspingMode_<ContainerAllocator>::PINCH;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t GraspingMode_<ContainerAllocator>::WIDE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t GraspingMode_<ContainerAllocator>::SCISSOR;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__GRASPING_MODE__STRUCT_HPP_
