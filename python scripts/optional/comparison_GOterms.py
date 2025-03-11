import pandas as pd

# Load QuickGO data
quickgo_df = pd.read_csv("output_quickgo.tsv", sep="\t")  # Load the QuickGO data from a TSV file

# Aggregate GO_Term for each UniProt_ID
quickgo_terms = quickgo_df.groupby("UniProt_ID")["GO_Term"].apply(lambda x: ','.join(x)).reset_index()  # Group by UniProt_ID and concatenate GO_Term values
quickgo_terms.columns = ["UniProt_ID", "QuickGO_Terms"]  # Rename columns for clarity

# Load UniProt data
uniprot_df = pd.read_csv("output_uniprot.tsv", sep="\t", usecols=["UniProt_ID", "GO_Terms"], low_memory=False)  # Load UniProt data with only relevant columns
uniprot_df.rename(columns={"GO_Terms": "UniProtGO_Terms"}, inplace=True)  # Rename the GO_Terms column to UniProtGO_Terms

# Merge tables
merged_df = pd.merge(quickgo_terms, uniprot_df, on="UniProt_ID", how="outer")  # Perform an outer join on UniProt_ID to merge QuickGO and UniProt data

# Identify common and unique GO terms
def compare_terms(row):
    quickgo_terms = set(row["QuickGO_Terms"].split(",")) if pd.notna(row["QuickGO_Terms"]) else set()  # Convert QuickGO terms to a set, handling missing values
    uniprot_terms = set(row["UniProtGO_Terms"].split(",")) if pd.notna(row["UniProtGO_Terms"]) else set()  # Convert UniProt terms to a set, handling missing values
    return {
        "common": quickgo_terms & uniprot_terms,  # Find common terms
        "unique_quickgo": quickgo_terms - uniprot_terms,  # Find terms unique to QuickGO
        "unique_uniprot": uniprot_terms - quickgo_terms  # Find terms unique to UniProt
    }

merged_df["Comparison"] = merged_df.apply(compare_terms, axis=1)  # Apply the comparison function to each row

# Save results
merged_df.to_csv("comparison_GOterms.tsv", sep="\t", index=False)  # Save the final comparison to a TSV file
