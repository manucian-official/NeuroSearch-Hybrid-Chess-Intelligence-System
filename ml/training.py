# model.py
# Advanced Chess Neural Network (Policy + Value)

import torch
import torch.nn as nn
import torch.nn.functional as F

# ===============================
# CONFIG
# ===============================

INPUT_CHANNELS = 12   # có thể nâng lên 13 (side-to-move)
BOARD_SIZE = 8
NUM_RES_BLOCKS = 6
NUM_FILTERS = 128
POLICY_SIZE = 4672  # max move space

# ===============================
# RESIDUAL BLOCK
# ===============================

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()

        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)

        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x

        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))

        x += residual
        x = F.relu(x)

        return x


# ===============================
# MAIN MODEL
# ===============================

class ChessModel(nn.Module):
    def __init__(self):
        super().__init__()

        # Input layer
        self.conv = nn.Conv2d(INPUT_CHANNELS, NUM_FILTERS, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(NUM_FILTERS)

        # Residual tower
        self.res_blocks = nn.Sequential(
            *[ResidualBlock(NUM_FILTERS) for _ in range(NUM_RES_BLOCKS)]
        )

        # ===============================
        # POLICY HEAD
        # ===============================
        self.policy_conv = nn.Conv2d(NUM_FILTERS, 32, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(32)
        self.policy_fc = nn.Linear(32 * 8 * 8, POLICY_SIZE)

        # ===============================
        # VALUE HEAD
        # ===============================
        self.value_conv = nn.Conv2d(NUM_FILTERS, 32, kernel_size=1)
        self.value_bn = nn.BatchNorm2d(32)
        self.value_fc1 = nn.Linear(32 * 8 * 8, 256)
        self.value_fc2 = nn.Linear(256, 1)

    def forward(self, x):
        # Input
        x = F.relu(self.bn(self.conv(x)))

        # Residual tower
        x = self.res_blocks(x)

        # ===============================
        # POLICY
        # ===============================
        p = F.relu(self.policy_bn(self.policy_conv(x)))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)

        # ===============================
        # VALUE
        # ===============================
        v = F.relu(self.value_bn(self.value_conv(x)))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))

        return p, v


# ===============================
# LOSS FUNCTION
# ===============================

class AlphaZeroLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, pred_policy, pred_value, target_policy, target_value):
        """
        pred_policy: logits
        target_policy: move index (Long)
        pred_value: [-1, 1]
        target_value: [-1, 1]
        """

        # Policy loss (cross entropy)
        policy_loss = F.cross_entropy(pred_policy, target_policy)

        # Value loss (MSE)
        value_loss = F.mse_loss(pred_value.squeeze(), target_value)

        return policy_loss + value_loss, policy_loss, value_loss


# ===============================
# MODEL UTILITIES
# ===============================

def create_model(device="cpu"):
    model = ChessModel().to(device)
    return model


def save_model(model, path):
    torch.save(model.state_dict(), path)


def load_model(model, path, device="cpu"):
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model