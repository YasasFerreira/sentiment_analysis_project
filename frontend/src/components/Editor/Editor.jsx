import React, { useState } from "react";
import "./Editor.css";
import robot from "../../assets/robot.png";

const Editor = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!text.trim()) {
      alert("Please enter some text!");
      return;
    }

    setLoading(true);
    setResult("");

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.sentiment); // Correct field from Flask
    } catch (error) {
      console.error("Error:", error);
      setResult("Error connecting to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="editor-container">
      <div className="editor-left">
        <img src={robot} alt="Robot" />
      </div>

      <div className="editor-right">
        <form onSubmit={handleSubmit}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={10}
            placeholder="Type your tweet..."
          />
          <br />
          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </form>
        {result && <p className="result-text">Sentiment: {result}</p>}
      </div>
    </div>
  );
};

export default Editor;
