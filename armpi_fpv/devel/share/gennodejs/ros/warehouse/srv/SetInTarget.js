// Auto-generated. Do not edit!

// (in-package warehouse.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class SetInTargetRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.goods = null;
      this.position = null;
    }
    else {
      if (initObj.hasOwnProperty('goods')) {
        this.goods = initObj.goods
      }
      else {
        this.goods = [];
      }
      if (initObj.hasOwnProperty('position')) {
        this.position = initObj.position
      }
      else {
        this.position = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetInTargetRequest
    // Serialize message field [goods]
    bufferOffset = _arraySerializer.string(obj.goods, buffer, bufferOffset, null);
    // Serialize message field [position]
    bufferOffset = _arraySerializer.string(obj.position, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetInTargetRequest
    let len;
    let data = new SetInTargetRequest(null);
    // Deserialize message field [goods]
    data.goods = _arrayDeserializer.string(buffer, bufferOffset, null)
    // Deserialize message field [position]
    data.position = _arrayDeserializer.string(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.goods.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    object.position.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'warehouse/SetInTargetRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '43f0c28a64c223b7f9e052a7a11ebdd1';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string[] goods
    string[] position
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetInTargetRequest(null);
    if (msg.goods !== undefined) {
      resolved.goods = msg.goods;
    }
    else {
      resolved.goods = []
    }

    if (msg.position !== undefined) {
      resolved.position = msg.position;
    }
    else {
      resolved.position = []
    }

    return resolved;
    }
};

class SetInTargetResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.success = null;
      this.message = null;
    }
    else {
      if (initObj.hasOwnProperty('success')) {
        this.success = initObj.success
      }
      else {
        this.success = false;
      }
      if (initObj.hasOwnProperty('message')) {
        this.message = initObj.message
      }
      else {
        this.message = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetInTargetResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetInTargetResponse
    let len;
    let data = new SetInTargetResponse(null);
    // Deserialize message field [success]
    data.success = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [message]
    data.message = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.message);
    return length + 5;
  }

  static datatype() {
    // Returns string type for a service object
    return 'warehouse/SetInTargetResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '937c9679a518e3a18d831e57125ea522';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool success
    string message
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetInTargetResponse(null);
    if (msg.success !== undefined) {
      resolved.success = msg.success;
    }
    else {
      resolved.success = false
    }

    if (msg.message !== undefined) {
      resolved.message = msg.message;
    }
    else {
      resolved.message = ''
    }

    return resolved;
    }
};

module.exports = {
  Request: SetInTargetRequest,
  Response: SetInTargetResponse,
  md5sum() { return '3a5188a131c4178e5804bbb1ba83e677'; },
  datatype() { return 'warehouse/SetInTarget'; }
};
