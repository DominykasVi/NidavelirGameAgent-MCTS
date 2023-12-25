import plotly.graph_objects as go
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.exporter import DotExporter
import subprocess
# class MyNode:
#     def __init__(self, name, parent=None):
#         self.name = name
#         self.parent = parent
#         self.children = []

# # Create a sample tree
# root = MyNode("Root")
# child1 = MyNode("Child1", parent=root)
# child2 = MyNode("Child2", parent=root)
# root.children = [child1, child2]
# grandchild = MyNode("GrandChild", parent=child1)
# child1.children.append(grandchild)
class Visualizer():
    def __init__(self, root) -> None:
        self.root = root
# Function to extract edges and nodes for plotting
    def extract_edges_nodes(self, node, nodes=[], edges=[], level=0, pos=0):
        nodes.append({'name': node.name, 'level': level, 'pos': pos})
        for index, child in enumerate(node.children):
            edges.append({'start': node.name, 'end': child.name})
            self.extract_edges_nodes(child, nodes, edges, level+1, pos + index)
        return nodes, edges
    
    def convert_to_anytree(self, node, parent=None):
        anytree_node = Node(name=node.name+f'\n{node.id}', parent=parent)
        for child in node.children:
            self.convert_to_anytree(child, parent=anytree_node)
        return anytree_node
    

    
    def visualize(self):
        anytree_root = self.convert_to_anytree(self.root)


        # # Export to Dot format
        DotExporter(anytree_root).to_dotfile("tree.dot")
        subprocess.call(['dot', '-Tpdf', 'tree.dot', '-o' 'tree.pdf'])
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
