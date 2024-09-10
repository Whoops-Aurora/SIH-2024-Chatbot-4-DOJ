import axios from "axios";

export const sendMessageToBot = (input) => {
  return axios.post("/api/chat", { question: input });
};
