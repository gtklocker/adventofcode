import           Data.List (group, sort)
import           Data.Set  ()
import qualified Data.Set  as Set
import           Utils

dim :: Int
dim = 1000

type Point = (Int, Int)

data Claim = Claim
  { id     :: Int
  , left   :: Int
  , top    :: Int
  , width  :: Int
  , height :: Int
  } deriving (Show)

parseClaim :: String -> Claim
parseClaim s = Claim id'' left' top' width' height'
  where
    [id', rest] = split '@' $ tail s
    id'' = parseInt id'
    [margins, dimensions] = split ':' rest
    [left', top'] = map parseInt $ split ',' $ lstrip margins
    [width', height'] = map parseInt $ split 'x' $ lstrip dimensions

pointsWithinClaim :: Claim -> [Point]
pointsWithinClaim (Claim _ l t w h) =
  [(i, j) | i <- [l .. l + w - 1], j <- [t .. t + h - 1]]

groupPoints :: [Claim] -> [[Point]]
groupPoints claims = group $ sort $ concatMap pointsWithinClaim claims

part1 :: [Claim] -> Int
part1 claims = length $ filter (>= 2) $ map length $ groupPoints claims

part2 :: [Claim] -> [Claim]
part2 claims =
  filter (all (\pt -> [pt] `Set.member` groups) . pointsWithinClaim) claims
  where
    groups = Set.fromList $ groupPoints claims

main :: IO ()
main = do
  contents <- readFile "./Day3.txt"
  let claims = map parseClaim $ lines contents
  print (part1 claims, part2 claims)
