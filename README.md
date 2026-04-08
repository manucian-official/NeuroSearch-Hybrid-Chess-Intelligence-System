<div align="center">

<h1>♟️ NeuroSearch Hybrid Chess Intelligence System</h1>

<p>
A High-Performance Bitboard-Based Engine Integrating Alpha-Beta Pruning, Monte Carlo Tree Search, Zobrist Hashing, and Deep Neural Network Evaluation
</p>

<p>
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Framework-FastAPI-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/AI-PyTorch-red?style=for-the-badge" />
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

<p>
<strong>🚀 A Research-Grade Hybrid Chess AI System Combining Classical Search and Deep Learning</strong>
</p>

</div>

---

<h2>🧠 Overview</h2>

<p>
NeuroSearch is a high-performance, research-oriented chess engine designed to bridge the gap between classical algorithmic search techniques and modern neural network-based AI systems. The project combines deterministic search algorithms with probabilistic exploration and deep learning-based evaluation, forming a hybrid architecture inspired by state-of-the-art systems.
</p>

<p>
This engine is built upon a highly optimized bitboard representation, enabling efficient low-level computation through 64-bit operations. It integrates multiple advanced techniques, including Alpha-Beta pruning, Monte Carlo Tree Search (MCTS), and neural policy-value evaluation, making it a powerful platform for experimentation in artificial intelligence and game theory.
</p>

---

<h2>⚡ Key Features</h2>

<ul>
<li>🚀 High-performance bitboard-based chess engine</li>
<li>🧠 Hybrid AI: Classical search + Neural network evaluation</li>
<li>♟️ Multiple search engines (Minimax, Hybrid, MCTS)</li>
<li>📊 Real-time analysis via REST API</li>
<li>🌐 Interactive React-based frontend</li>
<li>🔬 Research-ready architecture for experimentation</li>
</ul>

---

<h2>🔬 Core Algorithms & Techniques</h2>

<ul>
<li><strong>Bitboard Representation</strong> – Efficient 64-bit board encoding</li>
<li><strong>Minimax Algorithm</strong> with Alpha-Beta Pruning</li>
<li><strong>Quiescence Search</strong> for tactical stability</li>
<li><strong>Monte Carlo Tree Search (MCTS)</strong></li>
<li><strong>Zobrist Hashing</strong> for transposition tables</li>
<li><strong>Move Ordering Heuristics</strong></li>
<li><strong>Deep Convolutional Neural Networks</strong></li>
<li><strong>Residual Blocks Architecture</strong></li>
<li><strong>Policy-Value Network (AlphaZero-style)</strong></li>
<li><strong>Supervised Learning from PGN datasets</strong></li>
</ul>

---

<h2>🏗️ System Architecture</h2>

<pre>
                +----------------------+
                |   React Frontend     |
                |  (Chessboard UI)     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |     FastAPI API      |
                |  (Inference Layer)   |
                +----------+-----------+
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
+---------------+                   +-------------------+
| Hybrid Engine |                   |   MCTS Engine     |
| (Alpha-Beta + |                   | (Neural Guided)   |
| Neural Eval)  |                   +-------------------+
+---------------+
        |
        v
+----------------------+
| Neural Network Model |
| (Policy + Value)     |
+----------------------+
</pre>

---

<h2>📁 Project Structure</h2>

<pre>
NeuroSearch/
│
├── backend/
│   ├── bitboard.py
│   ├── move_gen.py
│   ├── minimax.py
│   ├── hybrid.py
│   ├── mcts.py
│   ├── zobrist.py
│   ├── heuristic.py
│   ├── neural_nt.py
│   ├── model.py
│   ├── dataset.py
│   ├── training.py
│   └── fastapi_app.py
│
├── frontend/
│   └── react-app/
│
├── experiments/
├── benchmarks/
├── docs/
└── README.md
</pre>

---

<h2>🚀 Getting Started</h2>

<h3>1. Clone Repository</h3>

<pre>
git clone https://github.com/your-username/neurosearch.git
cd neurosearch
</pre>

<h3>2. Backend Setup</h3>

<pre>
pip install -r requirements.txt
uvicorn fastapi_app:app --reload
</pre>

<h3>3. Frontend Setup</h3>

<pre>
cd frontend/react-app
npm install
npm start
</pre>

---

<h2>📡 API Endpoints</h2>

<table>
<tr>
<th>Endpoint</th>
<th>Method</th>
<th>Description</th>
</tr>
<tr>
<td>/analyze</td>
<td>POST</td>
<td>Returns best move using selected engine</td>
</tr>
<tr>
<td>/evaluate</td>
<td>POST</td>
<td>Returns evaluation score</td>
</tr>
</table>

---

<h2>🧠 Neural Network</h2>

<p>
The neural network follows a policy-value architecture inspired by modern reinforcement learning systems. It consists of a deep convolutional backbone with residual connections, enabling effective feature extraction from board states.
</p>

<ul>
<li>Input: 12-channel board tensor</li>
<li>Policy Head: Move probability distribution</li>
<li>Value Head: Position evaluation (-1 to 1)</li>
</ul>

---

<h2>📊 Training Pipeline</h2>

<pre>
PGN Dataset → DataLoader → Neural Network → Loss Function → Backpropagation
</pre>

<p>
Supports supervised learning from real game data and can be extended to self-play reinforcement learning.
</p>

---

<h2>🎯 Future Improvements</h2>

<ul>
<li>⚡ GPU-accelerated MCTS</li>
<li>🧠 Self-play reinforcement learning loop</li>
<li>📊 Advanced evaluation metrics</li>
<li>🌐 WebSocket real-time analysis</li>
<li>🎨 Enhanced UI (drag, arrows, animations)</li>
</ul>

---

<h2>🤝 Contributing</h2>

<p>
Contributions are welcome! Feel free to open issues or submit pull requests for improvements, optimizations, or new features.
</p>

---

<h2>📜 License</h2>

<p>
This project is licensed under the MIT License.
</p>

---

<div align="center">

<h3>🔥 Built for AI, Performance, and Innovation</h3>

<p>
If you like this project, give it a ⭐ on GitHub!
</p>

</div>
