"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from tree import Tree
from stack_sol import Stack
from game import Game


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

def recursive_strategy(g: 'Game') -> Any:
    initial_state = g.current_state
    current_player = g.current_state.get_current_player_name()
    possible_moves = initial_state.get_possible_moves()
    id = {}
    for i in possible_moves:
        id[helper_r(current_player, g.current_state.make_move(i))] = i
    return id[max(list(id))]

def helper_r(player, state):
    if not state.get_possible_moves() and player == state.get_current_player_name():
        return -1
    elif not state.get_possible_moves() and player != state.get_current_player_name():
        return 1
    elif not state.get_possible_moves():
        return 0
    else:
        return -1 * max([helper_r(state.get_current_player_name(), state.make_move(i)) for i in state.get_possible_moves()])


def iterative_strategy(game: 'Game') -> Any:
    new_game = game.current_state
    tree = Tree(new_game)
    s = Stack()
    old_state = {}
    s.add(tree)
    while not s.is_empty():
        state = s.remove()
        if state.value.get_possible_moves() == []:
            old_state[state.value] = -1
        else:
            if not state.children:
                new_state = [state.value.make_move(i) for i in state.value.get_possible_moves()]
                t_new_state = Tree(state, [Tree(new_state)])
                s.add(t_new_state)
                for i in state.value.get_possible_moves():
                    n = state.value.make_move(i)
                    s.add(Tree(n))
            elif state.children:
                possible_scores = [old_state[i] * -1 for i in state.children]
                old_state[state.value] = max(possible_scores)
    for i, z in zip(tree.children, new_game.get_possible_moves()):
        if old_state[i] == -1 * old_state[tree]:
            return z



if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
