import { useState, useEffect, useMemo } from 'react';

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [machines, setMachines] = useState([]);
  const [machineList, setMachineList] = useState([]);
  const [wins, setWins] = useState([]);
  const [machine, setMachine] = useState('');
  const [win, setWin] = useState(0);
  const [bonus, setBonus] = useState(false);

  const orderedMachines = useMemo(
    () => [...machines].sort((a, b) => b.heat - a.heat),
    [machines]
  );

  const loadData = async () => {
    const [machinesRes, listRes, winsRes] = await Promise.all([
      fetch(`${API}/machines`),
      fetch(`${API}/machine-list`),
      fetch(`${API}/recent-wins`),
    ]);

    const [machinesData, listData, winsData] = await Promise.all([
      machinesRes.json(),
      listRes.json(),
      winsRes.json(),
    ]);

    setMachines(machinesData);
    setMachineList(listData);
    setWins(winsData);
  };

  useEffect(() => {
    loadData();
  }, []);

  const submitSpin = async () => {
    if (!machine) {
      alert('Please select a machine');
      return;
    }

    await fetch(`${API}/spin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ machine, win: Number(win), bonus }),
    });

    setWin(0);
    setBonus(false);
    await loadData();
  };

  return (
    <div style={{ maxWidth: 880, margin: '0 auto', padding: 20, fontFamily: 'sans-serif' }}>
      <h1>🔥 Slot Machine Heat Map</h1>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
        <select value={machine} onChange={(e) => setMachine(e.target.value)}>
          <option value="">Select Machine</option>
          {machineList.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>

        <input
          type="number"
          placeholder="Win Amount"
          value={win}
          onChange={(e) => setWin(e.target.value)}
        />

        <label style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
          <input type="checkbox" checked={bonus} onChange={(e) => setBonus(e.target.checked)} />
          Bonus
        </label>

        <button onClick={submitSpin}>Log Spin</button>
      </div>

      <h2>Machines</h2>
      {orderedMachines.map((m) => (
        <div key={m.name} style={{ marginBottom: 10 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>{m.name}</strong>
            <span>{m.heat}%</span>
          </div>
          <div style={{ background: '#eee', height: 12, borderRadius: 6 }}>
            <div
              style={{
                width: `${m.heat}%`,
                height: 12,
                borderRadius: 6,
                background: m.heat > 70 ? '#dc2626' : m.heat > 40 ? '#f59e0b' : '#2563eb',
              }}
            />
          </div>
        </div>
      ))}

      <h2 style={{ marginTop: 28 }}>💰 Recent Wins</h2>
      {wins.length === 0 ? (
        <p>No wins yet.</p>
      ) : (
        wins.map((w, i) => (
          <div key={`${w.machine}-${i}`}>${w.win} - {w.machine}</div>
        ))
      )}
    </div>
  );
}
