import { useEffect, useRef, useState } from 'react';

type RunEvent = {
  agent_id: string;
  task_id: string;
  score: number;
  latency_ms: number;
  tool_calls: number;
  ts: number;
};

type Row = { agent_id: string; n: number; mean: number };

export function Leaderboard({ url }: { url: string }) {
  const [rows, setRows] = useState<Record<string, Row>>({});
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    socketRef.current = ws;
    ws.onmessage = (e) => {
      const ev: RunEvent = JSON.parse(e.data);
      setRows((prev) => {
        const r = prev[ev.agent_id] ?? { agent_id: ev.agent_id, n: 0, mean: 0 };
        const n = r.n + 1;
        const mean = (r.mean * r.n + ev.score) / n; // running average
        return { ...prev, [ev.agent_id]: { ...r, n, mean } };
      });
    };
    return () => ws.close();
  }, [url]);

  const ranked = Object.values(rows).sort((a, b) => b.mean - a.mean);

  return (
    <table>
      <thead><tr><th>#</th><th>Agent</th><th>Runs</th><th>Mean score</th></tr></thead>
      <tbody>
        {ranked.map((row, i) => (
          <tr key={row.agent_id}>
            <td>{i + 1}</td><td>{row.agent_id}</td>
            <td>{row.n}</td><td>{row.mean.toFixed(3)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
