# mcts.py
# Monte Carlo Tree Search with Neural Network guidance

import math
import random
from copy import deepcopy

from move_gen import generate_moves
from neural_nt import NeuralEvaluator

C_PUCT = 1.4


# ===============================
# NODE
# ===============================

class MCTSNode:
    def __init__(self, board, parent=None, move=None, prior=0):
        self.board = board
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.value_sum = 0.0
        self.prior = prior

    def value(self):
        if self.visits == 0:
            return 0
        return self.value_sum / self.visits

    def is_leaf(self):
        return len(self.children) == 0


# ===============================
# MCTS
# ===============================

class MCTS:
    def __init__(self, simulations=100):
        self.simulations = simulations
        self.nn = NeuralEvaluator()

    # ===============================
    # SEARCH ENTRY
    # ===============================

    def search(self, root_board, side):
        root = MCTSNode(deepcopy(root_board))

        for _ in range(self.simulations):
            node = root
            board = deepcopy(root_board)
            current_side = side

            # 1. Selection
            while not node.is_leaf():
                node = self.select(node)
                self.apply_move(board, node.move, current_side)
                current_side = 1 - current_side

            # 2. Expansion + Evaluation
            value = self.expand_and_evaluate(node, board, current_side)

            # 3. Backpropagation
            self.backpropagate(node, value, current_side)

        return self.best_move(root)

    # ===============================
    # SELECTION
    # ===============================

    def select(self, node):
        best_score = -float("inf")
        best_child = None

        for child in node.children:
            ucb = self.ucb_score(node, child)

            if ucb > best_score:
                best_score = ucb
                best_child = child

        return best_child

    def ucb_score(self, parent, child):
        q = child.value()
        u = C_PUCT * child.prior * math.sqrt(parent.visits + 1) / (child.visits + 1)
        return q + u

    # ===============================
    # EXPANSION + NN EVAL
    # ===============================

    def expand_and_evaluate(self, node, board, side):
        moves = generate_moves(board, side)

        if not moves:
            return 0  # draw fallback

        policy, value = self.nn.evaluate(board)
        policy = policy[0].tolist()

        # Normalize priors
        priors = []
        for move in moves:
            idx = (move.from_sq * 64 + move.to_sq) % len(policy)
            priors.append(policy[idx])

        total = sum(priors) + 1e-8
        priors = [p / total for p in priors]

        # Create children
        for move, p in zip(moves, priors):
            child_board = deepcopy(board)
            self.apply_move(child_board, move, side)

            child = MCTSNode(child_board, parent=node, move=move, prior=p)
            node.children.append(child)

        return value

    # ===============================
    # BACKPROPAGATION
    # ===============================

    def backpropagate(self, node, value, side):
        while node is not None:
            node.visits += 1

            # flip value depending on perspective
            node.value_sum += value if side == 0 else -value

            node = node.parent
            side = 1 - side

    # ===============================
    # APPLY MOVE (simple)
    # ===============================

    def apply_move(self, board, move, side):
        piece = move.piece

        # capture
        if move.capture:
            target = board.get_piece_at(move.to_sq)
            if target:
                c, p = target
                board.remove_piece(c, p, move.to_sq)

        board.move_piece(side, piece, move.from_sq, move.to_sq)

        if move.promotion is not None:
            board.remove_piece(side, piece, move.to_sq)
            board.set_piece(side, move.promotion, move.to_sq)

    # ===============================
    # BEST MOVE
    # ===============================

    def best_move(self, root):
        best = max(root.children, key=lambda c: c.visits)
        return best.move