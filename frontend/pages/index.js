export default function Home() {
  const machines = [
    { name: "Dragon Link #24", heat: 80 },
    { name: "Lightning Link #11", heat: 55 },
    { name: "Buffalo Gold #6", heat: 20 }
  ];

  return (
    <div style={{padding:20}}>
      <h1>🔥 Slot Machine Heat Map</h1>
      {machines.map((m,i)=>(
        <div key={i} style={{marginBottom:10}}>
          <strong>{m.name}</strong>
          <div style={{background:"#eee",height:10}}>
            <div style={{
              width: m.heat+"%",
              height:10,
              background: m.heat>70?"red":m.heat>40?"orange":"blue"
            }}/>
          </div>
        </div>
      ))}
    </div>
  );
}
const uploadImage = async (e) => {
  const file = e.target.files[0];

  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(API + "/detect", {
    method: "POST",
    body: formData
  });
<input
  type="number"
  placeholder="Win Amount"
  value={win}
  onChange={(e) => setWin(e.target.value)}
/>
  const data = await res.json();
  alert(JSON.stringify(data));
};
<input type="file" onChange={uploadImage} />
const wsProtocol = API.startsWith("https") ? "wss" : "ws";
const ws = new WebSocket(API.replace(/^https?/, wsProtocol) + "/ws");
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
<input
  type="number"
  placeholder="Win Amount"
  value={win}
  onChange={(e) => setWin(e.target.value)}
/>
<input
  placeholder="Machine Name"
  value={machine}
  onChange={(e) => setMachine(e.target.value)}
/>
    const [machineList, setMachineList] = useState([]);
fetch(API + "/machine-list")
  .then(res => res.json())
  .then(setMachineList);
<select
  value={machine}
  onChange={(e) => setMachine(e.target.value)}
>
  <option value="">Select Machine</option>
  {machineList.map((m, i) => (
    <option key={i} value={m}>
      {m}
    </option>
  ))}
</select>
const submitSpin = async () => {
  if (!machine) {
    alert("Please select a machine");
    return;
  }

  await fetch(API + "/spin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      machine,
      win: Number(win),
      bonus
    })
  });

  setMachine("");
  setWin(0);
  setBonus(false);
};
