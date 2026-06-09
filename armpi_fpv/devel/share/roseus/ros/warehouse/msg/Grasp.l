;; Auto-generated. Do not edit!


(when (boundp 'warehouse::Grasp)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'Grasp (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::GRASP")
  (make-package "WAREHOUSE::GRASP"))

(in-package "ROS")
;;//! \htmlinclude Grasp.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass warehouse::Grasp
  :super ros::object
  :slots (_grasp_pos _grasp_approach _grasp_retreat _up _grasp_posture _pre_grasp_posture ))

(defmethod warehouse::Grasp
  (:init
   (&key
    ((:grasp_pos __grasp_pos) (instance warehouse::Pose :init))
    ((:grasp_approach __grasp_approach) (instance geometry_msgs::Vector3 :init))
    ((:grasp_retreat __grasp_retreat) (instance geometry_msgs::Vector3 :init))
    ((:up __up) 0.0)
    ((:grasp_posture __grasp_posture) 0)
    ((:pre_grasp_posture __pre_grasp_posture) 0)
    )
   (send-super :init)
   (setq _grasp_pos __grasp_pos)
   (setq _grasp_approach __grasp_approach)
   (setq _grasp_retreat __grasp_retreat)
   (setq _up (float __up))
   (setq _grasp_posture (round __grasp_posture))
   (setq _pre_grasp_posture (round __pre_grasp_posture))
   self)
  (:grasp_pos
   (&rest __grasp_pos)
   (if (keywordp (car __grasp_pos))
       (send* _grasp_pos __grasp_pos)
     (progn
       (if __grasp_pos (setq _grasp_pos (car __grasp_pos)))
       _grasp_pos)))
  (:grasp_approach
   (&rest __grasp_approach)
   (if (keywordp (car __grasp_approach))
       (send* _grasp_approach __grasp_approach)
     (progn
       (if __grasp_approach (setq _grasp_approach (car __grasp_approach)))
       _grasp_approach)))
  (:grasp_retreat
   (&rest __grasp_retreat)
   (if (keywordp (car __grasp_retreat))
       (send* _grasp_retreat __grasp_retreat)
     (progn
       (if __grasp_retreat (setq _grasp_retreat (car __grasp_retreat)))
       _grasp_retreat)))
  (:up
   (&optional __up)
   (if __up (setq _up __up)) _up)
  (:grasp_posture
   (&optional __grasp_posture)
   (if __grasp_posture (setq _grasp_posture __grasp_posture)) _grasp_posture)
  (:pre_grasp_posture
   (&optional __pre_grasp_posture)
   (if __pre_grasp_posture (setq _pre_grasp_posture __pre_grasp_posture)) _pre_grasp_posture)
  (:serialization-length
   ()
   (+
    ;; warehouse/Pose _grasp_pos
    (send _grasp_pos :serialization-length)
    ;; geometry_msgs/Vector3 _grasp_approach
    (send _grasp_approach :serialization-length)
    ;; geometry_msgs/Vector3 _grasp_retreat
    (send _grasp_retreat :serialization-length)
    ;; float64 _up
    8
    ;; int16 _grasp_posture
    2
    ;; int16 _pre_grasp_posture
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; warehouse/Pose _grasp_pos
       (send _grasp_pos :serialize s)
     ;; geometry_msgs/Vector3 _grasp_approach
       (send _grasp_approach :serialize s)
     ;; geometry_msgs/Vector3 _grasp_retreat
       (send _grasp_retreat :serialize s)
     ;; float64 _up
       (sys::poke _up (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int16 _grasp_posture
       (write-word _grasp_posture s)
     ;; int16 _pre_grasp_posture
       (write-word _pre_grasp_posture s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; warehouse/Pose _grasp_pos
     (send _grasp_pos :deserialize buf ptr-) (incf ptr- (send _grasp_pos :serialization-length))
   ;; geometry_msgs/Vector3 _grasp_approach
     (send _grasp_approach :deserialize buf ptr-) (incf ptr- (send _grasp_approach :serialization-length))
   ;; geometry_msgs/Vector3 _grasp_retreat
     (send _grasp_retreat :deserialize buf ptr-) (incf ptr- (send _grasp_retreat :serialization-length))
   ;; float64 _up
     (setq _up (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int16 _grasp_posture
     (setq _grasp_posture (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16 _pre_grasp_posture
     (setq _pre_grasp_posture (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get warehouse::Grasp :md5sum-) "70d37fa314d53b4952d2f54caf3874d2")
(setf (get warehouse::Grasp :datatype-) "warehouse/Grasp")
(setf (get warehouse::Grasp :definition-)
      "# 夹取时的姿态和位置
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
")



(provide :warehouse/Grasp "70d37fa314d53b4952d2f54caf3874d2")


