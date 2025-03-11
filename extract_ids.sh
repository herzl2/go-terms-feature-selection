#!/bin/bash

# This cript extracts UniProt IDs from a FASTA file and saves them to an output txt file.
# This script processes a FASTA file containing protein sequences (with headers starting with '>'),
# extracts the UniProt IDs from the header lines, and writes them to a separate file.

# Dependencies: cat, grep awk 

# Define the path to the input FASTA file containing the protein sequences. 
input_file="oxidative_stress.faa"

# Define the output file that will contain the extracted UniProt IDs.
id_file="uniprot_ids.txt"

# Notification that the extraction process is starting.
echo "Extracting UniProt IDs from $input_file..."

# Processing the input FASTA file:
# 'cat $input_file' outputs the entire content of the FASTA file.
# 'grep "^>"' filters and returns only the header lines (which start with '>').
# 'awk -F'|' '{print $2}' splits each header line by the '|' delimiter and prints the second field,
#    which corresponds to the UniProt ID.
# The output is saved in the specified output file 

cat $input_file | grep "^>" | awk -F'|' '{print $2}' > $id_file

# Notification that the ID extraction is complete and saved 
echo "UniProt IDs saved to $id_file"
