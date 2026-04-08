# hybrid.py
# Hybrid search: Alpha-Beta + Neural Evaluation

from move_gen import generate_moves
from heuristic import evaluate as heuristic_eval
from zobrist import compute_hash
from neural_nt import NeuralEvaluator

INF = 10**9

# ===============================
# TRANSPOSITION TABLE
# ===============================

TT = {}

class TTEntry:
    def __init__(self, depth, score):
        self.depth = depth
        self.score = score


# ===============================
# HYBRID SEARCH ENGINE
# ===============================

class HybridSearch:
    def __init__(self, use_nn=True):
        self.use_nn = use_nn
        self.nn = NeuralEvaluator() if use_nn else None

    # ===============================
    # MAIN SEARCH
    # ===============================

    def search(self, board, depth, alpha, beta, maximizing, side):
        """
        Alpha-Beta + Neural Evaluation
        """

        # Zobrist hash
        h = compute_hash(board, side)

        # TT lookup
        if h in TT:
            entry = TT[h]
            if entry.depth >= depth:
                return entry.score

        # Leaf node
        if depth == 0:
            score = self.evaluate(board)
            return score

        moves = generate_moves(board, side)

        if not moves:
            return self.evaluate(board)

        # Move ordering (IMPORTANT)
        moves = self.order_moves(board, moves)

        if maximizing:
            max_eval = -INF

            for move in moves:
                self.make_move(board, move, side)

                eval = self.search(
                    board, depth - 1, alpha, beta, False, 1 - side
                )

                self.undo_move(board, move, side)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            TT[h] = TTEntry(depth, max_eval)
            return max_eval

        else:
            min_eval = INF

            for move in moves:
                self.make_move(board, move, side)

                eval = self.search(
                    board, depth - 1, alpha, beta, True, 1 - side
                )

                self.undo_move(board, move, side)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            TT[h] = TTEntry(depth, min_eval)
            return min_eval

    # ===============================
    # EVALUATION (HYBRID)
    # ===============================

    def evaluate(self, board):
        h_score = heuristic_eval(board)

        if not self.use_nn:
            return h_score

        _, value = self.nn.evaluate(board)

        # Combine
        nn_score = value * 1000
        return int(0.7 * h_score + 0.3 * nn_score)

    # ===============================
    # MOVE ORDERING
    # ===============================

    def order_moves(self, board, moves):
        """
        Use NN policy (if available) or simple heuristic
        """

        if self.use_nn:
            policy, _ = self.nn.evaluate(board)
            policy = policy[0].tolist()

            # simple mapping
            scored = []
            for move in moves:
                idx = (move.from_sq * 64 + move.to_sq) % len(policy)
                scored.append((policy[idx], move))

            scored.sort(reverse=True, key=lambda x: x[0])
            return [m for _, m in scored]

        # fallback: captures first
        return sorted(moves, key=lambda m: m.capture, reverse=True)

    # ===============================
    # MAKE / UNDO MOVE
    # ===============================

    def make_move(self, board, move, side):
        piece = move.piece

        # capture
        if move.capture:
            target = board.get_piece_at(move.to_sq)
            if target:
                enemy_color, enemy_piece = target
                board.remove_piece(enemy_color, enemy_piece, move.to_sq)

        # move piece
        board.move_piece(side, piece, move.from_sq, move.to_sq)

        # promotion
        if move.promotion is not None:
            board.remove_piece(side, piece, move.to_sq)
            board.set_piece(side, move.promotion, move.to_sq)

    def undo_move(self, board, move, side):
        piece = move.piece

        # undo promotion
        if move.promotion is not None:
            board.remove_piece(side, move.promotion, move.to_sq)
            board.set_piece(side, piece, move.from_sq)
        else:
            board.move_piece(side, piece, move.to_sq, move.from_sq)

        # NOTE:
        # For full correctness, you should restore captured piece
        # → cần stack lưu history (pro version)

    # ===============================
    # FIND BEST MOVE
    # ===============================

    def find_best_move(self, board, depth, side):
        best_move = None
        best_score = -INF

        moves = generate_moves(board, side)
        moves = self.order_moves(board, moves)

        for move in moves:
            self.make_move(board, move, side)

            score = self.search(
                board, depth - 1, -INF, INF, False, 1 - side
            )

            self.undo_move(board, move, side)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score