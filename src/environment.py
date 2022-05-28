import numpy as np

import utils


class Game:
    def __init__(self, n, sequence, state):
        self.n = n
        self.sequence = sequence
        self.available_colors = list(range(len(sequence)))

        self.state = state

    def move_player_1(self, position):
        self.state = [*self.state[:position], -1, *self.state[position:]]

    def move_player_2(self, value):
        self.state[self.state.index(-1)] = value

    def result(self):
        for color in self.available_colors:
            is_terminal, which_terminal = utils.is_color_terminal(self.state, color, self.sequence[color])
            if is_terminal:
                return 1, which_terminal

        if len(self.state) == self.n:
            return -1, []

        return 0, []

    def present_state(self, is_terminal=False):
        state_strs = list(map(str, self.state))
        state_line = "__"
        indices_line = "0 "
        for i, el in enumerate(state_strs):
            state_line += el
            indices_line += len(el) * " "
            state_line += "__"
            indices_line += str(i + 1)
            if len(str(i + 1)) == 1:
                indices_line += " "
        if is_terminal:
            print("Terminal game state:")
            print(state_line)
        else:
            print("Current game state:")
            print(state_line)
            print(indices_line)
            print(f'Select place from indices above: min = 0, max = {len(self.state)}')
