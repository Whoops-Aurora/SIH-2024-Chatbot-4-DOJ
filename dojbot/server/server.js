const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const { generateResponse } = require("./geminiIntegration");

const app = express();
app.use(bodyParser.json());
app.use(cors());

// API route to handle chatbot questions
app.post("/api/chat", async (req, res) => {
  const { question } = req.body;

  try {
    // Get the response from Gemini API
    const botResponse = await generateResponse(question);
    
    // Send the response back to the frontend
    res.status(200).json({ response: botResponse });
  } catch (error) {
    console.error("Error generating response:", error);
    res.status(500).json({ response: "Error generating content." });
  }
});

// Start the server
const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
