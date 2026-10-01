import networkx as nx


def build_transaction_graph(
    transactions
):

    graph = nx.DiGraph()

    for _, row in transactions.iterrows():

        graph.add_edge(

            row["sender_id"],

            row["receiver_id"],

            amount=row["amount"]

        )

    return graph
