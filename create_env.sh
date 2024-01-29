#!/bin/bash

# Set the directory path
directory="Distance_based_on_Cluster_Analysis/fortran"

# Concatenate the file paths
file_paths=""
for file in "$directory"/*.f90; do
    echo "File paths: $file"
    file_paths="$file_paths $file"
done
echo "File paths: $file_paths"
# Compile all Fortran files
gfortran $file_paths -o "make_nnlist.out"




# Wait for all background processes to finish
wait

echo "All compilations completed."

# Move make_nnlist.out to ~/bin
mv make_nnlist.out ~/.local/bin/make_nnlist.out