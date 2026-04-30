#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to linkattacher_msgs__srv__AttachLink_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttachLink_Request {
    /// Name of the first model.
    pub model1_name: std::string::String,

    /// Name of the link in the first model.
    pub link1_name: std::string::String,

    /// Name of the second model.
    pub model2_name: std::string::String,

    /// Name of the link in the second model.
    pub link2_name: std::string::String,

}



impl Default for AttachLink_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AttachLink_Request::default())
  }
}

impl rosidl_runtime_rs::Message for AttachLink_Request {
  type RmwMsg = super::srv::rmw::AttachLink_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model1_name: msg.model1_name.as_str().into(),
        link1_name: msg.link1_name.as_str().into(),
        model2_name: msg.model2_name.as_str().into(),
        link2_name: msg.link2_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model1_name: msg.model1_name.as_str().into(),
        link1_name: msg.link1_name.as_str().into(),
        model2_name: msg.model2_name.as_str().into(),
        link2_name: msg.link2_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model1_name: msg.model1_name.to_string(),
      link1_name: msg.link1_name.to_string(),
      model2_name: msg.model2_name.to_string(),
      link2_name: msg.link2_name.to_string(),
    }
  }
}


// Corresponds to linkattacher_msgs__srv__AttachLink_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttachLink_Response {
    /// Whether the links were successfully attached or not.
    pub success: bool,

    /// Feedback message.
    pub message: std::string::String,

}



impl Default for AttachLink_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AttachLink_Response::default())
  }
}

impl rosidl_runtime_rs::Message for AttachLink_Response {
  type RmwMsg = super::srv::rmw::AttachLink_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to linkattacher_msgs__srv__DetachLink_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetachLink_Request {
    /// Name of the first model.
    pub model1_name: std::string::String,

    /// Name of the link in the first model.
    pub link1_name: std::string::String,

    /// Name of the second model.
    pub model2_name: std::string::String,

    /// Name of the link in the second model.
    pub link2_name: std::string::String,

}



impl Default for DetachLink_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DetachLink_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DetachLink_Request {
  type RmwMsg = super::srv::rmw::DetachLink_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model1_name: msg.model1_name.as_str().into(),
        link1_name: msg.link1_name.as_str().into(),
        model2_name: msg.model2_name.as_str().into(),
        link2_name: msg.link2_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model1_name: msg.model1_name.as_str().into(),
        link1_name: msg.link1_name.as_str().into(),
        model2_name: msg.model2_name.as_str().into(),
        link2_name: msg.link2_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model1_name: msg.model1_name.to_string(),
      link1_name: msg.link1_name.to_string(),
      model2_name: msg.model2_name.to_string(),
      link2_name: msg.link2_name.to_string(),
    }
  }
}


// Corresponds to linkattacher_msgs__srv__DetachLink_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DetachLink_Response {
    /// Whether the links were successfully attached or not.
    pub success: bool,

    /// Feedback message.
    pub message: std::string::String,

}



impl Default for DetachLink_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DetachLink_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DetachLink_Response {
  type RmwMsg = super::srv::rmw::DetachLink_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
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


