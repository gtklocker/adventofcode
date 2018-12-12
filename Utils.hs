module Utils where

parseInt :: String -> Int
parseInt = read

lstrip :: String -> String
lstrip = dropWhile (== ' ')

split :: Char -> String -> [String]
split _ [] = []
split needle hay =
  takeWhile (/= needle) hay : split needle (tail' $ dropWhile (/= needle) hay)
  where
    tail' (_:xs) = xs
    tail' []     = []
