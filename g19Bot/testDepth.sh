#!/bin/sh
input="TEST.txt"
rm "TEST.txt"
printf "%s\t\t%s\t\t%s\t\t%s\n" "DEPTH" "PLAYER" "SPEED" "SCORE" >> TEST.txt
printf "%s\n" "---------------------------------Game:--------------------------------- "
for i in {1..25}
do
    printf "\n" >> TEST.txt
    echo "RUNNING PLAYER 1 AT DEPTH $i"
    java -jar ManKalah.jar "python3 -u g19Bot/game.py -d ${i} -m AB" "java -jar MKRefAgent.jar"
    echo "RUNNING PLAYER 2 AT DEPTH $i"
    java -jar ManKalah.jar "java -jar MKRefAgent.jar" "python3 -u g19Bot/game.py -d ${i} -m AB"
done 
printf "%s\n" "-------------------------------Log file:------------------------------- "
cat TEST.txt