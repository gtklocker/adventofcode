import           Data.Array
import           Utils

dim :: Int
dim = 1000

type Point = (Int, Int)
type Board = Array Point Int

initialBoard :: Board
initialBoard =
  array ((0, 0), (dim, dim)) [ ((i, j), 0) | i <- [0 .. dim], j <- [0 .. dim] ]

updateBoard :: Board -> [Point] -> Board
updateBoard board points =
  board // [ ((x, y), board ! (x, y) + 1) | (x, y) <- points ]

data Claim = Claim { id :: Int, left :: Int, top :: Int, width :: Int, height :: Int } deriving (Show);

parseClaim :: String -> Claim
parseClaim s = Claim id'' left' top' width' height'
 where
  [id', rest]           = split '@' $ tail s
  id''                  = parseInt id'
  [margins, dimensions] = split ':' rest
  [left'  , top'      ] = map parseInt $ split ',' $ lstrip margins
  [width' , height'   ] = map parseInt $ split 'x' $ lstrip dimensions

claimContains :: Point -> Claim -> Bool
claimContains (x, y) (Claim _ l t w h) =
  l <= x && x < l + w && t <= y && y < t + h

zone :: Claim -> [Point]
zone (Claim _ l t w h) =
  [ (i, j) | i <- [l .. l + w - 1], j <- [t .. t + h - 1] ]

produceBoard :: [Claim] -> Board
produceBoard = foldl (\acc claim -> updateBoard acc (zone claim)) initialBoard

part1 :: [Claim] -> Int
part1 claims = length $ filter (>= 2) $ elems $ produceBoard claims

part2 :: [Claim] -> [Claim]
part2 claims = filter (all (\pt -> finalBoard ! pt == 1) . zone) claims
  where finalBoard = produceBoard claims

main :: IO ()
main = do
  contents <- readFile "./Day3.txt"
  let claims = map parseClaim $ lines contents
  print $ part2 claims
