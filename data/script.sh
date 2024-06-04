#!/bin/bash

#Combine all the files
cat ./economic_events_* >> temp.csv

# Remove the header lines from the files
grep -v '^time' temp.csv >> economic_events.csv

rm temp.csv
