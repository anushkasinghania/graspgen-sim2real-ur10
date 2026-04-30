# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_interfaces:msg/IndependentControlCommand.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_IndependentControlCommand(type):
    """Metaclass of message 'IndependentControlCommand'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('robotiq_3f_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'robotiq_3f_interfaces.msg.IndependentControlCommand')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__independent_control_command
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__independent_control_command
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__independent_control_command
            cls._TYPE_SUPPORT = module.type_support_msg__msg__independent_control_command
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__independent_control_command

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class IndependentControlCommand(metaclass=Metaclass_IndependentControlCommand):
    """Message class 'IndependentControlCommand'."""

    __slots__ = [
        '_finger_a_position',
        '_finger_b_position',
        '_finger_c_position',
        '_scissor_position',
        '_finger_a_velocity',
        '_finger_b_velocity',
        '_finger_c_velocity',
        '_scissor_velocity',
        '_finger_a_force',
        '_finger_b_force',
        '_finger_c_force',
        '_scissor_force',
    ]

    _fields_and_field_types = {
        'finger_a_position': 'double',
        'finger_b_position': 'double',
        'finger_c_position': 'double',
        'scissor_position': 'double',
        'finger_a_velocity': 'double',
        'finger_b_velocity': 'double',
        'finger_c_velocity': 'double',
        'scissor_velocity': 'double',
        'finger_a_force': 'double',
        'finger_b_force': 'double',
        'finger_c_force': 'double',
        'scissor_force': 'double',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.finger_a_position = kwargs.get('finger_a_position', float())
        self.finger_b_position = kwargs.get('finger_b_position', float())
        self.finger_c_position = kwargs.get('finger_c_position', float())
        self.scissor_position = kwargs.get('scissor_position', float())
        self.finger_a_velocity = kwargs.get('finger_a_velocity', float())
        self.finger_b_velocity = kwargs.get('finger_b_velocity', float())
        self.finger_c_velocity = kwargs.get('finger_c_velocity', float())
        self.scissor_velocity = kwargs.get('scissor_velocity', float())
        self.finger_a_force = kwargs.get('finger_a_force', float())
        self.finger_b_force = kwargs.get('finger_b_force', float())
        self.finger_c_force = kwargs.get('finger_c_force', float())
        self.scissor_force = kwargs.get('scissor_force', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.finger_a_position != other.finger_a_position:
            return False
        if self.finger_b_position != other.finger_b_position:
            return False
        if self.finger_c_position != other.finger_c_position:
            return False
        if self.scissor_position != other.scissor_position:
            return False
        if self.finger_a_velocity != other.finger_a_velocity:
            return False
        if self.finger_b_velocity != other.finger_b_velocity:
            return False
        if self.finger_c_velocity != other.finger_c_velocity:
            return False
        if self.scissor_velocity != other.scissor_velocity:
            return False
        if self.finger_a_force != other.finger_a_force:
            return False
        if self.finger_b_force != other.finger_b_force:
            return False
        if self.finger_c_force != other.finger_c_force:
            return False
        if self.scissor_force != other.scissor_force:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def finger_a_position(self):
        """Message field 'finger_a_position'."""
        return self._finger_a_position

    @finger_a_position.setter
    def finger_a_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_a_position' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_a_position' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_a_position = value

    @builtins.property
    def finger_b_position(self):
        """Message field 'finger_b_position'."""
        return self._finger_b_position

    @finger_b_position.setter
    def finger_b_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_b_position' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_b_position' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_b_position = value

    @builtins.property
    def finger_c_position(self):
        """Message field 'finger_c_position'."""
        return self._finger_c_position

    @finger_c_position.setter
    def finger_c_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_c_position' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_c_position' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_c_position = value

    @builtins.property
    def scissor_position(self):
        """Message field 'scissor_position'."""
        return self._scissor_position

    @scissor_position.setter
    def scissor_position(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'scissor_position' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'scissor_position' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._scissor_position = value

    @builtins.property
    def finger_a_velocity(self):
        """Message field 'finger_a_velocity'."""
        return self._finger_a_velocity

    @finger_a_velocity.setter
    def finger_a_velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_a_velocity' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_a_velocity' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_a_velocity = value

    @builtins.property
    def finger_b_velocity(self):
        """Message field 'finger_b_velocity'."""
        return self._finger_b_velocity

    @finger_b_velocity.setter
    def finger_b_velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_b_velocity' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_b_velocity' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_b_velocity = value

    @builtins.property
    def finger_c_velocity(self):
        """Message field 'finger_c_velocity'."""
        return self._finger_c_velocity

    @finger_c_velocity.setter
    def finger_c_velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_c_velocity' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_c_velocity' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_c_velocity = value

    @builtins.property
    def scissor_velocity(self):
        """Message field 'scissor_velocity'."""
        return self._scissor_velocity

    @scissor_velocity.setter
    def scissor_velocity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'scissor_velocity' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'scissor_velocity' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._scissor_velocity = value

    @builtins.property
    def finger_a_force(self):
        """Message field 'finger_a_force'."""
        return self._finger_a_force

    @finger_a_force.setter
    def finger_a_force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_a_force' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_a_force' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_a_force = value

    @builtins.property
    def finger_b_force(self):
        """Message field 'finger_b_force'."""
        return self._finger_b_force

    @finger_b_force.setter
    def finger_b_force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_b_force' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_b_force' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_b_force = value

    @builtins.property
    def finger_c_force(self):
        """Message field 'finger_c_force'."""
        return self._finger_c_force

    @finger_c_force.setter
    def finger_c_force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'finger_c_force' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'finger_c_force' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._finger_c_force = value

    @builtins.property
    def scissor_force(self):
        """Message field 'scissor_force'."""
        return self._scissor_force

    @scissor_force.setter
    def scissor_force(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'scissor_force' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'scissor_force' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._scissor_force = value
