// ChatList.jsx

import React, { useState } from 'react';
import './ChatList.css';
import NewChatModal from './NewChatModal';

const ChatList = ({ onSelectChat }) => {
  const [showModal, setShowModal] = useState(false);
  const [chats, setChats] = useState([
    { id: 1, name: 'Избранное', isFavorite: true },

  ]);
  const [errorMessage, setErrorMessage] = useState('');

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setErrorMessage('');
  };


  const handleAddChat = async (newChatName) => {
    try {
      // Отправляем запрос на бэкенд для проверки существования чата
      const response = await fetch('https://example.com/api/chats/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newChatName }),
      });
      const data = await response.json();
      if (data.exists) {
        // Если чат уже существует, выводим сообщение об ошибке
        setErrorMessage('Чат уже существует');
      } else {
        // Если чата нет, добавляем его в список чатов
        const newChatId = chats.length + 1;
        const newChat = { id: newChatId, name: newChatName, isFavorite: false };
        setChats([...chats, newChat]);
        setShowModal(false);
      }
    } catch (error) {
      console.error('Ошибка при добавлении нового чата:', error);
      // В случае ошибки также выводим сообщение об ошибке
      setErrorMessage('Ошибка при добавлении нового чата');
    }
  };

  const handleChatClick = (chatId) => {
    onSelectChat(chatId); // Передача chatId родительскому компоненту
  };

  return (
    <div className="chat-list">
        <div className="chati">
          
      <h2>Чаты</h2>
      <button className='novi' onClick={handleOpenModal}></button>
      {errorMessage && <p className="error-message">{errorMessage}</p>}  
      </div>
      {showModal && <NewChatModal onAddChat={handleAddChat} onCloseModal={handleCloseModal} />}
      
      {chats.map(chat => (
        <div key={chat.id} className="chat-item" onClick={() => handleChatClick(chat.id)}>
          <p>{chat.name}</p>
          {chat.isFavorite && <span>Избранное</span>}
        </div>
      ))}
    </div>
  );
};

export default ChatList;
