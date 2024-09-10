async function sendMessage() {
    const input = document.getElementById('input').value;
    if (!input.trim()) return;

    // Display user's message
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<div class="message user">${input}</div>`;

    // Call the backend to get the chatbot response
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: input })
        });

        const data = await response.json();
        const botResponse = data.response;
        
        // Display bot's response
        messagesDiv.innerHTML += `<div class="message bot">${botResponse}</div>`;
    } catch (error) {
        console.error('Error fetching chatbot response:', error);
        messagesDiv.innerHTML += `<div class="message bot">Error fetching response from the bot.</div>`;
    }

    // Clear input
    document.getElementById('input').value = '';
}
