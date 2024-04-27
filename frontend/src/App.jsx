import React, { useState, useEffect } from 'react';
import ChatList from './ChatList';
import ChatWindow from './ChatWindow';
import ChatMetrics from './ChatMetrics';

import './ChatApp.css';
import { api } from './api';

const App = () => {
  const [selectedChat, setSelectedChat] = useState(null);
  const [chatData, setChatData] = useState(null);
  
  // Функция для загрузки данных о чатах 
  useEffect(() => {
    const fetchData = async () => {
      try {
        const {data} = await api.getChats()
        setChatData(data);
      } catch (error) {
        console.error('Ошибка при загрузке данных о чатах:', error);
      }
    };

    fetchData();
  }, []);

  // Функция для обработки выбора чата из списка
  const handleSelectChat = (chatId) => {
    setSelectedChat(chatId);
  };

  // Функция для обновления данных чата
  const handleChatUpdate = async (chatId, message) => {
    try {
      await api.sendMessage(chatId, message)
      // Обновляем данные чата после отправки сообщения
      // Можно также загружать новые сообщения и обновлять чат
    } catch (error) {
      console.error('Ошибка при отправке сообщения:', error);
    }
  };

  return (
    <div>
        <header className="header">
        <h1 className="team-name">Качество преподавания</h1>
        <div class="bio">
        <p className='sdelano'>сделано для</p>
        <img className='logo' src='src\assets\logo.png'/>
          <h1>GeekBrains</h1>
        </div>
      </header>
    <div className="app-container">
      <div className="column">
        <ChatList chats={chatData} onSelectChat={handleSelectChat} />
      </div>
      <div className="column">
        {selectedChat && <ChatWindow chatId={selectedChat} onUpdate={handleChatUpdate} />}
      </div>
      <div className="column">
        {selectedChat && <ChatMetrics chatId={selectedChat} />}
      </div>
    </div>
    </div>
  );
};

export default App;
