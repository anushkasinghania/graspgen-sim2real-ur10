#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__ObjectDetectionStatus() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(msg: *mut ObjectDetectionStatus) -> bool;
    fn robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObjectDetectionStatus>, size: usize) -> bool;
    fn robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObjectDetectionStatus>);
    fn robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObjectDetectionStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<ObjectDetectionStatus>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__msg__ObjectDetectionStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Reports whether an object has been gripped or not.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObjectDetectionStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,

}

impl ObjectDetectionStatus {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOVING: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OBJECT_DETECTED_OPENING: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OBJECT_DETECTED_CLOSING: i8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const AT_REQUESTED_POSITION: i8 = 3;

}


impl Default for ObjectDetectionStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__msg__ObjectDetectionStatus__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__msg__ObjectDetectionStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObjectDetectionStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__ObjectDetectionStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObjectDetectionStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObjectDetectionStatus where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/msg/ObjectDetectionStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__ObjectDetectionStatus() }
  }
}


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__Status() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__msg__Status__init(msg: *mut Status) -> bool;
    fn robotiq_3f_interfaces__msg__Status__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Status>, size: usize) -> bool;
    fn robotiq_3f_interfaces__msg__Status__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Status>);
    fn robotiq_3f_interfaces__msg__Status__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Status>, out_seq: *mut rosidl_runtime_rs::Sequence<Status>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__msg__Status
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Reports whether an object has been gripped or not.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Status {

    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_object_detection: super::super::msg::rmw::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_object_detection: super::super::msg::rmw::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_object_detection: super::super::msg::rmw::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_object_detection: super::super::msg::rmw::ObjectDetectionStatus,

    /// Actuator states
    pub finger_a_position: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_position: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_position: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_position: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_current: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_current: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_current: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_current: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_cmd_echo: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_cmd_echo: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_cmd_echo: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_cmd_echo: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: super::super::msg::rmw::GraspingMode,

}



impl Default for Status {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__msg__Status__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__msg__Status__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Status {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__Status__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__Status__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__Status__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Status {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Status where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/msg/Status";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__Status() }
  }
}


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__GraspingMode() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__msg__GraspingMode__init(msg: *mut GraspingMode) -> bool;
    fn robotiq_3f_interfaces__msg__GraspingMode__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GraspingMode>, size: usize) -> bool;
    fn robotiq_3f_interfaces__msg__GraspingMode__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GraspingMode>);
    fn robotiq_3f_interfaces__msg__GraspingMode__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GraspingMode>, out_seq: *mut rosidl_runtime_rs::Sequence<GraspingMode>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__msg__GraspingMode
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GraspingMode {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: i8,

}

impl GraspingMode {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const BASIC: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PINCH: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WIDE: i8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SCISSOR: i8 = 3;

}


impl Default for GraspingMode {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__msg__GraspingMode__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__msg__GraspingMode__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GraspingMode {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__GraspingMode__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__GraspingMode__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__GraspingMode__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GraspingMode {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GraspingMode where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/msg/GraspingMode";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__GraspingMode() }
  }
}


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__SimpleControlCommand() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__msg__SimpleControlCommand__init(msg: *mut SimpleControlCommand) -> bool;
    fn robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SimpleControlCommand>, size: usize) -> bool;
    fn robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SimpleControlCommand>);
    fn robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SimpleControlCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<SimpleControlCommand>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__msg__SimpleControlCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SimpleControlCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub force: f64,

}



impl Default for SimpleControlCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__msg__SimpleControlCommand__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__msg__SimpleControlCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SimpleControlCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__SimpleControlCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SimpleControlCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SimpleControlCommand where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/msg/SimpleControlCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__SimpleControlCommand() }
  }
}


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__IndependentControlCommand() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__msg__IndependentControlCommand__init(msg: *mut IndependentControlCommand) -> bool;
    fn robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<IndependentControlCommand>, size: usize) -> bool;
    fn robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<IndependentControlCommand>);
    fn robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<IndependentControlCommand>, out_seq: *mut rosidl_runtime_rs::Sequence<IndependentControlCommand>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__msg__IndependentControlCommand
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IndependentControlCommand {

    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_position: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_position: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_position: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_position: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_velocity: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_force: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_force: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_force: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_force: f64,

}



impl Default for IndependentControlCommand {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__msg__IndependentControlCommand__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__msg__IndependentControlCommand__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for IndependentControlCommand {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__msg__IndependentControlCommand__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for IndependentControlCommand {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for IndependentControlCommand where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/msg/IndependentControlCommand";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__msg__IndependentControlCommand() }
  }
}


