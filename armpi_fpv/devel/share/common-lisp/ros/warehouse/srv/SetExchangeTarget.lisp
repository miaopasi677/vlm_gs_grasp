; Auto-generated. Do not edit!


(cl:in-package warehouse-srv)


;//! \htmlinclude SetExchangeTarget-request.msg.html

(cl:defclass <SetExchangeTarget-request> (roslisp-msg-protocol:ros-message)
  ((position
    :reader position
    :initarg :position
    :type (cl:vector cl:string)
   :initform (cl:make-array 0 :element-type 'cl:string :initial-element "")))
)

(cl:defclass SetExchangeTarget-request (<SetExchangeTarget-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetExchangeTarget-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetExchangeTarget-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-srv:<SetExchangeTarget-request> is deprecated: use warehouse-srv:SetExchangeTarget-request instead.")))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <SetExchangeTarget-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:position-val is deprecated.  Use warehouse-srv:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetExchangeTarget-request>) ostream)
  "Serializes a message object of type '<SetExchangeTarget-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'position))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((__ros_str_len (cl:length ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) ele))
   (cl:slot-value msg 'position))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetExchangeTarget-request>) istream)
  "Deserializes a message object of type '<SetExchangeTarget-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'position) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'position)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:aref vals i) __ros_str_idx) (cl:code-char (cl:read-byte istream))))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetExchangeTarget-request>)))
  "Returns string type for a service object of type '<SetExchangeTarget-request>"
  "warehouse/SetExchangeTargetRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetExchangeTarget-request)))
  "Returns string type for a service object of type 'SetExchangeTarget-request"
  "warehouse/SetExchangeTargetRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetExchangeTarget-request>)))
  "Returns md5sum for a message object of type '<SetExchangeTarget-request>"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetExchangeTarget-request)))
  "Returns md5sum for a message object of type 'SetExchangeTarget-request"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetExchangeTarget-request>)))
  "Returns full string definition for message of type '<SetExchangeTarget-request>"
  (cl:format cl:nil "string[] position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetExchangeTarget-request)))
  "Returns full string definition for message of type 'SetExchangeTarget-request"
  (cl:format cl:nil "string[] position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetExchangeTarget-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'position) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4 (cl:length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetExchangeTarget-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetExchangeTarget-request
    (cl:cons ':position (position msg))
))
;//! \htmlinclude SetExchangeTarget-response.msg.html

(cl:defclass <SetExchangeTarget-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass SetExchangeTarget-response (<SetExchangeTarget-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetExchangeTarget-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetExchangeTarget-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-srv:<SetExchangeTarget-response> is deprecated: use warehouse-srv:SetExchangeTarget-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SetExchangeTarget-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:success-val is deprecated.  Use warehouse-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <SetExchangeTarget-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:message-val is deprecated.  Use warehouse-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetExchangeTarget-response>) ostream)
  "Serializes a message object of type '<SetExchangeTarget-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetExchangeTarget-response>) istream)
  "Deserializes a message object of type '<SetExchangeTarget-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetExchangeTarget-response>)))
  "Returns string type for a service object of type '<SetExchangeTarget-response>"
  "warehouse/SetExchangeTargetResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetExchangeTarget-response)))
  "Returns string type for a service object of type 'SetExchangeTarget-response"
  "warehouse/SetExchangeTargetResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetExchangeTarget-response>)))
  "Returns md5sum for a message object of type '<SetExchangeTarget-response>"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetExchangeTarget-response)))
  "Returns md5sum for a message object of type 'SetExchangeTarget-response"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetExchangeTarget-response>)))
  "Returns full string definition for message of type '<SetExchangeTarget-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetExchangeTarget-response)))
  "Returns full string definition for message of type 'SetExchangeTarget-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetExchangeTarget-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetExchangeTarget-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetExchangeTarget-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetExchangeTarget)))
  'SetExchangeTarget-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetExchangeTarget)))
  'SetExchangeTarget-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetExchangeTarget)))
  "Returns string type for a service object of type '<SetExchangeTarget>"
  "warehouse/SetExchangeTarget")