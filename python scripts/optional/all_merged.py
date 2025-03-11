import pandas as pd

# Load the files
merged_df = pd.read_csv('merged_uniprot_quickgo.tsv', sep='\t')  # Load the merged UniProt and QuickGO data
interpro_df = pd.read_csv('output_interpro.tsv', sep='\t')  # Load the InterPro data

# Remove leading and trailing spaces in column names
merged_df.columns = merged_df.columns.str.strip()  # Strip spaces from column names in the merged dataframe
interpro_df.columns = interpro_df.columns.str.strip()  # Strip spaces from column names in the InterPro dataframe

# Rename all columns in 'interpro_df' by appending '_IP'
interpro_df.columns = [f"{col}_IP" for col in interpro_df.columns]  # Add '_IP' suffix to each column name

# Ensure that 'InterPro_IDs_UP' is treated as a list
merged_df['InterPro_IDs_UP'] = merged_df['InterPro_IDs_UP'].str.split(',')  # Split the InterPro IDs into a list

# Split the InterPro IDs into multiple rows
merged_df_split = merged_df.explode('InterPro_IDs_UP')  # Explode the list of InterPro IDs into separate rows

# Merge based on the InterPro IDs
final_df = pd.merge(
    merged_df_split, 
    interpro_df, 
    left_on='InterPro_IDs_UP', 
    right_on='InterPro_ID', 
    how='left'
)  # Perform a left join on the exploded InterPro IDs with the InterPro data

# Remove duplicate rows, if any
final_df = final_df.drop_duplicates()  # Drop any duplicate rows

# Save the result to a new file
final_df.to_csv('all_final_merged_output.tsv', sep='\t', index=False)  # Save the final merged dataframe to a new file

print("Merging complete and file saved.")  # Print a confirmation message
