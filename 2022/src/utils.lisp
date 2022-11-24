(in-package :aoc)

(defun lines-from-stream (f)
  "Read lines of a given steam into a vector"
  (defun inner (acc)
    (let ((line (read-line f nil)))
      (if line
          (progn
            (vector-push line acc)
            (inner acc))
          acc)))
  (inner (make-array 1000 :fill-pointer 0 :adjustable t)))

(defun lines (src)
  "Open give the file and returns all lines (as a vector)"
  (lines-from-stream (open src)))

(defun ints (xs)
  "Parse a list of string into a list of integers."
  (map 'vector #'parse-integer xs))

(defun read-file (path)
  "Read an entire file into a string."
  (uiop:read-file-string path))

;; TODO: add support?
;; (defun repeat (x count)
;;   (labels ((inner (cur n)
;;              (if (= n 0)
;;                  cur
;;                  (inner (cons x cur) (- n 1)))
;;              ))
;;     (inner '() count)))

;; TODO: add support?
;; (defun replace-elt (x x-new xs)
;;   (mapcar (lambda (y) (if (= y x) x-new y)) xs))

(defun split (seq &key (sep #\Space))
  (defun inner (parts start cur)
    (if (>= cur (length seq))
        (progn
          (unless (= start cur)
            (vector-push (subseq seq start cur) parts)))
        (if (equal (aref seq cur) sep)
            (progn
              (unless (= start cur)
                (vector-push (subseq seq start cur) parts))
              (inner parts (+ cur 1) (+ cur 1)))
            (inner parts start (+ cur 1)))))
  (let* ((size-estimation (+ (count sep seq) 1))
         (dst (make-array size-estimation :fill-pointer 0 :adjustable t)))
    (inner dst 0 0)
    dst))

(defun split-ints (s &key (sep #\Space))
  "Split a string and parse integers on each part."
  (ints (split s :sep sep)))
