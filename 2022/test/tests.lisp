(in-package :aoc.test)

(defun array-equal (xs ys)
  "Compare two array element-wise, with 'equal' applied against each elements."
  (if (= (length xs) (length ys))
      (if (= (length xs) 0)
          t
          (reduce (lambda (x y) (and x y))
                  (map 'vector #'equal xs ys)))
      nil))

(test test-split
      (is (array-equal #("aa") (aoc:split "aa")))
      (is (array-equal #("aa") (aoc:split "aa   ")))
      (is (array-equal #() (aoc:split "")))
      (is (array-equal #() (aoc:split " ")))
      (is (array-equal #() (aoc:split "   ")))
      (is (array-equal #("xx") (aoc:split "  xx   ")))
      (is (array-equal #("aaa" "b" "c") (aoc:split "aaa,b,,c" :sep #\,))))

(defun run-tests ()
  (1am:run))
