import axios from "axios";

const API = "http://127.0.0.1:8000";

export const analyzePosition = async (fen) => {
  const res = await axios.post(`${API}/analyze`, {
    fen,
    engine: "hybrid",
    depth: 3
  });

  return res.data;
};