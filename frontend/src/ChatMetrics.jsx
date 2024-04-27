// ChatMetrics.jsx
import React, { useState, useEffect } from 'react';
import './ChatMetrics.css';

const ChatMetrics = ({ chatId }) => {
  const [metrics, setMetrics] = useState(null);

  // Загрузка метрик чата при выборе чата
  useEffect(() => {
    if (chatId) {
      const fetchMetrics = async () => {
        try {
          const response = await fetch(`https://backend.example.com/chats/${chatId}/metrics`);
          const data = await response.json();
          setMetrics(data);
        } catch (error) {
          console.error('Ошибка при загрузке метрик чата:', error);
        }
      };

      fetchMetrics();
    }
  }, [chatId]);

  return (
    <div className="chat-metrics-container">
      <h2>Метрики чата</h2>
      {metrics ? (
        <div>
          <p>Активные пользователи: {metrics.activeUsers}</p>
          <p>Количество сообщений: {metrics.messageCount}</p>
        </div>
      ) : (
        <p>Загрузка метрик...</p>
      )}
    </div>
  );
};

export default ChatMetrics;
