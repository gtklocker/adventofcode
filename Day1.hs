import           Data.Set (Set)
import qualified Data.Set as Set

parseSignedInt :: String -> Int
parseSignedInt (s:ss) =
  case s of
    '+' -> read ss
    '-' -> -read ss

part1 :: [Int] -> Int
part1 = sum

firstDupState :: Int -> Set Int -> [Int] -> Maybe Int
firstDupState cur seen (x:xs) =
  if cur `Set.member` seen
    then Just cur
    else firstDupState new (Set.insert cur seen) xs
  where
    new = cur + x
firstDupState _ _ [] = Nothing

part2 :: [Int] -> Maybe Int
part2 freqs = firstDupState 0 Set.empty (cycle freqs)

main :: IO ()
main = do
  contents <- readFile "./Day1.txt"
  let frequencies = map parseSignedInt $ lines contents
  print (part1 frequencies, part2 frequencies)
