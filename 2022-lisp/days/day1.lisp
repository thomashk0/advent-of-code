(defpackage :aoc_2022_day1 (:use :cl))
(in-package :aoc_2022_day1)

(defparameter *example* "../assets/day1_input_ex")
(defparameter *example-input* (coerce (aoc:lines *example*) 'list))

(defun string-empty-p (s) (string-equal "" s))

(defun group (input)
    (labels ((inner (result acc xs)
               (if (null xs)
                   result
                   (if (string-empty-p (car xs))
                       (push acc result)
                       (inner (cons (car xs) acc) (cdr xs))))))
      (inner '() '() input)
      ))
