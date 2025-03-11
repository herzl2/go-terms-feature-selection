# Gene Annotation & Feature Selection with GO Terms

## Overview
This project implements a pipeline for annotating human proteins using Gene Ontology (GO) terms with a focus on oxidative stress-related proteins. As a case study, we illustrate the pipeline using the glutathione peroxidase (GPX) family—chosen based on our research interest—but the workflow is fully adaptable to other protein families.

It integrates data from UniProt, QuickGO, and InterPro to perform feature selection and enrichment analysis, providing comprehensive insights into the functional landscape of proteins under oxidative stress.

## Key Features 
- **Automated Data Retrieval:** Fetches protein sequences and annotations via APIs.
- **GO Annotation Pipeline:** Uses shell scripts and Python to process, clean, and merge data.
- **Graph Extraction:** Generates comprehensive GO term networks and case-specific subgraphs (e.g., GPX family).
- **Enrichment Analysis:** Identifies the most abundant GO terms related to antioxidant functions.
- **Reproducible Workflow:** Managed by Snakemake for streamlined execution.

### Dependencies
- Unix-based system
- [Python 3.12](https://www.python.org/downloads/)
- [Snakemake](https://snakemake.readthedocs.io/en/stable/)
- [Cytoscape](https://cytoscape.org/) for graph visualization
- Required Python libraries:
  - pandas
  - networkx
  - matplotlib
  - obonet
  - requests
- Shell Tools
  - jq, curl, grep, sed, tr 

## Usage 
1. **Input Data:** Prepare your input file in FASTA format (e.g., `oxidative_stress.faa`).
2. **Configurations:** Adjust any parameters such as API endpoints or filtering criteria
3. **Run the Pipeline**
    The entire workflow is automated using Snakemake.
    - Run a dry-run to check the workflow:
    ```bash
    snakemake -n 
    ```
    - Then execite the full pipeline: 
    ```bash
    snakemake -j 1 
    ```
    This command will execute all the scripts in the correct order, generating the annotated output files and GO graphs.
   
4. **Outputs:**
   - Processed files (e.g., cleaned annotation TSV files) and merged results are generated in the output directory.
   - GO graphs are produced in GraphML format, including a full GO network (`go_graph.graphml`) and case-specific subgraphs (e.g., `gpx_graph.graphml`).
   - Enrichment analysis reports and any additional output files are also placed in the output directory.
  
## Workflow and Script Overview 
### 1. **extract_ids.sh:**  
  Reads the FASTA file (`oxidative_stress.faa`) and extracts UniProt IDs. The output is stored in `uniprot_ids.txt`.
  
### 2. Extracting Annotations from QuickGO/UniProt/InterProScan 
- **quickgo.sh:**  
  Queries QuickGO for GO annotations. The output is processed with `jq` to extract fields like qualifiers, GO aspects, and taxonomic IDs.

- **uniprot.sh:**  
  Uses `curl` to query the UniProt REST API for protein details including InterPro IDs, GO terms, and organism information. Uses `grep`, `sed`, and `tr` for data parsing.

- **interpro.sh:**  
  Processes InterPro IDs to retrieve functional domain data and related GO annotations.

### 3. Enrichment Analysis 
- **output_quickgo_cleaned.py:**  
  Cleans the QuickGO output by removing redundant entries and ensuring consistency across datasets (`output_quickgo_cleaned.tsv`).

- **go_enrichment.py:**  
  Analyzes the cleaned GO annotations and computes enrichment statistics to highlight significant GO terms (`go_enrichment_results.tsv`) and gives information in the terminal about not adopted UniProtIDs .

### 4. GO Subgraph Extraction 
- **obo_graphs.py:**  
  Build comprehensive GO term graphs from the `go.obo` file, generating full GO graphs (`obo_go_graph.graphml`) and case-specific subgraphs subgraphs (`obo_gpx_graph.graphml`) for the whole Gene Ontology to get an overview of possible GO terms for comparison of the actual results.

- **graphs.py:**  
  Vizualizes results as Go term-Graph for dataset of interest (`output_quickgo_cleaned.tsv` combined with go.obo) as `go_graph.graphml` and `go_graph.txt`. For case-specific subgraph `gpx_subgraph.graphml` and `gpx_subgrap.txt` are created.

- **proteins_gpx_go.py & uniprot-proteins_gpx.py:**  
  Map GPX-associated GO terms to protein IDs (`proteins_gpx_go.txt`) and then query UniProt to retrieve their names (`uniprot-proteins_gpx.tsv`), ultimately visualizing the association.

### 5. Optional Analysis
- **Comparison of GO Terms**:
    `comparison_GOterms.py`: Compares GO terms from QuickGO and UniProt outputs, identifying common and unique terms, and outputs the results to a TSV file.
- **Merging Results**:
    `merged_uniprot_quickgo.py`: Merges outputs from QuickGO and UniProt analyses.
    `all_merged.py`: Combines the merged data with InterProScan results into a comprehensive output file.

### Final Notes

- **Flexibility:** We used the GPX family as an example, but the pipeline works with any set of proteins.
- **Modularity:** The workflow is divided into simple steps for data extraction, cleaning, analysis, and visualization.
- **Reproducibility:** Snakemake ensures that the entire process is easily reproducible and extendable.

### Authors
- Barbara Sula
- Luna Herz


