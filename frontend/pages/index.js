import { useState, useEffect } from 'react';

export default function Home() {
  const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsProtocol = API.startsWith('https') ? 'wss' : 'ws';

  const [casinos, setCasinos] = useState([]);
  const [casinoId, setCasinoId] = useState('');
  const [machines, setMachines] = useState([]);
  const [machine, setMachine] = useState('');
  const [win, setWin] = useState(0);
  const [bonus, setBonus] = useState(false);
  const [leaders, setLeaders] = useState([]);
  const [stats, setStats] = useState(null);
  const [admin, setAdmin] = useState(null);
  const [ws, setWs] = useState(null);

  // Load casinos on mount
  useEffect(() => {
    fetch(API + '/casinos')
      .then(res => res.json())
      .then(setCasinos)
      .catch(err => console.error('Failed to load casinos:', err));
  }, []);

  // Load machines when casino changes
  useEffect(() => {
    if (!casinoId) return;
    fetch(API + '/machines/' + casinoId)
      .then(res => res.json())
      .then(setMachines)
      .catch(err => console.error('Failed to load machines:', err));
  }, [casinoId]);

  // Load leaderboard
  useEffect(() => {
    fetch(API + '/leaderboard')
      .then(res => res.json())
      .then(setLeaders)
      .catch(err => console.error('Failed to load leaderboard:', err));
  }, []);

  // Load user stats
  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) return;
    fetch(API + '/user-stats/' + userId)
      .then(res => res.json())
      .then(setStats)
      .catch(err => console.error('Failed to load user stats:', err));
  }, []);

  // Load admin stats
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    fetch(API + '/admin/stats', {
      headers: { Authorization: 'Bearer ' + token }
    })
      .then(res => res.json())
      .then(setAdmin)
      .catch(err => console.error('Failed to load admin stats:', err));
  }, []);

  // WebSocket connection
  useEffect(() => {
    const wsUrl = API.replace(/^https?/, wsProtocol) + '/ws';
    const websocket = new WebSocket(wsUrl);

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'big_win') {
          alert(`💰 BIG WIN: $${data.amount} on ${data.machine}`);
        } else {
          setMachines(data);
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    websocket.onerror = (err) => console.error('WebSocket error:', err);
    websocket.onclose = () => console.log('WebSocket closed');

    setWs(websocket);

    return () => websocket.close();
  }, []);

  const submitSpin = async () => {
    if (!machine) {
      alert('Please select a machine');
      return;
    }

    try {
      await fetch(API + '/spin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ machine, win: Number(win), bonus })
      });
      setMachine('');
      setWin(0);
      setBonus(false);
    } catch (err) {
      console.error('Failed to submit spin:', err);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h1>🎰 Slot Machine Tracker</h1>

      {/* Casino Selection */}
      <div style={{ marginBottom: 20 }}>
        <h2>Select Casino</h2>
        <select
          value={casinoId}
          onChange={(e) => setCasinoId(e.target.value)}
          style={{ padding: 8, fontSize: 16 }}
        >
          <option value="">Select Casino</option>
          {casinos.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {/* Machine Heat Map */}
      {machines.length > 0 && (
        <div style={{ marginBottom: 20 }}>
          <h2>🔥 Machine Heat Map</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 10
          }}>
            {machines.map((m, i) => (
              <div
                key={i}
                style={{
                  padding: 20,
                  textAlign: 'center',
                  background: m.heat > 70 ? 'red' : m.heat > 40 ? 'orange' : 'blue',
                  color: 'white',
                  borderRadius: 8,
                  cursor: 'pointer'
                }}
                onClick={() => setMachine(m.name)}
              >
                <strong>{m.name}</strong>
                <br />
                {m.heat}%
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Spin Submission */}
      <div style={{ marginBottom: 20, border: '1px solid #ccc', padding: 15, borderRadius: 8 }}>
        <h2>Submit Spin</h2>
        <div style={{ marginBottom: 10 }}>
          <label>Machine: </label>
          <select
            value={machine}
            onChange={(e) => setMachine(e.target.value)}
            style={{ padding: 8, marginLeft: 10 }}
          >
            <option value="">Select Machine</option>
            {machines.map((m, i) => (
              <option key={i} value={m.name}>{m.name}</option>
            ))}
          </select>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Win Amount: </label>
          <input
            type="number"
            value={win}
            onChange={(e) => setWin(e.target.value)}
            placeholder="0"
            style={{ padding: 8, marginLeft: 10 }}
          />
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>
            <input
              type="checkbox"
              checked={bonus}
              onChange={(e) => setBonus(e.target.checked)}
            />
            {' '}Bonus Win
          </label>
        </div>
        <button
          onClick={submitSpin}
          style={{
            padding: '10px 20px',
            background: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer',
            fontSize: 16
          }}
        >
          Submit Spin
        </button>
      </div>

      {/* Leaderboard */}
      {leaders.length > 0 && (
        <div style={{ marginBottom: 20 }}>
          <h2>🏆 Top Machines</h2>
          {leaders.map((l, i) => (
            <div key={i} style={{ padding: 10, borderBottom: '1px solid #eee' }}>
              #{i + 1} <strong>{l.machine}</strong> — ${l.total}
            </div>
          ))}
        </div>
      )}

      {/* User Stats */}
      {stats && (
        <div style={{ marginBottom: 20, background: '#f0f0f0', padding: 15, borderRadius: 8 }}>
          <h2>👤 My Stats</h2>
          <p>Spins: <strong>{stats.spins}</strong></p>
          <p>Total Won: <strong>${stats.winnings}</strong></p>
        </div>
      )}

      {/* Admin Dashboard */}
      {admin && (
        <div style={{ marginBottom: 20, background: '#fff3cd', padding: 15, borderRadius: 8 }}>
          <h2>📊 Admin Dashboard</h2>
          <p>Users: <strong>{admin.users}</strong></p>
          <p>Spins Logged: <strong>{admin.spins}</strong></p>
          <p>Total Wins: <strong>${admin.total_wins}</strong></p>
        </div>
      )}
    </div>
  );
}
