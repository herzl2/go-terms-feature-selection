import networkx as nx
import obonet
import re

# Paths to the files
obo_file = "go.obo"  # Path to the GO ontology file
output_graph_go = "obo_go_graph.graphml"  # Output file for the full GO graph
output_graph_gpx = "obo_gpx_graph.graphml"  # Output file for the GPX subgraph

# Load the GO ontology graph from the OBO file
def load_go_graph(obo_file):
    print("Loading GO graph...")
    graph = obonet.read_obo(obo_file)  # Read the OBO file into a NetworkX graph
    return graph

# Filter GO terms related to GPX (Glutathione Peroxidase)
def filter_gpx_terms(graph):
    gpx_terms = []
    for node, data in graph.nodes(data=True):
        # Use regex to find GO terms that mention GPX or Glutathione Peroxidase in possible spellings
        if re.search(r"GPX|Glutathione Peroxidase|glutathione peroxidase|Glutathioneeperoxidase|glutathioneperoxidase", 
                     str(data), re.IGNORECASE):
            gpx_terms.append(node)
    return gpx_terms  # Return the list of GPX-related GO terms

# Clean attributes of nodes, edges, and the graph
def clean_graph_attributes(graph):
    print("Cleaning attribute values...")

    # Clean node attributes and add 'Node' attribute
    for node, data in graph.nodes(data=True):
        data['Node'] = node  # Store the node ID as an attribute
        for key, value in list(data.items()):
            if isinstance(value, list):  # Convert lists to strings
                data[key] = "; ".join(map(str, value))
            elif not isinstance(value, (str, int, float, bool, type(None))):  # Remove unexpected data types
                del data[key]

    # Clean edge attributes
    for u, v, data in graph.edges(data=True):
        for key, value in list(data.items()):
            if isinstance(value, list):  # Convert lists to strings
                data[key] = "; ".join(map(str, value))
            elif not isinstance(value, (str, int, float, bool, type(None))):  # Remove unexpected data types
                del data[key]

    # Clean graph attributes
    for key, value in list(graph.graph.items()):
        if isinstance(value, list):  # Convert lists to strings
            graph.graph[key] = "; ".join(map(str, value))
        elif not isinstance(value, (str, int, float, bool, type(None))):  # Remove unexpected data types
            del graph.graph[key]

# Main function to execute the workflow
def main():
    # Load the GO ontology graph
    go_graph = load_go_graph(obo_file)

    # Clean attributes in the GO graph
    clean_graph_attributes(go_graph)

    # Save the full GO graph
    print(f"Saving the full GO graph with {len(go_graph.nodes)} nodes...")
    nx.write_graphml(go_graph, output_graph_go)
    print(f"Graph saved in {output_graph_go}.")

    # Filter GO terms related to GPX
    gpx_terms = filter_gpx_terms(go_graph)
    print(f"Found GPX-related GO terms: {gpx_terms}")

    # Create a subgraph containing only GPX-related GO terms
    gpx_subgraph = go_graph.subgraph(gpx_terms).copy()

    # Clean attributes in the GPX subgraph
    clean_graph_attributes(gpx_subgraph)

    # Save the GPX subgraph
    print(f"Saving the GPX graph with {len(gpx_subgraph.nodes)} nodes...")
    nx.write_graphml(gpx_subgraph, output_graph_gpx)
    print(f"GPX graph saved in {output_graph_gpx}.")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
