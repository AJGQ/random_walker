;; Auto-generated. Do not edit!


(when (boundp 'rand_walker::WheelDropEvent)
  (if (not (find-package "RAND_WALKER"))
    (make-package "RAND_WALKER"))
  (shadow 'WheelDropEvent (find-package "RAND_WALKER")))
(unless (find-package "RAND_WALKER::WHEELDROPEVENT")
  (make-package "RAND_WALKER::WHEELDROPEVENT"))

(in-package "ROS")
;;//! \htmlinclude WheelDropEvent.msg.html


(intern "*LEFT*" (find-package "RAND_WALKER::WHEELDROPEVENT"))
(shadow '*LEFT* (find-package "RAND_WALKER::WHEELDROPEVENT"))
(defconstant rand_walker::WheelDropEvent::*LEFT* 0)
(intern "*RIGHT*" (find-package "RAND_WALKER::WHEELDROPEVENT"))
(shadow '*RIGHT* (find-package "RAND_WALKER::WHEELDROPEVENT"))
(defconstant rand_walker::WheelDropEvent::*RIGHT* 1)
(intern "*RAISED*" (find-package "RAND_WALKER::WHEELDROPEVENT"))
(shadow '*RAISED* (find-package "RAND_WALKER::WHEELDROPEVENT"))
(defconstant rand_walker::WheelDropEvent::*RAISED* 0)
(intern "*DROPPED*" (find-package "RAND_WALKER::WHEELDROPEVENT"))
(shadow '*DROPPED* (find-package "RAND_WALKER::WHEELDROPEVENT"))
(defconstant rand_walker::WheelDropEvent::*DROPPED* 1)
(defclass rand_walker::WheelDropEvent
  :super ros::object
  :slots (_wheel _state ))

(defmethod rand_walker::WheelDropEvent
  (:init
   (&key
    ((:wheel __wheel) 0)
    ((:state __state) 0)
    )
   (send-super :init)
   (setq _wheel (round __wheel))
   (setq _state (round __state))
   self)
  (:wheel
   (&optional __wheel)
   (if __wheel (setq _wheel __wheel)) _wheel)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; uint8 _wheel
    1
    ;; uint8 _state
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _wheel
       (write-byte _wheel s)
     ;; uint8 _state
       (write-byte _state s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _wheel
     (setq _wheel (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _state
     (setq _state (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get rand_walker::WheelDropEvent :md5sum-) "e102837d89384d67669a0df86b63f33b")
(setf (get rand_walker::WheelDropEvent :datatype-) "rand_walker/WheelDropEvent")
(setf (get rand_walker::WheelDropEvent :definition-)
      "# wheel
uint8 LEFT  = 0
uint8 RIGHT = 1

# state
uint8 RAISED  = 0
uint8 DROPPED = 1

uint8 wheel
uint8 state

")



(provide :rand_walker/WheelDropEvent "e102837d89384d67669a0df86b63f33b")


