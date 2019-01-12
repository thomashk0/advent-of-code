{-# LANGUAGE QuasiQuotes #-}
module Main where

import System.Environment
import Data.SBV
import Text.Scanf

type SInt = SInteger
data Vec3 a = Vec3 a a a deriving (Eq, Ord, Show)
data NanoBot = NanoBot (Vec3 Int) Int deriving (Eq, Ord, Show)
type SVec3 = Vec3 SInt

parse :: String -> Maybe NanoBot
parse l = makeBot <$> scanf [fmt| pos=<%d,%d,%d>, r=%d |] l
    where
        makeBot (x :+ y :+ z :+ r :+ ()) = NanoBot (Vec3 x y z) r

makeSymbolic :: Integral a => Vec3 a -> Vec3 SInt
makeSymbolic (Vec3 x y z) = Vec3 (fromIntegral x) (fromIntegral y) (fromIntegral z)

manhattanDistance :: Num a => Vec3 a -> Vec3 a -> a
manhattanDistance (Vec3 x y z) (Vec3 x' y' z') =
    abs (x - x') + abs (y - y') + abs (z - z')

inRangeOf :: NanoBot -> SVec3 -> SBool
inRangeOf (NanoBot center@(Vec3 cx cy cz) radius) p@(Vec3 px py pz) =
    manhattanDistance p (makeSymbolic center) .<= fromIntegral radius

isEmpty :: [SBool] -> IO Bool
isEmpty constraints = not <$> isSatisfiable (bAnd constraints)

problem :: [NanoBot] -> Symbolic ()
problem bots = do
    [x, y, z] <- sIntegers ["px", "py", "pz"]
    let p = Vec3 x y z
        total = (sum $ map (oneIf . (`inRangeOf` p)) bots) :: SInteger
    maximize "n" total
    minimize "dist" (manhattanDistance p (Vec3 0 0 0))
    where
        forceInRange p pmin pmax =
            constrain $ (p .>= pmin) &&& (p .<= pmax)

main :: IO ()
main = do
    args <- getArgs
    content <- lines <$> readFile (head args)
    let (Just bots) = mapM parse content
        n = length bots
    putStrLn $ "found " ++ show n ++ " bots"
    res <- optimize Lexicographic (problem bots)
    print res
