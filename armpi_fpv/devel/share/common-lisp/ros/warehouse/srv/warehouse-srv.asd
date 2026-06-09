
(cl:in-package :asdf)

(defsystem "warehouse-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "SetExchangeTarget" :depends-on ("_package_SetExchangeTarget"))
    (:file "_package_SetExchangeTarget" :depends-on ("_package"))
    (:file "SetInTarget" :depends-on ("_package_SetInTarget"))
    (:file "_package_SetInTarget" :depends-on ("_package"))
    (:file "SetOutTarget" :depends-on ("_package_SetOutTarget"))
    (:file "_package_SetOutTarget" :depends-on ("_package"))
  ))