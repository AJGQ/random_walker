;; Auto-generated. Do not edit!


(when (boundp 'rand_walker::BumperEvent)
  (if (not (find-package "RAND_WALKER"))
    (make-package "RAND_WALKER"))
  (shadow 'BumperEvent (find-package "RAND_WALKER")))
(unless (find-package "RAND_WALKER::BUMPEREVENT")
  (make-package "RAND_WALKER::BUMPEREVENT"))

(in-package "ROS")
;;//! \htmlinclude BumperEvent.msg.html


(intern "*LEFT*" (find-package "RAND_WALKER::BUMPEREVENT"))
(shadow '*LEFT* (find-package "RAND_WALKER::BUMPEREVENT"))
(defconstant rand_walker::BumperEvent::*LEFT* 0)
(intern "*CENTER*" (find-package "RAND_WALKER::BUMPEREVENT"))
(shadow '*CENTER* (find-package "RAND_WALKER::BUMPEREVENT"))
(defconstant rand_walker::BumperEvent::*CENTER* 1)
(intern "*RIGHT*" (find-package "RAND_WALKER::BUMPEREVENT"))
(shadow '*RIGHT* (find-package "RAND_WALKER::BUMPEREVENT"))
(defconstant rand_walker::BumperEvent::*RIGHT* 2)
(intern "*RELEASED*" (find-package "RAND_WALKER::BUMPEREVENT"))
(shadow '*RELEASED* (find-package "RAND_WALKER::BUMPEREVENT"))
(defconstant rand_walker::BumperEvent::*RELEASED* 0)
(intern "*PRESSED*" (find-package "RAND_WALKER::BUMPEREVENT"))
(shadow '*PRESSED* (find-package "RAND_WALKER::BUMPEREVENT"))
(defconstant rand_walker::BumperEvent::*PRESSED* 1)
(defclass rand_walker::BumperEvent
  :super ros::object
  :slots (_bumper _state ))

(defmethod rand_walker::BumperEvent
  (:init
   (&key
    ((:bumper __bumper) 0)
    ((:state __state) 0)
    )
   (send-super :init)
   (setq _bumper (round __bumper))
   (setq _state (round __state))
   self)
  (:bumper
   (&optional __bumper)
   (if __bumper (setq _bumper __bumper)) _bumper)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; uint8 _bumper
    1
    ;; uint8 _state
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _bumper
       (write-byte _bumper s)
     ;; uint8 _state
       (write-byte _state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _bumper
     (setq _bumper (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _state
     (setq _state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get rand_walker::BumperEvent :md5sum-) "ffe360cd50f14f9251d9844083e72ac5")
(setf (get rand_walker::BumperEvent :datatype-) "rand_walker/BumperEvent")
(setf (get rand_walker::BumperEvent :definition-)
      "# bumper
uint8 LEFT   = 0
uint8 CENTER = 1
uint8 RIGHT  = 2

# state
uint8 RELEASED = 0
uint8 PRESSED  = 1

uint8 bumper
uint8 state

")



(provide :rand_walker/BumperEvent "ffe360cd50f14f9251d9844083e72ac5")


