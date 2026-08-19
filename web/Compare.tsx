import { useEffect, useState } from 'react';

type RunEvent = {
  agent_id: string;
  task_id: string;
  score: number;
  latency_ms: number;
  tool_calls: number;
  ts: number;
};

// Latest score per (agent, task), keyed "agent|task".
type Scores = Record<string, number>;

export function Compare({ url, left, right }: { url: string; left: string; right: string }) {
  const [scores, setScores] = useState<Scores>({});
  const [tasks, setTasks] = useState<string[]>([]);

  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (e) => {
      const ev: RunEvent = JSON.parse(e.data);
      if (ev.agent_id !== left && ev.agent_id !== right) return;
      setScores((prev) => ({ ...prev, [`${ev.agent_id}|${ev.task_id}`]: ev.score }));
      setTasks((prev) => (prev.includes(ev.task_id) ? prev : [...prev, ev.task_id]));
    };
    return () => ws.close();
  }, [url, left, right]);

  return (
    <table>
      <thead><tr><th>Task</th><th>{left}</th><th>{right}</th><th>Winner</th></tr></thead>
      <tbody>
        {tasks.map((t) => {
          const l = scores[`${left}|${t}`] ?? NaN;
          const r = scores[`${right}|${t}`] ?? NaN;
          const winner = l === r ? '=' : l > r ? left : right;
          return (
            <tr key={t}>
              <td>{t}</td><td>{l.toFixed(2)}</td><td>{r.toFixed(2)}</td><td>{winner}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
