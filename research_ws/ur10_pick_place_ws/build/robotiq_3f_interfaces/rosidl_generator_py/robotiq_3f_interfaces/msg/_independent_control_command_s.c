// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
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
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__struct.h"
#include "robotiq_3f_interfaces/msg/detail/independent_control_command__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool robotiq_3f_interfaces__msg__independent_control_command__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[81];
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
    assert(strncmp("robotiq_3f_interfaces.msg._independent_control_command.IndependentControlCommand", full_classname_dest, 80) == 0);
  }
  robotiq_3f_interfaces__msg__IndependentControlCommand * ros_message = _ros_message;
  {  // finger_a_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_a_position = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_b_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_b_position = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_c_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_c_position = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // scissor_position
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_position");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->scissor_position = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_a_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_a_velocity = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_b_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_b_velocity = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_c_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_c_velocity = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // scissor_velocity
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_velocity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->scissor_velocity = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_a_force
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_a_force");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_a_force = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_b_force
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_b_force");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_b_force = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // finger_c_force
    PyObject * field = PyObject_GetAttrString(_pymsg, "finger_c_force");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->finger_c_force = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // scissor_force
    PyObject * field = PyObject_GetAttrString(_pymsg, "scissor_force");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->scissor_force = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * robotiq_3f_interfaces__msg__independent_control_command__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of IndependentControlCommand */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("robotiq_3f_interfaces.msg._independent_control_command");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "IndependentControlCommand");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  robotiq_3f_interfaces__msg__IndependentControlCommand * ros_message = (robotiq_3f_interfaces__msg__IndependentControlCommand *)raw_ros_message;
  {  // finger_a_position
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_a_position);
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
    field = PyFloat_FromDouble(ros_message->finger_b_position);
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
    field = PyFloat_FromDouble(ros_message->finger_c_position);
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
    field = PyFloat_FromDouble(ros_message->scissor_position);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_position", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_a_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_a_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_b_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_c_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_velocity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->scissor_velocity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_velocity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_a_force
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_a_force);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_a_force", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_b_force
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_b_force);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_b_force", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // finger_c_force
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->finger_c_force);
    {
      int rc = PyObject_SetAttrString(_pymessage, "finger_c_force", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scissor_force
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->scissor_force);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scissor_force", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
