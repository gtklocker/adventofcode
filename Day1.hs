parseSignedInt :: String -> Int
parseSignedInt (s : ss) = case s of
  '+' -> read ss
  '-' -> -read ss

main :: IO ()
main = do
  contents <- readFile "./Day1.txt"
  print $ sum $ map parseSignedInt $ lines contents
