import pandas as pd
import networkx as nx
import obonet
import re

# File paths
obo_file = "go.obo"  # Path to the GO ontology file
tsv_file = "output_quickgo_cleaned.tsv"  # Path to the GO term annotation file
output_graph_go = "go_graph.graphml"  # Output file for the GO graph
output_txt_go = "go_graph.txt"  # Output text file for the GO graph
output_subgraph_gpx = "gpx_subgraph.graphml"  # Output file for the GPX subgraph
output_txt_gpx = "gpx_subgraph.txt"  # Output text file for the GPX subgraph

# Load the GO ontology graph from the OBO file
def load_go_graph(obo_file):
    print("Loading GO graph...")
    graph = obonet.read_obo(obo_file)  # Read the OBO file into a NetworkX graph
    return graph

# Filter GO terms based on the TSV file
def filter_go_terms(tsv_file, go_graph):
    print("Filtering relevant GO terms...")
    df = pd.read_csv(tsv_file, sep="\t")  # Load the TSV file into a DataFrame
    df.columns = df.columns.str.strip()  # Strip spaces from column names
    terms = df['GO_Term'].tolist()  # Extract the GO terms column as a list
    return set(terms)  # Convert the list into a set for faster lookups

# Create a subgraph that contains only the selected GO terms
def create_subgraph(go_graph, terms):
    print("Creating subgraph...")
    subgraph_nodes = {term for term in terms if term in go_graph}  # Keep only valid nodes
    subgraph = go_graph.subgraph(subgraph_nodes)

    # Assign node attributes
    for node, data in subgraph.nodes(data=True):
        data['Node'] = node  # Store the GO term as an attribute

    return subgraph

# Clean attributes of nodes, edges, and the graph
def clean_graph_attributes(graph):
    # Clean node attributes
    for node, data in graph.nodes(data=True):
        for key, value in list(data.items()):
            if isinstance(value, list):  # Convert lists to strings
                data[key] = "; ".join(map(str, value))
            elif not isinstance(value, (str, int, float, bool, type(None))):  # Remove invalid types
                del data[key]

    # Clean edge attributes
    for u, v, data in graph.edges(data=True):
        for key, value in list(data.items()):
            if isinstance(value, list):  
                data[key] = "; ".join(map(str, value))
            elif not isinstance(value, (str, int, float, bool, type(None))):
                del data[key]

    # Clean graph attributes
    for key, value in list(graph.graph.items()):
        if isinstance(value, list):  
            graph.graph[key] = "; ".join(map(str, value))
        elif not isinstance(value, (str, int, float, bool, type(None))):
            del graph.graph[key]

# Extract protein data from the TSV file
def extract_protein_data(tsv_file):
    print(f"Extracting protein data from {tsv_file}...")
    df = pd.read_csv(tsv_file, sep="\t")  
    df.columns = df.columns.str.strip()  # Clean column names

    protein_data = {}
    for _, row in df.iterrows():
        go_term = row['GO_Term']
        uniprot_id = row['UniProt_ID']
        qualifier = row['Qualifier']

        if go_term not in protein_data:
            protein_data[go_term] = []
        protein_data[go_term].append((uniprot_id, qualifier))

    return protein_data

# Save nodes to a text file, including protein data if available
def write_nodes_to_txt(graph, output_file, protein_data):
    with open(output_file, 'w') as f:
        nodes = list(graph.nodes(data=True))  
        for i, (node, data) in enumerate(nodes):
            if node not in protein_data:  
                continue

            f.write(f"Node: {node}\n")  
            for key, value in data.items():
                if key != 'Node':  
                    f.write(f"{key}: {value}\n")

            # Write protein information
            for uniprot_id, qualifier in protein_data[node]:
                f.write(f"Protein: {uniprot_id} {qualifier} {node} \n")

            if i != len(nodes) - 1:
                f.write("\n")

    print(f"Nodes saved in {output_file}.")

# Identify GPX-associated GO terms based on name matching
def identify_gpx_proteins(graph):
    gpx_proteins = []
    for node, data in graph.nodes(data=True):
        if re.search(r"GPX|Glutathione Peroxidase|glutathione peroxidase|Glutathioneperoxidase|glutathioneperoxidase", 
                     str(data), re.IGNORECASE):
            gpx_proteins.append(node)
    return gpx_proteins

# Main function to execute the analysis pipeline
def main():
    # Load the GO ontology graph
    go_graph = load_go_graph(obo_file)

    # Extract protein data from the TSV file
    protein_data = extract_protein_data(tsv_file)

    # Filter GO terms based on the TSV file
    filtered_terms = filter_go_terms(tsv_file, go_graph)

    # Create a subgraph that contains only relevant GO terms
    combined_subgraph = create_subgraph(go_graph, filtered_terms)
    clean_graph_attributes(combined_subgraph)

    # Save the full GO term graph
    print(f"Saving combined GO graph with {len(combined_subgraph.nodes)} nodes...")
    nx.write_graphml(combined_subgraph, output_graph_go)
    print(f"Graph saved in {output_graph_go}.")

    # Save the nodes of the combined GO term graph with protein data
    write_nodes_to_txt(combined_subgraph, output_txt_go, protein_data)

    # Identify GO terms associated with GPX proteins
    gpx_proteins = identify_gpx_proteins(combined_subgraph)
    print(f"Found GPX-associated proteins: {gpx_proteins}")

    # Create a subgraph containing only GPX-associated GO terms
    gpx_subgraph = combined_subgraph.subgraph(gpx_proteins).copy()
    nx.write_graphml(gpx_subgraph, output_subgraph_gpx)
    print(f"GPX subgraph saved in {output_subgraph_gpx}.")

    # Save the GPX-specific subgraph nodes with protein data
    write_nodes_to_txt(gpx_subgraph, output_txt_gpx, protein_data)


if __name__ == "__main__":
    main()  # Runs the main function to create and save the GO graph and subgraph files

    # Read 'go_graph.txt' after it has been written
    try:
        with open(output_txt_go, 'r') as f: # Extract GO terms from the saved text file
            graph_terms = {line.split()[1] for line in f if line.startswith('Node:')}

        # Check for missing terms
        quickgo_df = pd.read_csv(tsv_file, sep='\t')
        quickgo_df.columns = quickgo_df.columns.str.strip()
        quickgo_terms = set(quickgo_df['GO_Term'])
        missing_terms = quickgo_terms - graph_terms
        
        print("Missing GO-terms:")
        for term in missing_terms:
            print(term)

    except FileNotFoundError:
        print("Error: 'go_graph.txt' was not created. Check the script.")
