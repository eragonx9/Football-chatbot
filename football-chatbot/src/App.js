import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async () => {
    if (!query.trim()) return;
    
    const newMessages = [...messages, { text: query, sender: 'user' }];
    setMessages(newMessages);

    try {
      const response = await fetch('http://localhost:5000/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessages([...newMessages, { text: data.text, sender: 'bot' }]);
    } catch (error) {
      console.error("Error fetching data: ", error);
      setMessages([...newMessages, { text: "There was an error processing your request.", sender: 'bot' }]);
    }

    setQuery('');
  };

  const renderMessageText = (text) => {
    return text.split('\n').map((line, index) => (
      <p key={index} className="message">{line}</p>
    ));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Football Chatbot</h1>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-card ${msg.sender}`}>
              <div className="message-text">
                {renderMessageText(msg.text)}
              </div>
            </div>
          ))}
        </div>
        <div className="input-container">
          <input 
            type="text" 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            placeholder="Ask me about football..." 
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
