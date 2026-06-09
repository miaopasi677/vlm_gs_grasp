;; Auto-generated. Do not edit!


(when (boundp 'warehouse::Rotate)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'Rotate (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::ROTATE")
  (make-package "WAREHOUSE::ROTATE"))

(in-package "ROS")
;;//! \htmlinclude Rotate.msg.html


(defclass warehouse::Rotate
  :super ros::object
  :slots (_r _p _y ))

(defmethod warehouse::Rotate
  (:init
   (&key
    ((:r __r) 0.0)
    ((:p __p) 0.0)
    ((:y __y) 0.0)
    )
   (send-super :init)
   (setq _r (float __r))
   (setq _p (float __p))
   (setq _y (float __y))
   self)
  (:r
   (&optional __r)
   (if __r (setq _r __r)) _r)
  (:p
   (&optional __p)
   (if __p (setq _p __p)) _p)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; float64 _r
    8
    ;; float64 _p
    8
    ;; float64 _y
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _r
       (sys::poke _r (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _p
       (sys::poke _p (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _r
     (setq _r (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _p
     (setq _p (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get warehouse::Rotate :md5sum-) "c5585e6b09b13f56ed964334fed50470")
(setf (get warehouse::Rotate :datatype-) "warehouse/Rotate")
(setf (get warehouse::Rotate :definition-)
      "float64 r
float64 p
float64 y

")



(provide :warehouse/Rotate "c5585e6b09b13f56ed964334fed50470")


