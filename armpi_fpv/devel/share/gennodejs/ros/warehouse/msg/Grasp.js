// Auto-generated. Do not edit!

// (in-package warehouse.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Pose = require('./Pose.js');
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Grasp {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.grasp_pos = null;
      this.grasp_approach = null;
      this.grasp_retreat = null;
      this.up = null;
      this.grasp_posture = null;
      this.pre_grasp_posture = null;
    }
    else {
      if (initObj.hasOwnProperty('grasp_pos')) {
        this.grasp_pos = initObj.grasp_pos
      }
      else {
        this.grasp_pos = new Pose();
      }
      if (initObj.hasOwnProperty('grasp_approach')) {
        this.grasp_approach = initObj.grasp_approach
      }
      else {
        this.grasp_approach = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('grasp_retreat')) {
        this.grasp_retreat = initObj.grasp_retreat
      }
      else {
        this.grasp_retreat = new geometry_msgs.msg.Vector3();
      }
      if (initObj.hasOwnProperty('up')) {
        this.up = initObj.up
      }
      else {
        this.up = 0.0;
      }
      if (initObj.hasOwnProperty('grasp_posture')) {
        this.grasp_posture = initObj.grasp_posture
      }
      else {
        this.grasp_posture = 0;
      }
      if (initObj.hasOwnProperty('pre_grasp_posture')) {
        this.pre_grasp_posture = initObj.pre_grasp_posture
      }
      else {
        this.pre_grasp_posture = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Grasp
    // Serialize message field [grasp_pos]
    bufferOffset = Pose.serialize(obj.grasp_pos, buffer, bufferOffset);
    // Serialize message field [grasp_approach]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.grasp_approach, buffer, bufferOffset);
    // Serialize message field [grasp_retreat]
    bufferOffset = geometry_msgs.msg.Vector3.serialize(obj.grasp_retreat, buffer, bufferOffset);
    // Serialize message field [up]
    bufferOffset = _serializer.float64(obj.up, buffer, bufferOffset);
    // Serialize message field [grasp_posture]
    bufferOffset = _serializer.int16(obj.grasp_posture, buffer, bufferOffset);
    // Serialize message field [pre_grasp_posture]
    bufferOffset = _serializer.int16(obj.pre_grasp_posture, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Grasp
    let len;
    let data = new Grasp(null);
    // Deserialize message field [grasp_pos]
    data.grasp_pos = Pose.deserialize(buffer, bufferOffset);
    // Deserialize message field [grasp_approach]
    data.grasp_approach = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [grasp_retreat]
    data.grasp_retreat = geometry_msgs.msg.Vector3.deserialize(buffer, bufferOffset);
    // Deserialize message field [up]
    data.up = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [grasp_posture]
    data.grasp_posture = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [pre_grasp_posture]
    data.pre_grasp_posture = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 108;
  }

  static datatype() {
    // Returns string type for a message object
    return 'warehouse/Grasp';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '70d37fa314d53b4952d2f54caf3874d2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # 夹取时的姿态和位置
    warehouse/Pose grasp_pos
    
    # 接近时的距离和方向
    geometry_msgs/Vector3 grasp_approach
    
    # 撤离时的距离和方向
    geometry_msgs/Vector3 grasp_retreat
    
    # 抬高高度
    float64 up
    
    # 夹取时夹持器姿态
    int16 grasp_posture
    
    # 夹取前夹持器姿态
    int16 pre_grasp_posture
    
    
    ================================================================================
    MSG: warehouse/Pose
    geometry_msgs/Point position
    warehouse/Rotate rotation
    
    ================================================================================
    MSG: geometry_msgs/Point
    # This contains the position of a point in free space
    float64 x
    float64 y
    float64 z
    
    ================================================================================
    MSG: warehouse/Rotate
    float64 r
    float64 p
    float64 y
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Grasp(null);
    if (msg.grasp_pos !== undefined) {
      resolved.grasp_pos = Pose.Resolve(msg.grasp_pos)
    }
    else {
      resolved.grasp_pos = new Pose()
    }

    if (msg.grasp_approach !== undefined) {
      resolved.grasp_approach = geometry_msgs.msg.Vector3.Resolve(msg.grasp_approach)
    }
    else {
      resolved.grasp_approach = new geometry_msgs.msg.Vector3()
    }

    if (msg.grasp_retreat !== undefined) {
      resolved.grasp_retreat = geometry_msgs.msg.Vector3.Resolve(msg.grasp_retreat)
    }
    else {
      resolved.grasp_retreat = new geometry_msgs.msg.Vector3()
    }

    if (msg.up !== undefined) {
      resolved.up = msg.up;
    }
    else {
      resolved.up = 0.0
    }

    if (msg.grasp_posture !== undefined) {
      resolved.grasp_posture = msg.grasp_posture;
    }
    else {
      resolved.grasp_posture = 0
    }

    if (msg.pre_grasp_posture !== undefined) {
      resolved.pre_grasp_posture = msg.pre_grasp_posture;
    }
    else {
      resolved.pre_grasp_posture = 0
    }

    return resolved;
    }
};

module.exports = Grasp;
