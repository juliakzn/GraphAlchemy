from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import PickleType

Base = declarative_base()

# Use in memory SQLite as a database
engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(engine)()

class Graph(Base):
    """Class for non-directed graph"""

    __tablename__ = "graph"

    graph_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'nondirected'
    }

    def __init__(self, list_of_edges=None):
        if list_of_edges:
            self.extend(list_of_edges)

    def vertices(self):
        """Iterate through vertices in the graph"""
        for x in self.nodes:
            yield x.name

    def name_to_node_dict(self):
        """Create dictionary that relates node names and nodes"""
        return dict([(node.name, node) for node in self.nodes])

    def name_to_node(self, vertex):
        """Return node given node name"""
        return self.name_to_node_dict()[vertex]

    def edges(self):
        """Return list of tuples opf node names"""
        edges = list()
        for vertex in self.nodes:
            for lower_neighbor in vertex.lower_neighbors():
                edges.append((lower_neighbor.name, vertex.name))
        return edges

    def order(self):
        """Return order of the graph, i.e. number of vertices in the graph"""
        return len([v for v in self.vertices()])

    def size(self):
        """Return size of the graph, i.e. number of edges in the graph"""
        return len(self.edges())

    def add_vertex(self, vertex):
        """Add a new vertex to the graph"""
        if vertex not in self.vertices():
            Node(self, vertex)

    def append(self, edge):
        """Add a new edge to the graph"""
        from_vertex, to_vertex = edge
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        n1 = self.name_to_node(from_vertex)
        n2 = self.name_to_node(to_vertex)
        if (n1.name, n2.name) not in self.edges() and (n2.name, n1.name) not in self.edges():
            Edge(n1, n2)

    def extend(self, edges):
        """Extend the graph to contain new edges"""
        for edge in edges:
            self.append(edge)

    def __add__(self, graph):
        """Add two graphs"""
        new_graph = Graph()
        for edge in self.edges():
            new_graph.append(edge)
        for edge in graph.edges():
            new_graph.append(edge)
        return new_graph

    def __iter__(self):
        """Iterate through node name tuples"""
        return (i for i in self.edges())

    def __repr__(self):
        return "<Graph(graph_id='%s', type='%s', edges='%s')>" % (self.graph_id, self.type, self.edges())

class Node(Base):
    """Class for graph nodes"""

    __tablename__ = "node"

    node_id = Column(Integer, primary_key=True, autoincrement=True)
    graph_id = Column(Integer, ForeignKey("graph.graph_id"))
    name = Column(PickleType)

    graph_host = relationship(
        Graph, primaryjoin=graph_id == Graph.graph_id, backref="nodes"
    )

    def __init__(self, graph, name):
        self.graph_host = graph
        self.name = name

    def higher_neighbors(self):
        return [x.higher_node for x in self.lower_edges]

    def lower_neighbors(self):
        return [x.lower_node for x in self.higher_edges]


class Edge(Base):
    """Class for an edge of a non-directional graph"""

    __tablename__ = "edge"
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'nondirected'
    }

    lower_id = Column(Integer, ForeignKey("node.node_id"), primary_key=True)
    higher_id = Column(Integer, ForeignKey("node.node_id"), primary_key=True)
    weight = Column(Integer)  # weight is only initialized for WeightedEdge which is based on Edge

    lower_node = relationship(
        Node, primaryjoin=lower_id == Node.node_id, backref="lower_edges"
    )

    higher_node = relationship(
        Node, primaryjoin=higher_id == Node.node_id, backref="higher_edges"
    )

    def __init__(self, n1, n2):
        if n1.node_id == None or n2.node_id == None or n1.node_id < n2.node_id:
            self.lower_node = n1
            self.higher_node = n2
        else:
            self.lower_node = n2
            self.higher_node = n1


class DirectedGraph(Graph):
    """Class for directed graph"""

    __mapper_args__ = {'polymorphic_identity': 'directed'}

    def append(self, edge):
        """Add a new edge to the graph"""
        from_vertex, to_vertex = edge
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        n1 = self.name_to_node(from_vertex)
        n2 = self.name_to_node(to_vertex)
        DirectedEdge(n1, n2)

    def __add__(self, graph):
        """Add two graphs"""
        new_graph = DirectedGraph()
        for edge in self.edges():
            new_graph.append(edge)
        for edge in graph.edges():
            new_graph.append(edge)
        return new_graph

    def __repr__(self):
        return "<DirectedGraph(graph_id='%s', type='%s', edges='%s')>" % (self.graph_id, self.type, self.edges())


class DirectedEdge(Edge):
    """Class for directed edge; in contrast with undirected edge any two nodes can be connected"""

    __mapper_args__ = {'polymorphic_identity': 'directed'}

    def __init__(self, n1, n2):
        self.lower_node = n1
        self.higher_node = n2


class WeightedGraph(Graph):
    __mapper_args__ = {'polymorphic_identity': 'weighted'}

    def __init__(self, *args, **kwargs):
        super(WeightedGraph, self).__init__(*args, **kwargs)
        self.edge_dict = dict()

    def append(self, edge):
        """Add a new edge to the graph"""
        from_vertex, to_vertex, weight = edge
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        n1 = self.name_to_node(from_vertex)
        n2 = self.name_to_node(to_vertex)
        if (n1.name, n2.name) not in self.edges() and (n2.name, n1.name) not in self.edges():
            WeightedEdge(n1, n2, weight)
            self.edge_dict[(n1.name, n2.name)] = weight

    def weight(self):
        """Sum all weights in the graph"""
        weights = [v for k,v in self.edge_dict.items()]
        return sum(weights)

    def __add__(self, graph):
        """Add two graphs; sum weights for edges that appear in both graphs"""
        new_graph = WeightedGraph()

        edge_dict1 = self.edge_dict
        edge_dict2 = graph.edge_dict

        edges1 = set([k for k, v in edge_dict1.items()])
        edges2 = set([k for k, v in edge_dict2.items()])

        for edge in edges1.intersection(edges2):
            new_graph.append((edge[0], edge[1], edge_dict1[edge] + edge_dict2[edge]))

        for edge in edges1.difference(edges2):
            new_graph.append((edge[0], edge[1], edge_dict1[edge]))

        for edge in edges2.difference(edges1):
            new_graph.append((edge[0], edge[1], edge_dict2[edge]))

        return new_graph

    def __repr__(self):
        return "<WeightedGraph(graph_id='%s', type='%s', edges='%s')>" % (self.graph_id, self.type, self.edge_dict)


class WeightedEdge(Edge):
    """Class for weighted edge; stores weight for an edge"""
    __mapper_args__ = {'polymorphic_identity': 'weighted'}

    def __init__(self, n1, n2, weight):
        if n1.node_id == None or n2.node_id == None or n1.node_id < n2.node_id:
            self.lower_node = n1
            self.higher_node = n2
        else:
            self.lower_node = n2
            self.higher_node = n1
        self.weight = weight
