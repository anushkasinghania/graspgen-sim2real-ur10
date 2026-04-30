// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from robotiq_3f_interfaces:msg/Status.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "robotiq_3f_interfaces/msg/detail/status__struct.h"
#include "robotiq_3f_interfaces/msg/detail/status__functions.h"

bool robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(void * raw_ros_message);
bool robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(void * raw_ros_message);
bool robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(void * raw_ros_message);
bool robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(void * raw_ros_message);
bool robotiq_3f_interfaces__msg__grasping_mode__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * robotiq_3f_interfaces__msg__grasping_mode__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool robotiq_3f_interfaces__msg__status__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[41];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("robotiq_3f_interfaces.msg._status.Status", full_classname_dest, 40) == 0);
  }
  robotiq_3f_interfaces__msg__Status * ros_message = _ros_message;
  {  // finger_a_object_detection
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_object_detection");
    if (!field) {
      return false;
    }
    if (!robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(field, &ros_message->finger_a_object_detection)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // finger_b_object_detection
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_object_detection");
    if (!field) {
      return false;
    }
    if (!robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(field, &ros_message->finger_b_object_detection)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // finger_c_object_detection
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_object_detection");
    if (!field) {
      return false;
    }
    if (!robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(field, &ros_message->finger_c_object_detection)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // scissor_object_detection
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_object_detection");
    if (!field) {
      return false;
    }
    if (!robotiq_3f_interfaces__msg__object_detection_status__convert_from_py(field, &ros_message->scissor_object_detection)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // finger_a_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_position");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_a_position = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_b_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_position");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_b_position = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_c_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_position");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_c_position = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // scissor_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_position");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->scissor_position = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_a_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_current");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_a_current = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_b_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_current");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_b_current = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_c_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_current");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_c_current = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // scissor_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_current");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->scissor_current = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_a_cmd_echo
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_cmd_echo");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_a_cmd_echo = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_b_cmd_echo
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_cmd_echo");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_b_cmd_echo = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // finger_c_cmd_echo
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_cmd_echo");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->finger_c_cmd_echo = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // scissor_cmd_echo
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_cmd_echo");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->scissor_cmd_echo = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // mode
    PyObject * field = PyObject_GetAttrString(_pymsg, "mode");
    if (!field) {
      return false;
    }
    if (!robotiq_3f_interfaces__msg__grasping_mode__convert_from_py(field, &ros_message->mode)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * robotiq_3f_interfaces__msg__status__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Status */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("robotiq_3f_interfaces.msg._status");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Status");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  robotiq_3f_interfaces__msg__Status * ros_message = (robotiq_3f_interfaces__msg__Status *)raw_ros_message;
  {  // finger_a_object_detection
    PyObject * field = NULL;
    field = robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(&ros_message->finger_a_object_detection);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_object_detection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_object_detection
    PyObject * field = NULL;
    field = robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(&ros_message->finger_b_object_detection);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_object_detection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_object_detection
    PyObject * field = NULL;
    field = robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(&ros_message->finger_c_object_detection);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_object_detection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_object_detection
    PyObject * field = NULL;
    field = robotiq_3f_interfaces__msg__object_detection_status__convert_to_py(&ros_message->scissor_object_detection);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_object_detection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_a_position
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_a_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_position
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_b_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_position
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_c_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_position
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->scissor_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_a_current
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_a_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_current
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_b_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_current
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_c_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_current
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->scissor_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_a_cmd_echo
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_a_cmd_echo);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_cmd_echo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_cmd_echo
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_b_cmd_echo);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_cmd_echo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_cmd_echo
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->finger_c_cmd_echo);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_cmd_echo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_cmd_echo
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->scissor_cmd_echo);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_cmd_echo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mode
    PyObject * field = NULL;
    field = robotiq_3f_interfaces__msg__grasping_mode__convert_to_py(&ros_message->mode);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "mode", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
