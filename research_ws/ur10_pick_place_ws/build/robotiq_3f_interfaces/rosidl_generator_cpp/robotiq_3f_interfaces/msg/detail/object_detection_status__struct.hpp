// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:msg/ObjectDetectionStatus.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__msg__ObjectDetectionStatus __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__msg__ObjectDetectionStatus __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ObjectDetectionStatus_
{
  using Type = ObjectDetectionStatus_<ContainerAllocator>;

  explicit ObjectDetectionStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ObjectDetectionStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }

  // constant declarations
  static constexpr int8_t MOVING =
    0;
  static constexpr int8_t OBJECT_DETECTED_OPENING =
    1;
  static constexpr int8_t OBJECT_DETECTED_CLOSING =
    2;
  static constexpr int8_t AT_REQUESTED_POSITION =
    3;

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__msg__ObjectDetectionStatus
    std::shared_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__msg__ObjectDetectionStatus
    std::shared_ptr<robotiq_3f_interfaces::msg::ObjectDetectionStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ObjectDetectionStatus_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    return true;
  }
  bool operator!=(const ObjectDetectionStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ObjectDetectionStatus_

// alias to use template instance with default allocator
using ObjectDetectionStatus =
  robotiq_3f_interfaces::msg::ObjectDetectionStatus_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t ObjectDetectionStatus_<ContainerAllocator>::MOVING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t ObjectDetectionStatus_<ContainerAllocator>::OBJECT_DETECTED_OPENING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t ObjectDetectionStatus_<ContainerAllocator>::OBJECT_DETECTED_CLOSING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr int8_t ObjectDetectionStatus_<ContainerAllocator>::AT_REQUESTED_POSITION;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__MSG__DETAIL__OBJECT_DETECTION_STATUS__STRUCT_HPP_
