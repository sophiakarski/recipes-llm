import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

const API_BASE = "http://localhost:8000";

function App() {
  const [sophia, setSophia] = useState("");

  function handleChange(e) {
    // console.log(e.target.value);
    setSophia(e.target.value);
  }

async function handleSubmit(e) {
  e.preventDefault();
  console.log(sophia);

  // 1. Send the request to the backend
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: sophia,
    }),
  });

  // 2. Parse the readable stream into actual JSON data
  const data = await res.json();
  
  // This will log: { output: "The AI's actual response text" }
  console.log(data);
  
  // 3. (Optional) Typically you would save this to state here:
  // setAiResponse(data.output);
}

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Enter your recipe request:
        <input type="text" value={sophia} onChange={handleChange} />
      </label>
      <input type="submit" />
    </form>
  );
}

export default App;
