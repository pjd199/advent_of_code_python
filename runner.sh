#!/bin/bash
#url=https://5v3kzmattg7zsrul2l3dcb5d3q0odxja.lambda-url.eu-west-2.on.aws

#echo GET $url
#curl $url
#echo

for year in {2015..2022}
do
    for day in {1..25}
    do
        echo === $year $day ===
        python advent_of_code/daily_helper.py $year $day -T
        #echo GET $url/$year/$day
        #time curl $url/$year/$day
        #echo
    done
done