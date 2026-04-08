export default function ControlPanel({ onAnalyze }) {
  return (
    <div>
      <button onClick={onAnalyze}>Analyze Position</button>
    </div>
  );
}