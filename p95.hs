-- euler project p95

import Utils

properDivisors :: Integer -> [Integer]
properDivisors n =  tail (reverse (divisors n))

sumd :: Integer -> Integer
sumd = sum . properDivisors 

isPerfect :: Integer -> Bool
isPerfect n = n == sumd n

amicableChain :: [Integer] -> Integer -> [Integer]
amicableChain acc n
 | n >= 1000000 = acc
 | otherwise = if null acc == False && n == last acc
               then acc
               else let sn = sumd n
                    in if (sn > 1)
                       then amicableChain (n:acc) sn
                       else []

amiChain = amicableChain []

-- body:: [[Integer]] -> Integer -> [[Integer]]
body :: Integer -> Integer -> Integer
body n limit
 | sumd n >= limit = n
 | otherwise = body (succ n) limit

-- main = (body [[]] 100)

