(asdf:defsystem :aoc
  :description "Advent of code in Common Lisp."
  :author "Thomas Hiscock"
  :homepage "https://github.com/thomashk0/advent-of-code"

  :license "MIT"
  :version "1.0.0"

  ;; :depends-on (:split-sequence)

  ;; :in-order-to ((asdf:test-op (asdf:test-op :bobbin/test)))

  :serial t
  :components ((:file "package")
               (:module "src" :serial t
                :components (
                    (:file "utils")))
               (:module "days" :serial t
                :components (
                    (:file "2021_day6")))))


(asdf:defsystem :aoc/test
  :description "Advent of code in Common Lisp (tests)."
  :author "Thomas Hiscock"
  :homepage "https://github.com/thomashk0/advent-of-code"

  :depends-on (:1am :aoc)
  :serial t
  :components ((:file "package.test")
               (:module "test"
                :serial t
                :components ((:file "tests"))))

  :perform (asdf:test-op (op system)
             (funcall (read-from-string "aoc.test:run-tests"))))
