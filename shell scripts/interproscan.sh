#!/bin/bash

# InterProScan Annotation Script

# This script retrieves GO annotations from the InterPro API, using InterPro IDs.
# It reads a list of InterPro IDs from an input file, retrieves JSON annotation data, 
# extracts relevant fields and outputs them in a TSV file.

# Dependencies: curl, jq

# Define input and output file paths
input_file="interpro_ids.txt"
output_file="output_interpro.tsv"

# Header row of the output file 
echo -e "InterPro_ID\tName\tType\tGO_Term\tGO_Aspect\tGO_Categories" > "$output_file"

# Notification that the InterPro annotation fetching process has started 
echo -e "Fetching annotations from InterPro..."

# Loop through each InterPro ID in the input file
while read -r interpro_id; do
    #Skip processing if the current line is empty
    if [ -z "$interpro_id" ]; then  
        continue
    fi
    # Retrieve JSON data from InterPro using the current InterPro ID
    api=$(curl -s "https://www.ebi.ac.uk/interpro/api/entry/InterPro/$interpro_id")

    # Check if the response is empty or invalid JSON
    # if so output default values and skip further processing
    if [ -z "$api" ] || ! jq -e . >/dev/null 2>&1 <<<"$api"; then
        echo -e "$interpro_id\tNone\tNone\tNone\tNone\tNone" >> "$output_file"
        continue
    fi

    # Extract specific fields from the annotation, using 'None' for missing values 
    name=$(echo "$api" | jq -r '.metadata.name.short // "None"')
    type=$(echo "$api" | jq -r '.metadata.type // "None"')
    go_terms=$(echo "$api" | jq -r '.metadata.go_terms[]? | .identifier' | paste -sd "," -)
    go_names=$(echo "$api" | jq -r '.metadata.go_terms[]? | .name' | paste -sd "," -)
    go_categories=$(echo "$api" | jq -r '.metadata.go_terms[]? | .category.name' | paste -sd "," -)

    # Append the extracted annotation data to the output TSV file
    echo -e "$interpro_id\t$name\t$type\t$go_terms\t$go_names\t$go_categories" >> "$output_file"
done < "$input_file"

# Notification that the InterPro annotation retrieval is complete 
echo "InterPro annotations saved to $output_file." 

