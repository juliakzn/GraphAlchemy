import pytest

import graph_alchemy

from graph_alchemy import Graph, Node, Edge, DirectedGraph, DirectedEdge, WeightedGraph, WeightedEdge

def test_graph_append():
    g = Graph()
    g.append(('a', 'b'))
    g.append(('b', 'c'))
    assert [v for v in g.vertices()] == ['a', 'b', 'c']
    assert set(g.edges()) == {('a', 'b'), ('b', 'c')}
    assert g.order() == 3
    assert g.size() == 2

def test_directed_graph_append():
    from graph_alchemy import DirectedGraph
    g = DirectedGraph()
    g.append(('a', 'b'))
    g.append(('b', 'c'))
    assert [v for v in g.vertices()] == ['a', 'b', 'c']
    assert g.edges() == [('a', 'b'), ('b', 'c')]
    assert g.order() == 3
    assert g.size() == 2

def test_directed_graph_extend():
    g = DirectedGraph()
    g.append(('a', 'b'))
    g.append(('b', 'c'))
    g.extend([(x, x + 1) for x in range(42)])
    assert g.edges() == [('a', 'b'), ('b', 'c'), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 34), (34, 35), (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 42)]
    assert g.order() == 46
    assert g.size() == 44

def test_directed_graph():
    dir_g = DirectedGraph()
    dir_g.append(('a', 'b'))
    dir_g.append(('b', 'a'))
    assert [v for v in dir_g.vertices()] == ['a', 'b']
    assert set(dir_g.edges()) == {('a', 'b'), ('b', 'a')}
    assert dir_g.order() == 2
    assert dir_g.size() == 2

def test_undirected_graph():
    undir_g = Graph()
    undir_g.append(('a', 'b'))
    undir_g.append(('b', 'a'))
    assert [v for v in undir_g.vertices()] == ['a', 'b']
    assert set(undir_g.edges()) == {('a', 'b')}
    assert undir_g.order() == 2
    assert undir_g.size() == 1

def test_directed_graph_union():
    g = DirectedGraph()
    g.extend([('a', 'b'), ('b', 'c')])
    h = DirectedGraph()
    h.extend([('d', 'e'), ('f', 'd')])
    gh = g + h
    assert set([v for v in gh.vertices()]) == {'a', 'b', 'c', 'd', 'e', 'f'}
    assert set(gh.edges()) == {('a', 'b'), ('b', 'c'), ('d', 'e'), ('f', 'd')}

    g = DirectedGraph()
    g.extend([('a', 'b'), ('b', 'c')])
    h = DirectedGraph()
    h.extend([('a', 'c'), ('c', 'b')])
    gh = g + h
    assert set([v for v in gh.vertices()]) == {'a', 'b', 'c'}
    assert set(gh.edges()) == {('a', 'b'), ('a', 'c'), ('b', 'c'), ('c', 'b')}

def test_in():
    e_0, e_1, e_2 = ('a', 'b'), ('b', 'c'), ('c', 'd')
    g = DirectedGraph([e_0, e_1])
    assert e_0 in g
    assert e_1 in g
    assert e_2 not in g

def for_in_test():
    e_0, e_1, e_2 = ('a', 'b'), ('b', 'c'), ('c', 'd')
    g = DirectedGraph([e_0, e_1, e_2])
    assert [x for x in g] == [('a', 'b'), ('b', 'c'), ('c', 'd')]

def test_weight():
    g = WeightedGraph()
    g.append(('a', 'b', 5))
    g.append(('b', 'c', 10))
    assert g.weight() == 15

def test_union_weight():
    g = WeightedGraph()
    g.append(('a', 'b', 5))
    g.append(('b', 'c', 10))

    h = WeightedGraph()
    h.append(('a', 'b', 5))
    h.append(('c', 'd', 10))

    gh = g + h

    assert gh.edge_dict[('a', 'b')] == 10
    assert gh.weight() == 30