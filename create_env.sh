#!/bin/bash

# Set the directory path
directory="Distance_based_on_Cluster_Analysis/fortran"

# Compile all Fortran files in the directory
for file in $directory/*.f90; do
    if [[ -f $file ]]; then
        echo "Compiling $file..."
        gfortran -o "make_nnlist.out" "$file"  # Change the output file name
        echo "Compilation completed."
    fi
done

# Move make_nnlist.out to ~/bin
mv make_nnlist.out ~/bin/