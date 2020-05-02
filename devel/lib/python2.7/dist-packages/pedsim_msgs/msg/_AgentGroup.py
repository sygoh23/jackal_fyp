# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from pedsim_msgs/AgentGroup.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import geometry_msgs.msg
import std_msgs.msg

class AgentGroup(genpy.Message):
  _md5sum = "5fd22ef81e8e7ee63e1028ae9b798458"
  _type = "pedsim_msgs/AgentGroup"
  _has_header = True #flag to mark the presence of a Header object
  _full_text = """Header header
uint16 group_id
float64 age
uint64[] members
geometry_msgs/Pose center_of_mass

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
"""
  __slots__ = ['header','group_id','age','members','center_of_mass']
  _slot_types = ['std_msgs/Header','uint16','float64','uint64[]','geometry_msgs/Pose']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       header,group_id,age,members,center_of_mass

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(AgentGroup, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.group_id is None:
        self.group_id = 0
      if self.age is None:
        self.age = 0.
      if self.members is None:
        self.members = []
      if self.center_of_mass is None:
        self.center_of_mass = geometry_msgs.msg.Pose()
    else:
      self.header = std_msgs.msg.Header()
      self.group_id = 0
      self.age = 0.
      self.members = []
      self.center_of_mass = geometry_msgs.msg.Pose()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_Hd().pack(_x.group_id, _x.age))
      length = len(self.members)
      buff.write(_struct_I.pack(length))
      pattern = '<%sQ'%length
      buff.write(struct.pack(pattern, *self.members))
      _x = self
      buff.write(_get_struct_7d().pack(_x.center_of_mass.position.x, _x.center_of_mass.position.y, _x.center_of_mass.position.z, _x.center_of_mass.orientation.x, _x.center_of_mass.orientation.y, _x.center_of_mass.orientation.z, _x.center_of_mass.orientation.w))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.center_of_mass is None:
        self.center_of_mass = geometry_msgs.msg.Pose()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 10
      (_x.group_id, _x.age,) = _get_struct_Hd().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      pattern = '<%sQ'%length
      start = end
      end += struct.calcsize(pattern)
      self.members = struct.unpack(pattern, str[start:end])
      _x = self
      start = end
      end += 56
      (_x.center_of_mass.position.x, _x.center_of_mass.position.y, _x.center_of_mass.position.z, _x.center_of_mass.orientation.x, _x.center_of_mass.orientation.y, _x.center_of_mass.orientation.z, _x.center_of_mass.orientation.w,) = _get_struct_7d().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_3I().pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      if python3 or type(_x) == unicode:
        _x = _x.encode('utf-8')
        length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_get_struct_Hd().pack(_x.group_id, _x.age))
      length = len(self.members)
      buff.write(_struct_I.pack(length))
      pattern = '<%sQ'%length
      buff.write(self.members.tostring())
      _x = self
      buff.write(_get_struct_7d().pack(_x.center_of_mass.position.x, _x.center_of_mass.position.y, _x.center_of_mass.position.z, _x.center_of_mass.orientation.x, _x.center_of_mass.orientation.y, _x.center_of_mass.orientation.z, _x.center_of_mass.orientation.w))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.center_of_mass is None:
        self.center_of_mass = geometry_msgs.msg.Pose()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _get_struct_3I().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      if python3:
        self.header.frame_id = str[start:end].decode('utf-8')
      else:
        self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 10
      (_x.group_id, _x.age,) = _get_struct_Hd().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      pattern = '<%sQ'%length
      start = end
      end += struct.calcsize(pattern)
      self.members = numpy.frombuffer(str[start:end], dtype=numpy.uint64, count=length)
      _x = self
      start = end
      end += 56
      (_x.center_of_mass.position.x, _x.center_of_mass.position.y, _x.center_of_mass.position.z, _x.center_of_mass.orientation.x, _x.center_of_mass.orientation.y, _x.center_of_mass.orientation.z, _x.center_of_mass.orientation.w,) = _get_struct_7d().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_3I = None
def _get_struct_3I():
    global _struct_3I
    if _struct_3I is None:
        _struct_3I = struct.Struct("<3I")
    return _struct_3I
_struct_7d = None
def _get_struct_7d():
    global _struct_7d
    if _struct_7d is None:
        _struct_7d = struct.Struct("<7d")
    return _struct_7d
_struct_Hd = None
def _get_struct_Hd():
    global _struct_Hd
    if _struct_Hd is None:
        _struct_Hd = struct.Struct("<Hd")
    return _struct_Hd
