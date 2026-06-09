;; Auto-generated. Do not edit!


(when (boundp 'warehouse::SetInTarget)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'SetInTarget (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::SETINTARGET")
  (make-package "WAREHOUSE::SETINTARGET"))
(unless (find-package "WAREHOUSE::SETINTARGETREQUEST")
  (make-package "WAREHOUSE::SETINTARGETREQUEST"))
(unless (find-package "WAREHOUSE::SETINTARGETRESPONSE")
  (make-package "WAREHOUSE::SETINTARGETRESPONSE"))

(in-package "ROS")





(defclass warehouse::SetInTargetRequest
  :super ros::object
  :slots (_goods _position ))

(defmethod warehouse::SetInTargetRequest
  (:init
   (&key
    ((:goods __goods) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:position __position) (let (r) (dotimes (i 0) (push "" r)) r))
    )
   (send-super :init)
   (setq _goods __goods)
   (setq _position __position)
   self)
  (:goods
   (&optional __goods)
   (if __goods (setq _goods __goods)) _goods)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:serialization-length
   ()
   (+
    ;; string[] _goods
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _goods)) 4
    ;; string[] _position
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _position)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string[] _goods
     (write-long (length _goods) s)
     (dolist (elem _goods)
       (write-long (length elem) s) (princ elem s)
       )
     ;; string[] _position
     (write-long (length _position) s)
     (dolist (elem _position)
       (write-long (length elem) s) (princ elem s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string[] _goods
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _goods (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _goods i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
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

(defclass warehouse::SetInTargetResponse
  :super ros::object
  :slots (_success _message ))

(defmethod warehouse::SetInTargetResponse
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

(defclass warehouse::SetInTarget
  :super ros::object
  :slots ())

(setf (get warehouse::SetInTarget :md5sum-) "3a5188a131c4178e5804bbb1ba83e677")
(setf (get warehouse::SetInTarget :datatype-) "warehouse/SetInTarget")
(setf (get warehouse::SetInTarget :request) warehouse::SetInTargetRequest)
(setf (get warehouse::SetInTarget :response) warehouse::SetInTargetResponse)

(defmethod warehouse::SetInTargetRequest
  (:response () (instance warehouse::SetInTargetResponse :init)))

(setf (get warehouse::SetInTargetRequest :md5sum-) "3a5188a131c4178e5804bbb1ba83e677")
(setf (get warehouse::SetInTargetRequest :datatype-) "warehouse/SetInTargetRequest")
(setf (get warehouse::SetInTargetRequest :definition-)
      "string[] goods
string[] position
---
bool success
string message

")

(setf (get warehouse::SetInTargetResponse :md5sum-) "3a5188a131c4178e5804bbb1ba83e677")
(setf (get warehouse::SetInTargetResponse :datatype-) "warehouse/SetInTargetResponse")
(setf (get warehouse::SetInTargetResponse :definition-)
      "string[] goods
string[] position
---
bool success
string message

")



(provide :warehouse/SetInTarget "3a5188a131c4178e5804bbb1ba83e677")


