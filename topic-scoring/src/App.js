import { useState } from 'react';

export default function ScoresApp() {
  const [input, setInput] = useState('');
  const [results, setResults] = useState([]);
  const [sortBy, setSortBy] = useState('order');

  // Llamada a la API
  const handleSubmit = async (e) => {
  e.preventDefault();
  // esta vacio?
  if (!input.trim()) return;
    // try catch para evitar crasheos
  try {
    const response = await fetch("http://127.0.0.1:8000/ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input }),
    });

    if (!response.ok) throw new Error("Request failed");
    const data = await response.json();

    setResults((prev) => [...prev, data]);
  } catch (err) {
    console.error("Error:", err);
    alert("Backend not reachable or error in response");
  } finally {
    setInput('');
  }
};


  // sort
  const getSortedResults = () => {
    const sorted = [...results];
    
    if (sortBy === 'order') {
      return sorted; // por queue
    }
    
    // Sort por array
    const index = parseInt(sortBy);
    return sorted.sort((a, b) => {
      const scoreA = a.scores[index] ?? 0;
      const scoreB = b.scores[index] ?? 0;
      return scoreB - scoreA; // High to low
    });
  };

  const sortedResults = getSortedResults();

  return (
    <div >
      <div >
        <h1 >Scores Dashboard</h1>
        
        <div >
          <div >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
              placeholder="Enter your input..."
              
            />
            <button
              onClick={handleSubmit}
              
            >
              Submit
            </button>
          </div>
        </div>

        {results.length > 0 && (
          <div >
            <label >Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              
            >
              <option value="order">First-Come-First-Served</option>
              <option value="0">Score [0]</option>
              <option value="1">Score [1]</option>
              <option value="2">Score [2]</option>
              <option value="3">Score [3]</option>
              <option value="4">Score [4]</option>
            </select>
          </div>
        )}

        <div >
          {sortedResults.length === 0 ? (
            <div >
              No results yet. Submit an input to get started!
            </div>
          ) : (
            sortedResults.map((result, idx) => {

              
              return (
                <div 
                  key={result.timestamp} 
                  
                  style={{
                    transform: 'translateY(0)',
                    opacity: 1
                  }}
                >
                  <div >
                    <div>
                      <h3 >Input: {result.input}</h3>
                      <p >
                        Submitted: {new Date(result.timestamp).toLocaleTimeString()}
                      </p>
                    </div>

                  </div>
                  
                  <div >
                    {result.scores.map((score, i) => (
                      <div
                        key={i}
                        
                      >
                        {score}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}