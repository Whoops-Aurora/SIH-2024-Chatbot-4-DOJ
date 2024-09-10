import React, { useState } from "react";
import { sendMessageToBot } from "../services/chatService";

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Display the user’s message
    const userMessage = { role: "user", content: input };
    setMessages([...messages, userMessage]);

    // Call the backend to get the chatbot response
    try {
      const response = await sendMessageToBot(input);
      const botResponse = response.data.response; // Get the response from the backend

      // Add the bot response to the messages
      const botMessage = { role: "bot", content: botResponse };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      const errorMessage = {
        role: "bot",
        content: "Error fetching response from the bot.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    // Clear input
    setInput("");
  };

  return (
    <div className="chatbot">
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask me something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
