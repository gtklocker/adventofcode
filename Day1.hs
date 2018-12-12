parseInt :: String -> Int
parseInt = read

parseSignedInt :: String -> Int
parseSignedInt (s : ss) = case s of
  '+' -> parseInt ss
  '-' -> -parseInt ss

main :: IO ()
main = do
  contents <- readFile "./Day1.txt"
  let numbers = map parseSignedInt $ lines contents
  print $ sum numbers
