# GraphAlchemy

This project is for providing graph representation.

## Project use
In order to use the project import the library:
```
import graph_alchemy
```

## Data Storage
The project uses a database to hold all graph data. Three tables are used:
- ***graph*** - contains information about graphs
- ***node*** - contains information about graph nodes, related to 'graph' via ForeignKey graph_id
- ***edge*** - contains information about graph edges, related to 'node' via ForeignKeys lower_id and higher_id

All tables are used for undirected graphs, directed graphs and weighted graphs. The type of the graph is specified in the variable type of 'graph' and 'edge' tables. The items stored in the table 'node' do not differ for various types of graphs.

## Basic operations
To create a graph:
```
g = Graph()
```
To add an edge to a graph:
```
g.append(('a', 'b'))
```
To add multiple edges to a graph:
```
g.extend([(x, x + 1) for x in range(42)])
```
To see information about current order an size of the graph:
```buildoutcfg
g.order()
g.size()
```
List vertices of the graph:
```buildoutcfg
g.vertices()
```
Graphs support 'in' operator for edges:
```
e_0, e_1, e_2 = ('a', 'b'), ('b', 'c'), ('c', 'd')
g = DirectedGraph([e_0, e_1])
assert e_0 in g
assert e_1 in g
assert e_2 not in g
```
It is possible to iterate through edges of the graph:
```
e_0, e_1, e_2 = ('a', 'b'), ('b', 'c'), ('c', 'd')
g = DirectedGraph([e_0, e_1, e_2])
assert [x for x in g] == [('a', 'b'), ('b', 'c'), ('c', 'd')]
```
DirectedGraph can have an edge from 'a' to 'b', and from 'b' to 'a', while Graph contains only one edge for two vertices:
```
dir_g = DirectedGraph()
dir_g.append(('a', 'b'))
dir_g.append(('b', 'a'))
assert set(dir_g.edges()) == {('a', 'b'), ('b', 'a')}

undir_g = Graph()
undir_g.append(('a', 'b'))
undir_g.append(('b', 'a'))
assert set(undir_g.edges()) == {('a', 'b')}
```
## Union and weight
Graph (and DirectedGraph and WeightedGraph) support 'union' through '+' operator:
```
g = DirectedGraph()
g.extend([('a', 'b'), ('b', 'c')])
h = DirectedGraph()
h.extend([('d', 'e'), ('f', 'd')])
gh = g + h
assert set(gh.edges()) == {('a', 'b'), ('b', 'c'), ('d', 'e'), ('f', 'd')}
```
WeightedGraph provides overall weight for the graph (sum of weights of all edges).
```
g = WeightedGraph()
g.append(('a', 'b', 5))
g.append(('b', 'c', 10))
assert g.weight() == 15
```
For weighted graphs, an edge in the union has the sum of its weights in the initial graphs:
```
g = WeightedGraph()
g.append(('a', 'b', 5))
g.append(('b', 'c', 10))

h = WeightedGraph()
h.append(('a', 'b', 5))
h.append(('c', 'd', 10))

gh = g + h

assert gh.edge_dict[('a', 'b')] == 10
assert gh.weight() == 30
```
