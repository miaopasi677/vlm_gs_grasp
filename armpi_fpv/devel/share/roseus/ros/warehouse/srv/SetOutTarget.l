;; Auto-generated. Do not edit!


(when (boundp 'warehouse::SetOutTarget)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'SetOutTarget (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::SETOUTTARGET")
  (make-package "WAREHOUSE::SETOUTTARGET"))
(unless (find-package "WAREHOUSE::SETOUTTARGETREQUEST")
  (make-package "WAREHOUSE::SETOUTTARGETREQUEST"))
(unless (find-package "WAREHOUSE::SETOUTTARGETRESPONSE")
  (make-package "WAREHOUSE::SETOUTTARGETRESPONSE"))

(in-package "ROS")





(defclass warehouse::SetOutTargetRequest
  :super ros::object
  :slots (_position ))

(defmethod warehouse::SetOutTargetRequest
  (:init
   (&key
    ((:position __position) (let (r) (dotimes (i 0) (push "" r)) r))
    )
   (send-super :init)
   (setq _position __position)
   self)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; string[] _position
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _position)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string[] _position
     (write-long (length _position) s)
     (dolist (elem _position)
       (write-long (length elem) s) (princ elem s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string[] _position
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _position (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _position i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;;
   self)
  )

(defclass warehouse::SetOutTargetResponse
  :super ros::object
  :slots (_success _message ))

(defmethod warehouse::SetOutTargetResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass warehouse::SetOutTarget
  :super ros::object
  :slots ())

(setf (get warehouse::SetOutTarget :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetOutTarget :datatype-) "warehouse/SetOutTarget")
(setf (get warehouse::SetOutTarget :request) warehouse::SetOutTargetRequest)
(setf (get warehouse::SetOutTarget :response) warehouse::SetOutTargetResponse)

(defmethod warehouse::SetOutTargetRequest
  (:response () (instance warehouse::SetOutTargetResponse :init)))

(setf (get warehouse::SetOutTargetRequest :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetOutTargetRequest :datatype-) "warehouse/SetOutTargetRequest")
(setf (get warehouse::SetOutTargetRequest :definition-)
      "string[] position
---
bool success
string message

")

(setf (get warehouse::SetOutTargetResponse :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetOutTargetResponse :datatype-) "warehouse/SetOutTargetResponse")
(setf (get warehouse::SetOutTargetResponse :definition-)
      "string[] position
---
bool success
string message

")



(provide :warehouse/SetOutTarget "73a1985add1021f1387d4b37533c9d6c")


