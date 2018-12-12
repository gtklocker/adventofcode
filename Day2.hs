import           Data.Map.Strict       (Map)
import qualified Data.Map.Strict       as Map
import           Data.Maybe            (fromMaybe)
import           Foreign.Marshal.Utils (fromBool)

count :: (Ord a) => [a] -> Map a Int
count = foldl updateCount Map.empty
  where
    updateCount map' el = Map.alter (Just . (+ 1) . fromMaybe 0) el map'

hasOccurencies :: (Eq k) => Int -> Map k Int -> Bool
hasOccurencies howMany map' = Map.filter (== howMany) map' /= Map.empty

hash :: String -> (Int, Int)
hash boxID = (fromBool $ hasOccurencies 2 cnt, fromBool $ hasOccurencies 3 cnt)
  where
    cnt = count boxID

part1 :: [String] -> Int
part1 boxIDs =
  let hashes = map hash boxIDs
      (l, r) = foldl (\(a, b) (a', b') -> (a + a', b + b')) (0, 0) hashes
   in l * r

prod :: [a] -> [(a, a)]
prod (x:xs) = zip (repeat x) xs ++ prod xs
prod []     = []

diff :: (Eq a) => Int -> [a] -> [a] -> Maybe Int
diff idx (x:xs) (y:ys) =
  if x /= y
    then if xs == ys
           then Just idx
           else Nothing
    else diff (idx + 1) xs ys
diff _ _ [] = Nothing
diff _ [] _ = Nothing

deleteAt :: Int -> [a] -> [a]
deleteAt idx (x:xs) =
  if idx == 0
    then xs
    else x : deleteAt (idx - 1) xs
deleteAt _ _ = []

commonChars :: String -> String -> Maybe String
commonChars xs ys = (`deleteAt` xs) <$> diff 0 xs ys

firstJust :: [Maybe a] -> Maybe a
firstJust (x:xs) =
  case x of
    Nothing -> firstJust xs
    v       -> v
firstJust [] = Nothing

part2 :: [String] -> Maybe String
part2 boxIDs = firstJust $ uncurry commonChars <$> prod boxIDs

main :: IO ()
main = do
  contents <- readFile "./Day2.txt"
  let boxIDs = lines contents
  print (part1 boxIDs, part2 boxIDs)
