#lang racket

(define (range a b)
  (for/list ([i (stop-after (in-naturals a) (lambda (x) (>= x b)))]) i))

(define (th1 n)
  (round (/ (* n 4284) 10000)))

(define (th2 n)
  (add1 (round (/ (* 43 n) 100))))

(define (coprimes n)
  (let* ([ns (range (th1 n) (th2 n))])
    (filter (lambda (x) (= (gcd x n) 1)) ns)))

(define (rpf d)
  (map (lambda (x) (/ x d)) (coprimes d)))

(define limit 1000000)

(define (rpf-iter best d)
  (let* ([rpfs (rpf d)]
         [rpfs-f (filter (lambda (x) (< x (/ 3 7))) rpfs)]
         [tmpbest (if (not (null? rpfs-f)) (last rpfs-f) 0)])
    (cond ((and (not (null? tmpbest)) (> d limit)) (if (> tmpbest best)
                                                         tmpbest
                                                         best))
          ((and (not (null? tmpbest)) (<= d limit)) (if (> tmpbest best)
                                                          (rpf-iter tmpbest (add1 d))
                                                          (rpf-iter best (add1 d))))
          (else (rpf-iter best (add1 d))))))

(display "Computing Rpfs")
(newline)
(time (rpf-iter 0 1))
