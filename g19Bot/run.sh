#!/bin/sh
#TO RUN AS PLAYER 1 (SOUTH) ADD 1 AS ARGUMENT
printf "%s\n" "---------------------------------Game:--------------------------------- "
if [ "$1" != "1" ]; then
    java -jar ManKalah.jar 'java -jar MKRefAgent.jar' 'python -u g19Bot/game.py'
else
    java -jar ManKalah.jar 'python -u g19Bot/game.py' 'java -jar MKRefAgent.jar'
fi


printf "%s\n" "-------------------------------Log file:------------------------------- "
cat LOG.txt
