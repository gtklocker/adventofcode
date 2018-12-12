import           Data.Map.Strict                ( Map )
import qualified Data.Map.Strict               as Map
import           Data.Maybe                     ( fromMaybe )
import           Foreign.Marshal.Utils          ( fromBool )

count :: (Ord a) => [a] -> Map a Int
count = foldl updateCount Map.empty
  where updateCount map' el = Map.alter (Just . (+ 1) . fromMaybe 0) el map'

hasOccurencies :: (Eq k) => Int -> Map k Int -> Bool
hasOccurencies howMany map' = Map.filter (== howMany) map' /= Map.empty

hash :: String -> (Int, Int)
hash boxID = (fromBool $ hasOccurencies 2 cnt, fromBool $ hasOccurencies 3 cnt)
  where cnt = count boxID

main :: IO ()
main = do
  contents <- readFile "./Day2.txt"
  let boxIDs = lines contents
  let hashes = map hash boxIDs
  let (l, r) = foldl (\(a, b) (a', b') -> (a + a', b + b')) (0, 0) hashes
  print $ l * r
