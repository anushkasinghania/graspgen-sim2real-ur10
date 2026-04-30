# generated from rosidl_generator_py/resource/_idl.py.em
# with input from robotiq_3f_interfaces:msg/GraspingMode.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GraspingMode(type):
    """Metaclass of message 'GraspingMode'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'BASIC': 0,
        'PINCH': 1,
        'WIDE': 2,
        'SCISSOR': 3,
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
                'robotiq_3f_interfaces.msg.GraspingMode')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__grasping_mode
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__grasping_mode
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__grasping_mode
            cls._TYPE_SUPPORT = module.type_support_msg__msg__grasping_mode
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__grasping_mode

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'BASIC': cls.__constants['BASIC'],
            'PINCH': cls.__constants['PINCH'],
            'WIDE': cls.__constants['WIDE'],
            'SCISSOR': cls.__constants['SCISSOR'],
        }

    @property
    def BASIC(self):
        """Message constant 'BASIC'."""
        return Metaclass_GraspingMode.__constants['BASIC']

    @property
    def PINCH(self):
        """Message constant 'PINCH'."""
        return Metaclass_GraspingMode.__constants['PINCH']

    @property
    def WIDE(self):
        """Message constant 'WIDE'."""
        return Metaclass_GraspingMode.__constants['WIDE']

    @property
    def SCISSOR(self):
        """Message constant 'SCISSOR'."""
        return Metaclass_GraspingMode.__constants['SCISSOR']


class GraspingMode(metaclass=Metaclass_GraspingMode):
    """
    Message class 'GraspingMode'.

    Constants:
      BASIC
      PINCH
      WIDE
      SCISSOR
    """

    __slots__ = [
        '_mode',
    ]

    _fields_and_field_types = {
        'mode': 'int8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.mode = kwargs.get('mode', int())

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
        if self.mode != other.mode:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def mode(self):
        """Message field 'mode'."""
        return self._mode

    @mode.setter
    def mode(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'mode' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'mode' field must be an integer in [-128, 127]"
        self._mode = value
