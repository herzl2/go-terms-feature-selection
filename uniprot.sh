#!/bin/bash

# UniProt Annotation Script

# This script retrieves GO annotations by querying the UniProt REST API, using UniProt IDs.
# It extracts InterPro IDs, protein names, GO terms, organism information, and pathway details, 
# then writes the parsed data to an output TSV file.

# Dependencies: curl, grep (with Perl-compatible regex support using -oP), sed, tr
# Ensure that your version of grep supports the -oP option for Perl-compatible regular expressions (PCRE)

# Define input and output file paths 
id_file="uniprot_ids.txt"
output_file="output_uniprot.tsv"

# Header row of the output file 
echo -e "UniProt_ID\tInterPro_IDs\tName\tShort_Names\tGO_Term\tGO_Aspect\tOrganism\tPathways" > "$output_file"

# Notification that the UniProt annotation fetching process has started 
echo "Fetching annotations from UniProt..."

# Iterate over each UniProt ID in the input file
while read -r id; do
    # Skip empty lines in the input file
    if [ -z "$id" ]; then  
        continue
    fi

    # Retrieve the text-format UniProt record for the current ID
    api=$(curl -s "https://rest.uniprot.org/uniprotkb/$id.txt")

    # Extract InterPro IDs using regex; join multiple IDs with commas
    interpro_ids=$(echo "$api" | grep -oP 'IPR\d+' | tr '\n' ',' | sed 's/,$//')
    [ -z "$interpro_ids" ] && interpro_ids="None"

    # Extract the full protein name
    name=$(echo "$api" | grep -m 1 -oP '^DE\s+RecName: Full=\K.*' | sed 's/\s*{.*}//')
    [ -z "$name" ] && name="None"

    # Extract short names; join multiple names with commas
    short_names=$(echo "$api" | grep -oP '^DE\s+.*Short=\K[^;]+' | tr '\n' ',' | sed 's/,$//')
    [ -z "$short_names" ] && short_names="None"

    # Extract GO terms; join multiple terms with commas
    go_terms=$(echo "$api" | grep -oP '^DR\s+GO;\s+\KGO:\d+' | tr '\n' ',' | sed 's/,$//')
    [ -z "$go_terms" ] && go_terms="None"

    # Extract GO aspects (cellular component, biological process, molecular function)
    # and convert single-letter codes to descriptive text; join multiple aspects with commas
    go_aspect=$(echo "$api" | grep -oP '^DR\s+GO;\s+\KGO:\d+; \K(C|P|F):[^;]+' | sed -E 's/^C:/cellular component:/; s/^P:/biological process:/; s/^F:/molecular function:/' | tr '\n' ',' | sed 's/,$//')
    [ -z "$go_aspect" ] && go_aspect="None"

    # Extract organism name
    organism=$(echo "$api" | grep -m 1 -oP '^OS\s+\K.*')
    [ -z "$organism" ] && organism="None"

    # Extract pathway information (Reactome pathway)
    pathways=$(echo "$api" | grep '^DR.*Reactome;' | cut -d';' -f2- | tr -d ' ' | tr '\n' ',' | sed 's/,$//')
    [ -z "$pathways" ] && pathways="None"

    # Append the collected annotation information to the output file in TSV format
    echo -e "$id\t$interpro_ids\t$name\t$short_names\t$go_terms\t$go_aspect\t$organism\t$pathways" >> "$output_file"
done < "$id_file"

# Notification that the UniProt annotation retrieval is complete 
echo "UniProt annotations saved to $output_file."

