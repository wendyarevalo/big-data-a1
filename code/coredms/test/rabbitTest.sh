#!/bin/bash

for i in {1..100}
do
  docker run --rm --network bigdata-network producer &
done

wait
