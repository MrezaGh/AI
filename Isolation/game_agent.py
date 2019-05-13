"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
from random import randint


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves - 2*opp_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=15.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):

        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -1, -1
        score, max_move = max([(self.min_value(game.forecast_move(move), depth - 1), move) for move in legal_moves])
        return max_move

    def max_value(self, game, depth):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            if game.is_winner(game.active_player):
                return float('inf')
            else:
                return float('-inf')
        if depth == 0:
            return self.score(game, game.active_player)

        score = max([self.min_value(game.forecast_move(move), depth - 1) for move in legal_moves])
        return score

    def min_value(self, game, depth):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            if game.is_winner(game.inactive_player):
                return float('inf')
            else:
                return float('-inf')
        if depth == 0:
            return self.score(game, game.inactive_player)

        score = min([self.max_value(game.forecast_move(move), depth - 1) for move in legal_moves])
        return score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        current_depth = 0
        try:
            while True:
                current_depth += 1
                score, best_move = self.alphabeta(game, current_depth)
                if score == float('inf'):
                    return best_move
                if self.time_left() < self.TIMER_THRESHOLD:
                    # print("explosion: {}".format(self.time_left()))
                    raise SearchTimeout()

        except SearchTimeout:
            # print("depth reached: {}".format(current_depth))
            # print(self.time_left())
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print("alpha beta : {}".format(self.time_left()))
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float('-inf'), (-1, -1)

        max_score = float('-inf')
        best_move = (-1, -1)
        for move in legal_moves:
            value = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if value > max_score:
                max_score = value
                best_move = move
                alpha = max_score

        if best_move == (-1, -1):  # we probably loose no matter what
            # print("for spartaaaaa!")  # todo
            # if the opponent plays like us we loose no matter what
            # but instead of surrendering we fight and we choose a random move (for sprataaaa!)
            return max_score, legal_moves[randint(0, len(legal_moves) - 1)]  # IDK why but legal_move[0] is better

        return max_score, best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print("max value: {}".format(self.time_left()))
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            if game.is_winner(game.active_player):
                return float('inf')
            else:
                return float('-inf')
        if depth == 0:
            return self.score(game, game.active_player)

        max_score = float('-inf')
        for move in legal_moves:
            max_score = max(max_score, self.min_value(game.forecast_move(move), depth - 1, alpha, beta))
            if max_score >= beta:
                return max_score
            alpha = max(max_score, alpha)

        return max_score

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print("min value : {}".format(self.time_left()))
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            if game.is_winner(game.inactive_player):
                return float('inf')
            else:
                return float('-inf')
        if depth == 0:
            return self.score(game, game.inactive_player)

        min_score = float('inf')
        for move in legal_moves:
            min_score = min(min_score, self.max_value(game.forecast_move(move), depth - 1, alpha, beta))
            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)

        return min_score

