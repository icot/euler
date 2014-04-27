#lang racket
; starting constants
(define start (list 0 10.1))
(define p1 (list 1.4 -9.6))

; basic procedures
(define (to-degrees angle)
  (* (/ 180 pi) angle))

(define (make-line p1 p2)
  (list p1 p2))

(define (test-ellipse? p)
  (let ([x (car p)]
        [y (cadr p)])
    (= 100 (+ (* 4 (expt x 2)) (expt y 2)))))
  
(define (slope line)
  (let ([x1 (caar line)]
        [y1 (cadar line)]
        [x2 (caadr line)]
        [y2 (cadadr line)])
    (/ (- y2 y1) (- x2 x1))))

(define (tangent-slope p)
  (let ([x (car p)]
        [y (cadr p)])
    (/ (* -4 x) y)))

(define (normal-slope p)
  (let ([mt (tangent-slope p)])
    (/ -1 mt)))

; tests
(test-ellipse? p1)
(to-degrees (atan (tangent-slope p1)))
(to-degrees (atan (normal-slope p1)))