# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_interfaces:msg/Status.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Status(type):
    """Metaclass of message 'Status'."""

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
                'robotiq_3f_interfaces.msg.Status')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__status

            from robotiq_3f_interfaces.msg import GraspingMode
            if GraspingMode.__class__._TYPE_SUPPORT is None:
                GraspingMode.__class__.__import_type_support__()

            from robotiq_3f_interfaces.msg import ObjectDetectionStatus
            if ObjectDetectionStatus.__class__._TYPE_SUPPORT is None:
                ObjectDetectionStatus.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Status(metaclass=Metaclass_Status):
    """Message class 'Status'."""

    __slots__ = [
        '_finger_a_object_detection',
        '_finger_b_object_detection',
        '_finger_c_object_detection',
        '_scissor_object_detection',
        '_finger_a_position',
        '_finger_b_position',
        '_finger_c_position',
        '_scissor_position',
        '_finger_a_current',
        '_finger_b_current',
        '_finger_c_current',
        '_scissor_current',
        '_finger_a_cmd_echo',
        '_finger_b_cmd_echo',
        '_finger_c_cmd_echo',
        '_scissor_cmd_echo',
        '_mode',
    ]

    _fields_and_field_types = {
        'finger_a_object_detection': 'robotiq_3f_interfaces/ObjectDetectionStatus',
        'finger_b_object_detection': 'robotiq_3f_interfaces/ObjectDetectionStatus',
        'finger_c_object_detection': 'robotiq_3f_interfaces/ObjectDetectionStatus',
        'scissor_object_detection': 'robotiq_3f_interfaces/ObjectDetectionStatus',
        'finger_a_position': 'uint8',
        'finger_b_position': 'uint8',
        'finger_c_position': 'uint8',
        'scissor_position': 'uint8',
        'finger_a_current': 'uint8',
        'finger_b_current': 'uint8',
        'finger_c_current': 'uint8',
        'scissor_current': 'uint8',
        'finger_a_cmd_echo': 'uint8',
        'finger_b_cmd_echo': 'uint8',
        'finger_c_cmd_echo': 'uint8',
        'scissor_cmd_echo': 'uint8',
        'mode': 'robotiq_3f_interfaces/GraspingMode',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['robotiq_3f_interfaces', 'msg'], 'ObjectDetectionStatus'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_interfaces', 'msg'], 'ObjectDetectionStatus'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_interfaces', 'msg'], 'ObjectDetectionStatus'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_interfaces', 'msg'], 'ObjectDetectionStatus'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['robotiq_3f_interfaces', 'msg'], 'GraspingMode'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from robotiq_3f_interfaces.msg import ObjectDetectionStatus
        self.finger_a_object_detection = kwargs.get('finger_a_object_detection', ObjectDetectionStatus())
        from robotiq_3f_interfaces.msg import ObjectDetectionStatus
        self.finger_b_object_detection = kwargs.get('finger_b_object_detection', ObjectDetectionStatus())
        from robotiq_3f_interfaces.msg import ObjectDetectionStatus
        self.finger_c_object_detection = kwargs.get('finger_c_object_detection', ObjectDetectionStatus())
        from robotiq_3f_interfaces.msg import ObjectDetectionStatus
        self.scissor_object_detection = kwargs.get('scissor_object_detection', ObjectDetectionStatus())
        self.finger_a_position = kwargs.get('finger_a_position', int())
        self.finger_b_position = kwargs.get('finger_b_position', int())
        self.finger_c_position = kwargs.get('finger_c_position', int())
        self.scissor_position = kwargs.get('scissor_position', int())
        self.finger_a_current = kwargs.get('finger_a_current', int())
        self.finger_b_current = kwargs.get('finger_b_current', int())
        self.finger_c_current = kwargs.get('finger_c_current', int())
        self.scissor_current = kwargs.get('scissor_current', int())
        self.finger_a_cmd_echo = kwargs.get('finger_a_cmd_echo', int())
        self.finger_b_cmd_echo = kwargs.get('finger_b_cmd_echo', int())
        self.finger_c_cmd_echo = kwargs.get('finger_c_cmd_echo', int())
        self.scissor_cmd_echo = kwargs.get('scissor_cmd_echo', int())
        from robotiq_3f_interfaces.msg import GraspingMode
        self.mode = kwargs.get('mode', GraspingMode())

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
        if self.finger_a_object_detection != other.finger_a_object_detection:
            return False
        if self.finger_b_object_detection != other.finger_b_object_detection:
            return False
        if self.finger_c_object_detection != other.finger_c_object_detection:
            return False
        if self.scissor_object_detection != other.scissor_object_detection:
            return False
        if self.finger_a_position != other.finger_a_position:
            return False
        if self.finger_b_position != other.finger_b_position:
            return False
        if self.finger_c_position != other.finger_c_position:
            return False
        if self.scissor_position != other.scissor_position:
            return False
        if self.finger_a_current != other.finger_a_current:
            return False
        if self.finger_b_current != other.finger_b_current:
            return False
        if self.finger_c_current != other.finger_c_current:
            return False
        if self.scissor_current != other.scissor_current:
            return False
        if self.finger_a_cmd_echo != other.finger_a_cmd_echo:
            return False
        if self.finger_b_cmd_echo != other.finger_b_cmd_echo:
            return False
        if self.finger_c_cmd_echo != other.finger_c_cmd_echo:
            return False
        if self.scissor_cmd_echo != other.scissor_cmd_echo:
            return False
        if self.mode != other.mode:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def finger_a_object_detection(self):
        """Message field 'finger_a_object_detection'."""
        return self._finger_a_object_detection

    @finger_a_object_detection.setter
    def finger_a_object_detection(self, value):
        if __debug__:
            from robotiq_3f_interfaces.msg import ObjectDetectionStatus
            assert \
                isinstance(value, ObjectDetectionStatus), \
                "The 'finger_a_object_detection' field must be a sub message of type 'ObjectDetectionStatus'"
        self._finger_a_object_detection = value

    @builtins.property
    def finger_b_object_detection(self):
        """Message field 'finger_b_object_detection'."""
        return self._finger_b_object_detection

    @finger_b_object_detection.setter
    def finger_b_object_detection(self, value):
        if __debug__:
            from robotiq_3f_interfaces.msg import ObjectDetectionStatus
            assert \
                isinstance(value, ObjectDetectionStatus), \
                "The 'finger_b_object_detection' field must be a sub message of type 'ObjectDetectionStatus'"
        self._finger_b_object_detection = value

    @builtins.property
    def finger_c_object_detection(self):
        """Message field 'finger_c_object_detection'."""
        return self._finger_c_object_detection

    @finger_c_object_detection.setter
    def finger_c_object_detection(self, value):
        if __debug__:
            from robotiq_3f_interfaces.msg import ObjectDetectionStatus
            assert \
                isinstance(value, ObjectDetectionStatus), \
                "The 'finger_c_object_detection' field must be a sub message of type 'ObjectDetectionStatus'"
        self._finger_c_object_detection = value

    @builtins.property
    def scissor_object_detection(self):
        """Message field 'scissor_object_detection'."""
        return self._scissor_object_detection

    @scissor_object_detection.setter
    def scissor_object_detection(self, value):
        if __debug__:
            from robotiq_3f_interfaces.msg import ObjectDetectionStatus
            assert \
                isinstance(value, ObjectDetectionStatus), \
                "The 'scissor_object_detection' field must be a sub message of type 'ObjectDetectionStatus'"
        self._scissor_object_detection = value

    @builtins.property
    def finger_a_position(self):
        """Message field 'finger_a_position'."""
        return self._finger_a_position

    @finger_a_position.setter
    def finger_a_position(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_a_position' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_a_position' field must be an unsigned integer in [0, 255]"
        self._finger_a_position = value

    @builtins.property
    def finger_b_position(self):
        """Message field 'finger_b_position'."""
        return self._finger_b_position

    @finger_b_position.setter
    def finger_b_position(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_b_position' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_b_position' field must be an unsigned integer in [0, 255]"
        self._finger_b_position = value

    @builtins.property
    def finger_c_position(self):
        """Message field 'finger_c_position'."""
        return self._finger_c_position

    @finger_c_position.setter
    def finger_c_position(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_c_position' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_c_position' field must be an unsigned integer in [0, 255]"
        self._finger_c_position = value

    @builtins.property
    def scissor_position(self):
        """Message field 'scissor_position'."""
        return self._scissor_position

    @scissor_position.setter
    def scissor_position(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'scissor_position' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'scissor_position' field must be an unsigned integer in [0, 255]"
        self._scissor_position = value

    @builtins.property
    def finger_a_current(self):
        """Message field 'finger_a_current'."""
        return self._finger_a_current

    @finger_a_current.setter
    def finger_a_current(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_a_current' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_a_current' field must be an unsigned integer in [0, 255]"
        self._finger_a_current = value

    @builtins.property
    def finger_b_current(self):
        """Message field 'finger_b_current'."""
        return self._finger_b_current

    @finger_b_current.setter
    def finger_b_current(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_b_current' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_b_current' field must be an unsigned integer in [0, 255]"
        self._finger_b_current = value

    @builtins.property
    def finger_c_current(self):
        """Message field 'finger_c_current'."""
        return self._finger_c_current

    @finger_c_current.setter
    def finger_c_current(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_c_current' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_c_current' field must be an unsigned integer in [0, 255]"
        self._finger_c_current = value

    @builtins.property
    def scissor_current(self):
        """Message field 'scissor_current'."""
        return self._scissor_current

    @scissor_current.setter
    def scissor_current(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'scissor_current' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'scissor_current' field must be an unsigned integer in [0, 255]"
        self._scissor_current = value

    @builtins.property
    def finger_a_cmd_echo(self):
        """Message field 'finger_a_cmd_echo'."""
        return self._finger_a_cmd_echo

    @finger_a_cmd_echo.setter
    def finger_a_cmd_echo(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_a_cmd_echo' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_a_cmd_echo' field must be an unsigned integer in [0, 255]"
        self._finger_a_cmd_echo = value

    @builtins.property
    def finger_b_cmd_echo(self):
        """Message field 'finger_b_cmd_echo'."""
        return self._finger_b_cmd_echo

    @finger_b_cmd_echo.setter
    def finger_b_cmd_echo(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_b_cmd_echo' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_b_cmd_echo' field must be an unsigned integer in [0, 255]"
        self._finger_b_cmd_echo = value

    @builtins.property
    def finger_c_cmd_echo(self):
        """Message field 'finger_c_cmd_echo'."""
        return self._finger_c_cmd_echo

    @finger_c_cmd_echo.setter
    def finger_c_cmd_echo(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'finger_c_cmd_echo' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'finger_c_cmd_echo' field must be an unsigned integer in [0, 255]"
        self._finger_c_cmd_echo = value

    @builtins.property
    def scissor_cmd_echo(self):
        """Message field 'scissor_cmd_echo'."""
        return self._scissor_cmd_echo

    @scissor_cmd_echo.setter
    def scissor_cmd_echo(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'scissor_cmd_echo' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'scissor_cmd_echo' field must be an unsigned integer in [0, 255]"
        self._scissor_cmd_echo = value

    @builtins.property
    def mode(self):
        """Message field 'mode'."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if __debug__:
            from robotiq_3f_interfaces.msg import GraspingMode
            assert \
                isinstance(value, GraspingMode), \
                "The 'mode' field must be a sub message of type 'GraspingMode'"
        self._mode = value
