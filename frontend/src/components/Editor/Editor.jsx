import React, { useState } from "react";
import "./Editor.css";

const Editor = () => {
  const [text, setText] = useState("");            
  const [result, setResult] = useState("");       
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!text.trim()) {
      alert("Please enter some text!");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setResult(data.prediction); 
    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to server");
    }
  };

  return (
    <div className="editor-container">
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}  
          rows={5}
          cols={50}
          placeholder="Type your sentence..."
        />
        <br />
        <button type="submit" style={{ marginTop: "10px" }}>
          Analyze
        </button>
      </form>

      {result && (
        <p style={{ marginTop: "15px", fontWeight: "bold" }}>
          Sentiment: {result}
        </p>
      )}
    </div>
  );
};

export default Editor;
