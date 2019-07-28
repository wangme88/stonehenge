from game import Game
from game_state import GameState
from typing import Any
import copy


class StonehengeGame(Game):
    """
    Abstract class for a two-player game called Stonehenge.
    """
    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize StonehengeGame, using p1_starts to find who the first player is.
        """
        s_l = int(input("Enter the side length of the board: "))
        cell_num = sum([i + 2 for i in list(range(1, s_l + 1))])
        cell_id = {}
        cell_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                      'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                      'Y', 'Z']
        for i, n in zip(range(1, cell_num + 1), cell_names):
            cell_id[i] = n
        row = {}
        row_n = list(range(2, s_l + 2))
        row_n.append(s_l)
        for i, k in zip(row_n, range(1, len(row_n) + 1)):
            lst = {}
            for key in list(cell_id)[:i]:
                a = cell_id.pop(key)
                lst[key] = a
            row[k] = lst
        self.current_state = StonehengeState(p1_starts, s_l, row, ["@" for i in range(0, s_l+1)],
                                             ["@" for i in range(0, s_l + 1)], ["@" for i in range(0, s_l+1)])

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        instructions = "Players take turns claiming cells." + \
                       " When a player captures at least half of the cells in a ley-line," + \
                       " then the player captures the ley-line." + \
                       " The first player to capture at least half of the ley-lines is the winner."
        return instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this game is over at state.
        """
        l_line = [state.l, state.r, state.u]
        total = sum(l_line, [])
        if total.count(1) >= len(total) / 2:
            return True
        elif total.count(2) >= len(total) / 2:
            return True
        elif '@' not in total:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> Any:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        >>> StonehengeGame()
        """
        string = string.strip()
        if string.isupper() and string.isalpha():
            return string
        else:
            return 'Invalid'


class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.

    WIN - score if player is in a winning position
    LOSE - score if player is in a losing position
    DRAW - score if player is in a tied position
    p1_turn - whether it is p1's turn or not
    """
    WIN: int = 1
    LOSE: int = -1
    DRAW: int = 0
    p1_turn: bool

    def __init__(self, is_p1_turn: bool, sides, board_id, u, l, r) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        """
        super().__init__(is_p1_turn)
        self.sides = sides
        self.p1_turn = is_p1_turn
        self.id = board_id
        self.u = u
        self.l = l
        self.r = r

    def build_board(self):
        cell_num = sum([i + 2 for i in list(range(1, self.sides + 1))])
        cell_id = {}
        cell_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                      'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                      'Y', 'Z']
        for i, n in zip(range(1, cell_num + 1), cell_names):
            cell_id[i] = n
        row = {}
        row_n = list(range(2, self.sides + 2))
        row_n.append(self.sides)
        for i, k in zip(row_n, range(1, len(row_n) + 1)):
            lst = {}
            for key in list(cell_id)[:i]:
                a = cell_id.pop(key)
                lst[key] = a
            row[k] = lst
        return row

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        max_ds = self.sides + 1
        g_board = "  " * (self.sides+2) + \
                  "{}   {}\n".format(self.uley_line(1), self.uley_line(2)) + \
                  "  " * max_ds + " /   /\n"
        for row, row_info in self.id.items():
            row_letters = list(row_info.values())
            if row != self.sides + 1:
                g_board += " " * self.odd_row_lead(row - 1) + \
                           "{} - ".format(self.lley_line(row)) + \
                           " - ".join(str(i) for i in row_letters)
                if self.sides > 1:
                    if row != self.sides:
                        g_board += "   {}".format(self.uley_line(row+2))
                if len(self.id[row]) < len(self.id[row + 1]):
                    g_board += '\n' + " " * self.even_row_lead(row) + " / \\" * len(row_letters) + " /\n"
                else:
                    g_board += '\n' + " " * self.even_row_lead(row) + ' \\ /' * (len(row_letters) - 1) + " \\"
            if row == self.sides + 1:
                g_board += '\n' + " " * self.odd_row_lead(row - 1) + \
                           "{} - ".format(self.lley_line(row)) + \
                           " - ".join(str(i) for i in row_letters) + \
                           "   {}".format(self.rley_line(self.sides + 2 - row)) + \
                           "\n" + " " * self.even_row_lead(row-1) + "   \\" * len(row_letters) + \
                           "\n" + " " * self.odd_row_lead(row)
                last_row = list(range(self.sides + 3 - row, row + 1))
                last_row_r = last_row[::-1]
                for i in last_row_r:
                    g_board += "{}   ".format(self.rley_line(i))
        return g_board

    def even_row_lead(self,row):
        even_lead = [6, 4]
        if self.sides != 1:
            for i in range(0,self.sides-1):
                even_lead.append(4 + i*2)
        even_lead.reverse()
        return even_lead[row-1]

    def odd_row_lead(self,row):
        odd_lead = [8, 2]
        for i in range(0,self.sides):
                odd_lead.append(i*2)
        odd_lead.reverse()
        return odd_lead[row]

    def claimed(self,row) -> int:
        """Return the number of cells when the game is initialized"""

    def lley_line(self, row):
        if len(self.l) == self.sides+1:
            if list(self.id[row].values()).count(1) >= len(self.id[row])/2\
                    and self.l[row - 1] == '@':
                self.l[row - 1] = 1
            elif list(self.id[row].values()).count(2) >= len(self.id[row])/2\
                    and self.l[row - 1] == '@':
                self.l[row-1] = 2
        return self.l[row-1]

    def rley_line(self, row):
        r_row = {}
        r_row[1] = [self.id[1 + i][sum([c + 2 for c in range(0, 1 + i)])] for i in range(0, self.sides)]
        if self.sides == 1:
            r_row[2] =[self.id[1][1],self.id[2][3]]
        elif self.sides == 2:
            r_row[2] = [self.id[1][1],self.id[2][4],self.id[3][7]]
            r_row[3] = [self.id[2][3],self.id[3][6]]
        elif self.sides == 3:
            r_row[2] = [self.id[1][1],self.id[2][4],self.id[3][8],self.id[4][12]]
            r_row[3] = [self.id[2][3],self.id[3][7],self.id[4][11]]
            r_row[4] = [self.id[3][6],self.id[4][10]]
        elif self.sides == 4:
            r_row[2] = [self.id[1][1], self.id[2][4], self.id[3][8], self.id[4][13],self.id[5][18]]
            r_row[3] = [self.id[2][3], self.id[3][7], self.id[4][12],self.id[5][17]]
            r_row[4] = [self.id[3][6], self.id[4][11], self.id[5][16]]
            r_row[5] = [self.id[4][12], self.id[5][15]]
        elif self.sides == 5:
            r_row[2] = [self.id[1][1], self.id[2][4], self.id[3][8], self.id[4][13], self.id[5][19], self.id[6][25]]
            r_row[3] = [self.id[2][3], self.id[3][7], self.id[4][12], self.id[5][18], self.id[6][24]]
            r_row[4] = [self.id[3][6], self.id[4][11], self.id[5][17], self.id[6][23]]
            r_row[5] = [self.id[4][12], self.id[5][16], self.id[6][22]]
            r_row[6] = [self.id[5][15], self.id[6][21]]
        if len(self.l) == self.sides+1:
            if r_row[row].count(1) >= len(r_row[row]) / 2 \
                    and self.r[row - 1] == '@':
                self.r[row - 1] = 1
            elif r_row[row].count(2) >= len(r_row[row]) / 2 \
                    and self.r[row - 1] == '@':
                self.r[row - 1] = 2
        return self.r[row-1]

    def uley_line(self, row):
        u_row = {}
        u_row[1] = [self.id[1 + i][sum([c + 1 for c in range(0, 1 + i)])] for i in range(0, self.sides)]
        if self.sides == 1:
            u_row[2] =[self.id[1][2],self.id[2][3]]
        elif self.sides == 2:
            u_row[2] = [self.id[1][2],self.id[2][4],self.id[3][6]]
            u_row[3] = [self.id[2][5],self.id[3][7]]
        elif self.sides == 3:
            u_row[2] = [self.id[1][2],self.id[2][4],self.id[3][7],self.id[4][10]],
            u_row[3] = [self.id[2][5],self.id[3][8],self.id[4][11]]
            u_row[4] = [self.id[3][9],self.id[4][12]]
        elif self.sides == 4:
            u_row[2] = [self.id[1][2], self.id[2][4], self.id[3][7], self.id[4][11],self.id[5][15]],
            u_row[3] = [self.id[2][5], self.id[3][8], self.id[4][12],self.id[5][16]]
            u_row[4] = [self.id[3][9], self.id[4][13], self.id[5][17]]
            u_row[5] = [self.id[4][14], self.id[5][18]]
        elif self.sides == 5:
            u_row[2] = [self.id[1][2], self.id[2][4], self.id[3][7], self.id[4][11], self.id[5][16], self.id[6][21]],
            u_row[3] = [self.id[2][5], self.id[3][8], self.id[4][12], self.id[5][17], self.id[6][22]]
            u_row[4] = [self.id[3][9], self.id[4][13], self.id[5][18], self.id[6][23]]
            u_row[5] = [self.id[4][14], self.id[5][19], self.id[6][24]]
            u_row[6] = [self.id[5][20], self.id[6][25]]
        if len(self.l) == self.sides + 1:
            if u_row[row].count(1) >= len(u_row[row]) / 2 \
                    and self.u[row - 1] == '@':
                self.u[row - 1] = 1
            elif u_row[row].count(2) >= len(u_row[row]) / 2 \
                    and self.u[row - 1] == '@':
                self.u[row - 1] = 2
        return self.u[row - 1]

    def is_over(self):
        """
        Return whether or not this game is over at state.
        """
        l_line = [self.l, self.r, self.u]
        total = sum(l_line, [])
        if total.count(1) >= len(total) / 2:
            return True
        elif total.count(2) >= len(total) / 2:
            return True
        elif '@' not in total:
            return True
        return False

    def get_possible_moves(self) -> list:
        """
    Return all possible moves that can be applied to this state.
    """
        moves = []
        for letters in self.id.values():
            for letter in letters.values():
                if str(letter).isalpha() and not self.is_over():
                    moves.append(letter)
        return moves

    def get_current_player_name(self) -> str:
        """
    Return 'p1' if the current player is Player 1, and 'p2' if the current
    player is Player 2.
    """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: Any) -> 'StonehengeState':
        """
    Return the GameState that results from applying move to this GameState.
    """
        new_id = copy.deepcopy(self.id)
        for row, letters in new_id.items():
            for digit, letter in letters.items():
                if letter == move:
                    new_id[row][digit] = int(self.get_current_player_name().replace('p', ''))
        new_state = StonehengeState(not self.p1_turn,
                                    self.sides, new_id, self.u.copy(), self.l.copy(), self.r.copy())
        for i in range(1, new_state.sides+2):
            new_state.uley_line(i)
            new_state.lley_line(i)
            new_state.rley_line(i)
        return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
    Return whether move is a valid move for this GameState.
    """
        return move in self.get_possible_moves()

    def __repr__(self) -> Any:
        """
    Return a representation of this state (which can be used for
    equality testing).
    """
        return 'The current state of the game is:\n' \
               + self.__str__() \
               + "\n The current player is {}".format(self.get_current_player_name())

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        if not self.get_possible_moves():
            return -1
        else:
            for i in self.get_possible_moves():
                ultra_state = self.make_move(i)
                if not ultra_state.get_possible_moves():
                    return 1
                for u in ultra_state.get_possible_moves():
                    ter_state = ultra_state.make_move(u)
                    if not ter_state.get_possible_moves():
                        return -1
        return 0
