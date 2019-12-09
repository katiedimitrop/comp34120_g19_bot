#!/bin/sh
input="TEST.txt"
rm "TEST.txt"
printf "%s\t\t%s\t\t%s\t\t%s\n" "DEPTH" "PLAYER" "SPEED" "SCORE" >> TEST.txt
printf "%s\n" "---------------------------------Game:--------------------------------- "
depth=25
for ((i = 1; i <= depth; i++))
do
    echo "RUNNING PLAYER 1 AT DEPTH $i"
    java -jar ManKalah.jar "python3 -u g19Bot/game.py -d ${i} -m AB" "java -jar MKRefAgent.jar"
    echo "RUNNING PLAYER 2 AT DEPTH $i"
    java -jar ManKalah.jar "java -jar MKRefAgent.jar" "python3 -u g19Bot/game.py -d ${i} -m AB"
done 
printf "%s\n" "-------------------------------Log file:------------------------------- "
cat TEST.txt
IFS=$'\n' read -d '' -r -a lines < TEST.txt
lineNumber=0
declare -a newList

for x in ${lines[@]} 
do 
    #printf "line ${lineNumber}: %s\n" "${x}"
    let "lineNumber++"
    newList+=($x)
done
let "y=6*depth"
for ((i = 1; i <= depth; i++))
do
    let "x=i*7+(i-1)"
    #echo "DEPTH \t" ${i}
    let "score1=${newList[x]}"
    let "score2=${newList[x+4]}"
    let "score3=(${score1}+${score2}) / 2 "
    echo "DEPTH \t" ${i} "MEAN \t" ${score3}
done