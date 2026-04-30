#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__AttachLink_Request() -> *const std::ffi::c_void;
}

#[link(name = "linkattacher_msgs__rosidl_generator_c")]
extern "C" {
    fn linkattacher_msgs__srv__AttachLink_Request__init(msg: *mut AttachLink_Request) -> bool;
    fn linkattacher_msgs__srv__AttachLink_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Request>, size: usize) -> bool;
    fn linkattacher_msgs__srv__AttachLink_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Request>);
    fn linkattacher_msgs__srv__AttachLink_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AttachLink_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Request>) -> bool;
}

// Corresponds to linkattacher_msgs__srv__AttachLink_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttachLink_Request {
    /// Name of the first model.
    pub model1_name: rosidl_runtime_rs::String,

    /// Name of the link in the first model.
    pub link1_name: rosidl_runtime_rs::String,

    /// Name of the second model.
    pub model2_name: rosidl_runtime_rs::String,

    /// Name of the link in the second model.
    pub link2_name: rosidl_runtime_rs::String,

}



impl Default for AttachLink_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !linkattacher_msgs__srv__AttachLink_Request__init(&mut msg as *mut _) {
        panic!("Call to linkattacher_msgs__srv__AttachLink_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AttachLink_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AttachLink_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AttachLink_Request where Self: Sized {
  const TYPE_NAME: &'static str = "linkattacher_msgs/srv/AttachLink_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__AttachLink_Request() }
  }
}


#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__AttachLink_Response() -> *const std::ffi::c_void;
}

#[link(name = "linkattacher_msgs__rosidl_generator_c")]
extern "C" {
    fn linkattacher_msgs__srv__AttachLink_Response__init(msg: *mut AttachLink_Response) -> bool;
    fn linkattacher_msgs__srv__AttachLink_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Response>, size: usize) -> bool;
    fn linkattacher_msgs__srv__AttachLink_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Response>);
    fn linkattacher_msgs__srv__AttachLink_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AttachLink_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<AttachLink_Response>) -> bool;
}

// Corresponds to linkattacher_msgs__srv__AttachLink_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttachLink_Response {
    /// Whether the links were successfully attached or not.
    pub success: bool,

    /// Feedback message.
    pub message: rosidl_runtime_rs::String,

}



impl Default for AttachLink_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !linkattacher_msgs__srv__AttachLink_Response__init(&mut msg as *mut _) {
        panic!("Call to linkattacher_msgs__srv__AttachLink_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AttachLink_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__AttachLink_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AttachLink_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AttachLink_Response where Self: Sized {
  const TYPE_NAME: &'static str = "linkattacher_msgs/srv/AttachLink_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__AttachLink_Response() }
  }
}


#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__DetachLink_Request() -> *const std::ffi::c_void;
}

#[link(name = "linkattacher_msgs__rosidl_generator_c")]
extern "C" {
    fn linkattacher_msgs__srv__DetachLink_Request__init(msg: *mut DetachLink_Request) -> bool;
    fn linkattacher_msgs__srv__DetachLink_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Request>, size: usize) -> bool;
    fn linkattacher_msgs__srv__DetachLink_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Request>);
    fn linkattacher_msgs__srv__DetachLink_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DetachLink_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Request>) -> bool;
}

// Corresponds to linkattacher_msgs__srv__DetachLink_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetachLink_Request {
    /// Name of the first model.
    pub model1_name: rosidl_runtime_rs::String,

    /// Name of the link in the first model.
    pub link1_name: rosidl_runtime_rs::String,

    /// Name of the second model.
    pub model2_name: rosidl_runtime_rs::String,

    /// Name of the link in the second model.
    pub link2_name: rosidl_runtime_rs::String,

}



impl Default for DetachLink_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !linkattacher_msgs__srv__DetachLink_Request__init(&mut msg as *mut _) {
        panic!("Call to linkattacher_msgs__srv__DetachLink_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DetachLink_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DetachLink_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DetachLink_Request where Self: Sized {
  const TYPE_NAME: &'static str = "linkattacher_msgs/srv/DetachLink_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__DetachLink_Request() }
  }
}


#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__DetachLink_Response() -> *const std::ffi::c_void;
}

#[link(name = "linkattacher_msgs__rosidl_generator_c")]
extern "C" {
    fn linkattacher_msgs__srv__DetachLink_Response__init(msg: *mut DetachLink_Response) -> bool;
    fn linkattacher_msgs__srv__DetachLink_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Response>, size: usize) -> bool;
    fn linkattacher_msgs__srv__DetachLink_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Response>);
    fn linkattacher_msgs__srv__DetachLink_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DetachLink_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<DetachLink_Response>) -> bool;
}

// Corresponds to linkattacher_msgs__srv__DetachLink_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetachLink_Response {
    /// Whether the links were successfully attached or not.
    pub success: bool,

    /// Feedback message.
    pub message: rosidl_runtime_rs::String,

}



impl Default for DetachLink_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !linkattacher_msgs__srv__DetachLink_Response__init(&mut msg as *mut _) {
        panic!("Call to linkattacher_msgs__srv__DetachLink_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DetachLink_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { linkattacher_msgs__srv__DetachLink_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DetachLink_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DetachLink_Response where Self: Sized {
  const TYPE_NAME: &'static str = "linkattacher_msgs/srv/DetachLink_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__linkattacher_msgs__srv__DetachLink_Response() }
  }
}






#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__linkattacher_msgs__srv__AttachLink() -> *const std::ffi::c_void;
}

// Corresponds to linkattacher_msgs__srv__AttachLink
#[allow(missing_docs, non_camel_case_types)]
pub struct AttachLink;

impl rosidl_runtime_rs::Service for AttachLink {
    type Request = AttachLink_Request;
    type Response = AttachLink_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__linkattacher_msgs__srv__AttachLink() }
    }
}




#[link(name = "linkattacher_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__linkattacher_msgs__srv__DetachLink() -> *const std::ffi::c_void;
}

// Corresponds to linkattacher_msgs__srv__DetachLink
#[allow(missing_docs, non_camel_case_types)]
pub struct DetachLink;

impl rosidl_runtime_rs::Service for DetachLink {
    type Request = DetachLink_Request;
    type Response = DetachLink_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__linkattacher_msgs__srv__DetachLink() }
    }
}


