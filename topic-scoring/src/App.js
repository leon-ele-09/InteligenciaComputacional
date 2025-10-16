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
        <div class = "Headers">
          
          <div><h1 >Categorizacion de Topicos por BiLSTM</h1> <br /></div>
          <div><h2 >V0.1 : Categorizacion de Posts <strong> Positivos y Negativos</strong></h2> <br /></div>
          <div class = "postContainer" id = "title">
            Por : <br/>
            Eli Dominguez <br/>
            Alejandra Dominguez <br/>
            Alan Leon <br/>
          </div>
        </div>
        <div class = "inputPost">
          <div >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
              placeholder="Escribe el nuevo post..."
              
            />
            <button
              onClick={handleSubmit}
              
            >
              Procesar
            </button>
          </div>
        </div>

        {results.length > 0 && (
          <div class = "inputPost">
            <label >Ordenar por:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="order">First-Come-First-Served</option>
              <option value="0">Por Negatividad</option>
              <option value="1">Por positividad</option>
              
            </select>
          </div>
          
        )}

        <div >
          {sortedResults.length === 0 ? (
            <div class = "postContainer" style={{marginTop : '20px'}}>
              <div class = "postText"> Agrega una publicación para que el modelo la valore </div>
            </div>
          ) : (
            sortedResults.map((result, idx) => {

              
              return (
                <div class = "postContainer"
                  key={result.timestamp} 
                  
                  style={{
                    transform: 'translateY(0)',
                    opacity: 1
                  }}
                >
                  <div class = "postText">
                    <div>
                      <h3 >Input: {result.input}</h3>
                      <p >
                        Submitted: {new Date(result.timestamp).toLocaleTimeString()}
                      </p>
                    </div>

                  </div>
                  
                  <div class = "postText" >
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