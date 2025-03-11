import requests
import pandas as pd
from tabulate import tabulate  # Import tabulate

def fetch_protein_info(uniprot_ids):
    """Fetches protein information from the UniProt database using given UniProt IDs."""
    results = []  # List to store protein information

    # Iterate over the list of UniProt IDs
    for uniprot_id in uniprot_ids:
        # API URL to fetch protein details in text format
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
        
        try:
            response = requests.get(url)  # Send request to UniProt API
            response.raise_for_status()  # Check if the request was successful
            
            # Process the response text
            protein_info = {'UniProt ID': uniprot_id}  # Store UniProt ID
            lines = response.text.splitlines()  # Split response into lines
            for line in lines:
                if line.startswith("ID"):
                    protein_info['Protein Name'] = line.split()[1]  # Extract protein name
                elif line.startswith("DE"):
                    # Extract protein description
                    description = line[5:].strip()
                    if 'Description' in protein_info:
                        protein_info['Description'] += " " + description
                    else:
                        protein_info['Description'] = description
                elif line.startswith("OS"):
                    protein_info['Organism'] = line[5:].strip()  # Extract organism name
                elif line.startswith("OX"):
                    protein_info['Taxonomy ID'] = line.split()[1]  # Extract taxonomy ID
                elif line.startswith("GN"):
                    gene_name = line[5:].strip()
                    protein_info['Gene Name'] = gene_name  # Extract gene name
            
            # Add default values for missing information
            if 'Description' not in protein_info:
                protein_info['Description'] = "N/A"
            if 'Organism' not in protein_info:
                protein_info['Organism'] = "N/A"
            if 'Taxonomy ID' not in protein_info:
                protein_info['Taxonomy ID'] = "N/A"
            if 'Gene Name' not in protein_info:
                protein_info['Gene Name'] = "N/A"

            results.append(protein_info)  # Add extracted data to results list
        
        except requests.exceptions.HTTPError as err:
            print(f"Error fetching data for {uniprot_id}: {err}")  # Print HTTP error
        except Exception as e:
            print(f"An error occurred: {e}")  # Print general error

    return results  # Return the list of extracted protein data

def read_uniprot_ids_from_file(file_path):
    """Reads UniProt IDs from a given file."""
    df = pd.read_csv(file_path, sep=r"\s+", header=0)  # Use regex to split by whitespace
    return df['Protein'].tolist()  # Return a list of UniProt IDs from the 'Protein' column

# Path to the file containing UniProt IDs
input_file = "proteins_gpx_go.txt"

# Read UniProt IDs from the input file
uniprot_ids = read_uniprot_ids_from_file(input_file)

# Fetch protein information from UniProt
protein_data = fetch_protein_info(uniprot_ids)

# Convert the results into a DataFrame
df = pd.DataFrame(protein_data)

# Remove duplicates
df = df.drop_duplicates()

# Save the DataFrame as a TSV file
df.to_csv("uniprot-proteins_gpx.tsv", sep="\t", index=False)  # Save as TSV

# Use tabulate to create a formatted string and write it to a file
with open("uniprot-proteins_gpx.tsv", "w") as f:
    f.write(tabulate(df, headers='keys', tablefmt='tsv', showindex=False))

print("Protein information has been saved to uniprot-proteins_gpx.tsv")
