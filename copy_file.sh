#!/bin/bash
i=0
while (( i++ < 9 )); do
  cp -r  $1 "$1_$i"
done
