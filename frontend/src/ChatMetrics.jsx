// ChatMetrics.jsx
import React, { useState, useEffect } from 'react';
import './ChatMetrics.css';

const ChatMetrics = ({ chatId }) => {
  const [metrics, setMetrics] = useState(null);

  // Загрузка метрик чата при выборе чата
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const { data } = await api.getChatMetrics(chatId);
        setMetrics(data);
      } catch (error) {
        console.error('Ошибка при загрузке метрик чата:', error);
      }
    };

    if (chatId) {
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
