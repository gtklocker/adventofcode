{-# LANGUAGE OverloadedStrings #-}

import           Prelude                 hiding ( readFile )
import           Data.List                      ( null )
import           Data.Text.IO                   ( readFile )
import           Data.Text                      ( splitOn
                                                , unpack
                                                )

parseInt :: String -> Int
parseInt = read

parseSignedInt :: String -> Int
parseSignedInt (s : ss) = case s of
  '+' -> parseInt ss
  '-' -> -parseInt ss

main :: IO ()
main = readFile "./Day1.txt" >>= \contents ->
  print $ sum $ map parseSignedInt $ filter (not . null) $ map unpack $ splitOn
    "\n"
    contents
