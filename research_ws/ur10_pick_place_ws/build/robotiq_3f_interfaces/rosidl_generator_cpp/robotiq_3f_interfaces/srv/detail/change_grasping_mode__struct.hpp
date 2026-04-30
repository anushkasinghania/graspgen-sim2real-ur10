// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from robotiq_3f_interfaces:srv/ChangeGraspingMode.idl
// generated code does not contain a copyright notice

#ifndef ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_HPP_
#define ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'mode'
#include "robotiq_3f_interfaces/msg/detail/grasping_mode__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChangeGraspingMode_Request_
{
  using Type = ChangeGraspingMode_Request_<ContainerAllocator>;

  explicit ChangeGraspingMode_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mode(_init)
  {
    (void)_init;
  }

  explicit ChangeGraspingMode_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mode(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _mode_type =
    robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator>;
  _mode_type mode;

  // setters for named parameter idiom
  Type & set__mode(
    const robotiq_3f_interfaces::msg::GraspingMode_<ContainerAllocator> & _arg)
  {
    this->mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChangeGraspingMode_Request_ & other) const
  {
    if (this->mode != other.mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChangeGraspingMode_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChangeGraspingMode_Request_

// alias to use template instance with default allocator
using ChangeGraspingMode_Request =
  robotiq_3f_interfaces::srv::ChangeGraspingMode_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robotiq_3f_interfaces


#ifndef _WIN32
# define DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response __attribute__((deprecated))
#else
# define DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response __declspec(deprecated)
#endif

namespace robotiq_3f_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ChangeGraspingMode_Response_
{
  using Type = ChangeGraspingMode_Response_<ContainerAllocator>;

  explicit ChangeGraspingMode_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit ChangeGraspingMode_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response
    std::shared_ptr<robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ChangeGraspingMode_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const ChangeGraspingMode_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ChangeGraspingMode_Response_

// alias to use template instance with default allocator
using ChangeGraspingMode_Response =
  robotiq_3f_interfaces::srv::ChangeGraspingMode_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace robotiq_3f_interfaces

namespace robotiq_3f_interfaces
{

namespace srv
{

struct ChangeGraspingMode
{
  using Request = robotiq_3f_interfaces::srv::ChangeGraspingMode_Request;
  using Response = robotiq_3f_interfaces::srv::ChangeGraspingMode_Response;
};

}  // namespace srv

}  // namespace robotiq_3f_interfaces

#endif  // ROBOTIQ_3F_INTERFACES__SRV__DETAIL__CHANGE_GRASPING_MODE__STRUCT_HPP_
