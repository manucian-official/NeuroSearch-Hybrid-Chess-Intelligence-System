# neural_nt.py
# Neural Network Evaluation for Chess Engine

import torch
import torch.nn as nn
import torch.nn.functional as F

from bitboard import (
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
)

# ===============================
# CONFIG
# ===============================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

NUM_CHANNELS = 12  # 6 pieces x 2 colors
BOARD_SIZE = 8


# ===============================
# BOARD ENCODING
# ===============================

def encode_board(board):
    """
    Convert Bitboard -> tensor (12 x 8 x 8)
    """

    tensor = torch.zeros((NUM_CHANNELS, 8, 8), dtype=torch.float32)

    for color in (WHITE, BLACK):
        for piece in range(6):
            bb = board.pieces[color][piece]

            while bb:
                sq = (bb & -bb).bit_length() - 1
                bb &= bb - 1

                row = sq // 8
                col = sq % 8

                channel = piece + (0 if color == WHITE else 6)
                tensor[channel][row][col] = 1.0

    return tensor


# ===============================
# MODEL
# ===============================

class ChessNet(nn.Module):
    def __init__(self):
        super().__init__()

        # Convolution layers
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, padding=1)

        # Policy head (move probabilities)
        self.policy_conv = nn.Conv2d(128, 32, kernel_size=1)
        self.policy_fc = nn.Linear(32 * 8 * 8, 4672)  
        # 4672 ≈ max legal moves encoding

        # Value head (position evaluation)
        self.value_conv = nn.Conv2d(128, 32, kernel_size=1)
        self.value_fc1 = nn.Linear(32 * 8 * 8, 128)
        self.value_fc2 = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # Policy
        p = F.relu(self.policy_conv(x))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)

        # Value
        v = F.relu(self.value_conv(x))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))

        return p, v


# ===============================
# EVALUATION FUNCTION
# ===============================

class NeuralEvaluator:
    def __init__(self, model_path=None):
        self.model = ChessNet().to(DEVICE)

        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=DEVICE))

        self.model.eval()

    def evaluate(self, board):
        """
        Returns:
        - value: [-1, 1]
        - policy: move probabilities
        """

        with torch.no_grad():
            x = encode_board(board).unsqueeze(0).to(DEVICE)

            policy, value = self.model(x)

            policy = F.softmax(policy, dim=1)
            value = value.item()

        return policy, value