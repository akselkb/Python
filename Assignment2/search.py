from Map import Map_Obj as Map
from Node import Node_Obj as N
import heapq


def create_successors(x, map):
    SUCC = []
    x_pos = x.get_state()
    # positions = [left, below, right, above]
    positions = [[x_pos[0] - 1, x_pos[1]], [x_pos[0], x_pos[1] - 1],
                 [x_pos[0] + 1, x_pos[1]], [x_pos[0], x_pos[1] + 1]]
    # expanding node x
    for pos in positions:
        try:
            cost = map.get_cell_value(pos)
            if cost < 0:    # i.e. obstacle
                continue
            s = N(x, pos[0], pos[1], map.get_goal_pos()[0], map.get_goal_pos()[1], cost)
            SUCC.append(s)
        except IndexError:
            continue
    return SUCC


# The A* implementation
def solve_a_map(t):
    OPEN = []    # unexpanded nodes, sorted by ascending f values
    CLOSED = []  # already expanded nodes
    map = Map(task=t)
    goal_pos = map.get_goal_pos()

    # Initializing the start node
    n0 = N(None, map.get_start_pos()[0], map.get_start_pos()[1], goal_pos[0], goal_pos[1],
           map.get_cell_value(map.get_start_pos()))
    OPEN.append(n0)

    while True:
        if len(OPEN) == 0:  # i.e. there's no further nodes to expand
            print('could not find a solution to the problem')
            return
        x = heapq.heappop(OPEN)  # retrieve the node with the lowest f value
        CLOSED.append(x)
        if goal_pos == x.get_state():   # goal check
            x = x.get_parent()
            # create predecessor path in the map
            while x.get_parent():
                map.set_cell_value(x.get_state(), '+')
                x = x.get_parent()
            map.show_map()
            return
        SUCC = create_successors(x, map)
        for s in SUCC:
            open_flag, closed_flag = False, False
            # Check if x has a successor in OPEN
            for o in OPEN:
                if o.get_state() == s.get_state():
                    s = o
                    open_flag = True
                    break
            if not open_flag:
                # Check if x has a successor in CLOSED
                for c in CLOSED:
                    if c.get_state() == s.get_state():
                        s = c
                        closed_flag = True
                        break
            x.add_kid(s)
            if not open_flag and not closed_flag:  # i.e. s is a new node
                heapq.heappush(OPEN, s)
            elif x.get_g() + s.get_cost() < s.get_g():
                s.set_parent(x)
        heapq.heapify(OPEN)
        
        
solve_a_map(1)  # Part 1 - Task 1
solve_a_map(2)  # Part 1 - Task 2
solve_a_map(3)  # Part 2 - Task 3
solve_a_map(4)  # Part 2 - Task 4
