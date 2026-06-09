
(cl:in-package :asdf)

(defsystem "warehouse-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "Grasp" :depends-on ("_package_Grasp"))
    (:file "_package_Grasp" :depends-on ("_package"))
    (:file "Pose" :depends-on ("_package_Pose"))
    (:file "_package_Pose" :depends-on ("_package"))
    (:file "Rotate" :depends-on ("_package_Rotate"))
    (:file "_package_Rotate" :depends-on ("_package"))
  ))