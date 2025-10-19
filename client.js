let ws = null;
let clientId = null;

const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Auto-connect on page load
window.addEventListener('DOMContentLoaded', () => {
    connect();
});

function getOrCreateClientId() {
    // Check if client ID exists in localStorage
    let clientId = localStorage.getItem('chatClientId');

    if (!clientId) {
        // Generate a new unique ID
        clientId = 'client_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('chatClientId', clientId);
    }

    return clientId;
}

function connect() {
    clientId = getOrCreateClientId();
    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
        addMessage('System: Connected to server');

        // Send init message
        ws.send(JSON.stringify({
            type: 'init',
            client_id: clientId
        }));

        messageInput.disabled = false;
        sendBtn.disabled = false;
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'history') {
            addMessage('System: Loading message history...');
            data.messages.forEach(msg => {
                const sender = msg.sender === 'user' ? 'You' : 'System';
                addMessage(`${sender}: ${msg.content}`);
            });
        } else if (data.type === 'message') {
            addMessage(`System: ${data.message}`);
        } else if (data.type === 'error') {
            addMessage(`Error: ${data.message}`);
        }
    };

    ws.onerror = (error) => {
        addMessage('System: Connection error');
    };

    ws.onclose = () => {
        addMessage('System: Disconnected from server');
        resetUI();
    };
}

function sendMessage() {
    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    if (!ws || ws.readyState !== WebSocket.OPEN) {
        addMessage('System: Not connected to server');
        return;
    }

    ws.send(JSON.stringify({
        type: 'message',
        content: message
    }));

    addMessage(`You: ${message}`);
    messageInput.value = '';
}

function addMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.textContent = message;
    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function resetUI() {
    messageInput.disabled = true;
    sendBtn.disabled = true;
    ws = null;
}