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

### 3. optional Run Uniprot Analysis
- **Input:** `uniprot_ids.txt`
- **Script:** `uniprot.sh`
- **Output:** `output_uniprot.tsv`

### 4. optional Run InterProScan Analysis
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

### 7. Enrichment Analysis
- **Input:** `output_quickgo_cleaned.tsv`, `go.obo`
- **Script:** `go_enrichment.py`
- **Output:** `go_enrichment_results.csv`

### 8. Graph Creation 
- **Input:** `output_quickgo_cleaned.tsv`, `go.obo`
- **Script:** `graphs.py`
- **Output:** 
  - `go_graph.graphml`, `go_graph.txt`
  - `gpx_subgraph.graphml`, `gpx_subgraph.txt`

### 9. GO-terms-Proteins relationship
- **Input:** `gpx_subgraph.txt`
- **Script:** `proteins_gpx_go.py`
- **Output:** `proteins_gpx_go.txt`, `proteins_gpx_go.graphml`

### 10. UniprotID-Proteinnames
- **Input:** `proteins_gpx_go.txt`
- **Script:** `uniprot-proteins_gpx.py`
- **Output:** `uniprot-proteins_gpx.scv`
