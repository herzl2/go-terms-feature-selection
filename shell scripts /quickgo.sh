#!/bin/bash

# QuickGO Annotation Script

# This script retrieves GO annotations from the QuickGO API using UniProt IDs.
# It reads a list of UniProt IDs from an input file, retrieves JSON annotation data, 
# extracts relevant fields and outputs them in a TSV file.

# Dependencies: curl, jq

# Define input and output file paths 
id_file="uniprot_ids.txt"
output_file="output_quickgo.tsv"

# Header row of the output file 
echo -e "UniProt_ID\tQualifier\tGO_Term\tGO_Aspect\tTax_ID" > "$output_file"

# Notification that the QuickGO annotation fetching process has started 
echo "Fetching annotations from QuickGO..."

# Loop through each UniProt ID in the input file
while read -r id; do
    #Skip processing if the current line is empty
    if [ -z "$id" ]; then   
        continue
    fi

    # Retrieve JSON data from QuickGO using the current UniProt ID
    api=$(curl -s "https://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId=$id")

    # Check if the response is empty or invalid JSON
    # if so output default values and skip further processing
    if [ -z "$api" ] || ! jq -e . >/dev/null 2>&1 <<<"$api"; then
        echo -e "$id\tNone\tNone\tNone\tNone" >> "$output_file"
        continue
    fi

    # Parse and process each annotation in the JSON response 
    echo "$api" | jq -c '.results[]?' | while IFS= read -r annotation; do

        # Extract specific fields from the annotation, using 'None' for missing values 
        qualifier=$(echo "$annotation" | jq -r '.qualifier // "None"')
        go_term=$(echo "$annotation" | jq -r '.goId // "None"')
        go_aspect=$(echo "$annotation" | jq -r '.goAspect // "None"')
        tax_id=$(echo "$annotation" | jq -r '.taxonId // "None"')

        # Append the extracted annotation data to the output TSV file
        echo -e "$id\t$qualifier\t$go_term\t$go_aspect\t$tax_id" >> "$output_file"
    done
done < "$id_file"

# Notification that the QuickGO annotation retrieval is complete 
echo "QuickGO annotations saved to $output_file."


