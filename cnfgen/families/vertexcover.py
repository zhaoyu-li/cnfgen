#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Formulas that encode vertex cover problem
"""


from cnfgen.cnf import CNF
from cnfgen.graphs import enumerate_vertices, enumerate_edges, neighbors
from itertools import combinations, combinations_with_replacement, product


def VertexCoverFormula(G, k):
    r"""Generates the clauses for a vertex cover for G of size <= k

    Parameters
    ----------
    G : networkx.Graph
        a simple undirected graph
    k : a positive int
        the size limit for the vertex cover

    Returns
    -------
    CNF
       the CNF encoding for vertex cover of size :math:`\leq k` for graph :math:`G`

    """
    if not isinstance(k, int) or k < 1:
        ValueError("Parameter \"k\" is expected to be a positive integer")

    # Describe the formula
    name = "{}-Vertex Cover".format(k)

    if hasattr(G, 'name'):
        header = name + " of graph:\n" + G.name
    else:
        header = name
    
    col = CNF(description=header)

    # Fix the vertex order
    V = enumerate_vertices(G)
    E = enumerate_edges(G)

    def D(v):
        return "x_{{{0}}}".format(v)

    def M(v,i):
        return "g_{{{0},{1}}}".format(v,i)

    def N(v):
        return tuple(sorted([v] + [u for u in G.neighbors(v)]))

    # Create variables
    for v in V:
        col.add_variable(D(v))
    for i, v in product(range(1,k+1), V):
        col.add_variable(M(v,i))

    # No two (active) vertices map to the same index
    for i in range(1, k+1):
        for c in CNF.less_or_equal_constraint([M(v,i) for v in V], 1):
            col.add_clause(c)

    # (Active) Vertices in the sequence are not repeated
    for i,j in combinations_with_replacement(range(1,k+1), 2):
        i, j = min(i, j), max(i, j)
        for u, v in combinations(V, 2):
            u, v = max(u, v), min(u, v)
            col.add_clause([(False, M(u, i)), (False, M(v, j))])

    # D(v) = M(v,1) or M(v,2) or ... or M(v,k)
    for i, v in product(range(1, k+1), V):
        col.add_clause([(False, M(v, i)), (True, D(v))])
    for v in V:
        col.add_clause([(False, D(v))] + [(True, M(v, i)) for i in range(1, k+1)])

    # Every neighborhood must have a true D variable
    for v1, v2 in E:
        col.add_clause([(True, D(v1)), (True, D(v2))])

    return col
