import pandas as pd

# Load the two TSV files
uniprot_df = pd.read_csv('output_uniprot.tsv', sep='\t')  # Load the UniProt data from a TSV file
quickgo_df = pd.read_csv('output_quickgo.tsv', sep='\t')  # Load the QuickGO data from a TSV file

# Rename columns to indicate the source (UP/QG)
uniprot_df.columns = [f"{col}_UP" for col in uniprot_df.columns]  # Add '_UP' suffix to the column names in UniProt data
quickgo_df.columns = [f"{col}_QG" for col in quickgo_df.columns]  # Add '_QG' suffix to the column names in QuickGO data

# Merge the two DataFrames based on the 'UniProt_ID_UP' column
merged_df = pd.merge(uniprot_df, quickgo_df, left_on='UniProt_ID_UP', right_on='UniProt_ID_QG', how='inner')  # Perform an inner join on the UniProt IDs

# Save the merged DataFrame to a new TSV file
merged_df.to_csv('merged_uniprot_quickgo.tsv', sep='\t', index=False)  # Save the merged result to a new file

print("The files have been successfully merged and saved.")  # Print a confirmation message
