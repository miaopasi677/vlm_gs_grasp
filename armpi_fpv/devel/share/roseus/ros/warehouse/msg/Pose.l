;; Auto-generated. Do not edit!


(when (boundp 'warehouse::Pose)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'Pose (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::POSE")
  (make-package "WAREHOUSE::POSE"))

(in-package "ROS")
;;//! \htmlinclude Pose.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass warehouse::Pose
  :super ros::object
  :slots (_position _rotation ))

(defmethod warehouse::Pose
  (:init
   (&key
    ((:position __position) (instance geometry_msgs::Point :init))
    ((:rotation __rotation) (instance warehouse::Rotate :init))
    )
   (send-super :init)
   (setq _position __position)
   (setq _rotation __rotation)
   self)
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:rotation
   (&rest __rotation)
   (if (keywordp (car __rotation))
       (send* _rotation __rotation)
     (progn
       (if __rotation (setq _rotation (car __rotation)))
       _rotation)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Point _position
    (send _position :serialization-length)
    ;; warehouse/Rotate _rotation
    (send _rotation :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Point _position
       (send _position :serialize s)
     ;; warehouse/Rotate _rotation
       (send _rotation :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Point _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; warehouse/Rotate _rotation
     (send _rotation :deserialize buf ptr-) (incf ptr- (send _rotation :serialization-length))
   ;;
   self)
  )

(setf (get warehouse::Pose :md5sum-) "c2e48a5367d8266f8aaac3d6b58f5cb2")
(setf (get warehouse::Pose :datatype-) "warehouse/Pose")
(setf (get warehouse::Pose :definition-)
      "geometry_msgs/Point position
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

")



(provide :warehouse/Pose "c2e48a5367d8266f8aaac3d6b58f5cb2")


