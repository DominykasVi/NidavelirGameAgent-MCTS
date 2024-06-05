import plotly.graph_objects as go
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.exporter import DotExporter
import subprocess
import networkx as nx
import os
import numpy as np


class NewNode:
    def __init__(self, id, name, parent=None):
        self.id = id
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class Visualizer():
    def __init__(self, root, save_file) -> None:
        self.root = root
        self.total_runs = root.iterations
        self.save_path = f"Logs/Visualizations/{save_file}.html"
        
        folder_path = os.path.dirname(self.save_path)
        # Check if the folder exists
        if not os.path.exists(folder_path):
            # If the folder does not exist, create it including any necessary parent directories
            os.makedirs(folder_path)


    def calculate_angular_positions(depths):
        # Get unique depths and their counts to estimate angular span
        unique_depths = sorted(set(depths))
        max_depth = max(unique_depths)
        angle_increment = 2 * np.pi / max_depth  # Full circle divided by number of layers
        positions = {}

        for depth in unique_depths:
            radius = depth / max_depth  # Normalize radius
            angle = np.pi / 2 - (depth - 1) * angle_increment  # Position at the start of each layer
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            positions[depth] = (x, y, angle)
        
        return positions

# Function to extract edges and nodes for plotting
    def extract_edges_nodes(self, node, nodes=[], edges=[], level=0, pos=0):
        nodes.append({'name': node.name, 'level': level, 'pos': pos})
        for index, child in enumerate(node.children):
            edges.append({'start': node.name, 'end': child.name})
            self.extract_edges_nodes(child, nodes, edges, level+1, pos + index)
        return nodes, edges
    
    def convert_to_anytree(self, node, parent=None):
        anytree_node = Node(name='\n'.join(node.name.split('.'))+f'\n{node.id}', parent=parent)
        for child in node.children:
            self.convert_to_anytree(child, parent=anytree_node)
        return anytree_node
    
    def conver_to_plotly(self, node, parent=None):
        node.oma = False
        new_node = NewNode(str(node.id), '\n'.join(node.name.split('.')) + '\n' + str(node.calculate_node_value(self.total_runs)), parent)
        node.oma = True
        if node.mcts is True:
            new_node.name = new_node.name + f'\nHash_value: {node.history}'
            

        # new_node = NewNode(str(node.id), ''.join(e for e in node.name if e.isalnum() or e.isspace()) , parent)

        for child in node.children:
            child_node = self.conver_to_plotly(child, parent=new_node)
            new_node.add_child(child_node)
        return new_node
    
    @staticmethod
    def convert_to_plotly_format(node):
        if not node.children:
            return {"ids": [node.id], "labels": [node.name], "parents": [node.parent.id if node.parent else ""]}

        ids = [node.id]
        labels = [node.name]
        parents = [node.parent.id if node.parent else ""]

        for child in node.children:
            child_data = Visualizer.convert_to_plotly_format(child)
            ids.extend(child_data["ids"])
            labels.extend(child_data["labels"])
            parents.extend(child_data["parents"])

        return {"ids": ids, "labels": labels, "parents": parents}
    
    def convert_to_plotly_format_2(node, depth=1):
        if not node.children:
            return {
                "ids": [node.id],
                "labels": [f"{node.name} ({depth})"],  # Include depth in label
                "parents": [node.parent.id if node.parent else ""],
                "depths": [depth]
            }

        ids = [node.id]
        labels = [f"{node.name} ({depth})"]  # Include depth in label
        parents = [node.parent.id if node.parent else ""]
        depths = [depth]

        for child in node.children:
            child_data = Visualizer.convert_to_plotly_format_2(child, depth + 1)
            ids.extend(child_data["ids"])
            labels.extend(child_data["labels"])
            parents.extend(child_data["parents"])
            depths.extend(child_data["depths"])

        return {"ids": ids, "labels": labels, "parents": parents, "depths": depths}


    
    def traverse_node(node, ids=[], labels=[], parents=[]):
        ids.append(node.id)
        labels.append(node.name)
        parents.append(node.parent if node.parent else "")
        for child in node.children:
            Visualizer.traverse_node(child, ids, labels, parents)
        return ids, labels, parents
    

    
    def visualize(self):
        test = self.conver_to_plotly(self.root)
        # def add_edges(graph, node):
        #     for child in node.children:
        #         graph.add_edge(node.id, child.id)
        #         add_edges(graph, child)


        # # Build the NetworkX graph
        # G = nx.DiGraph()
        # add_edges(G, test)

        # # Generate positions for each node using a tree layout
        # # pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
        # pos = nx.spring_layout(G, seed=42)  
        # # Create edges
        # edge_x = []
        # edge_y = []
        # for edge in G.edges:
        #     x0, y0 = pos[edge[0]]
        #     x1, y1 = pos[edge[1]]
        #     edge_x += [x0, x1, None]
        #     edge_y += [y0, y1, None]

        # edge_trace = go.Scatter(
        #     x=edge_x, y=edge_y,
        #     line=dict(width=2, color='black'),
        #     mode='lines',
        #     hoverinfo='none'
        # )

        # # Create nodes
        # node_x = []
        # node_y = []
        # for node in G.nodes:
        #     x, y = pos[node]
        #     node_x.append(x)
        #     node_y.append(y)

        # node_trace = go.Scatter(
        #     x=node_x, y=node_y,
        #     mode='markers+text',
        #     text=[n for n in G.nodes],
        #     textposition="bottom center",
        #     hoverinfo='text',
        #     marker=dict(
        #         showscale=False,
        #         color='blue',
        #         size=10,
        #         line_width=2
        #     )
        # )

        # # Create figure
        # fig = go.Figure(data=[edge_trace, node_trace],
        #                 layout=go.Layout(
        #                     showlegend=False,
        #                     hovermode='closest',
        #                     margin=dict(b=0, l=0, t=0, r=0),
        #                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        #                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        #                     plot_bgcolor='white'
        #                 )
        #             )

        # # Remove axis
        # fig.update_xaxes(visible=False)
        # fig.update_yaxes(visible=False)

        # # Show the plot
        # fig.show()









        #v1
        plotly_data = self.convert_to_plotly_format(test)
        fig = go.Figure(go.Sunburst(
            ids=plotly_data['ids'],
            labels=plotly_data['labels'],
            parents=plotly_data['parents'],
        ))
        fig.write_html(f"{self.save_path.replace('.html', '_b.html')}")
        # fig.write_image(f"{self.save_path.replace('.html', '_b.png')}")

        
        plotly_data = Visualizer.convert_to_plotly_format_2(test)  # Replace with your actual function call
        # Define colors for each layer
        layer_colors = {
            1: '#ffffff',   # white for depth 1
            2: '#1f77b4',   # muted blue
            3: '#ff7f0e',   # safety orange
            4: '#2ca02c',   # cooked asparagus green
            5: '#d62728',   # brick red
            6: '#9467bd',   # muted purple
            7: '#8c564b',   # chestnut brown
            8: '#e377c2',   # raspberry yogurt pink
            9: '#7f7f7f',   # middle gray
            10: '#bcbd22',  # curry yellow-green
            11: '#17becf',  # blue-teal
            12: '#aec7e8',  # soft blue
            13: '#ffbb78',  # soft orange
            14: '#98df8a',  # pale green
            15: '#ff9896',  # pale red
            16: '#c5b0d5',  # soft purple
            17: '#c49c94',  # pale brown
            18: '#f7b6d2',  # pale pink
            19: '#c7c7c7',  # light gray
            20: '#dbdb8d'   # faded yellow
        }

        # Create color array for sunburst chart
        colors = [layer_colors.get(depth, '#ddd') for depth in plotly_data['depths']]

        # Generate the sunburst chart
        fig = go.Figure(go.Sunburst(
            ids=plotly_data['ids'],
            labels=plotly_data['labels'],
            parents=plotly_data['parents'],
            branchvalues="total",
            marker=dict(colors=colors),  # Assign colors directly
        ))

        legend_x = 1.05  # x position for legend (a little to the right of the sunburst)
        legend_y_start = 1  # starting y position for the legend
        max_depth = max(plotly_data['depths'])
        # Add legend entries as scatter plot markers and text annotations
        for i, (depth, color) in enumerate(sorted(layer_colors.items(), key=lambda x: x[0]), 1):
            # Add color block as a rectangle annotation
            if int(depth) <= max_depth:
                fig.add_annotation(
                    x=legend_x, xref="paper",
                    y=legend_y_start - 0.05 * i, yref="paper",
                    xanchor="left", yanchor="middle",
                    text="&#9608;",  # Unicode character for a solid block
                    font=dict(family="Arial", size=16, color=color),
                    showarrow=False
                )

                # Add text next to the color block
                fig.add_annotation(
                    x=legend_x + 0.02, xref="paper",
                    y=legend_y_start - 0.05 * i, yref="paper",
                    xanchor="left", yanchor="middle",
                    text=f"Depth {depth}",
                    font=dict(family="Arial", size=12, color='black'),
                    showarrow=False
                )
        fig.update_layout(
            margin=dict(t=0, l=0, r=200, b=0)  # Adjust right margin to fit legend
        )
        fig.write_html(f"{self.save_path}")
        # fig.write_image(f"{self.save_path.replace('.html', '.png')}")
        print('Drawn')

        # # good code
        # anytree_root = self.convert_to_anytree(self.root)
        # # # Export to Dot format
        # DotExporter(anytree_root).to_dotfile("tree.dot")
        # subprocess.call(['dot', '-Tpdf', 'tree.dot', '-o', f"{self.save_path.replace('.html', '.pdf')}"])












        # Convert to an image file
        # DotExporter(anytree_root, graph="graph [size=\"12,12\"]").to_picture("tree.png")
        # UniqueDotExporter(anytree_root).to_picture("tree.png")
    # def visualize(self):h
    #     nodes, edges = self.extract_edges_nodes(self.root)

    #     # Creating the scatter plot for nodes
    #     trace_nodes = go.Scatter(
    #         x=[node['level'] for node in nodes], 
    #         y=[node['pos'] for node in nodes],
    #         text=[node['name'] for node in nodes],
    #         mode='markers+text',
    #         textposition='bottom center',
    #         marker=dict(size=10, color='blue')
    #     )

    #     # Creating the line plot for edges
    #     edge_x = []
    #     edge_y = []
    #     for edge in edges:
    #         start_node = next(item for item in nodes if item["name"] == edge['start'])
    #         end_node = next(item for item in nodes if item["name"] == edge['end'])
    #         edge_x.extend([start_node['level'], end_node['level'], None])
    #         edge_y.extend([start_node['pos'], end_node['pos'], None])

    #     trace_edges = go.Scatter(
    #         x=edge_x,
    #         y=edge_y,
    #         line=dict(width=1, color='black'),
    #         hoverinfo='none',
    #         mode='lines'
    #     )

    #     # Defining the layout
    #     layout = go.Layout(
    #         paper_bgcolor='white',
    #         plot_bgcolor='white',
    #         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    #     )

    #     # Creating the figure
    #     fig = go.Figure(data=[trace_edges, trace_nodes], layout=layout)
    #     fig.show()
