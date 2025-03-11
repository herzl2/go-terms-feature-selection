import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate  # Import tabulate

# Paths to the input and output files
input_file = "gpx_subgraph.txt"  # Input file containing protein-GO term relationships
output_file = "proteins_gpx_go.txt"  # Output file to store extracted relationships

# Function to create a graph and write the extracted information to a file
def create_graph_and_write_to_file(input_file, output_file):
    G = nx.Graph()  # Create an empty undirected graph
    current_go_term = None  # Variable to store the current GO term
    table_data = []  # List to store rows for tabulate

    with open(input_file, 'r') as f, open(output_file, 'w') as out_f:
        # Add headers to the table data
        table_data.append(["Protein", "Relation", "GO Term"])

        for line in f:
            line = line.strip()
            # Check if the line represents a GO term
            if line.startswith("Node:"):
                current_go_term = line.split(": ")[1]  # Extract the GO term
                G.add_node(current_go_term, type='GO')  # Add the GO term as a node
            # Check if the line represents a protein entry
            elif line.startswith("Protein:"):
                if current_go_term:  # Ensure a GO term is set before adding a protein
                    parts = line.split()  # Split the line by whitespace
                    protein_info = parts[1]  # Extract the protein ID (second element)
                    relationship = parts[2]  # Extract the relationship type (third element)
                    G.add_node(protein_info, type='Protein')  # Add the protein as a node
                    G.add_edge(current_go_term, protein_info, relationship=relationship)  # Create an edge between the GO term and protein

                    # Add the row to the table data
                    table_data.append([protein_info, relationship, current_go_term])

        # Write the formatted table to the output file using tabulate
        out_f.write(tabulate(table_data, headers="firstrow", tablefmt="plain"))

    return G  # Return the created graph

# Function to visualize the graph
def draw_graph(G):
    pos = nx.spring_layout(G)  # Compute the positions of nodes for visualization
    plt.figure(figsize=(12, 8))  # Set the figure size

    # Define colors for different relationships
    edge_colors = []
    for u, v, data in G.edges(data=True):
        if data['relationship'] == 'enables':
            edge_colors.append('blue')
        elif data['relationship'] == 'contributes_to':
            edge_colors.append('red')
        else:
            edge_colors.append('gray')  # Default color for other relationships

    # Draw nodes for GO terms in light blue
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue', label='GO Terms', 
                           nodelist=[n for n, d in G.nodes(data=True) if d['type'] == 'GO'])
    
    # Draw nodes for proteins in light grey
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgrey', label='Proteins', 
                           nodelist=[n for n, d in G.nodes(data=True) if d['type'] == 'Protein'])

    # Draw edges with different colors based on relationships
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color=edge_colors)

    # Draw labels for nodes
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Add a legend explaining the edge colors
    handles = [
        plt.Line2D([0], [0], color='blue', lw=2, label='enables'),
        plt.Line2D([0], [0], color='red', lw=2, label='contributes_to'),
    ]
    plt.legend(handles=handles)

    # Add a title and remove axis labels
    plt.title("Protein-GO Term Relationships")
    plt.axis('off')  # Hide axis labels
    plt.show()  # Display the graph

# Main function to execute the workflow
def main():
    # Create a graph from the input file and write the extracted relationships to a new file
    G = create_graph_and_write_to_file(input_file, output_file)

    # Visualize the created graph
    draw_graph(G)

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
