#lang racket

; requirements
(require srfi/1)

(define cf61 '(7 1 4 3 1 2 2 1 3 4 1 14))
(define body (take (cdr cf61) (sub1 (length (cdr cf61)))))
(define lb (length body))
(define part1 (take body (floor (/ lb 2))))
(define part2 (drop body (/ lb 2)))

; continued fraction generator
(define (cf n)
  ; computes next element of continued fraction
  (define (step r)
    (let* ([a0 (inexact->exact (floor r))] 
           [a1 (- r a0)])
      (if (zero? a1) (cons a0 null) (cons a0 (/ 1 a1)))))
  ; tests completeness of the cf representation
  (define (testcf? repr)
    ; compares two list for equality
    (define (eq-list? xs ys)
      (null? (filter false? (map (lambda (x y) (= x y)) xs ys))))
    (let* ([body (take (cdr repr) (sub1 (length (cdr repr))))]
           [lb (length body)]
           [part1 (take body (floor (/ lb 2)))])
      (if (even? lb) 
          (let ([part2 (drop body (/ lb 2))])
            (eq-list? part1 (reverse part2)))
          (let ([part2 (drop body (add1 (floor (/ lb 2))))])
            (eq-list? part1 (reverse part2))))))
  ; Recursive body
  (define (cfgen n acc)
    (begin 
      (printf "n: ~a acc: ~a\n" n acc)
    (cond
      ; first iteration
      [(false? (pair? n)) (let ([as (step (sqrt n))])
                            (cfgen as (append acc (list (car as)))))]
      [(null? (cdr n)) acc]
      ; general case
      [else (cond
              [(= 1 (length acc)) (let ([as (step (cdr n))])
                                    (cfgen as (append acc (list (car as)))))]
              ; general case
              [else (let ([a0 (first acc)]
                          [an (last acc)])
                      (cond
                        ; check end candidate
                        [(= an (* 2 a0)) (if (testcf? acc)
                                             acc
                                             (let ([as (step (cdr n))])
                                               (cfgen as (append acc (list (car as))))))]
                        ; general case
                        [else (let* ([as (step (cdr n))])
                                (cfgen as (append acc (list (car as)))) )]))]
              )]))
    )                
  (cfgen n '()))

; Computes solution from a continued fraction representation
(define (solution repr)
  (let* ([k (sub1 (length repr))]
         [frepr (if (even? k) 
                    repr
                    (append repr (take (cdr repr) (sub1 (length (cdr repr))))))])
    (reduce-right (lambda (a b) (+ a (/ 1 b))) '() frepr)))


; main body
