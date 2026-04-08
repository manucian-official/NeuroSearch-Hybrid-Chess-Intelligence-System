import { Chessboard } from "react-chessboard";
import { useState } from "react";
import axios from "axios";

export default function ChessBoard() {
  const [fen, setFen] = useState("start");
  const [bestMove, setBestMove] = useState(null);

  const analyze = async () => {
    const res = await axios.post("http://127.0.0.1:8000/analyze", {
      fen: fen,
      engine: "hybrid",
      depth: 3
    });

    setBestMove(res.data.best_move);
  };

  return (
    <div>
      <Chessboard position={fen} />

      <button onClick={analyze}>
        Analyze
      </button>

      {bestMove && <p>Best Move: {bestMove}</p>}
    </div>
  );
}