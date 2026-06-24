import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

const API_BASE = "http://localhost:8000";

function App() {
  const [requestRecipe, setRequestRecipe] = useState("");
  const [responseRecipe, setResponseRecipe] = useState("");

  function handleChange(e) {
    // console.log(e.target.value);
    setRequestRecipe(e.target.value);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    console.log(requestRecipe);

    // 1. Send the request to the backend
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: requestRecipe,
      }),
    });

    // 2. Parse the readable stream into actual JSON data
    const data = await res.json();

    console.log(data.output);
    // This will log: { output: "The AI's actual response text" }
    // .output is the key that contains the AI's response text !!!!!!!!!
    // Changes from object to string

    if (!data.output) {
      console.error("Error: data.output is missing or empty");
      return;
    }
    setResponseRecipe(data.output);

    // 3. (Optional) Typically you would save this to state here:
    // setAiResponse(data.output);
  }

  // console.log("AI Response:", responseRecipe);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Enter your recipe request:
          <input type="text" value={requestRecipe} onChange={handleChange} />
        </label>
        <input type="submit" />
      </form>
      <textarea value={responseRecipe}/>
    </div>
  );
}

export default App;
