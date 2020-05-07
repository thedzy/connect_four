#!/usr/bin/env bash

# Change to the directory with the script
cd $(dirname $0)

# Initialise variables
RED=0
BLUE=0

# Run time in minutes
RUNTIME=0.5

# Pause between each run to verify the results
PAUSE=1

LOOPS=$(echo "scale=3; ($RUNTIME * 60) / $PAUSE" | bc -l)
printf "Loops: $LOOPS \n"

# Run tests
for X in $(seq 0 ${LOOPS%.*}); do
  python3 connect_four.py --self
  SCORE=$?

  [ $SCORE = 1 ] && ((RED++))
  [ $SCORE = 2 ] && ((BLUE++))

  printf "%d of %d runs \n " $X ${LOOPS%.*}
  sleep $PAUSE
done

# Print results
printf "Red: %d vs Blue: %d \n" $RED $BLUE

exit