import pandas as pd
from tabulate import tabulate

# Load the TSV file
quickgo_df = pd.read_csv('output_quickgo_cleaned.tsv', sep='\t')  # Read the QuickGO file as a DataFrame

# Strip whitespace from column names
quickgo_df.columns = quickgo_df.columns.str.strip()

# Clean the 'GO_Term' column by stripping whitespace and normalizing
quickgo_df['GO_Term'] = quickgo_df['GO_Term'].str.strip()  # Strip leading and trailing whitespace
quickgo_df['GO_Term'] = quickgo_df['GO_Term'].str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with a single space

# Count the frequency of GO terms
go_counts = quickgo_df['GO_Term'].value_counts().reset_index()  # Count occurrences of each GO term
go_counts.columns = ['GO-Term', 'Count']  # Rename columns to 'GO-Term' and 'Count'

# Output the total number of assignments and unique GO terms
print(f"Number of assignments in the QuickGO file: {len(quickgo_df)}")  # Print total number of lines
print(f"Number of unique GO terms: {len(go_counts)}")  # Print number of unique GO terms

# Load the GO.obo file and extract GO terms, names, and namespaces
go_obo_dict = {}  # Dictionary to store GO terms and names
namespace_dict = {}  # Dictionary to store namespaces
with open('go.obo', 'r') as f:  # Open the GO.obo file
    go_term = None  # Temporary variable for GO term
    go_name = None  # Temporary variable for GO name
    go_namespace = None  # Temporary variable for GO namespace
    for line in f:  # Loop through each line in the file
        line = line.strip()  # Remove whitespace
        if line.startswith('id: GO:'):  # Check for GO term ID
            go_term = line.split(' ')[1]  # Extract GO term ID
        elif line.startswith('name:'):  # Check for GO term name
            go_name = line.split(' ', 1)[1]  # Extract GO term name
        elif line.startswith('namespace:'):  # Check for GO term namespace
            go_namespace = line.split(' ', 1)[1]  # Extract namespace
        if go_term and go_name and go_namespace:  # If all values are found
            go_obo_dict[go_term] = go_name  # Store GO term name
            namespace_dict[go_term] = go_namespace  # Store GO term namespace
            go_term, go_name, go_namespace = None, None, None  # Reset variables

# Add the name and namespace (as category) of the GO term to the counts DataFrame
go_counts['Name'] = go_counts['GO-Term'].map(go_obo_dict)  # Map GO term names to DataFrame
go_counts['Category'] = go_counts['GO-Term'].map(namespace_dict)  # Map GO term namespaces to DataFrame

# Format the DataFrame with tabulate to align columns
table = tabulate(go_counts, headers='keys', tablefmt='tsv', showindex=False)  # Create tab-separated table

# Save to a TSV file with properly aligned headers
with open('go_enrichment_results.tsv', 'w') as f:  # Open output file
    f.write(table + '\n')  # Write table to file

print("The GO enrichment results have been successfully saved in go_enrichment_results.tsv.")  # Confirm success