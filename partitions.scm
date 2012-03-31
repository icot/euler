
(require-extension srfi-1)

(define (neg_unit_pow k)
  (let ((r (modulo k 2)))
    (if (= r 1) -1 1)))

(define (partitions n cache)
  (cond ((<= n 1) 1)
        ((= n 2) 2)
        (else (let* ([ks (iota (sub1 n) 1 1)]
                     [j1 (filter (lambda (x) (< x n)) (map (lambda (k) (/ (- (* 3 k k) k) 2)) ks))]
                     [j2 (filter (lambda (x) (< x n)) (map (lambda (k) (/ (+ (* 3 k k) k) 2)) ks))]
                     [kj1 (zip j1 ks)]
                     [kj2 (zip j2 ks)])
                (cons kj1 kj2) ))))

(printf "Result: ~A" (partitions 10 '()))
