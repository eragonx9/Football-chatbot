import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import backgroundImage from './images.jpg'; // Import background image

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
      <p key={index} className="mb-1">{line}</p>
    ));
  };

  return (
    <div className="App" style={{ backgroundImage: `url(${backgroundImage})`, color: 'white' }}>
      <header className="App-header">
        <h1 style={{ fontWeight: 'bold' }}>Football Chatbot</h1>
      </header>
      <div className="chat-container container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-card card mb-3 ${msg.sender}`}>
              <div className="card-body">
                <div className="d-flex">
                  <div className="message-icon">
                    {msg.sender === 'user' ? '🧑' : '🤖'}
                  </div>
                  <div className="message-text ml-2">
                    {renderMessageText(msg.text)}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="input-container input-group mt-3">
          <input 
            type="text" 
            value={query} 
            onChange={(e) => setQuery(e.target.value)} 
            className="form-control" 
            placeholder="Ask me about football..."
            style={{ backgroundColor: 'rgba(255, 255, 255, 0.1)', color: 'white' }} // Adjust input style
          />
          <div className="input-group-append">
            <button onClick={handleSendMessage} className="btn btn-primary">Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
