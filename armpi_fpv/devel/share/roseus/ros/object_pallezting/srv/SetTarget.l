;; Auto-generated. Do not edit!


(when (boundp 'object_pallezting::SetTarget)
  (if (not (find-package "OBJECT_PALLEZTING"))
    (make-package "OBJECT_PALLEZTING"))
  (shadow 'SetTarget (find-package "OBJECT_PALLEZTING")))
(unless (find-package "OBJECT_PALLEZTING::SETTARGET")
  (make-package "OBJECT_PALLEZTING::SETTARGET"))
(unless (find-package "OBJECT_PALLEZTING::SETTARGETREQUEST")
  (make-package "OBJECT_PALLEZTING::SETTARGETREQUEST"))
(unless (find-package "OBJECT_PALLEZTING::SETTARGETRESPONSE")
  (make-package "OBJECT_PALLEZTING::SETTARGETRESPONSE"))

(in-package "ROS")





(defclass object_pallezting::SetTargetRequest
  :super ros::object
  :slots (_color _tag ))

(defmethod object_pallezting::SetTargetRequest
  (:init
   (&key
    ((:color __color) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:tag __tag) (let (r) (dotimes (i 0) (push "" r)) r))
    )
   (send-super :init)
   (setq _color __color)
   (setq _tag __tag)
   self)
  (:color
   (&optional __color)
   (if __color (setq _color __color)) _color)
  (:tag
   (&optional __tag)
   (if __tag (setq _tag __tag)) _tag)
  (:serialization-length
   ()
   (+
    ;; string[] _color
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _color)) 4
    ;; string[] _tag
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _tag)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string[] _color
     (write-long (length _color) s)
     (dolist (elem _color)
       (write-long (length elem) s) (princ elem s)
       )
     ;; string[] _tag
     (write-long (length _tag) s)
     (dolist (elem _tag)
       (write-long (length elem) s) (princ elem s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string[] _color
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _color (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _color i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; string[] _tag
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _tag (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _tag i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;;
   self)
  )

(defclass object_pallezting::SetTargetResponse
  :super ros::object
  :slots (_success _message ))

(defmethod object_pallezting::SetTargetResponse
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

(defclass object_pallezting::SetTarget
  :super ros::object
  :slots ())

(setf (get object_pallezting::SetTarget :md5sum-) "15a6bbca6b7bdaa8c9ab1c07de00a6ac")
(setf (get object_pallezting::SetTarget :datatype-) "object_pallezting/SetTarget")
(setf (get object_pallezting::SetTarget :request) object_pallezting::SetTargetRequest)
(setf (get object_pallezting::SetTarget :response) object_pallezting::SetTargetResponse)

(defmethod object_pallezting::SetTargetRequest
  (:response () (instance object_pallezting::SetTargetResponse :init)))

(setf (get object_pallezting::SetTargetRequest :md5sum-) "15a6bbca6b7bdaa8c9ab1c07de00a6ac")
(setf (get object_pallezting::SetTargetRequest :datatype-) "object_pallezting/SetTargetRequest")
(setf (get object_pallezting::SetTargetRequest :definition-)
      "string[] color
string[] tag
---
bool success
string message

")

(setf (get object_pallezting::SetTargetResponse :md5sum-) "15a6bbca6b7bdaa8c9ab1c07de00a6ac")
(setf (get object_pallezting::SetTargetResponse :datatype-) "object_pallezting/SetTargetResponse")
(setf (get object_pallezting::SetTargetResponse :definition-)
      "string[] color
string[] tag
---
bool success
string message

")



(provide :object_pallezting/SetTarget "15a6bbca6b7bdaa8c9ab1c07de00a6ac")


