from argparse import ArgumentParser
from pathlib import Path

import utils
from environment import Game
from agents import MonteCarlo, Node, heuristic_best_move


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-o', '--output_dir', type=Path, default=Path('games'), 
                        help='Output directory where logs from played games will be saved.')
    parser.add_argument('-gn', '--game_number', type=int, default=-1, 
                        help=('Game number which will be logs file name. Should be a non negative integer.'
                              ' Default -1 finds first free integer to save'))
    
    parser.add_argument('-a', '--agent', type=str, default='MonteCarlo', 
                        help='Name of enemy agent. One of: MonteCarlo | Heuristic')
    parser.add_argument('--simulations', type=int, default=100, help='MC simulation amount')

    parser.add_argument('-n', type=int, default=8, help='Max number of tokens to be placed.')
    parser.add_argument('-seq', nargs='*', type=int, help='Max amount of colors')

    return parser.parse_args()


def main(args):
    print(args, end='\n\n')
    args.output_dir.mkdir(exist_ok=True, parents=True)
    if args.game_number == -1:
        output_path = utils.get_first_free_path(args.output_dir)
    else:
        output_path = args.output_dir / f'{args.game_number}.txt'
    logs = '-' * 20 + f'Agent Name: {args.agent}\n' + '-' * 20

    game = Game(args.n, args.seq, [])
    running = True

    while running:
        game.present_state()
        is_move_correct = False
        while not is_move_correct:
            move = input("(select place and press enter) ")
            is_move_correct = utils.move_correctness(move, len(game.state))
        move = int(move)
        game.move_player_1(move)

        if args.agent == 'MonteCarlo':
            root_node = Node(game.state.copy(), args.n, args.seq)
            agent = MonteCarlo(root_node)

            print('Agent is thinking...')
            agent.calculate(expansion_num=args.simulations)
            agent_move, agent_win_prob = agent.make_choice()
            agent_win_prob *= 100
            print(f'Agent calculated his win probability to be {round(agent_win_prob, 2)}%.')
            print(f'Agent inserts {agent_move}')
            game.move_player_2(agent_move)

        elif args.agent == 'Heuristic':
            print('Agent is thinking...')
            agent_move = heuristic_best_move(game)
            print(f'Agent inserts {agent_move}')
            game.move_player_2(agent_move)

        else:
            raise NotImplementedError(f'Agent {args.agent} not implemented!')

        res, which_terminal = game.result()
        if res in (-1, 1):
            running = False
            game.present_state(is_terminal=True)
            if res == 1:
                print('You won, boxed tokens make arithmetic subsequence:')
                utils.print_arithmetic_subseq(game.state, which_terminal)
            else:
                print(f'Agent won -- {args.n} tokens has been placed.')

        logs = utils.write_one_state(logs, game.state)

    logs = utils.write_result(logs, (res, which_terminal))
    utils.write_logs(output_path, logs)



if __name__ == '__main__':
    main(parse_args())
