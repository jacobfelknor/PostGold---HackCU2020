import networkx as nx
import random


class Node:
    def __init__(self, *args, **kwargs):
        self.word = kwargs.pop("word", None)
        self.frequency = kwargs.pop("frequency", None)
        self.start = kwargs.pop("start", False)
        self.start_freq = kwargs.pop("start_freq", 0)
        self.end = kwargs.pop("end", False)
        self.end_freq = kwargs.pop("end_freq", 0)

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word


def search_graph(word, g):
    for node in g.nodes:
        if node.word == word:
            return node
    return None


if __name__ == "__main__":
    g = nx.DiGraph()

    words = ["this", "is", "a", "test", "sentence"]
    # nodes = []
    for x in words:
        g.add_node(
            Node(
                word=x,
                frequency=random.randint(1, 10),
                start=bool(random.getrandbits(1)),
                end=bool(random.getrandbits(1)),
            )
        )

    g.add_edge()

    # g.add_node(
    #     Node(
    #         word="this",
    #         frequency=random.randint(1, 10),
    #         start=bool(random.getrandbits(1)),
    #         end=bool(random.getrandbits(1)),
    #     )
    # )

    print(g.nodes)
    # g.add_edge()
