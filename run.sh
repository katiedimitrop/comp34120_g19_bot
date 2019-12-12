#!/bin/sh
#TO RUN AS PLAYER 1 (SOUTH) ADD 1 AS ARGUMENT
printf "%s\n" "---------------------------------Game:--------------------------------- "
if [ "$1" != "1" ]; then
    java -jar ManKalah.jar 'java -jar MKRefAgent.jar' 'python3 -u g19Bot/game.py -d 14 -m AB'
else
    java -jar ManKalah.jar 'python3 -u g19Bot/game.py -d 14 -m AB' 'java -jar MKRefAgent.jar'
fi


printf "%s\n" "-------------------------------Log file:------------------------------- "
