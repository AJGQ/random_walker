;; Auto-generated. Do not edit!


(when (boundp 'rand_walker::Led)
  (if (not (find-package "RAND_WALKER"))
    (make-package "RAND_WALKER"))
  (shadow 'Led (find-package "RAND_WALKER")))
(unless (find-package "RAND_WALKER::LED")
  (make-package "RAND_WALKER::LED"))

(in-package "ROS")
;;//! \htmlinclude Led.msg.html


(intern "*BLACK*" (find-package "RAND_WALKER::LED"))
(shadow '*BLACK* (find-package "RAND_WALKER::LED"))
(defconstant rand_walker::Led::*BLACK* 0)
(intern "*GREEN*" (find-package "RAND_WALKER::LED"))
(shadow '*GREEN* (find-package "RAND_WALKER::LED"))
(defconstant rand_walker::Led::*GREEN* 1)
(intern "*ORANGE*" (find-package "RAND_WALKER::LED"))
(shadow '*ORANGE* (find-package "RAND_WALKER::LED"))
(defconstant rand_walker::Led::*ORANGE* 2)
(intern "*RED*" (find-package "RAND_WALKER::LED"))
(shadow '*RED* (find-package "RAND_WALKER::LED"))
(defconstant rand_walker::Led::*RED* 3)
(defclass rand_walker::Led
  :super ros::object
  :slots (_value ))

(defmethod rand_walker::Led
  (:init
   (&key
    ((:value __value) 0)
    )
   (send-super :init)
   (setq _value (round __value))
   self)
  (:value
   (&optional __value)
   (if __value (setq _value __value)) _value)
  (:serialization-length
   ()
   (+
    ;; uint8 _value
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _value
       (write-byte _value s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _value
     (setq _value (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get rand_walker::Led :md5sum-) "4391183b0cf05f8f25d04220401b9f43")
(setf (get rand_walker::Led :datatype-) "rand_walker/Led")
(setf (get rand_walker::Led :definition-)
      "uint8 BLACK   = 0
uint8 GREEN   = 1
uint8 ORANGE  = 2
uint8 RED     = 3

uint8 value

")



(provide :rand_walker/Led "4391183b0cf05f8f25d04220401b9f43")


