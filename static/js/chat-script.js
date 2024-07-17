function sendMessage() {
    const chatBox = document.getElementById('chat-box');
    const chatInput = document.getElementById('chat-input');

    const message = chatInput.value.trim();
    if (message !== '') {
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.textContent = message;
        chatBox.appendChild(userMessage);

        chatInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        // Simulate bot response
        setTimeout(() => {
            const botMessage = document.createElement('div');
            botMessage.classList.add('message');
            botMessage.textContent = "Bot: " + message;
            chatBox.appendChild(botMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 500);
    }
}

document.getElementById('chat-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
