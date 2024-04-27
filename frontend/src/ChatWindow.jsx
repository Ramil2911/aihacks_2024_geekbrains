import React, { useState, useEffect } from 'react';
import './ChatWindow.css';

const ChatWindow = ({ chatId, chatName }) => {
  const [message, setMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);

  // Загрузка сообщений чата при выборе чата
  useEffect(() => {
    if (chatId) {
      const fetchMessages = async () => {
        try {
          const response = await fetch(`https://backend.example.com/chats/${chatId}/messages`);
          const data = await response.json();
          setChatMessages(data);
        } catch (error) {
          console.error('Ошибка при загрузке сообщений чата:', error);
        }
      };

      fetchMessages();
    }
  }, [chatId]);

  // Функция для отправки сообщения
  const sendMessage = async () => {
    try {
      if (message.trim() !== '') {
        // Отправляем сообщение на бэкенд
        await fetch(`https://backend.example.com/chats/${chatId}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: message }),
        });
        
        // Обновляем сообщения чата после отправки
        setChatMessages([...chatMessages, { text: message, fromServer: false }]);
        setMessage('');
      }
    } catch (error) {
      console.error('Ошибка при отправке сообщения:', error);
    }
  };

  return (
    <div className="chat-window-container">
      <div className="chat-header" style={{ backgroundColor: '#f0f0f0', padding: '10px', marginBottom: '10px' }}>
        <h2>{chatName}</h2>
      </div>
      <div className="chat-messages-container">
        {chatMessages.map((msg, index) => (
          <div key={index} className={`message ${msg.fromServer ? 'server-message' : 'user-message'}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="message-input">
        <input
          type="text"
          placeholder="Сообщение..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') sendMessage();
          }}
        />
        <button className="send-button" onClick={sendMessage}></button>
      </div>
    </div>
  );
};

export default ChatWindow;
