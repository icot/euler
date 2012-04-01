#lang racket

(require srfi/1)
(require srfi/69)

(define (neg_unit_pow k)
  (let ((r (modulo k 2)))
    (if (= r 1) -1 1)))

(define cached_values (make-hash-table))

(define (partitions n cache)
  (cond ((<= n 1) 1)
        ((= n 2) 2)
        ((hash-table-exists? cache n) (hash-table-ref cache n))
        (else (let* ((ks (iota (sub1 n) 1 1))
                     (j1 (filter (lambda (x) (<= x n)) 
                                 (map (lambda (k) (/ (- (* 3 k k) k) 2)) ks)))
                     (j2 (filter (lambda (x) (<= x n)) 
                                 (map (lambda (k) (/ (+ (* 3 k k) k) 2)) ks)))
                     (kj1 (zip j1 ks))
                     (kj2 (zip j2 ks))
                     (pkj1 (map (lambda (p) (* (neg_unit_pow (sub1 (last p))) 
                                               (partitions (- n (first p)) cache))) kj1))
                     (pkj2 (map (lambda (p) (* (neg_unit_pow (sub1 (last p))) 
                                               (partitions (- n (first p)) cache))) kj2))
                     (pn (append pkj1 pkj2)))
                (begin 
                  ;(printf " N: ~A kj1: ~A kj2: ~A\n" n kj1 kj2)
                  (hash-table-set! cache n (fold + 0 pn))
                  (hash-table-ref cache n)) ))))

(define (parts n cached_values)
  (let ((pn (partitions n cached_values)))
        (begin
          (printf "n: ~A, p(n): ~A\n" n pn)
          pn)))

; (for-each (lambda (x) (parts x cached_values)) (iota 11))

(define (main n)
  (let* ((pn (partitions n cached_values))
         (mod (remainder pn 1000000)))
    (begin
      (printf "n: ~A mod: ~A p(n): ~A\n" n mod pn)
      (if (= mod 0)
        #t
        (main (add1 n))))))

(main 1)
