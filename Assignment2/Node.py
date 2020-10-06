from functools import total_ordering


@total_ordering  # In order for the heap to compare nodes
class Node_Obj:
    def __init__(self, parent, x, y, x0, y0, cost):
        if parent is not None:  # i.e. not the start node
            self.g = parent.get_g() + cost
        else:
            self.g = 0
        self.h = abs(x-x0) + abs(y-y0)  # calculating the Manhattan distance
        self.parent = parent
        self.kids = []
        self.x = x
        self.y = y
        self.cost = cost

    # Getters and setters for node fields
    def get_g(self):
        return self.g

    def get_h(self):
        return self.h

    def get_f(self):
        return self.get_h() + self.get_g()

    def add_kid(self, kid):
        self.kids.append(kid)

    def get_cost(self):
        return self.cost

    def set_parent(self, parent):
        self.parent = parent
        self.g = parent.get_g() + self.get_cost()
        for kid in self.kids:
            if kid.get_g() > self.g + kid.get_cost():
                kid.set_parent(self)

    def get_state(self):
        return [self.x, self.y]

    def get_parent(self):
        return self.parent

    # Comparison definitions
    def __eq__(self, other):
        return self.get_f() == other.get_f()

    def __lt__(self, other):
        return self.get_f() < other.get_f()

    def __gt__(self, other):
        return self.get_f() > other.get_f()
