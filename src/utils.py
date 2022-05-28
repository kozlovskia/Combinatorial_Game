from pathlib import Path

import numpy as np


def is_color_terminal(state, color, max_color_num):
    state = np.array(state)
    color_positions = np.argwhere(state == color).flatten()
    for dist in range(1, len(state)):
        for i, pos in enumerate(color_positions):
            later_dists = color_positions[i:].copy() - pos
            sequence_len = 1
            ret_seq = [i]
            while len(later_dists):
                later_dists -= dist
                if 0 in later_dists:
                    which_idx = np.argwhere(later_dists == 0).flatten()[0]
                    ret_seq.append(ret_seq[-1] + which_idx)
                    sequence_len += 1
                    later_dists = later_dists[which_idx:]
                else:
                    break
                if sequence_len == max_color_num:
                    return True, list(color_positions[ret_seq])

    return False, list()


def write_one_state(logs, state):
    logs = logs + '\n' + ' '.join(list(map(str, state)))

    return logs


def write_result(logs, result):
    winner = {1: 'player_1', -1: 'player_2'}[result[0]]

    if winner == 'player_1':
        explanation = 'Given ids make arithmetic subsequence ' + ' '.join(list(map(str, result[1])))
    elif winner == 'player_2':
        explanation = 'Already placed n tokens'
    else:
        explanation = 'BUG!'

    logs += f'\n\n{explanation}'

    return logs


def write_logs(output_path, logs):
    with output_path.open('w') as f:
        f.write(logs)
    print(f'Saved logs to {output_path}')


def get_first_free_path(path):
    used = [int(file.stem) for file in path.iterdir()]
    used = sorted(used)
    if not len(used):
        return path / '0.txt'

    for i in range(used[-1] + 2):
        if i not in used:
            return path / f'{i}.txt'


def move_correctness(move, max_move):
    try:
        move = int(move)
    except:
        return False
    if move < 0 or move > max_move:
        return False
    return True


def print_arithmetic_subseq(state, terminal_indices):
    state_strs = list(map(str, state))
    top_line = ""
    ret = ""
    bot_line = ""
    for i, el in enumerate(state_strs):
        if i in terminal_indices:
            top_line += " "
            top_line += "_" * len(el)
            top_line += " "
            ret += f"|{el}|"
            bot_line += " "
            bot_line += "T" * len(el)
            bot_line += " "
        else:
            top_line += " " * len(el)
            ret += el
            bot_line += " " * len(el)
        top_line += " "
        ret += " "
        bot_line += " "

    print(top_line)
    print(ret)
    print(bot_line)
