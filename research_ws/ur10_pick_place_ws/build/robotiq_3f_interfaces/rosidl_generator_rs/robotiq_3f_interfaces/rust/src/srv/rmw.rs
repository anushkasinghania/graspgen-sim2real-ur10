#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(msg: *mut ChangeGraspingMode_Request) -> bool;
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Request>, size: usize) -> bool;
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Request>);
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ChangeGraspingMode_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Request>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__srv__ChangeGraspingMode_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeGraspingMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: super::super::msg::rmw::GraspingMode,

}



impl Default for ChangeGraspingMode_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ChangeGraspingMode_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ChangeGraspingMode_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ChangeGraspingMode_Request where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/srv/ChangeGraspingMode_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode_Request() }
  }
}


#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response() -> *const std::ffi::c_void;
}

#[link(name = "robotiq_3f_interfaces__rosidl_generator_c")]
extern "C" {
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(msg: *mut ChangeGraspingMode_Response) -> bool;
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Response>, size: usize) -> bool;
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Response>);
    fn robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ChangeGraspingMode_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ChangeGraspingMode_Response>) -> bool;
}

// Corresponds to robotiq_3f_interfaces__srv__ChangeGraspingMode_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeGraspingMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ChangeGraspingMode_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init(&mut msg as *mut _) {
        panic!("Call to robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ChangeGraspingMode_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { robotiq_3f_interfaces__srv__ChangeGraspingMode_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ChangeGraspingMode_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ChangeGraspingMode_Response where Self: Sized {
  const TYPE_NAME: &'static str = "robotiq_3f_interfaces/srv/ChangeGraspingMode_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode_Response() }
  }
}






#[link(name = "robotiq_3f_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode() -> *const std::ffi::c_void;
}

// Corresponds to robotiq_3f_interfaces__srv__ChangeGraspingMode
#[allow(missing_docs, non_camel_case_types)]
pub struct ChangeGraspingMode;

impl rosidl_runtime_rs::Service for ChangeGraspingMode {
    type Request = ChangeGraspingMode_Request;
    type Response = ChangeGraspingMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__robotiq_3f_interfaces__srv__ChangeGraspingMode() }
    }
}


