import pandas as pd
from tabulate import tabulate

# Cleaning quickgo output
# Path to the input and output TSV files
input_file = "output_quickgo.tsv"  # Input file containing GO term data
output_file = "output_quickgo_cleaned.tsv"  # Output file for the cleaned data

# Read the TSV file into a Pandas DataFrame
df = pd.read_csv(input_file, sep="\t")

# Remove duplicate rows to ensure unique entries
df_cleaned = df.drop_duplicates()

# Center the columns using tabulate and prepare it as a string
centered_table = tabulate(df_cleaned, headers='keys', tablefmt='tsv', showindex=False, numalign="center", stralign="center")

# Save the centered table to a new TSV file
with open(output_file, "w") as f:
    f.write(centered_table)

# Count the number of unique UniProt IDs in the cleaned file
unique_uniprot_ids = df_cleaned['UniProt_ID'].nunique()

print(f"Number of unique UniProt IDs in output_quickgo_cleaned.tsv: {unique_uniprot_ids}")
print(f"Cleaned file saved as: {output_file}")

# Load the UniProt IDs from the text file
with open('uniprot_ids.txt', 'r') as f:
    uniprot_ids = set(line.strip() for line in f)

# Load the QuickGO data
quickgo_df = pd.read_csv(output_file, sep='\t')

# Strip whitespace from the column names
quickgo_df.columns = quickgo_df.columns.str.strip()


# Extract the UniProt IDs from the QuickGO file
quickgo_ids = set(quickgo_df['UniProt_ID'].str.strip())  # Strip whitespace from UniProt IDs

# Find the IDs that are in uniprot_ids but not in quickgo_ids
missing_ids = uniprot_ids - quickgo_ids

# Output the missing IDs
print("Missing UniProt IDs:")
if missing_ids:
    for uniprot_id in missing_ids:
        print(uniprot_id)
else:
    print("No missing UniProt IDs.")


# Comparison if Uniprot IDs get lost
# Function to count the number of lines in a file
def count_lines(file_path):
    with open(file_path, 'r') as f:
        line_count = sum(1 for line in f)  # Count lines by iterating through the file
    return line_count  # Return the total line count

# Function to check for duplicates in a file
def check_duplicates(file_path):
    with open(file_path, 'r') as f:
        # Read lines, strip whitespace, and store them in a list
        uniprot_ids = [line.strip() for line in f]

    # Create a dictionary to count occurrences of each UniProt ID
    id_count = {}
    for uniprot_id in uniprot_ids:
        if uniprot_id in id_count:
            id_count[uniprot_id] += 1  # Increment count if ID already exists
        else:
            id_count[uniprot_id] = 1  # Initialize count for new ID

    # Find duplicates: IDs that appear more than once
    duplicates = {uniprot_id: count for uniprot_id, count in id_count.items() if count > 1}

    return duplicates  # Return the dictionary of duplicates

# Main function
def main():
    # Path to the UniProt IDs file
    uniprot_file = 'uniprot_ids.txt'
    
    # Count the number of lines in the file
    num_lines = count_lines(uniprot_file)
    print(f"Number of unique UniProt IDs in {uniprot_file}: {num_lines}")  # Print the line count

    # Check for duplicates in the file
    duplicates = check_duplicates(uniprot_file)

    # Output the results of the duplicate check
    if duplicates:
        print("Duplicate UniProt IDs found:")
        for uniprot_id, count in duplicates.items():
            print(f"{uniprot_id}: {count} times")  # Print each duplicate ID and its count
    else:
        print("No duplicates found in the UniProt IDs file.")  # Message if no duplicates are found

# Entry point of the script
if __name__ == "__main__":
    main()  # Execute the main function 
