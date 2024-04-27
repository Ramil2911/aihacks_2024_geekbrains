import React, { useState, useEffect } from 'react';
import './ChatList.css';
import NewChatModal from './NewChatModal';

const ChatList = ({ onSelectChat }) => {
  const [showModal, setShowModal] = useState(false);
  const [chats, setChats] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await fetch('https://example.com/api/chats');
        const data = await response.json();
        setChats(data);
      } catch (error) {
        console.error('Ошибка при загрузке чатов:', error);
        setErrorMessage('Ошибка при загрузке чатов');
      }
    };

    fetchChats();
  }, []);

  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setErrorMessage('');
  };

  const handleAddChat = async (newChatName) => {
    try {
      // Отправляем запрос на бэкенд для добавления нового чата
      const response = await fetch('https://example.com/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newChatName }),
      });
      const data = await response.json();
      if (data.success) {
        // Если чат успешно добавлен на сервере, обновляем список чатов
        setChats(prevChats => [...prevChats, { id: data.chatId, name: newChatName, isFavorite: false }]);
        setShowModal(false);
      } else {
        setErrorMessage('Ошибка при добавлении нового чата');
      }
    } catch (error) {
      console.error('Ошибка при добавлении нового чата:', error);
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
        <button className="novi" onClick={handleOpenModal}></button>
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
