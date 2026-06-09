; Auto-generated. Do not edit!


(cl:in-package warehouse-msg)


;//! \htmlinclude Rotate.msg.html

(cl:defclass <Rotate> (roslisp-msg-protocol:ros-message)
  ((r
    :reader r
    :initarg :r
    :type cl:float
    :initform 0.0)
   (p
    :reader p
    :initarg :p
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0))
)

(cl:defclass Rotate (<Rotate>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Rotate>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Rotate)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-msg:<Rotate> is deprecated: use warehouse-msg:Rotate instead.")))

(cl:ensure-generic-function 'r-val :lambda-list '(m))
(cl:defmethod r-val ((m <Rotate>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:r-val is deprecated.  Use warehouse-msg:r instead.")
  (r m))

(cl:ensure-generic-function 'p-val :lambda-list '(m))
(cl:defmethod p-val ((m <Rotate>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:p-val is deprecated.  Use warehouse-msg:p instead.")
  (p m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <Rotate>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:y-val is deprecated.  Use warehouse-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Rotate>) ostream)
  "Serializes a message object of type '<Rotate>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'r))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'p))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Rotate>) istream)
  "Deserializes a message object of type '<Rotate>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'r) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'p) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Rotate>)))
  "Returns string type for a message object of type '<Rotate>"
  "warehouse/Rotate")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Rotate)))
  "Returns string type for a message object of type 'Rotate"
  "warehouse/Rotate")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Rotate>)))
  "Returns md5sum for a message object of type '<Rotate>"
  "c5585e6b09b13f56ed964334fed50470")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Rotate)))
  "Returns md5sum for a message object of type 'Rotate"
  "c5585e6b09b13f56ed964334fed50470")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Rotate>)))
  "Returns full string definition for message of type '<Rotate>"
  (cl:format cl:nil "float64 r~%float64 p~%float64 y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Rotate)))
  "Returns full string definition for message of type 'Rotate"
  (cl:format cl:nil "float64 r~%float64 p~%float64 y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Rotate>))
  (cl:+ 0
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Rotate>))
  "Converts a ROS message object to a list"
  (cl:list 'Rotate
    (cl:cons ':r (r msg))
    (cl:cons ':p (p msg))
    (cl:cons ':y (y msg))
))
