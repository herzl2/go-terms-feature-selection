# Gene Annotation & Feature Selection with GO Terms

## Workflow

### 1. Extract Uniprot IDs
- **Input:** `oxidative_stress.faa`
- **Script:** `extract_ids.sh`
- **Output:** `uniprot_ids.txt`
- Description: This script extracts Uniprot IDs from the provided protein sequence file  and saves them to a text file.

### 2. Run QuickGO Analysis 
- **Input:** `uniprot_ids.txt`
- **Script:** `quickgo.sh`
- **Output:** `output_quickgo.tsv`
- Description: This script performs a GO term analysis using the extracted Uniprot IDs and generates a tab-separated values file containing the results.

### 3. optional Run Uniprot Analysis
- **Input:** `uniprot_ids.txt`
- **Script:** `uniprot.sh`
- **Output:** `output_uniprot.tsv`
- Description: This optional script conducts an analysis using the Uniprot database and outputs the results to a TSV file.

### 4. optional Run InterProScan Analysis
- **Input:** `interpro_ids.txt`
- **Script:** `interproscan.sh`
- **Output:** `output_interpro.tsv`
- Description: This optional script runs InterProScan analysis on the provided InterPro IDs and generates a TSV file with the results.

### 5. optional Comparison of GO Terms (Common & Unique)
- **Input:** `output_quickgo.tsv`, `output_uniprot.tsv`
- **Script:** `comparison_GOterms.py`
- **Output:** `comparison_GOterms.tsv`
- Description: This script compares the GO terms obtained from QuickGO and Uniprot analyses, identifying common and unique terms, and outputs the comparison results to a TSV file.

### 6. optional Merging Results
- **Input:** `output_quickgo.tsv`, `output_uniprot.tsv`
- **Script:** `merged_uniprot_quickgo.py`
- **Output:** `merged_uniprot_quickgo.tsv`
- Description: This script merges the results from QuickGO and Uniprot analyses into a single file.

- **Input:** `merged_uniprot_quickgo.tsv`, `output_interpro.tsv`
- **Script:** `all_merged.py`
- **Output:** `all_final_merged_output.tsv`
- Description: This script merges the previously merged results with the InterProScan results, producing a comprehensive output file

### 7. Enrichment Analysis
- **Input:** `output_quickgo_cleaned.tsv`, `go.obo`
- **Script:** `go_enrichment.py`
- **Output:** `go_enrichment_results.tsv`
- Description: This script performs GO term enrichment analysis using the cleaned QuickGO results and the GO ontology file, outputting the results to a TSV file.

### 8. Graph Creation 
- **Input:** `output_quickgo_cleaned.tsv`, `go.obo`
- **Script:** `graphs.py`
- **Output:** 
  - `go_graph.graphml`, `go_graph.txt`
  - `gpx_subgraph.graphml`, `gpx_subgraph.txt`
- Description: This script generates graphs representing the relationships between GO terms and outputs them in both GraphML and text formats.

### 9. GO-terms-Proteins relationship
- **Input:** `gpx_subgraph.txt`
- **Script:** `proteins_gpx_go.py`
- **Output:** `proteins_gpx_go.txt`, `proteins_gpx_go.graphml`
- Description: This script analyzes the relationship between proteins and GO terms, producing a text file and a GraphML file representing these relationships.

### 10. UniprotID-Proteinnames
- **Input:** `proteins_gpx_go.txt`
- **Script:** `uniprot-proteins_gpx.py`
- **Output:** `uniprot-proteins_gpx.tsv`
- Description: This script maps Uniprot IDs to their corresponding protein names and outputs the results to a TSV file
