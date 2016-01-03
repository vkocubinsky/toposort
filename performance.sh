#!/bin/bash

if [ ! -f divisors.data ]; then
	echo "File divisors.data doesn't exists"
        echo "You can produce data with:"
	echo "./divisors_data.py 50000 > divisors.data" 
	exit 1;
fi

echo Run python toposort.py
time ./toposort.py divisors.data > toposort.sorted.data 
echo Run standard tsort
time tsort divisors.data > tsort.sorted.data 
