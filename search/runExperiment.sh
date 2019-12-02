#!/bin/bash

depthFirstOUTPUTFILE="experiment/depthFirstResults.txt"
breadthFirstOUTPUTFILE="experiment/breadthFirstResults.txt"
bestFirstOUTPUTFILE="experiment/bestFirstResults.txt"
aStarOUTPUTFILE="experiment/aStarResults.txt"

for i in {1..30};
do
  echo "Jogada #$i"
  python pacman.py -l mediumMaze -p SearchAgent -a fn=depthFirstSearch > experiment/stdout.txt
  cat "$depthFirstOUTPUTFILE" experiment/stdout.txt >> "$depthFirstOUTPUTFILE"
  rm -f experiment/stdout.txt
done

for i in {1..30};
do
  echo "Jogada #$i"
  python pacman.py -l mediumMaze -p SearchAgent -a fn=breadthFirstSearch > experiment/stdout.txt
  cat "$breadthFirstOUTPUTFILE" experiment/stdout.txt >> "$breadthFirstOUTPUTFILE"
  rm -f experiment/stdout.txt
done

for i in {1..30};
do
  echo "Jogada #$i"
  python pacman.py -l mediumMaze -p SearchAgent -a fn=bestFirstSearch > experiment/stdout.txt
  cat "$bestFirstOUTPUTFILE" experiment/stdout.txt >> "$bestFirstOUTPUTFILE"
  rm -f experiment/stdout.txt
done

for i in {1..30};
do
  echo "Jogada #$i"
  python pacman.py -l mediumMaze -p SearchAgent -a fn=aStarSearch > experiment/stdout.txt
  cat "$aStarOUTPUTFILE" experiment/stdout.txt >> "$aStarOUTPUTFILE"
  rm -f experiment/stdout.txt
done
