
(cl:in-package :asdf)

(defsystem "rand_walker-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BumperEvent" :depends-on ("_package_BumperEvent"))
    (:file "_package_BumperEvent" :depends-on ("_package"))
    (:file "CliffEvent" :depends-on ("_package_CliffEvent"))
    (:file "_package_CliffEvent" :depends-on ("_package"))
    (:file "Led" :depends-on ("_package_Led"))
    (:file "_package_Led" :depends-on ("_package"))
    (:file "WheelDropEvent" :depends-on ("_package_WheelDropEvent"))
    (:file "_package_WheelDropEvent" :depends-on ("_package"))
  ))