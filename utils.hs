-- primes.hs

module Utils where

import List (group)

factorize :: Integer -> [Integer]
factorize 1 = [1]
factorize n = myfact [1] n 2 
            where myfact factors n' f = if n' < f 
                                        then factors
                                        else let r = mod n' f
                                             in if r == 0 
                                                then myfact (f:factors) (div n' f) f
                                                else myfact factors n' (f+1)
                  
divisors :: Integer -> [Integer]
divisors n = filter isDiv [1..n]
            where isDiv a = (n `mod` a) == 0

isPrime :: Integer -> Bool
isPrime 1 = True
isPrime n = mydiv n 2
          where mydiv n' k = if k >= ((n' `div` 2) + 1) 
                             then True
                             else if (n' `mod` k) == 0
                                  then False
                                  else mydiv n' (k+1)

primeFactors :: Integer -> [Integer]
primeFactors s = filter (\x -> x > 1) (map head (group (factorize s)))

phi :: Integer -> Integer
phi 1 = 1
phi n = round (product (fromInteger n : map func (primeFactors n)))
        where func n' = 1 - (1 / fromInteger n')

sumDigits :: Integer -> Integer
sumDigits n
 | n < 10 = n 
 | otherwise = n `mod` 10 + sumDigits (n `div` 10)

truncateLeft :: Integer -> Integer
truncateLeft n
 | n >= 10 = n `mod` (10^(floor (logBase 10 (fromInteger n))))

 | otherwise = n

truncateRight :: Integer -> Integer
truncateRight n
 | n >= 10 = n `div` 10
 | otherwise = n

fact :: Integer -> Integer
fact n = product [1..n]

cyphers :: Integer -> [Integer]
cyphers n
 | n < 10 = n:[]
 | otherwise = cyphers (truncateRight n) ++ [nk]
             where nk = n `mod` 10

rot :: Int -> [Integer] -> [Integer]
rot k ns = (drop k ns) ++ (take k ns)

isPalindrome :: Integer -> Bool
isPalindrome n = let cifs = cyphers n
                 in if cifs == reverse cifs
                    then True
                    else False


-- fib 
