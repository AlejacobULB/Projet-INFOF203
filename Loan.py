

class Loan(object):

    def __init__(self, node_from, node_to, amount):
        self.node_from = node_from
        self.node_to = node_to
        self.amount = amount
    def get_node_from(self):
        return self.node_from

    def get_node_to(self):
        return self.node_to

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount
        if self.amount == 0:
            self.node_from.removeLoan()
            self.node_to.delCreditor()


def create_loan(graph, name_from, name_to, amount):
    return Loan(graph.get_node(name_from), graph.get_node(name_to), amount)
