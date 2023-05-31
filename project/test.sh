#!/bin/bash

echo "Testing pipeline..."

python3.11 ./data/pipeline.py

if [ $? -eq 0 ]; then
	echo "Successs: Pipeline works"
else
	echo "Error: Pipeline fails"
	exit 1
fi

echo "Testing DB..."

if [ -f "./data/data.sqlite" ]; then
	echo "Success: DB exists"
else
	echo "Error: DB does not exist"
	exit 1
fi

exit 0