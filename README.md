# go-terms-feature-selection

# Gene Annotation & Feature Selection with GO Terms

## Workflow

### 1. Extract Uniprot IDs
- **Input:** `oxidative_stress.faa`
- **Script:** `1extract_ids.sh`
- **Output:** `uniprot_ids.txt`

### 2. Run QuickGO Analysis 
- **Input:** `uniprot_ids.txt`
- **Script:** `quickgo.sh`
- **Output:** `output_quickgo.tsv`

### 3. Run Uniprot Analysis
- **Input:** `uniprot_ids.txt`
- **Script:** `uniprot.sh`
- **Output:** `output_uniprot.tsv`

### 4. Run InterProScan Analysis
- **Input:** `interpro_ids.txt`
- **Script:** `interproscan.sh`
- **Output:** `output_interpro.tsv`

### optional 5. Comparison of GO Terms (Common & Unique)
- **Input:** `output_quickgo.tsv`, `output_uniprot.tsv`
- **Script:** `comparison_GOterms.py`
- **Output:** `comparison_GOterms.tsv`

### optional 6. Merging Results
- **Input:** `output_quickgo.tsv`, `output_uniprot.tsv`
- **Script:** `merged_uniprot_quickgo.py`
- **Output:** `merged_uniprot_quickgo.tsv`

- **Input:** `merged_uniprot_quickgo.tsv`, `output_interpro.tsv`
- **Script:** `all_merged.py`
- **Output:** `all_final_merged_output.tsv`

### 7. Subgraph Creation (Biological Process & Molecular Function)
- **Input:** `output_quickgo.tsv`, `go-basic.obo`
- **Script:** `subgraph_biological_process.py`, `subgraph_molecular_function.py`
- **Output:** 
  - `subgraph_biological_process.graphml`
  - `subgraph_molecular_function.graphml`

### 8. GPX Filter (for Biological Process & Molecular Function)
- **Output:**
  - `gpx_subgraph_biological_process.graphml`
  - `gpx_subgraph_molecular_function.graphml`
