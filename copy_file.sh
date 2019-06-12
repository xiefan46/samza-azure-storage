#!/bin/bash
i=0
while (( i++ < 9 )); do
  cp data_file "data_file_$i"
done
