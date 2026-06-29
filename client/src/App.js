import "./App.css";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

const API_BASE = "http://localhost:8000";

// --- 1. NEW ANALYSIS PAGE COMPONENT ---
function Analysis({ourRequestRecipe, ourResponseRecipe}) {
    console.log("hello", ourRequestRecipe);
    console.log("hellooo", ourResponseRecipe);
    return (
    <div className="analysis-container">
      <h2>Recipe Insights & Analysis</h2>
      <p>This is your new /analysis route! You can display your cooking trends, history, or metrics here.</p>
      <Link to="/" className="nav-link">← Back to Generator</Link>
    </div>
  );
}

// --- 2. YOUR ORIGINAL RECIPE GENERATOR ---
function RecipeGenerator() {
  const [requestRecipe, setRequestRecipe] = useState("");
  const [responseRecipe, setResponseRecipe] = useState("");

  function handleChange(e) {
    setRequestRecipe(e.target.value);
  }

  async function handleSubmit(e) {
    e.preventDefault();

    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: requestRecipe,
      }),
    });

    const data = await res.json();

    if (!data.output) {
      console.error("Error: data.output is missing or empty");
      return;
    }
    setResponseRecipe(data.output);
  }

  return (
    <div>
      <div className="nav-header">
        <Link to="/analysis" className="nav-link">Go to Analysis →</Link>
      </div>

      <form onSubmit={handleSubmit}>
        <label>
          Enter your recipe request:
          <input
            type="text"
            value={requestRecipe}
            onChange={handleChange}
            placeholder="e.g., Spicy garlic chicken pasta"
          />
        </label>
        <input type="submit" value="Generate Recipe" />
      </form>

      {responseRecipe && <div className="recipe-output">{responseRecipe}</div>}
    </div>
  );
}

// --- 3. MAIN APP ROOT WITH ROUTING ---
function App() {
  // 1. Lift the states up to the parent App component
  const [requestRecipe, setRequestRecipe] = useState("");
  const [responseRecipe, setResponseRecipe] = useState("");

  return (
    <Router>
      <Routes>
        {/* Main Route: Pass the state and setters down as props */}
        <Route 
          path="/" 
          element={
            <RecipeGenerator 
              requestRecipe={requestRecipe}
              setRequestRecipe={setRequestRecipe}
              responseRecipe={responseRecipe}
              setResponseRecipe={setResponseRecipe}
            />
          } 
        />
        
        {/* Your New Analysis Route: Receives the data seamlessly */}
        <Route 
          path="/analysis" 
          element={
            <Analysis 
              ourRequestRecipe={requestRecipe}
              ourResponseRecipe={responseRecipe}
            />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;