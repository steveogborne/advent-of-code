#! /usr/bin/bash
echo "Let's go!"

# Define new directory name
directory = "09"
mkdir $directory
cp solver_template.py $directory/solver.py
touch $directory/puzzle_input.txt
