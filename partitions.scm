#lang racket

(define (neg_unit_pow k)
  (let ([r (modulo k 2)])
    (if (= r 1) -1 1)))

(define (range a b)
  (for/list ([i (stop-after (in-naturals a) (lambda (x) (>= x b)))]) i))

(define (partitions n cache)
  (cond ((<= n 1) 1)
        ((= n 2) 2)
        (else (let* ([ks (range 1 n)]
                     [j1 (filter (lambda (x) (< x n)) (map (lambda (k) (/ (- (* 3 k k) k) 2)) ks))]
                     [j2 (filter (lambda (x) (< x n)) (map (lambda (k) (/ (+ (* 3 k k) k) 2)) ks))])
                j2))))

(partitions 10 '())
