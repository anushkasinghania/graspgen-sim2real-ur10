#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to robotiq_3f_interfaces__msg__ObjectDetectionStatus
/// Reports whether an object has been gripped or not.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObjectDetectionStatus::default())
  }
}

impl rosidl_runtime_rs::Message for ObjectDetectionStatus {
  type RmwMsg = super::msg::rmw::ObjectDetectionStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
    }
  }
}


// Corresponds to robotiq_3f_interfaces__msg__Status
/// Reports whether an object has been gripped or not.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Status {

    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_a_object_detection: super::msg::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_b_object_detection: super::msg::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub finger_c_object_detection: super::msg::ObjectDetectionStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scissor_object_detection: super::msg::ObjectDetectionStatus,

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
    pub mode: super::msg::GraspingMode,

}



impl Default for Status {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Status::default())
  }
}

impl rosidl_runtime_rs::Message for Status {
  type RmwMsg = super::msg::rmw::Status;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        finger_a_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Owned(msg.finger_a_object_detection)).into_owned(),
        finger_b_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Owned(msg.finger_b_object_detection)).into_owned(),
        finger_c_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Owned(msg.finger_c_object_detection)).into_owned(),
        scissor_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Owned(msg.scissor_object_detection)).into_owned(),
        finger_a_position: msg.finger_a_position,
        finger_b_position: msg.finger_b_position,
        finger_c_position: msg.finger_c_position,
        scissor_position: msg.scissor_position,
        finger_a_current: msg.finger_a_current,
        finger_b_current: msg.finger_b_current,
        finger_c_current: msg.finger_c_current,
        scissor_current: msg.scissor_current,
        finger_a_cmd_echo: msg.finger_a_cmd_echo,
        finger_b_cmd_echo: msg.finger_b_cmd_echo,
        finger_c_cmd_echo: msg.finger_c_cmd_echo,
        scissor_cmd_echo: msg.scissor_cmd_echo,
        mode: super::msg::GraspingMode::into_rmw_message(std::borrow::Cow::Owned(msg.mode)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        finger_a_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.finger_a_object_detection)).into_owned(),
        finger_b_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.finger_b_object_detection)).into_owned(),
        finger_c_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.finger_c_object_detection)).into_owned(),
        scissor_object_detection: super::msg::ObjectDetectionStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.scissor_object_detection)).into_owned(),
      finger_a_position: msg.finger_a_position,
      finger_b_position: msg.finger_b_position,
      finger_c_position: msg.finger_c_position,
      scissor_position: msg.scissor_position,
      finger_a_current: msg.finger_a_current,
      finger_b_current: msg.finger_b_current,
      finger_c_current: msg.finger_c_current,
      scissor_current: msg.scissor_current,
      finger_a_cmd_echo: msg.finger_a_cmd_echo,
      finger_b_cmd_echo: msg.finger_b_cmd_echo,
      finger_c_cmd_echo: msg.finger_c_cmd_echo,
      scissor_cmd_echo: msg.scissor_cmd_echo,
        mode: super::msg::GraspingMode::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mode)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      finger_a_object_detection: super::msg::ObjectDetectionStatus::from_rmw_message(msg.finger_a_object_detection),
      finger_b_object_detection: super::msg::ObjectDetectionStatus::from_rmw_message(msg.finger_b_object_detection),
      finger_c_object_detection: super::msg::ObjectDetectionStatus::from_rmw_message(msg.finger_c_object_detection),
      scissor_object_detection: super::msg::ObjectDetectionStatus::from_rmw_message(msg.scissor_object_detection),
      finger_a_position: msg.finger_a_position,
      finger_b_position: msg.finger_b_position,
      finger_c_position: msg.finger_c_position,
      scissor_position: msg.scissor_position,
      finger_a_current: msg.finger_a_current,
      finger_b_current: msg.finger_b_current,
      finger_c_current: msg.finger_c_current,
      scissor_current: msg.scissor_current,
      finger_a_cmd_echo: msg.finger_a_cmd_echo,
      finger_b_cmd_echo: msg.finger_b_cmd_echo,
      finger_c_cmd_echo: msg.finger_c_cmd_echo,
      scissor_cmd_echo: msg.scissor_cmd_echo,
      mode: super::msg::GraspingMode::from_rmw_message(msg.mode),
    }
  }
}


// Corresponds to robotiq_3f_interfaces__msg__GraspingMode

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GraspingMode::default())
  }
}

impl rosidl_runtime_rs::Message for GraspingMode {
  type RmwMsg = super::msg::rmw::GraspingMode;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode: msg.mode,
    }
  }
}


// Corresponds to robotiq_3f_interfaces__msg__SimpleControlCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SimpleControlCommand::default())
  }
}

impl rosidl_runtime_rs::Message for SimpleControlCommand {
  type RmwMsg = super::msg::rmw::SimpleControlCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: msg.position,
        velocity: msg.velocity,
        force: msg.force,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      position: msg.position,
      velocity: msg.velocity,
      force: msg.force,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      position: msg.position,
      velocity: msg.velocity,
      force: msg.force,
    }
  }
}


// Corresponds to robotiq_3f_interfaces__msg__IndependentControlCommand

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::IndependentControlCommand::default())
  }
}

impl rosidl_runtime_rs::Message for IndependentControlCommand {
  type RmwMsg = super::msg::rmw::IndependentControlCommand;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        finger_a_position: msg.finger_a_position,
        finger_b_position: msg.finger_b_position,
        finger_c_position: msg.finger_c_position,
        scissor_position: msg.scissor_position,
        finger_a_velocity: msg.finger_a_velocity,
        finger_b_velocity: msg.finger_b_velocity,
        finger_c_velocity: msg.finger_c_velocity,
        scissor_velocity: msg.scissor_velocity,
        finger_a_force: msg.finger_a_force,
        finger_b_force: msg.finger_b_force,
        finger_c_force: msg.finger_c_force,
        scissor_force: msg.scissor_force,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      finger_a_position: msg.finger_a_position,
      finger_b_position: msg.finger_b_position,
      finger_c_position: msg.finger_c_position,
      scissor_position: msg.scissor_position,
      finger_a_velocity: msg.finger_a_velocity,
      finger_b_velocity: msg.finger_b_velocity,
      finger_c_velocity: msg.finger_c_velocity,
      scissor_velocity: msg.scissor_velocity,
      finger_a_force: msg.finger_a_force,
      finger_b_force: msg.finger_b_force,
      finger_c_force: msg.finger_c_force,
      scissor_force: msg.scissor_force,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      finger_a_position: msg.finger_a_position,
      finger_b_position: msg.finger_b_position,
      finger_c_position: msg.finger_c_position,
      scissor_position: msg.scissor_position,
      finger_a_velocity: msg.finger_a_velocity,
      finger_b_velocity: msg.finger_b_velocity,
      finger_c_velocity: msg.finger_c_velocity,
      scissor_velocity: msg.scissor_velocity,
      finger_a_force: msg.finger_a_force,
      finger_b_force: msg.finger_b_force,
      finger_c_force: msg.finger_c_force,
      scissor_force: msg.scissor_force,
    }
  }
}


