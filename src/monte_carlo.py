import random
from collections import defaultdict
from math import sqrt, log
from unittest import result

import utils
from environment import Game


class Node(Game):
    def __init__(self, state, n, sequence):
        self.results = defaultdict(int)
        self.visits = 0
        self.parent = None
        self.children = []
        self.expanded = False
        self.simulations = 0

        self.state = state
        self.move = -1
        self.terminal_result = 0

        self.n = n
        self.sequence = sequence
        self.available_colors = list(range(len(sequence)))


    def precalc_terminal_result(self):
        result = 0
        for color in self.available_colors:
            is_color_term, _ = utils.is_color_terminal(self.state, color, self.sequence[color])
            if is_color_term:
                result = 1
            
        if len(self.state) >= 8 and result == 0:
            result = -1
        
        self.terminal_result = result
        

    def backpropagate(self, result):
        self.results[result] += 1
        self.visits += 1

        if self.parent:
            self.parent.backpropagate(result)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def make_children(self):
        for value in self.available_colors:
            for position in range(len(self.state) + 1):
                child = Node(self.state.copy(), self.n, self.sequence)
                child.move_player_2(value)
                if self.terminal_result != 0:
                    child.terminal_result = self.terminal_result
                else:
                    child.precalc_terminal_result()
                child.move = value
                child.move_player_1(position)
                

                self.add_child(child)

    def get_preferred_child(self, num_simulations):
        best_children = []
        best_score = float('-inf')

        for child in self.children:
            score = child.get_score(num_simulations)

            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)

        return random.choice(best_children)

    def get_score(self, num_simulations, c=sqrt(2)):
        exploitation_score = self.results[-1] / self.visits
        exploration_score = c * sqrt(log(num_simulations) / self.simulations)

        return exploitation_score + exploration_score


    
class MonteCarlo:
    def __init__(self, root_node):
        self.root_node = root_node

    def calculate(self, expansion_num):
        for i in range(expansion_num):
            current_node = self.root_node
            current_node.simulations += 1
            while len(current_node.children):
                current_node = self.select(current_node, i)
                current_node.simulations += 1

            self.expand(current_node)

    def expand(self, node):
        node.make_children()
        node.expanded = True
        for child in node.children:
            self.simulate(child)

    def simulate(self, node):
        node.simulations += 1
        current_state = node.state.copy()
        position = current_state.index(-1)
        result = node.terminal_result

        while result == 0:
            value = random.choice(node.available_colors)
            current_state[position] = value
            position = random.choice(list(range(len(current_state) + 1)))
            current_state = [*current_state[:position], -1, *current_state[position:]]

            for color in node.available_colors:
                check_state = current_state.copy()
                check_state.remove(-1)
                is_col_term, _ = utils.is_color_terminal(check_state, color, node.sequence[color])
                if is_col_term:
                    result = 1
                    break

            if len(current_state) > node.n and result == 0:
                result = -1

        node.backpropagate(result)

    def select(self, node, num_simulations):
        return node.get_preferred_child(num_simulations)

    def make_choice(self):
        scores = []
        for move in self.root_node.available_colors:
            children_subset_scores = [child.results[-1] / child.visits for child in self.root_node.children if child.move == move]
            scores.append(min(children_subset_scores))
        print(scores)
        win_prob = max(scores)
        best_move = scores.index(win_prob)

        return best_move, win_prob
