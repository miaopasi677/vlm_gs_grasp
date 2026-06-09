; Auto-generated. Do not edit!


(cl:in-package warehouse-msg)


;//! \htmlinclude Grasp.msg.html

(cl:defclass <Grasp> (roslisp-msg-protocol:ros-message)
  ((grasp_pos
    :reader grasp_pos
    :initarg :grasp_pos
    :type warehouse-msg:Pose
    :initform (cl:make-instance 'warehouse-msg:Pose))
   (grasp_approach
    :reader grasp_approach
    :initarg :grasp_approach
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (grasp_retreat
    :reader grasp_retreat
    :initarg :grasp_retreat
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (up
    :reader up
    :initarg :up
    :type cl:float
    :initform 0.0)
   (grasp_posture
    :reader grasp_posture
    :initarg :grasp_posture
    :type cl:fixnum
    :initform 0)
   (pre_grasp_posture
    :reader pre_grasp_posture
    :initarg :pre_grasp_posture
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Grasp (<Grasp>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Grasp>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Grasp)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name warehouse-msg:<Grasp> is deprecated: use warehouse-msg:Grasp instead.")))

(cl:ensure-generic-function 'grasp_pos-val :lambda-list '(m))
(cl:defmethod grasp_pos-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:grasp_pos-val is deprecated.  Use warehouse-msg:grasp_pos instead.")
  (grasp_pos m))

(cl:ensure-generic-function 'grasp_approach-val :lambda-list '(m))
(cl:defmethod grasp_approach-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:grasp_approach-val is deprecated.  Use warehouse-msg:grasp_approach instead.")
  (grasp_approach m))

(cl:ensure-generic-function 'grasp_retreat-val :lambda-list '(m))
(cl:defmethod grasp_retreat-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:grasp_retreat-val is deprecated.  Use warehouse-msg:grasp_retreat instead.")
  (grasp_retreat m))

(cl:ensure-generic-function 'up-val :lambda-list '(m))
(cl:defmethod up-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:up-val is deprecated.  Use warehouse-msg:up instead.")
  (up m))

(cl:ensure-generic-function 'grasp_posture-val :lambda-list '(m))
(cl:defmethod grasp_posture-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:grasp_posture-val is deprecated.  Use warehouse-msg:grasp_posture instead.")
  (grasp_posture m))

(cl:ensure-generic-function 'pre_grasp_posture-val :lambda-list '(m))
(cl:defmethod pre_grasp_posture-val ((m <Grasp>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader warehouse-msg:pre_grasp_posture-val is deprecated.  Use warehouse-msg:pre_grasp_posture instead.")
  (pre_grasp_posture m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Grasp>) ostream)
  "Serializes a message object of type '<Grasp>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grasp_pos) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grasp_approach) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grasp_retreat) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'up))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let* ((signed (cl:slot-value msg 'grasp_posture)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'pre_grasp_posture)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Grasp>) istream)
  "Deserializes a message object of type '<Grasp>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grasp_pos) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grasp_approach) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grasp_retreat) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'up) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'grasp_posture) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'pre_grasp_posture) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Grasp>)))
  "Returns string type for a message object of type '<Grasp>"
  "warehouse/Grasp")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Grasp)))
  "Returns string type for a message object of type 'Grasp"
  "warehouse/Grasp")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Grasp>)))
  "Returns md5sum for a message object of type '<Grasp>"
  "70d37fa314d53b4952d2f54caf3874d2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Grasp)))
  "Returns md5sum for a message object of type 'Grasp"
  "70d37fa314d53b4952d2f54caf3874d2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Grasp>)))
  "Returns full string definition for message of type '<Grasp>"
  (cl:format cl:nil "# 夹取时的姿态和位置~%warehouse/Pose grasp_pos~%~%# 接近时的距离和方向~%geometry_msgs/Vector3 grasp_approach~%~%# 撤离时的距离和方向~%geometry_msgs/Vector3 grasp_retreat~%~%# 抬高高度~%float64 up~%~%# 夹取时夹持器姿态~%int16 grasp_posture~%~%# 夹取前夹持器姿态~%int16 pre_grasp_posture~%~%~%================================================================================~%MSG: warehouse/Pose~%geometry_msgs/Point position~%warehouse/Rotate rotation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: warehouse/Rotate~%float64 r~%float64 p~%float64 y~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Grasp)))
  "Returns full string definition for message of type 'Grasp"
  (cl:format cl:nil "# 夹取时的姿态和位置~%warehouse/Pose grasp_pos~%~%# 接近时的距离和方向~%geometry_msgs/Vector3 grasp_approach~%~%# 撤离时的距离和方向~%geometry_msgs/Vector3 grasp_retreat~%~%# 抬高高度~%float64 up~%~%# 夹取时夹持器姿态~%int16 grasp_posture~%~%# 夹取前夹持器姿态~%int16 pre_grasp_posture~%~%~%================================================================================~%MSG: warehouse/Pose~%geometry_msgs/Point position~%warehouse/Rotate rotation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: warehouse/Rotate~%float64 r~%float64 p~%float64 y~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Grasp>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grasp_pos))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grasp_approach))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grasp_retreat))
     8
     2
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Grasp>))
  "Converts a ROS message object to a list"
  (cl:list 'Grasp
    (cl:cons ':grasp_pos (grasp_pos msg))
    (cl:cons ':grasp_approach (grasp_approach msg))
    (cl:cons ':grasp_retreat (grasp_retreat msg))
    (cl:cons ':up (up msg))
    (cl:cons ':grasp_posture (grasp_posture msg))
    (cl:cons ':pre_grasp_posture (pre_grasp_posture msg))
))
