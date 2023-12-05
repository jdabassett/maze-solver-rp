import math
from typing import NamedTuple, TypeAlias

import networkx as nx

from src.models.border import Border
from src.models.maze import Maze
from src.models.role import Role
from src.models.square import Square

Node: TypeAlias = Square


class Edge(NamedTuple):
    node1: Node
    node2: Node

    @property
    def flip(self) -> "Edge":
        """
        Reverse order of nodes in edge
        Output new Edge instance
        :return:
        """
        return Edge(self.node2, self.node1)

    @property
    def distance(self) -> float:
        """
        Find and return distance between adjacent nodes connected by edge
        :return: float
        """
        return math.dist(
            (self.node1.row, self.node1.column),
            (self.node2.row, self.node2.column),
        )

    def weight(self, bonus=1, penalty=2) -> float:
        """
        Based on role of second node in from edge pair
        Alters and returns new distance measurement
        :param bonus:
        :param penalty:
        :return:
        """
        match self.node2.role:
            case Role.REWARD:
                return self.distance - bonus
            case Role.ENEMY:
                return self.distance + penalty
            case _:
                return self.distance


def make_graph(maze: Maze) -> nx.DiGraph:
    """
    Input a maze instance.
    Create available nodes then edges from maze.
    Generate a tuple containing tuples of edges containing node1, node2, and edge weight.
    Create graph from tuple and return.
    :param maze:
    :return:
    """
    return nx.DiGraph(
        (edge.node1, edge.node2, {"weight": edge.weight()})
        for edge in get_directed_edges(maze, get_nodes(maze))
    )

# def make_graph(maze: Maze) -> nx.DiGraph:
#     # Retrieve nodes from the maze
#     nodes = get_nodes(maze)
#
#     # Get directed edges based on the maze nodes
#     directed_edges = get_directed_edges(maze, nodes)
#
#     # Generate tuples for edges with node connections and weights
#     edges_with_weights = [
#         (edge.node1, edge.node2, {"weight": edge.weight()})
#         for edge in directed_edges
#     ]
#
#     # Create a directed graph using the generated edge tuples
#     graph = nx.DiGraph(edges_with_weights)
#
#     return graph


def get_directed_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    """
    Input maze instance and set of nodes.
    Calls get_edges function to generate set of edges.
    Generates their complement before combining both sets.
    Output is set of all possible edges.
    :param maze:
    :param nodes:
    :return: set[Edge]
    """
    # set combine forward and reverse edges
    return (edges := get_edges(maze, nodes)) | {edge.flip for edge in edges}


# def get_directed_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
#     # Get edges from the maze for the given nodes
#     edges = get_edges(maze, nodes)
#
#     # Create a set of flipped edges using set comprehension
#     flipped_edges = {edge.flip for edge in edges}
#
#     # Combine the original edges with the flipped edges
#     directed_edges = edges | flipped_edges
#
#     return directed_edges


def get_nodes(maze: Maze) -> set[Node]:
    """
    Input maze instance.
    Add squares that are corridors, intersections, corners, dead-ends, entrances, or exits to set.
    Output set of nodes.
    :param maze:
    :return: set[Node]
    """
    nodes: set[Node] = set()
    for square in maze:
        # don't add exterior or wall squares
        if square.role in (Role.EXTERIOR, Role.WALL):
            continue
        # add every square with a role other than None, Exterior, or Wall
        # if square.role is not Role.NONE:
        #     nodes.add(square)
        # # add squares with intersection, dead-end, and corner borders
        # # remember sets cannot have duplicates, so it won't matter if it has already been added
        # if (
        #     square.border.intersection
        #     or square.border.dead_end
        #     or square.border.corner
        # ):
        nodes.add(square)
    # return set of nodes/squares
    return nodes


def get_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    """
    Input maze instance and set of nodes.
    Return set of edges between those nodes.
    Must generate complement to make multidirectional
    :param maze:
    :param nodes:
    :return: set[Edge]
    """
    edges: set[Edge] = set()
    for source_node in nodes:
        # traverse right
        node = source_node
        # start traverse one column right of current
        for x in range(node.column + 1, maze.width):
            # if current node has right border, break
            if node.border & Border.RIGHT:
                break
            # reassign right adjacent node to current node
            node = maze.squares[node.row * maze.width + x]
            # if new current node is already in set of nodes
            # create new edge, add to edge set, and break
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
        # traverse down
        node = source_node
        # start traverse one row below current
        for y in range(node.row + 1, maze.height):
            # if current node has bottom border, break
            if node.border & Border.BOTTOM:
                break
            # reassign bottom adjacent border to current
            node = maze.squares[y * maze.width + node.column]
            # if new current node is already in set of nodes
            # create new edge, add to edge set, and break
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
    return edges
