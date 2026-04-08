export default function EvalBar({ score }) {
  const percent = Math.max(0, Math.min(100, 50 + score / 20));

  return (
    <div style={{ width: "40px", height: "300px", border: "1px solid black" }}>
      <div
        style={{
          height: `${percent}%`,
          background: "white"
        }}
      />
      <div
        style={{
          height: `${100 - percent}%`,
          background: "black"
        }}
      />
    </div>
  );
}