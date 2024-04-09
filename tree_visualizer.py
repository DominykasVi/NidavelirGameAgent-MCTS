import plotly.graph_objects as go
# from anytree import Node, RenderTree
# from anytree.exporter import UniqueDotExporter
# from anytree.exporter import DotExporter
import subprocess
import networkx as nx
import os

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
        new_node = NewNode(str(node.id), '\n'.join(node.name.split('.')) + '\n' + str(node.calculate_node_value(self.total_runs)), parent)
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










        plotly_data = self.convert_to_plotly_format(test)
        # fig = go.Figure(go.Treemap(
        #     ids=plotly_data['ids'],
        #     labels=plotly_data['labels'],
        #     parents=plotly_data['parents'],
        #     root_color="lightgrey"
        # ))
        fig = go.Figure(go.Sunburst(
            ids=plotly_data['ids'],
            labels=plotly_data['labels'],
            parents=plotly_data['parents'],
        ))
        # for obj in plotly_data['ids']:
        #     if not isinstance(obj, str):
        #         print(f'ids {obj}')
        # for obj in plotly_data['labels']:
        #     if not isinstance(obj, str):
        #         print(f'labels {obj}')
        # for obj in plotly_data['parents']:
        #     if not isinstance(obj, str):
        #         print(f'parents {obj}')

        fig.write_html(f"{self.save_path}")
        # good code
        # anytree_root = self.convert_to_anytree(self.root)
        # # # Export to Dot format
        # DotExporter(anytree_root).to_dotfile("tree.dot")
        # subprocess.call(['dot', '-Tpdf', 'tree.dot', '-o' 'tree.pdf'])












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
