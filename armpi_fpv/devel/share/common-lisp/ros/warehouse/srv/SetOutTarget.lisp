; Auto-generated. Do not edit!


(cl:in-package warehouse-srv)


;//! \htmlinclude SetOutTarget-request.msg.html

(cl:defclass <SetOutTarget-request> (roslisp-msg-protocol:ros-message)
  ((position
    :reader position
    :initarg :position
    :type (cl:vector cl:string)
   :initform (cl:make-array 0 :element-type 'cl:string :initial-element "")))
)

(cl:defclass SetOutTarget-request (<SetOutTarget-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetOutTarget-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetOutTarget-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-srv:<SetOutTarget-request> is deprecated: use warehouse-srv:SetOutTarget-request instead.")))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <SetOutTarget-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:position-val is deprecated.  Use warehouse-srv:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetOutTarget-request>) ostream)
  "Serializes a message object of type '<SetOutTarget-request>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetOutTarget-request>) istream)
  "Deserializes a message object of type '<SetOutTarget-request>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetOutTarget-request>)))
  "Returns string type for a service object of type '<SetOutTarget-request>"
  "warehouse/SetOutTargetRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetOutTarget-request)))
  "Returns string type for a service object of type 'SetOutTarget-request"
  "warehouse/SetOutTargetRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetOutTarget-request>)))
  "Returns md5sum for a message object of type '<SetOutTarget-request>"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetOutTarget-request)))
  "Returns md5sum for a message object of type 'SetOutTarget-request"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetOutTarget-request>)))
  "Returns full string definition for message of type '<SetOutTarget-request>"
  (cl:format cl:nil "string[] position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetOutTarget-request)))
  "Returns full string definition for message of type 'SetOutTarget-request"
  (cl:format cl:nil "string[] position~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetOutTarget-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'position) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4 (cl:length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetOutTarget-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetOutTarget-request
    (cl:cons ':position (position msg))
))
;//! \htmlinclude SetOutTarget-response.msg.html

(cl:defclass <SetOutTarget-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass SetOutTarget-response (<SetOutTarget-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetOutTarget-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetOutTarget-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-srv:<SetOutTarget-response> is deprecated: use warehouse-srv:SetOutTarget-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <SetOutTarget-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:success-val is deprecated.  Use warehouse-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <SetOutTarget-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-srv:message-val is deprecated.  Use warehouse-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetOutTarget-response>) ostream)
  "Serializes a message object of type '<SetOutTarget-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetOutTarget-response>) istream)
  "Deserializes a message object of type '<SetOutTarget-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetOutTarget-response>)))
  "Returns string type for a service object of type '<SetOutTarget-response>"
  "warehouse/SetOutTargetResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetOutTarget-response)))
  "Returns string type for a service object of type 'SetOutTarget-response"
  "warehouse/SetOutTargetResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetOutTarget-response>)))
  "Returns md5sum for a message object of type '<SetOutTarget-response>"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetOutTarget-response)))
  "Returns md5sum for a message object of type 'SetOutTarget-response"
  "73a1985add1021f1387d4b37533c9d6c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetOutTarget-response>)))
  "Returns full string definition for message of type '<SetOutTarget-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetOutTarget-response)))
  "Returns full string definition for message of type 'SetOutTarget-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetOutTarget-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetOutTarget-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetOutTarget-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetOutTarget)))
  'SetOutTarget-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetOutTarget)))
  'SetOutTarget-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetOutTarget)))
  "Returns string type for a service object of type '<SetOutTarget>"
  "warehouse/SetOutTarget")