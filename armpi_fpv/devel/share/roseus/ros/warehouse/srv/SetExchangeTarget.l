;; Auto-generated. Do not edit!


(when (boundp 'warehouse::SetExchangeTarget)
  (if (not (find-package "WAREHOUSE"))
    (make-package "WAREHOUSE"))
  (shadow 'SetExchangeTarget (find-package "WAREHOUSE")))
(unless (find-package "WAREHOUSE::SETEXCHANGETARGET")
  (make-package "WAREHOUSE::SETEXCHANGETARGET"))
(unless (find-package "WAREHOUSE::SETEXCHANGETARGETREQUEST")
  (make-package "WAREHOUSE::SETEXCHANGETARGETREQUEST"))
(unless (find-package "WAREHOUSE::SETEXCHANGETARGETRESPONSE")
  (make-package "WAREHOUSE::SETEXCHANGETARGETRESPONSE"))

(in-package "ROS")





(defclass warehouse::SetExchangeTargetRequest
  :super ros::object
  :slots (_position ))

(defmethod warehouse::SetExchangeTargetRequest
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

(defclass warehouse::SetExchangeTargetResponse
  :super ros::object
  :slots (_success _message ))

(defmethod warehouse::SetExchangeTargetResponse
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

(defclass warehouse::SetExchangeTarget
  :super ros::object
  :slots ())

(setf (get warehouse::SetExchangeTarget :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetExchangeTarget :datatype-) "warehouse/SetExchangeTarget")
(setf (get warehouse::SetExchangeTarget :request) warehouse::SetExchangeTargetRequest)
(setf (get warehouse::SetExchangeTarget :response) warehouse::SetExchangeTargetResponse)

(defmethod warehouse::SetExchangeTargetRequest
  (:response () (instance warehouse::SetExchangeTargetResponse :init)))

(setf (get warehouse::SetExchangeTargetRequest :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetExchangeTargetRequest :datatype-) "warehouse/SetExchangeTargetRequest")
(setf (get warehouse::SetExchangeTargetRequest :definition-)
      "string[] position
---
bool success
string message

")

(setf (get warehouse::SetExchangeTargetResponse :md5sum-) "73a1985add1021f1387d4b37533c9d6c")
(setf (get warehouse::SetExchangeTargetResponse :datatype-) "warehouse/SetExchangeTargetResponse")
(setf (get warehouse::SetExchangeTargetResponse :definition-)
      "string[] position
---
bool success
string message

")



(provide :warehouse/SetExchangeTarget "73a1985add1021f1387d4b37533c9d6c")


