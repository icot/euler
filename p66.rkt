#lang racket

; requirements
(require srfi/1)

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
    ;(begin 
    ;  (printf "n: ~a acc: ~a\n" n acc)
    (cond
      ; first iteration
      [(false? (pair? n)) (let ([as (step (sqrt n))])
                            (cfgen as (append acc (list (car as)))))]
      [(null? (cdr n)) acc]
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
                [else (let* ([as (step (cdr n))])
                         (cfgen as (append acc (list (car as)))) )]))]
              ))      
  (cfgen n '()))

; Computes solution from a continued fraction representation
(define (solution repr)
  (let* ([tail (cdr repr)]
         [k (length tail)]
         [frepr (if (even? k) 
                    (take repr k)
                    (append repr (take tail (sub1 k))))]
         [frac (reduce-right (lambda (a b) (+ a (/ 1 b))) '() frepr)])
    (if (> (length repr) 1)
        frac
        (car repr))))

(define (test_solution? xy d)
  (let ([x (car xy)]
        [y (cdr xy)])
    (or 
     (= 1 (- (* x x) (* (* y y) d)))
     (= 1 y))))

; main body
(define (body D)
  (define (body-rec d D maxx maxd)
    (let* ([sol (solution (cf d))]
          [x (numerator sol)]
          [y (denominator sol)]
          [xy (cons x y)])
      (begin
        (printf "d:~a, xy = ~a test: ~a\n" d xy (test_solution? xy d)) 
        (cond
          [(> d D) (cons maxd maxx)]
          [(> (car xy) maxx) (body-rec (add1 d) D (car xy) d)]
          [else (body-rec (add1 d) D maxx maxd)]))))
  (body-rec 3 D 0 0))
         
(body 1000)

