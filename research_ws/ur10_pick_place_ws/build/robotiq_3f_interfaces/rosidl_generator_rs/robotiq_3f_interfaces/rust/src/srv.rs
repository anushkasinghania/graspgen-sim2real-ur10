#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to robotiq_3f_interfaces__srv__ChangeGraspingMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeGraspingMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode: super::msg::GraspingMode,

}



impl Default for ChangeGraspingMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeGraspingMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeGraspingMode_Request {
  type RmwMsg = super::srv::rmw::ChangeGraspingMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: super::msg::GraspingMode::into_rmw_message(std::borrow::Cow::Owned(msg.mode)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: super::msg::GraspingMode::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mode)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode: super::msg::GraspingMode::from_rmw_message(msg.mode),
    }
  }
}


// Corresponds to robotiq_3f_interfaces__srv__ChangeGraspingMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeGraspingMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ChangeGraspingMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeGraspingMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeGraspingMode_Response {
  type RmwMsg = super::srv::rmw::ChangeGraspingMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
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


