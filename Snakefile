rule all:
    input:
        "uniprot_ids.txt",
        "output_quickgo.tsv",
        "output_quickgo_cleaned.tsv",
        "go_graph.graphml",
        "go_graph.txt",
        "gpx_subgraph.graphml",
        "gpx_subgraph.txt",
        "go_enrichment_results.tsv",
        "proteins_gpx_go.txt",
        "uniprot-proteins_gpx.tsv"

rule extract_ids:
    input:
        "oxidative_stress.faa"
    output:
        "uniprot_ids.txt"
    shell:
        "bash extract_ids.sh"

rule quickgo:
    input:
        "uniprot_ids.txt"
    output:
        "output_quickgo.tsv"
    shell:
        "bash quickgo.sh"

rule clean_quickgo:
    input:
        "output_quickgo.tsv"
    output:
        "output_quickgo_cleaned.tsv"
    script:
        "output_quickgo_cleaned.py"

rule obo_graphs:
    input:
        "go.obo"
    output:
        "obo_go_graph.graphml",
        "obo_gpx_graph.graphml"
    script:
        "obo_graphs.py"

rule graphs:
    input:
        "output_quickgo_cleaned.tsv",
        "go.obo"
    output:
        "go_graph.graphml",
        "go_graph.txt",
        "gpx_subgraph.graphml",
        "gpx_subgraph.txt"
    script:
        "graphs.py"

rule enrichment:
    input:
        "output_quickgo_cleaned.tsv",
        "go.obo"
    output:
        "go_enrichment_results.tsv"
    script:
        "go_enrichment.py"

rule proteins_gpx_go:
    input:
        "gpx_subgraph.txt"
    output:
        "proteins_gpx_go.txt"
    script:
        "proteins_gpx_go.py"

rule uniprot_proteins_gpx:
    input:
        "proteins_gpx_go.txt"
    output:
        "uniprot-proteins_gpx.tsv"
    script:
        "uniprot-proteins_gpx.py"
