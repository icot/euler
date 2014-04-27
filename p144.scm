#lang racket

(require srfi/1)

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

(define (solve-quadratic a b c)
  (let* ([radix (sqrt (- (* b b) (* 4 a c)))]
         [s1 (/ (+ b radix) (* 2 a))]
         [s2 (/ (- b radix) (* 2 a))])
    (list s1 s2)))

(define (cross-points m p)
  (let* ([b (- (cadr p) (* m (car p)))]
         [a2 (+ 100 (* 16 (expt m 2)))]
         [a1 (* 2 16 m b)]
         [a0 (- (expt b 2) 100)]
         [xs (solve-quadratic a2 a1 a0)]
         [ys (map (lambda (x)(+ (* m x) b)) xs)])
    (zip xs ys)))
    
; tests
(test-ellipse? p1)
(define m1 (slope (make-line start p1)))
(cross-points m1 start)