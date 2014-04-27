-- Partitions.hs

restrictedPArtitions :: Integer -> Integer -> Integer
restrictedPArtitions _ 1 = 1
restrictedPArtitions _ 0 = 1
restrictedPArtitions n k 
 | n >= k = restrictedPArtitions (n-k) (k) + restrictedPArtitions n (pred k)
 | otherwise = 0

partitions :: Integer -> Integer
partitions n = restrictedPArtitions n n
