#! /usr/bin/bash
echo "Let's go!"

parent="${1:-.}"    ## parent directory as 1st arg (default .)
count="${2:-1}"     ## initial count as 2nd arg    (default 1)

printf -v dname "%02d" "$count"           ## store 5 digit number in dname

while [ -d "$parent/$dname" ]             ## while dir exists
do
  ((count++))                             ## increment count
  printf -v dname "%02d" "$count"         ## store new 5 digit number in dname
done

printf "creating %s\n" "$parent/$dname"   ## (optional) output dirname
mkdir -p "$parent/$dname"                 ## create dir
cp solver_template.py $dname/solver.py
touch $dname/puzzle_input.txt
