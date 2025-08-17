'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'

data_path = "/data/imdb_movies_2000to2022.prolific.json"

edge = []

with open(data_path, "r", encoding="utf-8") as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions

        # Load the movie from this line
        this_movie = json.loads(line)
            
        # Create a node for every actor
        for actor_id, actor_name in this_movie['actors']:
        # add the actor to the graph
            g.add_node(actor_name)    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
            i = 0 #counter
        for left_actor_id,left_actor_name in this_movie['actors']:
            for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:
                current = g[left_actor_name][right_actor_name]['weight'] if g.has_edge(left_actor_name, 
                                                                                       right_actor_name) else 0
                # Get the current weight, if it exists
                g.add_edge(left_actor_name, right_actor_name, weight = current + 1)
                
                # Add an edge for these actors
                edge.append((left_actor_name, "<->", right_actor_name))
            i += 1
                
#helper to give us the top 10 nodes 
def top_10_Nodes(x, n = 10):
    nodes = nx.degree_centrality(x)
    return sorted(nodes(), key= lambda y: y[1], reverse= True)[:n]

# Print the info below
print("Nodes:", len(g.nodes))

#Print the 10 the most central nodes
print("\nTop 10 most central nodes:")
for node, score in top_10_Nodes(x, n=10):
    print(f"{node}: {score:.2f}")

# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
timestamp = pd.Timestamp.now().strftime()
output = f"/data/network_centrality_{timestamp}.csv"
