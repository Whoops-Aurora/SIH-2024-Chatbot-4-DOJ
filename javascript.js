async function fetchLLMResponse(prompt) {
    try {
      const response = await fetch('http://localhost:1234/api/response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
  
      if (!response.ok) {
        throw new Error(`Failed to fetch LLM response: ${response.statusText}`);
      }
  
      const data = await response.json();
      return data.response;
    } catch (error) {
      console.error('Error fetching LLM response:', error);
      return null;
    }
  }
  
  // Example usage:
  const prompt = "What is the capital of France?";
  fetchLLMResponse(prompt)
    .then((response) => {
      console.log('LLM response:', response);
    })
    
    .catch((error) => {
      console.error('Error:', error);
    });