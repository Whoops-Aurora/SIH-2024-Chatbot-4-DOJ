// Import Google Generative AI SDK
const { GoogleGenerativeAI } = require("@google/generative-ai");

// Set up API Key (use environment variable for security)
const genAI = new GoogleGenerativeAI("AIzaSyAi4RcPWCz6gP2dff23o65fXoi4a_9lXek");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// Function to send the question to Gemini API and return the response
const generateResponse = async (question) => {
  try {
    const result = await model.generateContent(question);
    
    // Extract the response text (from candidates array)
    const responseText = result.candidates[0].output || "No response generated.";
    
    return responseText;
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    throw new Error("Error generating content.");
  }
};

module.exports = { generateResponse };
