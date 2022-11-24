(defpackage :aoc_2021_06 (:use :cl))
(in-package :aoc_2021_06)

(defparameter *test-input*
  (aoc:split-ints "3,4,3,1,2" :sep #\,))

(defparameter *input*
  (aoc:split-ints (aoc:read-file "../assets/2021_day6_input") :sep #\,))

;; TODO: include in utils?
(defun compose-n (func n input)
  ;; (format t "fishes: ~a~%" fishes)
  (if (= n 0)
      input
      (compose-n func (- n 1) (funcall func input))))

;; TODO: include in utils?
(defun sum (xs) (reduce #'+ xs))

;; TODO: include in utils?
(defun updatef (array field func)
  (setf (aref array field) (funcall func (aref array field))))

(defun init-ages (fishes)
  (let ((ages (make-array 9)))
    (loop for x across fishes do
      (updatef ages x #'1+))
    ages))

(defun update-ages (fishes)
  (let ((spawned (aref fishes 0))
         (n (- (length fishes) 1)))
     (loop for i from 1 to n do
       ;; FIXME: this is a shift
       (setf (aref fishes (- i 1)) (aref fishes i)))
     (setf (aref fishes 8) spawned)
     (updatef fishes 6 (lambda (x) (+ x spawned)))
     fishes))

(defun solve (input rep)
  (sum (compose-n #'update-ages rep (init-ages input))))

(assert (= 5934 (solve *test-input* 80)))
(assert (= 26984457539 (solve *test-input* 256)))

;; FIXME: this should not be done at compile-time!
(format t "part-1: ~a~%" (solve *input* 80))
(format t "part-2: ~a~%" (solve *input* 256))
