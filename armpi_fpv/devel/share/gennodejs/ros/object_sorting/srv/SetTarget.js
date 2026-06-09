// Auto-generated. Do not edit!

// (in-package object_sorting.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class SetTargetRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.color = null;
      this.tag = null;
    }
    else {
      if (initObj.hasOwnProperty('color')) {
        this.color = initObj.color
      }
      else {
        this.color = [];
      }
      if (initObj.hasOwnProperty('tag')) {
        this.tag = initObj.tag
      }
      else {
        this.tag = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetTargetRequest
    // Serialize message field [color]
    bufferOffset = _arraySerializer.string(obj.color, buffer, bufferOffset, null);
    // Serialize message field [tag]
    bufferOffset = _arraySerializer.string(obj.tag, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetTargetRequest
    let len;
    let data = new SetTargetRequest(null);
    // Deserialize message field [color]
    data.color = _arrayDeserializer.string(buffer, bufferOffset, null)
    // Deserialize message field [tag]
    data.tag = _arrayDeserializer.string(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.color.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    object.tag.forEach((val) => {
      length += 4 + _getByteLength(val);
    });
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'object_sorting/SetTargetRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2d56a5dd57cf3ca58e9236294da9e9e4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string[] color
    string[] tag
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetTargetRequest(null);
    if (msg.color !== undefined) {
      resolved.color = msg.color;
    }
    else {
      resolved.color = []
    }

    if (msg.tag !== undefined) {
      resolved.tag = msg.tag;
    }
    else {
      resolved.tag = []
    }

    return resolved;
    }
};

class SetTargetResponse {
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
    // Serializes a message object of type SetTargetResponse
    // Serialize message field [success]
    bufferOffset = _serializer.bool(obj.success, buffer, bufferOffset);
    // Serialize message field [message]
    bufferOffset = _serializer.string(obj.message, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetTargetResponse
    let len;
    let data = new SetTargetResponse(null);
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
    return 'object_sorting/SetTargetResponse';
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
    const resolved = new SetTargetResponse(null);
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
  Request: SetTargetRequest,
  Response: SetTargetResponse,
  md5sum() { return '15a6bbca6b7bdaa8c9ab1c07de00a6ac'; },
  datatype() { return 'object_sorting/SetTarget'; }
};
