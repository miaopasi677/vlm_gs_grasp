// Auto-generated. Do not edit!

// (in-package warehouse.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Rotate = require('./Rotate.js');
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Pose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.position = null;
      this.rotation = null;
    }
    else {
      if (initObj.hasOwnProperty('position')) {
        this.position = initObj.position
      }
      else {
        this.position = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('rotation')) {
        this.rotation = initObj.rotation
      }
      else {
        this.rotation = new Rotate();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Pose
    // Serialize message field [position]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.position, buffer, bufferOffset);
    // Serialize message field [rotation]
    bufferOffset = Rotate.serialize(obj.rotation, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Pose
    let len;
    let data = new Pose(null);
    // Deserialize message field [position]
    data.position = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [rotation]
    data.rotation = Rotate.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 48;
  }

  static datatype() {
    // Returns string type for a message object
    return 'warehouse/Pose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c2e48a5367d8266f8aaac3d6b58f5cb2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Pose(null);
    if (msg.position !== undefined) {
      resolved.position = geometry_msgs.msg.Point.Resolve(msg.position)
    }
    else {
      resolved.position = new geometry_msgs.msg.Point()
    }

    if (msg.rotation !== undefined) {
      resolved.rotation = Rotate.Resolve(msg.rotation)
    }
    else {
      resolved.rotation = new Rotate()
    }

    return resolved;
    }
};

module.exports = Pose;
